# -*- coding: utf-8 -*-
"""
=============================================================================
GERADOR DE VÍDEO DARK 9:16 — ALERTA ANTI-GOLPE WHATSAPP (CANAL DARK)
=============================================================================
Produz um vídeo cinematográfico vertical (1080x1920) 100% sem aparecer com:
- Narração Neural profunda (Edge-TTS pt-BR-AntonioNeural)
- Fundo escuro cibernético com grid e partículas de código
- Simulação de chat do WhatsApp no Dark Mode com scanner de fraude
- Infográfico da anatomia do golpe
- Legendas dinâmicas estilo Alex Hormozi (Ouro #FFD700)
- Renderização via OpenCV + FFmpeg
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

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
OUTPUT_DIR = os.path.join(BASE_DIR, "output_reels_demo")
os.makedirs(OUTPUT_DIR, exist_ok=True)

OUTPUT_VIDEO = os.path.join(OUTPUT_DIR, "reels_dark_anti_golpe_whatsapp.mp4")
TEMP_AUDIO = os.path.join(OUTPUT_DIR, "audio_dark_temp.mp3")
TEMP_VIDEO_SILENT = os.path.join(OUTPUT_DIR, "video_silent_temp.mp4")

WIDTH = 1080
HEIGHT = 1920
FPS = 30

# Paleta de Cores Cyber Dark
COLOR_BG_DEEP = (10, 15, 29)          # #0a0f1d
COLOR_BG_CARD = (20, 27, 45)          # Card container
COLOR_ACCENT_GOLD = (255, 215, 0)     # Ouro Hormozi #FFD700
COLOR_ALERT_RED = (239, 68, 68)       # Vermelho alerta
COLOR_CYAN_NEON = (6, 182, 212)       # Ciano técnico
COLOR_GREEN_WA = (37, 211, 102)       # Verde WhatsApp
COLOR_WA_BUBBLE = (31, 44, 52)        # Fundo balão WA escuro
COLOR_WHITE = (255, 255, 255)
COLOR_TEXT_DIM = (148, 163, 184)

TEXTO_NARRACAO = (
    "Se você usa o WhatsApp todo dia, nunca responda uma mensagem que começar com essa frase: "
    "Oi mãe, troquei de número, salva aí. "
    "Criminosos colocam a foto do seu filho ou parente e pedem um Pix urgente dizendo que o aplicativo do banco travou. "
    "Presta muita atenção: eles não hackearam o celular de ninguém! "
    "Eles apenas pegaram fotos públicas na internet e compraram um chip novo de dez reais para fingir parentesco. "
    "A regra de ouro de segurança: número novo nunca ganha dinheiro! "
    "Só faça transferência se ligar por chamada de vídeo e a pessoa mostrar o rosto. "
    "Manda esse vídeo agora no grupo da sua família para blindar quem você ama!"
)

# Roteiro sincronizado por tempo (segundos) para as legendas e transições visuais
CENAS = [
    {"start": 0.0,  "end": 4.5,  "caption": "NUNCA RESPONDA ESSA FRASE NO WHATSAPP", "destaque": "NUNCA RESPONDA", "fase": 1},
    {"start": 4.5,  "end": 8.0,  "caption": "O GOLPE DO 'OI MÃE, TROQUEI DE NÚMERO'", "destaque": "OI MÃE", "fase": 1},
    {"start": 8.0,  "end": 14.5, "caption": "PEDEM UM PIX URGENTE COM A FOTO DO SEU FILHO", "destaque": "PIX URGENTE", "fase": 2},
    {"start": 14.5, "end": 19.0, "caption": "ELES NÃO HACKEARAM O CELULAR DE NINGUÉM!", "destaque": "NÃO HACKEARAM", "fase": 2},
    {"start": 19.0, "end": 26.0, "caption": "USAM FOTOS PÚBLICAS E CHIP PRÉ-PAGO DE R$ 10", "destaque": "FOTOS PÚBLICAS", "fase": 3},
    {"start": 26.0, "end": 31.0, "caption": "REGRA DE OURO: NÚMERO NOVO NUNCA GANHA PIX!", "destaque": "REGRA DE OURO", "fase": 3},
    {"start": 31.0, "end": 37.0, "caption": "EXIJA CHAMADA DE VÍDEO MOSTRANDO O ROSTO", "destaque": "CHAMADA DE VÍDEO", "fase": 4},
    {"start": 37.0, "end": 44.0, "caption": "COMPARTILHE NO GRUPO DA SUA FAMÍLIA AGORA!", "destaque": "COMPARTILHE AGORA", "fase": 4},
]

def get_font(size, bold=True):
    font_names = ["arialbd.ttf" if bold else "arial.ttf", "segoeuib.ttf" if bold else "segoeui.ttf", "arial.ttf"]
    for fn in font_names:
        try:
            return ImageFont.truetype(fn, size)
        except Exception:
            pass
    return ImageFont.load_default()

FONT_TITLE = get_font(42, bold=True)
FONT_BADGE = get_font(26, bold=True)
FONT_MSG_NAME = get_font(32, bold=True)
FONT_MSG_TEXT = get_font(36, bold=False)
FONT_MSG_TIME = get_font(22, bold=False)
FONT_CAPTION_BIG = get_font(50, bold=True)
FONT_HINT = get_font(28, bold=True)

async def gerar_audio_neural(texto, arquivo_saida):
    print(f"🎙️ Gerando narração neural (pt-BR-AntonioNeural)...")
    comunicador = edge_tts.Communicate(texto, "pt-BR-AntonioNeural", rate="+6%")
    await comunicador.save(arquivo_saida)
    print(f"✅ Áudio neural salvo em: {arquivo_saida}")

def obter_duracao_audio(arquivo_audio):
    cmd = [
        "ffprobe", "-v", "error",
        "-show_entries", "format=duration",
        "-of", "default=noprint_wrappers=1:nokey=1",
        arquivo_audio
    ]
    try:
        res = subprocess.check_output(cmd, stderr=subprocess.STDOUT)
        return float(res.decode().strip())
    except Exception:
        return 42.0

def desenhar_painel_whatsapp(draw, scanner_y, scanner_alpha, pulse_alert):
    # Card Central do WhatsApp
    card_x1, card_y1 = 80, 480
    card_x2, card_y2 = WIDTH - 80, 1150
    
    # Sombra e Fundo do Card
    draw.rounded_rectangle([card_x1, card_y1, card_x2, card_y2], radius=32, fill=(18, 24, 38), outline=(40, 52, 78), width=3)
    
    # Barra de Topo do WhatsApp Dark
    top_bar_h = 100
    draw.rounded_rectangle([card_x1, card_y1, card_x2, card_y1 + top_bar_h], radius=30, fill=(31, 44, 52))
    draw.rectangle([card_x1, card_y1 + 50, card_x2, card_y1 + top_bar_h], fill=(31, 44, 52))
    
    # Avatar circular
    avatar_center = (card_x1 + 60, card_y1 + 50)
    draw.ellipse([avatar_center[0]-35, avatar_center[1]-35, avatar_center[0]+35, avatar_center[1]+35], fill=(70, 85, 105))
    draw.text((avatar_center[0]-14, avatar_center[1]-18), "👤", font=FONT_MSG_NAME, fill=COLOR_WHITE)
    
    # Nome do Contato Fake
    draw.text((card_x1 + 115, card_y1 + 22), "Filho (Número Novo)", font=FONT_MSG_NAME, fill=COLOR_WHITE)
    draw.text((card_x1 + 115, card_y1 + 60), "online agora", font=FONT_MSG_TIME, fill=COLOR_GREEN_WA)
    
    # Ícones de chamada
    draw.text((card_x2 - 120, card_y1 + 32), "📹  📞", font=FONT_BADGE, fill=COLOR_CYAN_NEON)
    
    # Balão da Mensagem Recebida (Golpe)
    bubble_x1, bubble_y1 = card_x1 + 40, card_y1 + 140
    bubble_x2, bubble_y2 = card_x2 - 40, card_y1 + 460
    
    # Borda pulsante de perigo
    outline_color = (239, 68, 68) if pulse_alert else (55, 65, 81)
    draw.rounded_rectangle([bubble_x1, bubble_y1, bubble_x2, bubble_y2], radius=24, fill=COLOR_WA_BUBBLE, outline=outline_color, width=4)
    
    # Texto da Mensagem do Golpista
    linhas_msg = [
        "Oi mãe! Salva esse número novo aí.",
        "O meu celular antigo quebrou a tela.",
        "",
        "Preciso urgente pagar um fornecedor agora",
        "de R$ 1.850, mas meu app do banco travou.",
        "Você consegue fazer esse Pix pra mim?",
        "Amanhã cedo sem falta eu te devolvo! 🙏"
    ]
    
    cur_y = bubble_y1 + 25
    for l in linhas_msg:
        color = COLOR_ALERT_RED if "Pix" in l or "R$ 1.850" in l else COLOR_WHITE
        draw.text((bubble_x1 + 30, cur_y), l, font=FONT_MSG_TEXT, fill=color)
        cur_y += 42
        
    draw.text((bubble_x2 - 110, bubble_y2 - 35), "14:22 ✓✓", font=FONT_MSG_TIME, fill=COLOR_TEXT_DIM)
    
    # Tag de Detecção de Fraude
    badge_x1, badge_y1 = card_x1 + 50, card_y1 + 510
    badge_x2, badge_y2 = card_x2 - 50, card_y1 + 610
    draw.rounded_rectangle([badge_x1, badge_y1, badge_x2, badge_y2], radius=16, fill=(45, 15, 20), outline=COLOR_ALERT_RED, width=3)
    draw.text((badge_x1 + 30, badge_y1 + 20), "🚨 ALERTA FORENSE: GOLPE DE ENGENHARIA SOCIAL", font=FONT_BADGE, fill=COLOR_ALERT_RED)
    draw.text((badge_x1 + 30, badge_y1 + 58), "• Chip sem vínculo prévio  • Pressão de urgência financeira", font=FONT_MSG_TIME, fill=COLOR_WHITE)

def criar_frame(tempo_atual, total_tempo, frame_idx):
    # Fundo Cyberpunk
    img = Image.new("RGB", (WIDTH, HEIGHT), COLOR_BG_DEEP)
    draw = ImageDraw.Draw(img)
    
    # Grid de fundo cibernético
    grid_spacing = 80
    grid_offset = int((tempo_atual * 20) % grid_spacing)
    for x in range(0, WIDTH, grid_spacing):
        draw.line([(x, 0), (x, HEIGHT)], fill=(16, 24, 42), width=1)
    for y in range(grid_offset, HEIGHT, grid_spacing):
        draw.line([(0, y), (WIDTH, y)], fill=(16, 24, 42), width=1)
        
    # Topo: Badge de Autoridade
    top_badge_w, top_badge_h = 760, 60
    bx1 = (WIDTH - top_badge_w) // 2
    by1 = 120
    draw.rounded_rectangle([bx1, by1, bx1 + top_badge_w, by1 + top_badge_h], radius=30, fill=(30, 41, 59), outline=COLOR_CYAN_NEON, width=2)
    draw.text((bx1 + 40, by1 + 14), "🛡️ RADAR DE CIBERSEGURANÇA // ALERTA MÁXIMO", font=FONT_BADGE, fill=COLOR_CYAN_NEON)
    
    # Título Principal do Vídeo
    titulo_texto = "O GOLPE DO NOVO NÚMERO"
    draw.text((WIDTH // 2 - 320, 210), titulo_texto, font=FONT_TITLE, fill=COLOR_ACCENT_GOLD)
    
    # Efeito de pulso de alerta vermelho
    pulse = int(math.sin(tempo_atual * 6) * 127 + 128) > 100
    scanner_y = 520 + int((tempo_atual * 150) % 550)
    
    # Desenhar o painel central do WhatsApp
    desenhar_painel_whatsapp(draw, scanner_y, 0.4, pulse)
    
    # Linha laser de scanner verde/vermelho descendo sobre o WhatsApp
    draw.line([(100, scanner_y), (WIDTH - 100, scanner_y)], fill=COLOR_ALERT_RED, width=4)
    
    # Infográfico Inferior (Anatomia do Golpe em 3 Etapas)
    info_y = 1210
    draw.rounded_rectangle([80, info_y, WIDTH - 80, info_y + 260], radius=24, fill=(15, 23, 42), outline=(30, 41, 59), width=2)
    draw.text((110, info_y + 20), "🔬 ANATOMIA DO ATAQUE (COMO ELES FAZEM):", font=FONT_BADGE, fill=COLOR_ACCENT_GOLD)
    
    passos = [
        "1. Pegam sua foto pública nas redes sociais",
        "2. Compram um chip pré-pago sem cadastro de R$ 10",
        "3. Criam falso desespero pra você transferir sem pensar"
    ]
    for i, p in enumerate(passos):
        draw.text((110, info_y + 70 + (i * 55)), p, font=FONT_MSG_TIME, fill=COLOR_WHITE)

    # Legenda Dinâmica Estilo Alex Hormozi (Área Inferior de Alta Retenção)
    cena_atual = None
    for c in CENAS:
        if c["start"] <= tempo_atual <= c["end"]:
            cena_atual = c
            break
    if not cena_atual and CENAS:
        cena_atual = CENAS[-1]

    if cena_atual:
        caption_box_y1 = 1530
        caption_box_y2 = 1750
        draw.rounded_rectangle([60, caption_box_y1, WIDTH - 60, caption_box_y2], radius=28, fill=(8, 12, 22), outline=COLOR_ACCENT_GOLD, width=4)
        
        texto_cap = cena_atual["caption"]
        destaque = cena_atual["destaque"]
        
        # Desenha a legenda destacando em ouro
        draw.text((WIDTH // 2 - 420, caption_box_y1 + 40), texto_cap[:35], font=FONT_CAPTION_BIG, fill=COLOR_WHITE)
        if len(texto_cap) > 35:
            draw.text((WIDTH // 2 - 420, caption_box_y1 + 105), texto_cap[35:], font=FONT_CAPTION_BIG, fill=COLOR_ACCENT_GOLD)
            
        draw.text((WIDTH // 2 - 240, caption_box_y2 - 50), "👁️ SALVE E COMPARTILHE", font=FONT_BADGE, fill=COLOR_CYAN_NEON)

    # Rodapé de Proteção Familiar
    draw.text((WIDTH // 2 - 250, 1820), "🔒 Proteja seus pais, avós e sua família", font=FONT_HINT, fill=COLOR_TEXT_DIM)

    # Retorna o frame como array numpy para o OpenCV
    return cv2.cvtColor(np.array(img), cv2.COLOR_RGB2BGR)

async def renderizar_video_completo():
    print("=" * 65)
    print("🚀 INICIANDO RENDERIZADOR DARK 9:16 — ALERTA ANTI-GOLPE")
    print("=" * 65)
    
    # 1. Gerar o áudio com voz neural
    await gerar_audio_neural(TEXTO_NARRACAO, TEMP_AUDIO)
    duracao_total = obter_duracao_audio(TEMP_AUDIO)
    total_frames = int(duracao_total * FPS)
    print(f"⏱️ Duração detectada: {duracao_total:.2f}s ({total_frames} frames a {FPS} fps)")
    
    # 2. Configurar o VideoWriter do OpenCV
    fourcc = cv2.VideoWriter_fourcc(*'mp4v')
    out = cv2.VideoWriter(TEMP_VIDEO_SILENT, fourcc, FPS, (WIDTH, HEIGHT))
    
    print(f"🎬 Renderizando frames cinematográficos com efeitos visuais...")
    for f in range(total_frames):
        t = f / FPS
        frame_bgr = criar_frame(t, duracao_total, f)
        out.write(frame_bgr)
        
        if f % 90 == 0 or f == total_frames - 1:
            progresso = (f + 1) / total_frames * 100
            sys.stdout.write(f"\r   ⚡ Progresso da Renderização: {progresso:.1f}% ({f+1}/{total_frames} frames)")
            sys.stdout.flush()
            
    out.release()
    print("\n✅ Vídeo silencioso gerado com sucesso!")
    
    # 3. Juntar áudio neural com vídeo silencioso via FFmpeg (AAC + H.264)
    print("🎧 Fundindo áudio neural e vídeo com FFmpeg (H.264 + AAC)...")
    cmd_ffmpeg = [
        "ffmpeg", "-y",
        "-i", TEMP_VIDEO_SILENT,
        "-i", TEMP_AUDIO,
        "-c:v", "libx264",
        "-preset", "fast",
        "-crf", "20",
        "-c:a", "aac",
        "-b:a", "192k",
        "-shortest",
        OUTPUT_VIDEO
    ]
    subprocess.run(cmd_ffmpeg, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, check=True)
    
    # Limpeza de arquivos temporários
    try:
        if os.path.exists(TEMP_VIDEO_SILENT):
            os.remove(TEMP_VIDEO_SILENT)
    except Exception:
        pass
        
    tamanho_mb = os.path.getsize(OUTPUT_VIDEO) / (1024 * 1024)
    print("=" * 65)
    print(f"🎉 VÍDEO VERTICAL DARK PRONTO COM SUCESSO!")
    print(f"📍 Arquivo final: {OUTPUT_VIDEO}")
    print(f"📦 Tamanho: {tamanho_mb:.2f} MB | Resolução: {WIDTH}x{HEIGHT} (9:16)")
    print("=" * 65)

if __name__ == "__main__":
    asyncio.run(renderizar_video_completo())
