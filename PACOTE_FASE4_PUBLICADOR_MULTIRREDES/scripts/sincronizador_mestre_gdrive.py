#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
SINCRONIZADOR MESTRE DO GOOGLE DRIVE (15 TB) — REPOSITÓRIO CENTRAL DEFINITIVO
IBPM CR Automation System

Gerencia e sincroniza TODOS os cortes do projeto para a pasta oficial do Drive:
Conta: marybarbosaa139@gmail.com (15 TB)
Pasta Raiz: https://drive.google.com/drive/folders/1hcRgIFmJBqiUq1w1dXnMwcFdCc7nzOFk

Escaneia e sincroniza:
1. Todos os vídeos já renderizados em CORTES_MULTIMODAIS_IBPM (Tier 1, Tier 2, Tier 3)
2. Todos os vídeos do culto 459 (05_SHORTS_APICE_45S)
3. Modo contínuo (--watch / --daemon) para enviar automaticamente os NOVOS cortes assim que forem renderizados!
"""

import os
import sys
import json
import time
import argparse
import shutil
from pathlib import Path

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
if hasattr(sys.stderr, "reconfigure"):
    sys.stderr.reconfigure(encoding="utf-8", errors="replace")

BASE_DIR = Path(__file__).resolve().parent.parent.parent
CREDENTIALS_DIR = BASE_DIR / "config" / "credentials"
CLIENT_SECRETS = CREDENTIALS_DIR / "client_secret.json"
TOKEN_GDRIVE = CREDENTIALS_DIR / "token_gdrive.json"
CACHE_SYNC = BASE_DIR / "data" / "gdrive_synced_files.json"

ROOT_FOLDER_ID = "1hcRgIFmJBqiUq1w1dXnMwcFdCc7nzOFk"
DESKTOP_DIR = Path.home() / "Desktop"

PASTAS_FONTE = {
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

SCOPES = ["https://www.googleapis.com/auth/drive.file"]


def carregar_cache_sincronizados() -> dict:
    if CACHE_SYNC.exists():
        try:
            return json.load(open(CACHE_SYNC, encoding="utf-8"))
        except Exception:
            return {}
    return {}


def salvar_cache_sincronizados(cache: dict):
    CACHE_SYNC.parent.mkdir(parents=True, exist_ok=True)
    with open(CACHE_SYNC, "w", encoding="utf-8") as f:
        json.dump(cache, f, indent=2, ensure_ascii=False)


def autenticar_gdrive():
    try:
        from google_auth_oauthlib.flow import InstalledAppFlow
        from google.oauth2.credentials import Credentials
        from googleapiclient.discovery import build
    except ImportError:
        print("⚠️ Bibliotecas do Google não instaladas. Execute: pip install google-api-python-client google-auth-oauthlib")
        return None

    creds = None
    if TOKEN_GDRIVE.exists():
        try:
            creds = Credentials.from_authorized_user_file(str(TOKEN_GDRIVE), SCOPES)
        except Exception:
            pass

    if not creds or not creds.valid:
        if not CLIENT_SECRETS.exists():
            print(f"❌ client_secret.json não encontrado em: {CLIENT_SECRETS}")
            return None
        print("\n🌐 Abrindo janela de autorização do Google Drive no navegador...")
        print("👉 Selecione a conta: marybarbosaa139@gmail.com")
        flow = InstalledAppFlow.from_client_secrets_file(str(CLIENT_SECRETS), SCOPES)
        creds = flow.run_local_server(port=0)
        with open(TOKEN_GDRIVE, "w", encoding="utf-8") as f:
            f.write(creds.to_json())
        print("✅ Autenticação realizada com sucesso!")

    return build("drive", "v3", credentials=creds)


def obter_ou_criar_subpasta(service, nome_pasta: str, parent_id: str) -> str:
    """Garante que a subpasta exista no Drive dentro da pasta raiz de 15 TB."""
    query = f"'{parent_id}' in parents and name='{nome_pasta}' and mimeType='application/vnd.google-apps.folder' and trashed=false"
    results = service.files().list(q=query, fields="files(id, name)").execute()
    pastas = results.get("files", [])
    if pastas:
        return pastas[0]["id"]

    metadata = {
        "name": nome_pasta,
        "mimeType": "application/vnd.google-apps.folder",
        "parents": [parent_id]
    }
    nova_pasta = service.files().create(body=metadata, fields="id").execute()
    print(f"   📁 Subpasta criada no Drive: {nome_pasta} (ID: {nova_pasta.get('id')})")
    return nova_pasta.get("id")


def executar_sincronizacao_completa(service = None):
    print("=" * 80)
    print("📦 INVENTÁRIO GERAL DE CORTES PARA O GOOGLE DRIVE (15 TB)")
    print("=" * 80)

    cache = carregar_cache_sincronizados()
    total_encontrados = 0
    total_pendentes = 0
    arquivos_para_upload = []

    for categoria, caminhos in PASTAS_FONTE.items():
        print(f"\n📂 Categoria: {categoria}")
        cat_encontrados = 0
        for p in caminhos:
            if not p.exists():
                continue
            mp4s = list(p.glob("*.mp4"))
            for mp4 in mp4s:
                if mp4.stat().st_size < 100000:
                    continue  # Pula arquivos incompletos
                total_encontrados += 1
                cat_encontrados += 1
                nome = mp4.name
                tamanho_mb = mp4.stat().st_size / (1024 * 1024)

                ja_sincronizado = nome in cache
                if ja_sincronizado:
                    status = "✔ JÁ NO DRIVE"
                else:
                    status = "⏳ PENDENTE UPLOAD"
                    total_pendentes += 1
                    arquivos_para_upload.append({
                        "categoria": categoria,
                        "arquivo": mp4,
                        "nome": nome,
                        "tamanho_mb": tamanho_mb
                    })

        print(f"   Total de vídeos nesta categoria: {cat_encontrados}")

    print("\n" + "=" * 80)
    print(f"📊 RESUMO DO ACERVO:")
    print(f"   Total de Vídeos Prontos: {total_encontrados}")
    print(f"   Já Sincronizados no Drive: {len(cache)}")
    print(f"   Pendentes de Upload: {total_pendentes}")
    print("=" * 80)

    if total_pendentes == 0:
        print("🎉 Todos os cortes já estão sincronizados no Google Drive!")
        return

    # Se serviço foi fornecido, executa o upload
    if service:
        from googleapiclient.http import MediaFileUpload
        subpastas_ids = {}

        for i, item in enumerate(arquivos_para_upload):
            cat = item["categoria"]
            nome = item["nome"]
            arq_path = item["arquivo"]
            mb = item["tamanho_mb"]

            if cat not in subpastas_ids:
                subpastas_ids[cat] = obter_ou_criar_subpasta(service, cat, ROOT_FOLDER_ID)

            folder_alvo = subpastas_ids[cat]
            print(f"\n[{i+1}/{len(arquivos_para_upload)}] ☁️ Enviando '{nome}' ({mb:.1f} MB) para '{cat}'...")

            try:
                metadata = {"name": nome, "parents": [folder_alvo]}
                media = MediaFileUpload(str(arq_path), mimetype="video/mp4", resumable=True)
                res = service.files().create(body=metadata, media_body=media, fields="id").execute()
                file_id = res.get("id")
                print(f"   ✅ Concluído! Drive ID: {file_id}")

                cache[nome] = {
                    "drive_id": file_id,
                    "categoria": cat,
                    "data_upload": time.strftime("%Y-%m-%d %H:%M:%S")
                }
                salvar_cache_sincronizados(cache)
            except Exception as e:
                print(f"   ❌ Falha no envio de {nome}: {e}")

        print("\n🎉 Lote enviado com sucesso para a pasta oficial de 15 TB!")


def main():
    parser = argparse.ArgumentParser(description="Sincronizador Mestre Google Drive 15 TB — IBPM CR")
    parser.add_argument("--inventario", action="store_true", help="Lista todos os vídeos locais e status de sync")
    parser.add_argument("--upload", action="store_true", help="Inicia o upload de todos os vídeos pendentes")
    parser.add_argument("--watch", action="store_true", help="Fica em segundo plano enviando novos cortes que a esteira renderizar")
    args = parser.parse_args()

    if args.inventario or (not args.upload and not args.watch):
        executar_sincronizacao_completa(service=None)
        print("\n💡 Para iniciar o upload automático de todos os vídeos pendentes:")
        print("   python scripts/fase4_publicacao/sincronizador_mestre_gdrive.py --upload")
        print("\n💡 Ou para deixar assistindo novos cortes em segundo plano:")
        print("   python scripts/fase4_publicacao/sincronizador_mestre_gdrive.py --watch")
        return

    service = autenticar_gdrive()
    if not service:
        print("❌ Não foi possível autenticar com o Google Drive.")
        return

    if args.upload:
        executar_sincronizacao_completa(service=service)

    if args.watch:
        print("\n👀 MODO CONTÍNUO (WATCHER) ATIVADO!")
        print("   O script agora fica monitorando novas renderizações da esteira.")
        print("   Assim que um novo corte for salvo, ele é enviado automaticamente para o Drive.")
        while True:
            time.sleep(30)
            executar_sincronizacao_completa(service=service)


if __name__ == "__main__":
    main()
