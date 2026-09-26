#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
SINCRONIZADOR MESTRE MULTIRREDES — 3 VÍDEOS POR DIA (FASE 4)
IBPM CR Automation System

Sincroniza rigorosamente com o mesmo conteúdo, mesmas copies, mesmas tags e mesmos horários em:
1. 🔴 YouTube Shorts
2. 🟣 Instagram Reels
3. 🔵 Facebook Reels (via Meta Graph)
4. ⚫ TikTok
5. 🟢 WhatsApp Status & Canal

Horários Nobres de Pico Diário:
- Almoço: 12:00 BRT
- Final de Tarde: 18:00 BRT
- Noite: 21:00 BRT
"""

import sys
import json
from pathlib import Path
from datetime import datetime, timedelta, timezone

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")

BASE_DIR = Path(__file__).resolve().parent.parent.parent
DESKTOP_DIR = Path.home() / "Desktop" / "cortes_audio_culto_459_20_09_2026"
SHORTS_DIR = DESKTOP_DIR / "05_SHORTS_APICE_45S"
METADADOS_FILE = DESKTOP_DIR / "00_COPIES_E_METADADOS_POSTAGEM.json"

TZ_BRT = timezone(timedelta(hours=-3))

def main():
    print("=" * 80)
    print("⚡ SINCRONIZADOR MULTIRREDES OMNICHANNEL — 3 POSTAGENS POR DIA")
    print("=" * 80)

    arquivos_shorts = sorted(list(SHORTS_DIR.glob("*.mp4")))
    if not arquivos_shorts:
        print("❌ Nenhum short encontrado no diretório.")
        return

    with open(METADADOS_FILE, "r", encoding="utf-8") as f:
        meta_geral = json.load(f)

    cortes_lista = meta_geral.get("cortes_medios_tier2", [])
    mapa_info = {c.get("numero", i+1): c for i, c in enumerate(cortes_lista)}

    # Horários da Grade Massiva de 6 Vídeos por Dia:
    horarios_pico = ["06:00", "09:00", "12:00", "15:00", "18:00", "21:00"]
    data_base = datetime(2026, 9, 22, tzinfo=TZ_BRT)

    plano_sincronizado = []
    total_slots = len(horarios_pico)

    for i, arq in enumerate(arquivos_shorts):
        num_corte = i + 1
        dia_offset = i // total_slots
        slot_idx = i % total_slots
        horario_str = horarios_pico[slot_idx]
        hora, minuto = map(int, horario_str.split(":"))

        dt_agendada = data_base + timedelta(days=dia_offset)
        dt_agendada = dt_agendada.replace(hour=hora, minute=minuto, second=0)

        info = mapa_info.get(num_corte, {})
        yt = info.get("youtube_16x9", {})
        ig = info.get("instagram_reels_9x16", {})
        tk = info.get("tiktok_9x16", {})

        titulo = ig.get("headline_gancho") or yt.get("titulo_seo") or f"Corte #{num_corte}"
        legenda = ig.get("copy_legenda") or tk.get("copy_tiktok") or titulo
        hashtags = ig.get("hashtags_estrategicas") or "#fe #deus #milagre #jesus #pregacao"

        item = {
            "id_corte": f"SHORT_{num_corte:02d}",
            "arquivo_mp4": arq.name,
            "tamanho_mb": round(arq.stat().st_size / (1024 * 1024), 2),
            "dia_numero": dia_offset + 1,
            "data_horario_brt": dt_agendada.strftime("%d/%m/%Y às %H:%M BRT"),
            "timestamp_iso": dt_agendada.isoformat(),
            "titulo_unificado": titulo,
            "copy_unificada": legenda,
            "hashtags_unificadas": hashtags,
            "redes_ativas": [
                "YouTube Shorts",
                "Instagram Reels",
                "Facebook Reels",
                "TikTok",
                "WhatsApp Status",
                "Canal WhatsApp"
            ],
            "status_sincronizacao": "PROGRAMADO"
        }
        plano_sincronizado.append(item)

    # 1. Salva JSON Mestre de Sincronização (Ambos os nomes para máxima compatibilidade)
    out_json = DESKTOP_DIR / "00_SINCRONIZACAO_MULTIRREDES_3_POSTS_DIA.json"
    out_json_6 = DESKTOP_DIR / "00_SINCRONIZACAO_MULTIRREDES_6_POSTS_DIA.json"
    with open(out_json, "w", encoding="utf-8") as f:
        json.dump(plano_sincronizado, f, indent=2, ensure_ascii=False)
    with open(out_json_6, "w", encoding="utf-8") as f:
        json.dump(plano_sincronizado, f, indent=2, ensure_ascii=False)

    # 2. Salva Relatório Markdown Visual
    out_md = DESKTOP_DIR / "00_GRADE_6_POSTS_DIA_SINCRONIZADA.md"
    with open(out_md, "w", encoding="utf-8") as f:
        f.write("# 📡 GRADE OFICIAL SINCRONIZADA MULTIRREDES — 6 VÍDEOS POR DIA\n")
        f.write("### YouTube Shorts • Instagram Reels • Facebook • TikTok • WhatsApp\n\n")
        f.write("> **Alinhamento Rigoroso:** O mesmo vídeo, mesmo gancho e mesma mensagem disparados simultaneamente a cada 3 horas.\n\n")
        f.write("| Horário de Pico | Foco Espiritual | Redes Sincronizadas |\n")
        f.write("| :---: | :--- | :--- |\n")
        f.write("| **06:00 BRT** | 🌅 Oração do Despertar & Versículo | YouTube + Instagram + TikTok + WhatsApp |\n")
        f.write("| **09:00 BRT** | ☕ Ânimo & Força no Trabalho | YouTube + Instagram + TikTok + WhatsApp |\n")
        f.write("| **12:00 BRT** | 📖 Alimento Bíblico do Almoço | YouTube + Instagram + TikTok + WhatsApp |\n")
        f.write("| **15:00 BRT** | 🔥 Renovo & Quebra de Desânimo | YouTube + Instagram + TikTok + WhatsApp |\n")
        f.write("| **18:00 BRT** | 🛡️ Família & Volta para Casa | YouTube + Instagram + TikTok + WhatsApp |\n")
        f.write("| **21:00 BRT** | 🕊️ Paz, Cura da Alma & Descanso | YouTube + Instagram + TikTok + WhatsApp |\n\n")
        f.write("---\n\n")

        dia_atual = 0
        for p in plano_sincronizado:
            if p["dia_numero"] != dia_atual:
                dia_atual = p["dia_numero"]
                f.write(f"\n## 📅 DIA {dia_atual:02d} — {p['data_horario_brt'].split(' às ')[0]}\n\n")

            f.write(f"### ⚡ [{p['data_horario_brt'].split(' às ')[1]}] {p['id_corte']} — {p['titulo_unificado']}\n")
            f.write(f"- 📁 **Arquivo:** `{p['arquivo_mp4']}` ({p['tamanho_mb']} MB)\n")
            f.write(f"- 🌐 **Canais:** {', '.join(p['redes_ativas'])}\n")
            f.write(f"- 📝 **Copy:**\n> {p['copy_unificada'][:200]}...\n\n")

    print("✅ Plano Multirredes de 6 Vídeos/Dia gerado com sucesso!")
    print(f"   📄 Markdown: {out_md.name}")
    print(f"   💾 JSON: {out_json_6.name}")

if __name__ == "__main__":
    main()
