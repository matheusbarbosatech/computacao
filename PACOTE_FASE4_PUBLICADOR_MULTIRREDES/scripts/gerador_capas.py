#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
GERADOR AUTOMÁTICO DE CAPAS E THUMBNAILS PROFISSIONAIS — CULTO 459 (20/09/2026)
IBPM CR Automation System — Fase 4

Produz:
1. 📺 Capas 16:9 para YouTube (1280x720):
   - Frame nítido 1080p do pregador.
   - Vinheta escura de contraste.
   - Tipografia de alto impacto (Impact / Arial Bold).
   - Palavras-chave em Amarelo Ouro (#FFD700) e Branco puro com contorno preto 6px.
   - Badge oficial "IBPM PALAVRA E MOVIMENTO".
2. 📱 Capas 9:16 para Reels/Shorts/TikTok (1080x1920):
   - Frame vertical com a headline no terço superior seguro (Safe Zone).
3. 📖 Capa Mestre do Tier 3 (Pregação Completa 16:9).

Destino: C:\\Users\\matheus\\Desktop\\cortes_audio_culto_459_20_09_2026\\04_CAPAS_THUMBNAILS\\
"""

import sys
import subprocess
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont, ImageEnhance, ImageFilter

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
if hasattr(sys.stderr, "reconfigure"):
    sys.stderr.reconfigure(encoding="utf-8", errors="replace")

BASE_DIR = Path(__file__).resolve().parent.parent.parent
DESKTOP_DIR = Path.home() / "Desktop" / "cortes_audio_culto_459_20_09_2026"
DIR_16x9_SRC = DESKTOP_DIR / "01_VIDEOS_16x9_YOUTUBE"
DIR_9x16_SRC = DESKTOP_DIR / "02_VIDEOS_9x16_REELS"

OUT_DIR_THUMBS = DESKTOP_DIR / "04_CAPAS_THUMBNAILS"
OUT_16x9 = OUT_DIR_THUMBS / "16x9_YOUTUBE"
OUT_9x16 = OUT_DIR_THUMBS / "9x16_REELS"

for d in [OUT_16x9, OUT_9x16]:
    d.mkdir(parents=True, exist_ok=True)

# Fontes padrão do Windows
FONT_IMPACT = Path(r"C:\Windows\Fonts\impact.ttf")
FONT_ARIAL_BD = Path(r"C:\Windows\Fonts\arialbd.ttf")

FONT_PATH = str(FONT_IMPACT) if FONT_IMPACT.exists() else str(FONT_ARIAL_BD)
FONT_SUB_PATH = str(FONT_ARIAL_BD) if FONT_ARIAL_BD.exists() else FONT_PATH

# 14 Cortes + Tier 3 com títulos de thumbnail em caixa alta
TITULOS_CAPAS = {
    "MEDIO_01": {
        "linha1": "FUI ALCANÇADA",
        "linha2": "PELA TRANSMISSÃO!",
        "palavra_ouro": "TRANSMISSÃO!",
        "tag": "TESTEMUNHO FORTE"
    },
    "MEDIO_02": {
        "linha1": "VOCÊ NÃO É QUEM",
        "linha2": "O CHÃO DISSE!",
        "palavra_ouro": "NÃO É QUEM",
        "tag": "MENSAGEM DE GIDEÃO"
    },
    "MEDIO_04": {
        "linha1": "A SEMENTE",
        "linha2": "NO ESCURO!",
        "palavra_ouro": "NO ESCURO!",
        "tag": "TEMPO DE DEUS"
    },
    "MEDIO_05": {
        "linha1": "QUANDO O CHÃO",
        "linha2": "DESAPARECE!",
        "palavra_ouro": "DESAPARECE!",
        "tag": "ESPÍRITO SANTO NO LUTO"
    },
    "MEDIO_06": {
        "linha1": "LEVANTE E",
        "linha2": "PROFETIZE HOJE!",
        "palavra_ouro": "PROFETIZE HOJE!",
        "tag": "RECUPERE SUA IDENTIDADE"
    },
    "MEDIO_07": {
        "linha1": "VALE DE",
        "linha2": "OSSOS SECOS!",
        "palavra_ouro": "OSSOS SECOS!",
        "tag": "ONDE HÁ MORTE, HÁ VIDA"
    },
    "MEDIO_08": {
        "linha1": "OU VOCÊ É O OSSO",
        "linha2": "OU O PROFETA!",
        "palavra_ouro": "O PROFETA!",
        "tag": "DECISÃO ESPIRITUAL"
    },
    "MEDIO_09": {
        "linha1": "MÃO NA CABEÇA",
        "linha2": "PROFETIZE VIDA!",
        "palavra_ouro": "PROFETIZE VIDA!",
        "tag": "ORAÇÃO DE LIBERTAÇÃO"
    },
    "MEDIO_03": {
        "linha1": "O DEUS DO",
        "linha2": "DE REPENTE!",
        "palavra_ouro": "DE REPENTE!",
        "tag": "20 ANOS EM 1 SEGUNDO"
    },
    "MEDIO_10": {
        "linha1": "O ANEL E AS",
        "linha2": "SANDÁLIAS DO PAI!",
        "palavra_ouro": "SANDÁLIAS DO PAI!",
        "tag": "RESTITUIÇÃO DE FILHO"
    },
    "MEDIO_11": {
        "linha1": "DE MÃOS DADAS COM",
        "linha2": "O ESPÍRITO SANTO!",
        "palavra_ouro": "O ESPÍRITO SANTO!",
        "tag": "INTIMIDADE E FORÇA"
    },
    "MEDIO_12": {
        "linha1": "TIRE A VESTE",
        "linha2": "DE VERGONHA!",
        "palavra_ouro": "DE VERGONHA!",
        "tag": "RECEBA O VINHO NOVO"
    },
    "PASTOR_01": {
        "linha1": "A VERDADEIRA",
        "linha2": "ADORAÇÃO A DEUS!",
        "palavra_ouro": "ADORAÇÃO A DEUS!",
        "tag": "PR. PRESIDENTE"
    },
    "PASTOR_02": {
        "linha1": "ESTÁ DOENDO, MAS",
        "linha2": "DOU O MEU MELHOR!",
        "palavra_ouro": "MEU MELHOR!",
        "tag": "ENTREGA NO ALTAR"
    }
}


def extrair_frame(video_path: Path, out_path: Path, segundo: float = 18.0) -> bool:
    """Extrai frame em altíssima qualidade via FFmpeg."""
    cmd = [
        "ffmpeg", "-y", "-ss", str(segundo),
        "-i", str(video_path),
        "-vframes", "1",
        "-q:v", "2",
        str(out_path)
    ]
    res = subprocess.run(cmd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    return res.returncode == 0 and out_path.exists() and out_path.stat().st_size > 0


def desenhar_texto_com_contorno(
    draw: ImageDraw.ImageDraw,
    pos: tuple,
    texto: str,
    fonte: ImageFont.FreeTypeFont,
    cor_texto: str = "#FFFFFF",
    cor_contorno: str = "#000000",
    espessura: int = 5,
    sombra_offset: int = 4
):
    x, y = pos
    # Sombra suave projetada
    if sombra_offset > 0:
        for ox in range(sombra_offset - 1, sombra_offset + 2):
            for oy in range(sombra_offset - 1, sombra_offset + 2):
                draw.text((x + ox, y + oy), texto, font=fonte, fill=(0, 0, 0, 180))

    # Contorno espesso (Stroke)
    for ox in range(-espessura, espessura + 1):
        for oy in range(-espessura, espessura + 1):
            if ox != 0 or oy != 0:
                draw.text((x + ox, y + oy), texto, font=fonte, fill=cor_contorno)

    # Texto principal
    draw.text((x, y), texto, font=fonte, fill=cor_texto)


def criar_gradiente_vinheta(largura: int, altura: int, intensidade_esquerda: float = 0.85, intensidade_baixo: float = 0.7) -> Image.Image:
    """Gera máscara escura degradê para garantir legibilidade de 100%."""
    img = Image.new("RGBA", (largura, altura), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)

    for y in range(altura):
        fator_y = (y / altura) ** 1.5 * intensidade_baixo
        for x in range(0, int(largura * 0.75), 10):
            fator_x = (1.0 - (x / (largura * 0.75))) ** 1.3 * intensidade_esquerda
            alpha = int(min(255, (fator_x + fator_y) * 255))
            draw.rectangle([x, y, x + 10, y + 1], fill=(0, 0, 0, alpha))

    return img


def gerar_thumbnail_16x9(video_path: Path, info: dict, out_img_path: Path):
    temp_frame = out_img_path.parent / f"temp_{video_path.stem}.jpg"
    if not extrair_frame(video_path, temp_frame, segundo=20.0):
        # Fallback para o segundo 5 caso o corte seja curto
        extrair_frame(video_path, temp_frame, segundo=5.0)

    if not temp_frame.exists():
        print(f"⚠️ Não foi possível extrair frame de {video_path.name}")
        return

    # Abre e redimensiona para 1280x720 (padrão ouro YouTube)
    base = Image.open(temp_frame).convert("RGB")
    base = base.resize((1280, 720), Image.Resampling.LANCZOS)

    # Realce de cor e contraste para visual moderno
    base = ImageEnhance.Color(base).enhance(1.15)
    base = ImageEnhance.Contrast(base).enhance(1.18)

    # Aplica vinheta escura lateral e inferior
    vinheta = criar_gradiente_vinheta(1280, 720, intensidade_esquerda=0.9, intensidade_baixo=0.6)
    base.paste(vinheta, (0, 0), vinheta)

    draw = ImageDraw.Draw(base)

    # Carrega fontes com tamanhos ajustados
    fonte_badge = ImageFont.truetype(FONT_SUB_PATH, 24)
    fonte_tag = ImageFont.truetype(FONT_SUB_PATH, 28)
    fonte_titulo = ImageFont.truetype(FONT_PATH, 68)

    # 1. Badge Topo: IBPM PALAVRA E MOVIMENTO
    badge_texto = "IBPM | CAMPO GRANDE"
    draw.rounded_rectangle([45, 40, 45 + 320, 80], radius=8, fill=(0, 0, 0, 210), outline="#FFD700", width=2)
    draw.text((65, 46), badge_texto, font=fonte_badge, fill="#FFFFFF")

    # 2. Tag Temática com fundo vermelho vivo ou dourado
    tag_texto = f"  {info['tag']}  "
    bbox_tag = draw.textbbox((0, 0), tag_texto, font=fonte_tag)
    tag_w = bbox_tag[2] - bbox_tag[0]
    draw.rounded_rectangle([45, 105, 45 + tag_w, 150], radius=6, fill="#E50914")
    draw.text((45, 110), tag_texto, font=fonte_tag, fill="#FFFFFF")

    # 3. Título Principal em 2 Linhas
    linha1 = info["linha1"]
    linha2 = info["linha2"]

    # Se uma linha tiver a palavra de ouro, destaca ela
    cor_l1 = "#FFD700" if info["palavra_ouro"] in linha1 else "#FFFFFF"
    cor_l2 = "#FFD700" if info["palavra_ouro"] in linha2 else "#FFFFFF"

    desenhar_texto_com_contorno(draw, (45, 490), linha1, fonte_titulo, cor_texto=cor_l1, cor_contorno="#000000", espessura=6)
    desenhar_texto_com_contorno(draw, (45, 575), linha2, fonte_titulo, cor_texto=cor_l2, cor_contorno="#000000", espessura=6)

    # Borda sutil de moldura de 3px
    draw.rectangle([0, 0, 1279, 719], outline=(255, 215, 0, 160), width=3)

    base.save(out_img_path, quality=95)
    temp_frame.unlink(missing_ok=True)
    print(f"   📺 [16:9] Capa YouTube gerada: {out_img_path.name}")


def gerar_thumbnail_9x16(video_path: Path, info: dict, out_img_path: Path):
    temp_frame = out_img_path.parent / f"temp_{video_path.stem}.jpg"
    if not extrair_frame(video_path, temp_frame, segundo=20.0):
        extrair_frame(video_path, temp_frame, segundo=5.0)

    if not temp_frame.exists():
        return

    # Abre e redimensiona para 1080x1920
    base = Image.open(temp_frame).convert("RGB")
    base = base.resize((1080, 1920), Image.Resampling.LANCZOS)
    base = ImageEnhance.Color(base).enhance(1.12)
    base = ImageEnhance.Contrast(base).enhance(1.15)

    draw = ImageDraw.Draw(base)

    fonte_card_sub = ImageFont.truetype(FONT_SUB_PATH, 30)
    fonte_card_tit = ImageFont.truetype(FONT_PATH, 74)

    # Card superior no Terço Seguro (Safe Zone de Reels: y=250 a y=560)
    card_box = [60, 240, 1020, 560]
    draw.rounded_rectangle(card_box, radius=24, fill=(0, 0, 0, 210), outline="#FFD700", width=4)

    # Tag no card
    draw.text((100, 270), f"⚡ {info['tag']}", font=fonte_card_sub, fill="#FFD700")

    # Linha 1 e Linha 2
    l1 = info["linha1"]
    l2 = info["linha2"]
    cor_l1 = "#FFD700" if info["palavra_ouro"] in l1 else "#FFFFFF"
    cor_l2 = "#FFD700" if info["palavra_ouro"] in l2 else "#FFFFFF"

    desenhar_texto_com_contorno(draw, (100, 335), l1, fonte_card_tit, cor_texto=cor_l1, cor_contorno="#000000", espessura=5)
    desenhar_texto_com_contorno(draw, (100, 425), l2, fonte_card_tit, cor_texto=cor_l2, cor_contorno="#000000", espessura=5)

    base.save(out_img_path, quality=95)
    temp_frame.unlink(missing_ok=True)
    print(f"   📱 [9:16] Capa Reels gerada:   {out_img_path.name}")


def gerar_capa_tier3_mestre():
    """Gera a Capa Oficial de Impacto da Pregação Completa (Tier 3)."""
    # Usa como base o vídeo do culto 459 ou o corte de Gideão/Pastor
    video_ref = list(DIR_16x9_SRC.glob("MEDIO_02*.mp4"))
    if not video_ref:
        video_ref = list(DIR_16x9_SRC.glob("*.mp4"))
    if not video_ref:
        return

    out_tier3 = OUT_16x9 / "THUMBNAIL_TIER3_PREGACAO_COMPLETA_CULTO_459.jpg"
    temp_frame = OUT_DIR_THUMBS / "temp_tier3.jpg"

    extrair_frame(video_ref[0], temp_frame, segundo=25.0)
    if not temp_frame.exists():
        return

    base = Image.open(temp_frame).convert("RGB")
    base = base.resize((1280, 720), Image.Resampling.LANCZOS)
    base = ImageEnhance.Color(base).enhance(1.20)
    base = ImageEnhance.Contrast(base).enhance(1.25)

    vinheta = criar_gradiente_vinheta(1280, 720, intensidade_esquerda=0.95, intensidade_baixo=0.8)
    base.paste(vinheta, (0, 0), vinheta)

    draw = ImageDraw.Draw(base)

    fonte_badge = ImageFont.truetype(FONT_SUB_PATH, 26)
    fonte_super = ImageFont.truetype(FONT_PATH, 86)
    fonte_selo = ImageFont.truetype(FONT_SUB_PATH, 34)

    # 1. Selo Topo Esquerda: PREGAÇÃO COMPLETA
    draw.rounded_rectangle([45, 38, 45 + 380, 95], radius=10, fill="#E50914", outline="#FFFFFF", width=2)
    draw.text((65, 47), "★ PREGAÇÃO COMPLETA ★", font=fonte_selo, fill="#FFFFFF")

    # 2. Data / Local
    draw.rounded_rectangle([45, 115, 45 + 340, 158], radius=8, fill=(0, 0, 0, 220), outline="#FFD700", width=2)
    draw.text((60, 122), "DOMINGO DE CELEBRAÇÃO • 20/09", font=fonte_badge, fill="#FFD700")

    # 3. Título Épico
    desenhar_texto_com_contorno(draw, (45, 450), "O DEUS DO", fonte_super, cor_texto="#FFFFFF", cor_contorno="#000000", espessura=8)
    desenhar_texto_com_contorno(draw, (45, 550), "DE REPENTE!", fonte_super, cor_texto="#FFD700", cor_contorno="#000000", espessura=8)

    # Moldura Dourada
    draw.rectangle([0, 0, 1279, 719], outline="#FFD700", width=5)

    base.save(out_tier3, quality=98)
    temp_frame.unlink(missing_ok=True)
    print(f"\n🌟 [TIER 3] Capa Mestre da Pregação Completa gerada:")
    print(f"   --> {out_tier3.name}")


def executar():
    print("=" * 80)
    print("🎨 INICIANDO GERAÇÃO AUTOMÁTICA DE CAPAS E THUMBNAILS — CULTO 459")
    print(f"   Destino 16:9: {OUT_16x9}")
    print(f"   Destino 9:16: {OUT_9x16}")
    print("=" * 80)

    # 1. Capa Mestre do Tier 3
    gerar_capa_tier3_mestre()

    # 2. Capas dos 14 Cortes Médios (16:9 e 9:16)
    for c_id, info in TITULOS_CAPAS.items():
        v16_list = list(DIR_16x9_SRC.glob(f"*{c_id}*.mp4"))
        v9_list  = list(DIR_9x16_SRC.glob(f"*{c_id}*.mp4"))

        if v16_list:
            out_16 = OUT_16x9 / f"THUMB_{v16_list[0].stem}.jpg"
            gerar_thumbnail_16x9(v16_list[0], info, out_16)

        if v9_list:
            out_9 = OUT_9x16 / f"CAPA_REELS_{v9_list[0].stem}.jpg"
            gerar_thumbnail_9x16(v9_list[0], info, out_9)

    print("\n" + "=" * 80)
    print("✅ TODAS AS CAPAS FORAM GERADAS COM SUCESSO!")
    print(f"   Total de Capas 16:9 (YouTube): {len(list(OUT_16x9.glob('*.jpg')))}")
    print(f"   Total de Capas 9:16 (Reels):   {len(list(OUT_9x16.glob('*.jpg')))}")
    print("=" * 80)


if __name__ == "__main__":
    executar()
