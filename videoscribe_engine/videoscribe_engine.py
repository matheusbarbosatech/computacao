"""
=============================================================================
VIDEOSCRIBE CLONE ENGINE (WHITEBOARD ANIMATION EM PYTHON)
=============================================================================
Gerador automático de vídeos curtos verticais (9:16 - 1080x1920) estilo VideoScribe.
Simula a mão desenhando textos, diagramas e ilustrações em tempo real, com voz de
IA neural (Edge-TTS) e legendas dinâmicas sincronizadas para Reels/TikTok/Shorts.
=============================================================================
"""

import os
import sys
import math
import time
import asyncio
import subprocess
import numpy as np
import cv2
from PIL import Image, ImageDraw, ImageFont
import edge_tts

if sys.platform == "win32":
    try:
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
        sys.stderr.reconfigure(encoding="utf-8", errors="replace")
    except Exception:
        pass


BASE_DIR = os.path.dirname(os.path.abspath(__file__))
ASSETS_DIR = os.path.join(BASE_DIR, "assets")
OUTPUT_DIR = os.path.join(BASE_DIR, "output")
os.makedirs(OUTPUT_DIR, exist_ok=True)

WIDTH = 1080
HEIGHT = 1920
FPS = 30

# Cores Sketchnote
BG_COLOR = (252, 250, 246)        # Papel Sketchnote Quente
INK_BLACK = (15, 23, 42)          # Tinta Preta / Azul Escuro
INK_BLUE = (2, 132, 199)          # Destaque Azul (Pilha)
INK_GREEN = (16, 185, 129)        # Destaque Verde (Fila)
INK_RED = (239, 68, 68)           # Destaque Vermelho
INK_YELLOW = (245, 158, 11)       # Destaque Amarelo Ouro
CARD_BG_BLUE = (240, 249, 255)    # Fundo Suave Pilha
CARD_BG_GREEN = (236, 253, 245)   # Fundo Suave Fila
BORDER_GRAY = (226, 232, 240)

# Carrega fontes com fallback
def get_font(name, size):
    try:
        return ImageFont.truetype(name, size)
    except Exception:
        try:
            return ImageFont.truetype("arialbd.ttf", size)
        except Exception:
            return ImageFont.load_default()

FONT_TITLE = get_font("arialbd.ttf", 64)
FONT_SUBTITLE = get_font("arialbd.ttf", 40)
FONT_CARD_HEAD = get_font("arialbd.ttf", 36)
FONT_BODY = get_font("arialbd.ttf", 32)
FONT_HAND = get_font("comicbd.ttf", 34)
FONT_TAG = get_font("arialbd.ttf", 26)
FONT_SUBTITLE_BOTTOM = get_font("arialbd.ttf", 36)

