# -*- coding: utf-8 -*-
"""
=============================================================================
GERADOR DE REELS / TIKTOK CINEMÁTICO (KEN BURNS + NEON HIGHLIGHTER)
=============================================================================
Transforma qualquer mapa mental sketchnote em um vídeo vertical (1080x1920)
estilo documentário moderno com:
- Zoom e Pan cinematográficos (Ken Burns dinâmico)
- Destaques tipo marca-texto neon sobre os blocos conceituais
- Fundo ambiente dinâmico com blur cinematográfico
- Narração neural (Edge-TTS pt-BR-AntonioNeural)
- Legendas dinâmicas estilo Alex Hormozi (alto contraste e retenção)
- Card de chamada para ação (CTA) para vender o kit de 700 mapas
=============================================================================
"""
import os
import sys
import math
import asyncio
import subprocess
import numpy as np
import cv2
from PIL import Image, ImageDraw, ImageFont
import edge_tts

sys.stdout.reconfigure(encoding='utf-8', line_buffering=True)
sys.stderr.reconfigure(encoding='utf-8', line_buffering=True)

BASE_DIR = r"c:\Users\matheus\Desktop\computacao"
OUTPUT_DIR = os.path.join(BASE_DIR, "output_reels_demo")
os.makedirs(OUTPUT_DIR, exist_ok=True)

MAP_IMAGE_PATH = os.path.join(BASE_DIR, "02_logica_e_algoritmos", "imagens", "mapa_001.png")
OUTPUT_VIDEO = os.path.join(OUTPUT_DIR, "reels_mapa_001_cinematico.mp4")
TEMP_AUDIO = os.path.join(OUTPUT_DIR, "audio_reels_temp.mp3")

WIDTH = 1080
HEIGHT = 1920
FPS = 30

# Cores do Design System
COLOR_BG_DARK = (15, 23, 42)          # Slate escuro
COLOR_GOLD = (245, 158, 11)           # Destaque Ouro
COLOR_CYAN = (6, 182, 212)            # Destaque Ciano
COLOR_GREEN = (16, 185, 129)          # Verde Esmeralda
COLOR_WHITE = (255, 255, 255)
COLOR_TEXT_DIM = (148, 163, 184)

def get_font(size, bold=True):
    font_names = ["arialbd.ttf" if bold else "arial.ttf", "segoeuib.ttf" if bold else "segoeui.ttf", "arial.ttf"]
    for fn in font_names:
        try:
            return ImageFont.truetype(fn, size)
        except Exception:
            pass
    return ImageFont.load_default()

FONT_HEADER_BADGE = get_font(28, bold=True)
FONT_HEADER_TITLE = get_font(42, bold=True)
FONT_CAPTION = get_font(46, bold=True)
FONT_CTA_TITLE = get_font(38, bold=True)
FONT_CTA_SUB = get_font(28, bold=False)

# Roteiro das Cenas
CENAS = [
    {
        "id": "intro",
        "texto": "Se você está começando na programação, pare de ler PDFs de 500 páginas. O que é programar em 30 segundos?",
        "legenda": "O que é Programação em 30 segundos?",
        # Foco geral no centro do mapa
        "target_box": (0, 0, 1536, 1024),
        "highlight_box": None,
        "highlight_color": None
    },
    {
        "id": "ideia_central",
        "texto": "Primeiro: o computador é burro e 100% obediente. Ele só faz exatamente o que você escreveu.",
        "legenda": "💡 O computador só faz o que você manda!",
        # Foco no quadrante superior esquerdo (Ideia Central)
        "target_box": (40, 140, 720, 520),
        "highlight_box": (60, 240, 680, 480),
        "highlight_color": (250, 204, 21) # Amarelo Marca-texto
    },
    {
        "id": "maquina_pensa",
        "texto": "Ele não interpreta sua intenção. Se você não der uma instrução clara, ele trava ou erra feio.",
        "legenda": "🖥️ Sem instrução clara, ele trava ou erra!",
        # Foco no quadrante superior direito (Como a máquina pensa)
        "target_box": (800, 140, 1500, 520),
        "highlight_box": (820, 240, 1480, 480),
        "highlight_color": (34, 211, 238) # Ciano Neon
    },
    {
        "id": "codigo",
        "texto": "Código é simplesmente uma receita escrita numa linguagem que ele entende, como Python.",
        "legenda": "{ } Código é a receita que a máquina entende",
        # Foco no bloco de código (meio direito)
        "target_box": (800, 480, 1500, 850),
        "highlight_box": (820, 560, 1480, 820),
        "highlight_color": (52, 211, 153) # Verde Esmeralda
    },
    {
        "id": "cta",
        "texto": "Esse é só o mapa número um do nosso acervo com mais de 700 resumos e Anki. Garanta o seu no link da bio!",
        "legenda": "🚀 Garanta o Kit 700 Mapas Mentais no Link da Bio!",
        # Zoom out revelando o mapa completo
        "target_box": (0, 0, 1536, 1024),
        "highlight_box": None,
        "highlight_color": None
    }
]

