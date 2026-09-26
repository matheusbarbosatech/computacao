#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
SINCRONIZADOR DE CORTES LOCAIS PARA O GOOGLE DRIVE DESKTOP (FASE 4)
IBPM CR Automation System

Copia automaticamente todos os vídeos renderizados (Shorts 9:16)
da máquina local para a pasta do Google Drive Desktop (marybarbosaa139@gmail.com).
"""

import sys
import shutil
from pathlib import Path

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")

DESKTOP_DIR = Path.home() / "Desktop"

ORIGENS = [
    DESKTOP_DIR / "cortes_audio_culto_459_20_09_2026" / "05_SHORTS_APICE_45S",
    DESKTOP_DIR / "CORTES_MULTIMODAIS_IBPM"
]

POSSIVEIS_DESTINOS_GDRIVE = [
    Path("G:/Meu Drive/IBPM_CORTES_2026"),
    Path("G:/My Drive/IBPM_CORTES_2026"),
    Path.home() / "Google Drive" / "IBPM_CORTES_2026",
    Path.home() / "Meu Drive" / "IBPM_CORTES_2026"
]


def encontrar_pasta_gdrive() -> Path:
    for d in POSSIVEIS_DESTINOS_GDRIVE:
        if d.parent.exists():
            d.mkdir(parents=True, exist_ok=True)
            return d
    return None


def main():
    print("=" * 80)
    print("☁️ SINCRONIZADOR DE VÍDEOS: COMPUTADOR ➡️ GOOGLE DRIVE (15 TB)")
    print("=" * 80)

    destino = encontrar_pasta_gdrive()
    if not destino:
        print("\n⚠️ A pasta do Google Drive Desktop não foi detectada automaticamente.")
        print("   Se você já instalou o Google Drive para Desktop:")
        print("   1. Abra o app do Google Drive no Windows e certifique-se de que está logado.")
        print("   2. Crie uma pasta 'IBPM_CORTES_2026' dentro do seu Meu Drive.")
        print(f"   Ou copie manualmente os arquivos das seguintes pastas para o seu Drive:")
        for o in ORIGENS:
            print(f"   📂 {o}")
        return

    print(f"\n📁 Destino detectado no Google Drive: {destino}")

    total_copiados = 0
    total_bytes = 0

    for origem in ORIGENS:
        if not origem.exists():
            continue
        arquivos = list(origem.glob("*.mp4"))
        print(f"\n🔍 Varrendo pasta: {origem.name} ({len(arquivos)} vídeos encontrados)...")

        for arq in arquivos:
            dest_arq = destino / arq.name
            if not dest_arq.exists() or dest_arq.stat().st_size != arq.stat().st_size:
                print(f"   🚀 Copiando: {arq.name} ({arq.stat().st_size / (1024*1024):.2f} MB)...")
                try:
                    shutil.copy2(arq, dest_arq)
                    total_copiados += 1
                    total_bytes += arq.stat().st_size
                except Exception as e:
                    print(f"   ❌ Erro ao copiar {arq.name}: {e}")
            else:
                print(f"   ✔ Já sincronizado no Drive: {arq.name}")

    print("\n" + "=" * 80)
    print(f"🎉 SINCRONIZAÇÃO CONCLUÍDA!")
    print(f"   Novos vídeos copiados para o Google Drive: {total_copiados}")
    print(f"   Volume transferido: {total_bytes / (1024*1024):.2f} MB")
    print(f"   Os vídeos serão enviados para a nuvem pelo Google Drive Desktop em segundo plano.")
    print("=" * 80)


if __name__ == "__main__":
    main()