class VideoScribeEngine:
    def __init__(self):
        # Carrega e prepara a mão com caneta
        hand_path = os.path.join(ASSETS_DIR, "hand_pen_clean.png")
        if not os.path.exists(hand_path):
            raise FileNotFoundError(f"Asset da mão não encontrado: {hand_path}")
        
        raw_hand = Image.open(hand_path).convert("RGBA")
        self.hand_scale = 0.58
        hw = int(raw_hand.width * self.hand_scale)
        hh = int(raw_hand.height * self.hand_scale)
        self.hand_img = raw_hand.resize((hw, hh), Image.Resampling.LANCZOS)
        
        # Coordenada da ponta da caneta relativa à imagem redimensionada
        self.tip_x = int(512 * self.hand_scale)
        self.tip_y = int(714 * self.hand_scale)
        
        # Posição de repouso da mão (fora da tela à direita)
        self.rest_pos = (WIDTH + 150, 800)
        self.last_pen_pos = self.rest_pos

    def create_base_canvas(self):
        canvas = Image.new("RGB", (WIDTH, HEIGHT), BG_COLOR)
        draw = ImageDraw.Draw(canvas)
        
        # Margem externa pontilhada ou sutil de prancheta
        draw.rectangle([(25, 25), (WIDTH - 25, HEIGHT - 25)], outline=BORDER_GRAY, width=4)
        
        # Linha de cabeçalho sutil
        draw.line([(30, 290), (WIDTH - 30, 290)], fill=(235, 230, 220), width=2)
        return canvas

    def overlay_hand(self, canvas, pen_pos):
        """Sobrepõe a mão no canvas colocando a ponta da caneta exatamente em pen_pos."""
        if pen_pos[0] > WIDTH + 80:
            return canvas # Mão fora da tela
        
        pos_x = int(pen_pos[0] - self.tip_x)
        pos_y = int(pen_pos[1] - self.tip_y)
        
        # Adiciona micro-vibração humana natural (1 a 2px)
        jitter_x = int(np.random.choice([-1, 0, 1]))
        jitter_y = int(np.random.choice([-1, 0, 1]))
        pos_x += jitter_x
        pos_y += jitter_y

        canvas.paste(self.hand_img, (pos_x, pos_y), self.hand_img)
        return canvas

    def render_frame_at_time(self, t, subtitles_info):
        """Renderiza um frame exato para o instante de tempo t (em segundos)."""
        canvas = self.create_base_canvas()
        draw = ImageDraw.Draw(canvas)
        
        active_pen = self.rest_pos

        # -------------------------------------------------------------
        # 1. CABEÇALHO: BADGE + TÍTULO (t: 0.2s a 4.0s)
        # -------------------------------------------------------------
        # Badge: ESTRUTURAS DE DADOS (t: 0.2s a 1.2s)
        p_badge = np.clip((t - 0.2) / 1.0, 0.0, 1.0)
        if p_badge > 0:
            bx1, by1, bx2, by2 = 320, 80, 760, 150
            draw.rounded_rectangle([(bx1, by1), (bx2, by2)], radius=16, fill=(37, 99, 235))
            if p_badge < 1.0:
                # Caneta desenha o contorno do badge
                active_pen = (bx1 + (bx2 - bx1) * p_badge, by2)
            else:
                draw.text((540, 115), "ESTRUTURAS DE DADOS", fill=(255, 255, 255), font=FONT_TAG, anchor="mm")

        # Título: PILHA vs FILA (t: 1.2s a 3.2s)
        p_tit = np.clip((t - 1.2) / 1.8, 0.0, 1.0)
        if p_tit > 0:
            title_text = "PILHA  vs  FILA"
            chars_show = int(len(title_text) * p_tit)
            txt_drawn = title_text[:chars_show]
            if txt_drawn:
                draw.text((540, 215), txt_drawn, fill=INK_BLACK, font=FONT_TITLE, anchor="mm")
            if p_tit < 1.0:
                active_pen = (240 + int(p_tit * 600), 220)

        # -------------------------------------------------------------
        # 2. BLOCO 1: A PILHA (STACK) — LIFO (t: 3.5s a 14.5s)
        # -------------------------------------------------------------
        # Container do Card Pilha
        p_card1 = np.clip((t - 3.5) / 1.5, 0.0, 1.0)
        if p_card1 > 0:
            cx1, cy1, cx2, cy2 = 80, 320, WIDTH - 80, 940
            # Desenha fundo suave
            draw.rounded_rectangle([(cx1, cy1), (cx2, cy2)], radius=24, fill=CARD_BG_BLUE, outline=INK_BLUE, width=5)
            if p_card1 < 1.0:
                active_pen = (cx1 + (cx2 - cx1) * p_card1, cy1)

        # Cabeçalho do Card: 1. PILHA (STACK) — LIFO (t: 5.0s a 7.0s)
        p_txt1 = np.clip((t - 5.0) / 1.8, 0.0, 1.0)
        if p_txt1 > 0:
            txt = "1. A PILHA (STACK) — LIFO"
            draw.text((120, 360), txt[:int(len(txt) * p_txt1)], fill=INK_BLUE, font=FONT_CARD_HEAD)
            if p_txt1 < 1.0:
                active_pen = (120 + int(p_txt1 * 450), 375)

        # Desenho dos Pratos da Pilha (t: 7.0s a 12.0s)
        # 3 Pratos empilhados
        pratos = [
            ("Elemento 1 (Base)", 760, (186, 230, 253)),
            ("Elemento 2 (Meio)", 650, (125, 211, 252)),
            ("Elemento 3 (TOPO)", 540, (56, 189, 248)),
        ]
        
        for i, (label, py, cor_fundo) in enumerate(pratos):
            t_start = 7.0 + i * 1.3
            p_prato = np.clip((t - t_start) / 1.1, 0.0, 1.0)
            if p_prato > 0:
                px1, py1, px2, py2 = 240, py, 740, py + 80
                draw.rounded_rectangle([(px1, py1), (px2, py2)], radius=14, fill=cor_fundo, outline=INK_BLUE, width=4)
                if p_prato > 0.5:
                    draw.text((490, py + 40), label, fill=INK_BLACK, font=FONT_BODY, anchor="mm")
                if p_prato < 1.0:
                    active_pen = (px1 + (px2 - px1) * p_prato, py2)

        # Setas e Textos de PUSH e POP (t: 11.5s a 13.5s)
        p_arrows1 = np.clip((t - 11.5) / 1.5, 0.0, 1.0)
        if p_arrows1 > 0:
            # PUSH (Entra pelo topo)
            draw.text((790, 530), "PUSH ->\n(Entra no Topo)", fill=(14, 116, 144), font=FONT_TAG)
            # POP (Sai pelo topo)
            draw.text((70, 530), "<- POP\n(Sai do Topo)", fill=(185, 28, 28), font=FONT_TAG)
            if p_arrows1 < 1.0:
                active_pen = (820, 560)

        # Regra de Ouro da Pilha: LIFO (t: 13.0s a 14.5s)
        p_regra1 = np.clip((t - 13.0) / 1.3, 0.0, 1.0)
        if p_regra1 > 0:
            rx1, ry1, rx2, ry2 = 120, 850, WIDTH - 120, 915
            draw.rounded_rectangle([(rx1, ry1), (rx2, ry2)], radius=12, fill=(219, 234, 254), outline=(147, 197, 253), width=2)
            draw.text((540, 882), "REGRA LIFO: O Último que entra é o Primeiro que sai!", fill=(30, 58, 138), font=FONT_TAG, anchor="mm")
            if p_regra1 < 1.0:
                active_pen = (rx1 + (rx2 - rx1) * p_regra1, ry2)

        # -------------------------------------------------------------
        # 3. BLOCO 2: A FILA (QUEUE) — FIFO (t: 15.0s a 24.5s)
        # -------------------------------------------------------------
        # Container do Card Fila
        p_card2 = np.clip((t - 15.0) / 1.5, 0.0, 1.0)
        if p_card2 > 0:
            cx1, cy1, cx2, cy2 = 80, 970, WIDTH - 80, 1580
            draw.rounded_rectangle([(cx1, cy1), (cx2, cy2)], radius=24, fill=CARD_BG_GREEN, outline=INK_GREEN, width=5)
            if p_card2 < 1.0:
                active_pen = (cx1 + (cx2 - cx1) * p_card2, cy1)

        # Título Fila (t: 16.2s a 18.0s)
        p_txt2 = np.clip((t - 16.2) / 1.5, 0.0, 1.0)
        if p_txt2 > 0:
            txt = "2. A FILA (QUEUE) — FIFO"
            draw.text((120, 1010), txt[:int(len(txt) * p_txt2)], fill=(4, 120, 87), font=FONT_CARD_HEAD)
            if p_txt2 < 1.0:
                active_pen = (120 + int(p_txt2 * 450), 1025)

        # Nós Horizontais da Fila: [1º] -> [2º] -> [3º] (t: 18.0s a 22.5s)
        nodes = [
            ("1o (Frente)", 150, (110, 231, 183)),
            ("2o", 450, (167, 243, 208)),
            ("3o (Fim)", 710, (209, 250, 229)),
        ]
        
        for j, (label, nx, cor_fundo) in enumerate(nodes):
            t_node = 18.0 + j * 1.3
            p_node = np.clip((t - t_node) / 1.1, 0.0, 1.0)
            if p_node > 0:
                nx1, ny1, nx2, ny2 = nx, 1150, nx + 220, 1270
                draw.rounded_rectangle([(nx1, ny1), (nx2, ny2)], radius=18, fill=cor_fundo, outline=INK_GREEN, width=4)
                if p_node > 0.5:
                    draw.text((nx + 110, 1210), label, fill=INK_BLACK, font=FONT_BODY, anchor="mm")
                if p_node < 1.0:
                    active_pen = (nx1 + 220 * p_node, ny2)

        # Setas de fluxo da fila (t: 21.5s a 23.0s)
        p_flow = np.clip((t - 21.5) / 1.5, 0.0, 1.0)
        if p_flow > 0:
            # Entrada e Saída
            draw.text((150, 1310), "<- SAI PRIMEIRO\n(DEQUEUE)", fill=(4, 120, 87), font=FONT_TAG)
            draw.text((710, 1310), "<- ENTRA NO FIM\n(ENQUEUE)", fill=(14, 116, 144), font=FONT_TAG)
            if p_flow < 1.0:
                active_pen = (300, 1330)

        # Regra FIFO (t: 23.0s a 24.5s)
        p_regra2 = np.clip((t - 23.0) / 1.3, 0.0, 1.0)
        if p_regra2 > 0:
            rx1, ry1, rx2, ry2 = 120, 1480, WIDTH - 120, 1545
            draw.rounded_rectangle([(rx1, ry1), (rx2, ry2)], radius=12, fill=(209, 250, 229), outline=(110, 231, 183), width=2)
            draw.text((540, 1512), "REGRA FIFO: O Primeiro que chega é o Primeiro atendido!", fill=(6, 95, 70), font=FONT_TAG, anchor="mm")
            if p_regra2 < 1.0:
                active_pen = (rx1 + (rx2 - rx1) * p_regra2, ry2)

        # -------------------------------------------------------------
        # 4. CALL TO ACTION FINAL (t: 25.0s a 28.8s)
        # -------------------------------------------------------------
        p_cta = np.clip((t - 25.0) / 1.8, 0.0, 1.0)
        if p_cta > 0:
            cx1, cy1, cx2, cy2 = 80, 1610, WIDTH - 80, 1720
            draw.rounded_rectangle([(cx1, cy1), (cx2, cy2)], radius=20, fill=(254, 240, 138), outline=INK_YELLOW, width=5)
            draw.text((540, 1648), "SALVE ESTE VÍDEO & SIGA O PERFIL!", fill=(146, 64, 14), font=FONT_SUBTITLE, anchor="mm")
            draw.text((540, 1688), "Domine 700 Mapas da Computação em @DevSketch", fill=INK_BLACK, font=FONT_TAG, anchor="mm")
            if p_cta < 1.0:
                active_pen = (cx1 + (cx2 - cx1) * p_cta, cy2)
            else:
                active_pen = (WIDTH + 150, 1650)

        # -------------------------------------------------------------
        # 5. LEGENDAS DINÂMICAS TIKTOK / REELS NO RODAPÉ
        # -------------------------------------------------------------
        current_sub = ""
        for sub in subtitles_info:
            if sub["start"] <= t <= sub["end"]:
                current_sub = sub["text"]
                break
        
        if current_sub:
            words = current_sub.split()
            lines = []
            cur_line = []
            for w in words:
                cur_line.append(w)
                if len(" ".join(cur_line)) > 30:
                    cur_line.pop()
                    lines.append(" ".join(cur_line))
                    cur_line = [w]
            if cur_line:
                lines.append(" ".join(cur_line))
            
            sub_text = "\n".join(lines)
            bbox = draw.multiline_textbbox((WIDTH // 2, 1810), sub_text, font=FONT_SUBTITLE_BOTTOM, anchor="mm", align="center")
            pad_x, pad_y = 28, 16
            draw.rounded_rectangle([(bbox[0] - pad_x, bbox[1] - pad_y), (bbox[2] + pad_x, bbox[3] + pad_y)], radius=20, fill=(15, 23, 42, 240), outline=(250, 204, 21), width=3)
            draw.multiline_text((WIDTH // 2, 1810), sub_text, fill=(255, 255, 255), font=FONT_SUBTITLE_BOTTOM, anchor="mm", align="center")


        # -------------------------------------------------------------
        # 6. SOBREPÕE A MÃO DESENHISTA
        # -------------------------------------------------------------
        # Suaviza a transição da mão
        target_x, target_y = active_pen
        last_x, last_y = self.last_pen_pos
        smooth_x = int(last_x + (target_x - last_x) * 0.45)
        smooth_y = int(last_y + (target_y - last_y) * 0.45)
        self.last_pen_pos = (smooth_x, smooth_y)

        canvas = self.overlay_hand(canvas, (smooth_x, smooth_y))
        return canvas

    async def render_video(self, output_filename="video_pilha_vs_fila_short.mp4"):
        print("=" * 70, flush=True)
        print("🎬 INICIANDO GERAÇÃO DO VÍDEO VERTICAL (CLONE VIDEOSCRIBE)", flush=True)
        print("=" * 70, flush=True)

        # 1. Roteiro e Narração Neural com Edge-TTS
        script_text = (
            "Você sabe a diferença crucial entre uma PILHA e uma FILA na Ciência da Computação? "
            "É muito simples. "
            "A Pilha funciona como uma pilha de pratos: o último que entra é o primeiro que sai. Isso se chama LIFO! "
            "Já a Fila funciona como uma fila de banco: o primeiro que chega é o primeiro atendido. Isso se chama FIFO! "
            "Salve esse vídeo e domine estruturas de dados para suas entrevistas!"
        )

        audio_path = os.path.join(OUTPUT_DIR, "narracao_temp.mp3")
        print("🎙️ Gerando narração neural pt-BR (AntonioNeural)...", flush=True)

        communicate = edge_tts.Communicate(script_text, "pt-BR-AntonioNeural", rate="+6%")
        subtitles_info = []

        with open(audio_path, "wb") as f:
            async for chunk in communicate.stream():
                if chunk["type"] == "audio":
                    f.write(chunk["data"])
                elif chunk["type"] in ("WordBoundary", "SentenceBoundary"):
                    start_sec = (chunk["offset"]) / 10_000_000.0
                    dur_sec = (chunk["duration"]) / 10_000_000.0
                    subtitles_info.append({
                        "start": start_sec,
                        "end": start_sec + dur_sec,
                        "text": chunk["text"]
                    })

        # Duração total via ffprobe
        probe_cmd = [
            r"C:\bin\ffmpeg\bin\ffprobe.exe",
            "-v", "error",
            "-show_entries", "format=duration",
            "-of", "default=noprint_wrappers=1:nokey=1",
            audio_path
        ]
        duration = float(subprocess.check_output(probe_cmd).decode().strip())
        # Garante pelo menos 1 segundo a mais no final para o CTA respirar
        total_duration = duration + 1.2
        total_frames = int(total_duration * FPS)

        print(f"⏱️ Duração do Áudio: {duration:.2f}s | Duração do Vídeo: {total_duration:.2f}s ({total_frames} frames)", flush=True)

        output_video_path = os.path.join(OUTPUT_DIR, output_filename)

        # Inicia processo do ffmpeg recebendo frames via pipe stdin
        ffmpeg_cmd = [
            r"C:\bin\ffmpeg\bin\ffmpeg.exe",
            "-y",
            "-loglevel", "error",
            "-f", "rawvideo",
            "-vcodec", "rawvideo",
            "-s", f"{WIDTH}x{HEIGHT}",
            "-pix_fmt", "bgr24",
            "-r", str(FPS),
            "-i", "-",  # Entrada do vídeo via pipe
            "-i", audio_path,  # Entrada do áudio
            "-c:v", "libx264",
            "-preset", "fast",
            "-crf", "20",
            "-pix_fmt", "yuv420p",
            "-c:a", "aac",
            "-b:a", "192k",
            "-shortest",
            output_video_path
        ]

        print("🚀 Processando e renderizando frames whiteboard em tempo real...", flush=True)
        proc = subprocess.Popen(ffmpeg_cmd, stdin=subprocess.PIPE, stderr=subprocess.DEVNULL)


        start_time = time.time()
        for frame_idx in range(total_frames):
            t = frame_idx / FPS
            pil_img = self.render_frame_at_time(t, subtitles_info)
            
            # Converte PIL para BGR array para o FFmpeg
            bgr_frame = cv2.cvtColor(np.array(pil_img), cv2.COLOR_RGB2BGR)
            proc.stdin.write(bgr_frame.tobytes())

            if frame_idx % 60 == 0 or frame_idx == total_frames - 1:
                prog = (frame_idx + 1) / total_frames * 100
                elapsed = time.time() - start_time
                fps_actual = (frame_idx + 1) / max(0.1, elapsed)
                print(f"   🎞️ Progresso: [{frame_idx + 1}/{total_frames}] {prog:.1f}% ({fps_actual:.1f} fps)", flush=True)

        proc.stdin.close()
        proc.wait()

        print("=" * 70, flush=True)
        print(f"✅ VÍDEO CONCLUÍDO COM SUCESSO!", flush=True)
        print(f"📁 Arquivo Final: {output_video_path}", flush=True)
        print(f"💾 Tamanho: {os.path.getsize(output_video_path) / (1024*1024):.2f} MB", flush=True)
        print("=" * 70, flush=True)
        return output_video_path

if __name__ == "__main__":
    engine = VideoScribeEngine()
    asyncio.run(engine.render_video())