async def gerar_audios():
    print("🎙️ Sintetizando narração neural completa com Edge-TTS...")
    textos_combinados = " ".join([c["texto"] for c in CENAS])
    comm = edge_tts.Communicate(textos_combinados, voice="pt-BR-AntonioNeural", rate="+6%")
    await comm.save(TEMP_AUDIO)
    
    # Obtém duração total via ffprobe
    cmd = [
        "ffprobe", "-v", "error",
        "-show_entries", "format=duration",
        "-of", "default=noprint_wrappers=1:nokey=1",
        TEMP_AUDIO
    ]
    res = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    duracao_total = float(res.stdout.strip())
    print(f"✅ Áudio gerado com sucesso! Duração total: {duracao_total:.2f} segundos")
    return duracao_total

def ler_e_preparar_mapa():
    if not os.path.exists(MAP_IMAGE_PATH):
        raise FileNotFoundError(f"Mapa não encontrado em: {MAP_IMAGE_PATH}")
    img_bgr = cv2.imread(MAP_IMAGE_PATH)
    return img_bgr

def ease_in_out(t):
    """Interpolação cinematográfica suave (Sigmoid / Smoothstep)."""
    return t * t * (3 - 2 * t)

def renderizar_reels(duracao_total):
    print("🎬 Inicializando Motor Cinematográfico de Renderização...")
    mapa_bgr = ler_e_preparar_mapa()
    orig_h, orig_w = mapa_bgr.shape[:2]
    
    total_frames = int(duracao_total * FPS)
    num_cenas = len(CENAS)
    frames_por_cena = total_frames / num_cenas
    
    FFMPEG_BIN = r"C:\bin\ffmpeg\bin\ffmpeg.exe"
    ffmpeg_cmd = [
        FFMPEG_BIN, "-y",
        "-loglevel", "error",
        "-f", "rawvideo",
        "-vcodec", "rawvideo",
        "-s", f"{WIDTH}x{HEIGHT}",
        "-pix_fmt", "bgr24",
        "-r", str(FPS),
        "-i", "-",
        "-i", TEMP_AUDIO,
        "-c:v", "libx264",
        "-preset", "veryfast",
        "-crf", "18",
        "-pix_fmt", "yuv420p",
        "-c:a", "aac",
        "-b:a", "192k",
        "-shortest",
        OUTPUT_VIDEO
    ]
    
    proc = subprocess.Popen(ffmpeg_cmd, stdin=subprocess.PIPE)
    
    # Pré-computa o fundo ambiente com blur UMA ÚNICA VEZ fora do loop
    print("🎨 Pré-computando fundo ambiente desfocado...", flush=True)
    bg_resized = cv2.resize(mapa_bgr, (WIDTH, HEIGHT))
    base_bg_blur = cv2.GaussianBlur(bg_resized, (51, 51), 0)
    base_bg_dark = np.zeros((HEIGHT, WIDTH, 3), dtype=np.uint8)
    base_bg_blur = cv2.addWeighted(base_bg_blur, 0.28, base_bg_dark, 0.72, 0)
    
    current_cam = list(CENAS[0]["target_box"])
    for frame_idx in range(total_frames):
        tempo_atual = frame_idx / FPS
        cena_idx = min(int(frame_idx / frames_por_cena), num_cenas - 1)
        cena_atual = CENAS[cena_idx]
        
        # Progresso local da cena (0.0 a 1.0)
        t_local = (frame_idx - (cena_idx * frames_por_cena)) / frames_por_cena
        t_smooth = ease_in_out(max(0.0, min(1.0, t_local * 1.5)))
        
        # Interpola a câmera em direção ao alvo da cena
        target_cam = cena_atual["target_box"]
        for i in range(4):
            current_cam[i] = current_cam[i] + (target_cam[i] - current_cam[i]) * 0.12
            
        cx1, cy1, cx2, cy2 = [int(v) for v in current_cam]
        cx1 = max(0, min(cx1, orig_w - 100))
        cy1 = max(0, min(cy1, orig_h - 100))
        cx2 = max(cx1 + 100, min(cx2, orig_w))
        cy2 = max(cy1 + 100, min(cy2, orig_h))
        
        # 1. Recorta a região focada do mapa mental
        crop = mapa_bgr[cy1:cy2, cx1:cx2].copy()
        
        # 2. Se houver marca-texto ativo, aplica o efeito de destaque neon
        if cena_atual["highlight_box"] and t_local > 0.25:
            hx1, hy1, hx2, hy2 = cena_atual["highlight_box"]
            rx1 = max(0, hx1 - cx1)
            ry1 = max(0, hy1 - cy1)
            rx2 = min(crop.shape[1], hx2 - cx1)
            ry2 = min(crop.shape[0], hy2 - cy1)
            
            if rx2 > rx1 and ry2 > ry1:
                prog_hl = min(1.0, (t_local - 0.25) * 3.0)
                anim_rx2 = int(rx1 + (rx2 - rx1) * prog_hl)
                
                overlay = crop.copy()
                color_bgr = (cena_atual["highlight_color"][2], cena_atual["highlight_color"][1], cena_atual["highlight_color"][0])
                cv2.rectangle(overlay, (rx1, ry1), (anim_rx2, ry2), color_bgr, -1)
                cv2.rectangle(overlay, (rx1, ry1), (anim_rx2, ry2), color_bgr, 3)
                cv2.addWeighted(overlay, 0.38, crop, 0.62, 0, crop)
                
        # 3. Monta o Canvas Vertical (1080x1920) utilizando o fundo pré-computado
        canvas = base_bg_blur.copy()
        
        # Redimensiona o crop do mapa para caber com margens estéticas no centro vertical
        target_display_w = WIDTH - 90
        scale = target_display_w / crop.shape[1]
        target_display_h = int(crop.shape[0] * scale)
        
        if target_display_h > 1150:
            target_display_h = 1150
            scale = target_display_h / crop.shape[0]
            target_display_w = int(crop.shape[1] * scale)
            
        resized_crop = cv2.resize(crop, (target_display_w, target_display_h), interpolation=cv2.INTER_CUBIC)
        
        # Posição central na tela vertical
        pos_x = (WIDTH - target_display_w) // 2
        pos_y = 360 + (1150 - target_display_h) // 2
        
        # Sombra suave sob o card do mapa
        shadow_margin = 16
        cv2.rectangle(canvas, 
                      (pos_x - shadow_margin, pos_y - shadow_margin), 
                      (pos_x + target_display_w + shadow_margin, pos_y + target_display_h + shadow_margin), 
                      (5, 10, 20), -1)
        
        # Borda arredondada / moldura moderna
        cv2.rectangle(canvas, (pos_x - 4, pos_y - 4), (pos_x + target_display_w + 4, pos_y + target_display_h + 4), (51, 65, 85), 2)
        
        # Insere o mapa renderizado
        canvas[pos_y:pos_y + target_display_h, pos_x:pos_x + target_display_w] = resized_crop
        
        # 4. Overlays Gráficos com Pillow (Textos, Badges, Legendas)
        pil_frame = Image.fromarray(cv2.cvtColor(canvas, cv2.COLOR_BGR2RGB))
        draw = ImageDraw.Draw(pil_frame)
        
        # --- CABEÇALHO SUPERIOR ---
        # Badge "⚡ COMPUTAÇÃO EM 30 SEGUNDOS"
        badge_text = "⚡ COMPUTAÇÃO EM 30 SEGUNDOS"
        badge_w = 480
        badge_h = 52
        badge_x = (WIDTH - badge_w) // 2
        badge_y = 120
        draw.rounded_rectangle([(badge_x, badge_y), (badge_x + badge_w, badge_y + badge_h)], radius=26, fill=(245, 158, 11))
        draw.text((badge_x + 36, badge_y + 11), badge_text, font=FONT_HEADER_BADGE, fill=(15, 23, 42))
        
        # Título do Mapa
        title_text = "MAPA 001 • O QUE É PROGRAMAÇÃO?"
        bbox = draw.textbbox((0, 0), title_text, font=FONT_HEADER_TITLE)
        tw = bbox[2] - bbox[0]
        draw.text(((WIDTH - tw) // 2, 205), title_text, font=FONT_HEADER_TITLE, fill=(255, 255, 255))
        
        # --- LEGENDA DINÂMICA (LOWER-THIRD) ---
        legenda_text = cena_atual["legenda"]
        bbox_leg = draw.textbbox((0, 0), legenda_text, font=FONT_CAPTION)
        leg_w = bbox_leg[2] - bbox_leg[0] + 50
        leg_h = 76
        leg_x = (WIDTH - leg_w) // 2
        leg_y = 1580
        
        # Pill da legenda com fundo escuro e borda neon
        draw.rounded_rectangle([(leg_x, leg_y), (leg_x + leg_w, leg_y + leg_h)], radius=38, fill=(15, 23, 42))
        draw.rounded_rectangle([(leg_x, leg_y), (leg_x + leg_w, leg_y + leg_h)], radius=38, outline=(245, 158, 11), width=3)
        draw.text((leg_x + 25, leg_y + 14), legenda_text, font=FONT_CAPTION, fill=(254, 240, 138))
        
        # --- CALL TO ACTION (CENA FINAL) ---
        if cena_atual["id"] == "cta":
            cta_w = WIDTH - 120
            cta_h = 130
            cta_x = 60
            cta_y = 1710
            # Fundo Pulsante do CTA
            pulse = math.sin(tempo_atual * 8.0) * 0.5 + 0.5
            cta_color = (16, 185, 129) if pulse > 0.5 else (5, 150, 105)
            draw.rounded_rectangle([(cta_x, cta_y), (cta_x + cta_w, cta_y + cta_h)], radius=24, fill=cta_color)
            
            cta_title = "👉 GARANTA O KIT 700 MAPAS + ANKI"
            bbox_cta = draw.textbbox((0, 0), cta_title, font=FONT_CTA_TITLE)
            tw_cta = bbox_cta[2] - bbox_cta[0]
            draw.text(((WIDTH - tw_cta) // 2, cta_y + 24), cta_title, font=FONT_CTA_TITLE, fill=(255, 255, 255))
            
            cta_sub = "Acesse o link na bio do nosso perfil"
            bbox_sub = draw.textbbox((0, 0), cta_sub, font=FONT_CTA_SUB)
            tw_sub = bbox_sub[2] - bbox_sub[0]
            draw.text(((WIDTH - tw_sub) // 2, cta_y + 78), cta_sub, font=FONT_CTA_SUB, fill=(240, 253, 244))
            
        # Converte de volta para BGR e envia o frame para o FFmpeg
        final_bgr = cv2.cvtColor(np.array(pil_frame), cv2.COLOR_RGB2BGR)
        proc.stdin.write(final_bgr.tobytes())
        
        if frame_idx % 90 == 0:
            pct = (frame_idx / total_frames) * 100
            print(f"   ⏳ Renderizando: {pct:.1f}% ({frame_idx}/{total_frames} frames)...")
            
    proc.stdin.close()
    proc.wait()
    print("\n" + "=" * 65)
    print("🎉 VÍDEO CINEMÁTICO RENDERIZADO COM SUCESSO!")
    print(f"📁 Arquivo gerado: {OUTPUT_VIDEO}")
    print("=" * 65)

async def main():
    duracao = await gerar_audios()
    renderizar_reels(duracao)

if __name__ == "__main__":
    asyncio.run(main())
