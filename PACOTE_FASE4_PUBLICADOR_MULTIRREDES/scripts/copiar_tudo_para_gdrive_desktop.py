#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
COPIADOR OFICIAL DE TODOS OS CORTES PARA O GOOGLE DRIVE DESKTOP (15 TB)
IBPM CR Automation System

Destino Oficial: G:\Meu Drive\#IBPM_CORTES_2026
"""

import sys
import shutil
import time
from pathlib import Path

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace", line_buffering=True)

DESTINO_ROOT = Path(r"G:\Meu Drive\#IBPM_CORTES_2026")
DESKTOP_DIR = Path.home() / "Desktop"

MAPEAMENTO = {
    "01_SHORTS_VERTICAIS_9x16": [
        DESKTOP_DIR / "CORTES_MULTIMODAIS_IBPM" / "TIER1_SHORTS_VERTICAIS",
        DESKTOP_DIR / "cortes_audio_culto_459_20_09_2026" / "05_SHORTS_APICE_45S"
    ],
    "02_CORTES_MEDIOS_VERTICAIS_9x16": [
        DESKTOP_DIR / "CORTES_MULTIMODAIS_IBPM" / "TIER2_MEDIOS_VERTICAIS_9x16",
        DESKTOP_DIR / "cortes_audio_culto_459_20_09_2026" / "02_VIDEOS_9x16_REELS"
    ],
    "03_CORTES_MEDIOS_HORIZONTAIS_16x9": [
        DESKTOP_DIR / "CORTES_MULTIMODAIS_IBPM" / "TIER2_MEDIOS_HORIZONTAIS_16x9",
        DESKTOP_DIR / "cortes_audio_culto_459_20_09_2026" / "01_VIDEOS_16x9_YOUTUBE"
    ],
    "04_PREGACOES_COMPLETAS_16x9": [
        DESKTOP_DIR / "CORTES_MULTIMODAIS_IBPM" / "TIER3_PREGACOES_TEMATICAS_16x9",
        DESKTOP_DIR / "cortes_audio_culto_459_20_09_2026" / "00_PREGACAO_COMPLETA_TIER3"
    ]
}


def main():
    print("=" * 80)
    print("🚀 SINCRONIZANDO ACERVO DE VÍDEOS COM GOOGLE DRIVE DESKTOP (15 TB)")
    print(f"📁 Destino Oficial: {DESTINO_ROOT}")
    print("=" * 80)

    if not DESTINO_ROOT.exists():
        print(f"❌ Erro: Destino {DESTINO_ROOT} não encontrado!")
        sys.exit(1)

    total_copiados = 0
    total_bytes = 0
    total_ja_existiam = 0

    for subpasta, origens in MAPEAMENTO.items():
        pasta_destino = DESTINO_ROOT / subpasta
        pasta_destino.mkdir(parents=True, exist_ok=True)
        print(f"\n📂 Processando Categoria: {subpasta}")

        for origem in origens:
            if not origem.exists():
                continue
            mp4s = sorted(list(origem.glob("*.mp4")))
            for mp4 in mp4s:
                tamanho = mp4.stat().st_size
                if tamanho < 100000:
                    continue  # Pula arquivo corrompido ou incompleto

                alvo = pasta_destino / mp4.name
                if alvo.exists() and alvo.stat().st_size == tamanho:
                    total_ja_existiam += 1
                    continue

                mb = tamanho / (1024 * 1024)
                print(f"   🚀 Copiando: {mp4.name} ({mb:.1f} MB)...", flush=True)
                try:
                    shutil.copy2(mp4, alvo)
                    total_copiados += 1
                    total_bytes += tamanho
                except Exception as e:
                    print(f"   ❌ Erro ao copiar {mp4.name}: {e}", flush=True)

    print("\n" + "=" * 80)
    print("🎉 SINCRONIZAÇÃO COMPLETA COM O GOOGLE DRIVE!")
    print(f"   ✔ Novos vídeos copiados agora: {total_copiados} ({total_bytes / (1024*1024):.1f} MB)")
    print(f"   ✔ Vídeos já presentes: {total_ja_existiam}")
    print(f"   🔥 Total no Google Drive: {total_copiados + total_ja_existiam} vídeos!")
    print("   O Google Drive para Desktop está enviando tudo para a nuvem de 15 TB.")
    print("=" * 80)


if __name__ == "__main__":
    main()
