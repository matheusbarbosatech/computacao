#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
UPLOADER AUTOMÁTICO PARA GOOGLE DRIVE (FASE 4)
IBPM CR Automation System

Faz upload de todos os 14 Shorts para a pasta do Google Drive:
https://drive.google.com/drive/folders/1hcRgIFmJBqiUq1w1dXnMwcFdCc7nzOFk
"""

import os
import sys
import json
from pathlib import Path

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")

BASE_DIR = Path(__file__).resolve().parent.parent.parent
CREDENTIALS_DIR = BASE_DIR / "config" / "credentials"
CLIENT_SECRETS = CREDENTIALS_DIR / "client_secret.json"
TOKEN_GDRIVE = CREDENTIALS_DIR / "token_gdrive.json"

FOLDER_ID = "1hcRgIFmJBqiUq1w1dXnMwcFdCc7nzOFk"
SHORTS_DIR = Path.home() / "Desktop" / "cortes_audio_culto_459_20_09_2026" / "05_SHORTS_APICE_45S"

SCOPES = ["https://www.googleapis.com/auth/drive.file"]


def autenticar_gdrive():
    from google_auth_oauthlib.flow import InstalledAppFlow
    from google.oauth2.credentials import Credentials
    from googleapiclient.discovery import build

    creds = None
    if TOKEN_GDRIVE.exists():
        try:
            creds = Credentials.from_authorized_user_file(str(TOKEN_GDRIVE), SCOPES)
        except Exception:
            pass

    if not creds or not creds.valid:
        if not CLIENT_SECRETS.exists():
            print(f"❌ Arquivo client_secret.json não encontrado em: {CLIENT_SECRETS}")
            return None
        print("🌐 Abrindo janela de autorização no navegador para o Google Drive...")
        flow = InstalledAppFlow.from_client_secrets_file(str(CLIENT_SECRETS), SCOPES)
        creds = flow.run_local_server(port=0)
        with open(TOKEN_GDRIVE, "w", encoding="utf-8") as f:
            f.write(creds.to_json())
        print("✅ Credencial do Google Drive salva com sucesso!")

    return build("drive", "v3", credentials=creds)


def main():
    print("=" * 80)
    print("🚀 UPLOAD AUTOMÁTICO DE VÍDEOS PARA O GOOGLE DRIVE (15 TB)")
    print("=" * 80)
    print(f"📁 Pasta de Origem: {SHORTS_DIR}")
    print(f"🎯 Pasta de Destino no Drive: {FOLDER_ID}")

    if not SHORTS_DIR.exists():
        print(f"❌ Pasta de origem não encontrada: {SHORTS_DIR}")
        return

    arquivos = sorted(list(SHORTS_DIR.glob("*.mp4")))
    print(f"\n📦 {len(arquivos)} vídeos encontrados para upload:")

    try:
        from googleapiclient.http import MediaFileUpload
        service = autenticar_gdrive()
        if not service:
            return

        # Lista arquivos já existentes no Drive para não duplicar
        results = service.files().list(
            q=f"'{FOLDER_ID}' in parents and trashed=false",
            fields="files(id, name)"
        ).execute()
        arquivos_drive = {f["name"]: f["id"] for f in results.get("files", [])}

        for i, video_path in enumerate(arquivos):
            nome = video_path.name
            tamanho_mb = video_path.stat().st_size / (1024 * 1024)

            if nome in arquivos_drive:
                print(f"[{i+1}/{len(arquivos)}] ✔ Já existe no Drive: {nome} (ID: {arquivos_drive[nome]})")
                continue

            print(f"[{i+1}/{len(arquivos)}] ☁️ Enviando {nome} ({tamanho_mb:.1f} MB)...")
            file_metadata = {
                "name": nome,
                "parents": [FOLDER_ID]
            }
            media = MediaFileUpload(str(video_path), mimetype="video/mp4", resumable=True)
            arquivo_criado = service.files().create(
                body=file_metadata,
                media_body=media,
                fields="id"
            ).execute()
            print(f"   ✅ Concluído! ID: {arquivo_criado.get('id')}")

        print("\n" + "=" * 80)
        print("🎉 TODOS OS VÍDEOS FORAM SINCRONIZADOS COM O GOOGLE DRIVE!")
        print("=" * 80)

    except Exception as e:
        print(f"⚠️ Erro no fluxo automático de API: {e}")
        print("💡 Abrindo a pasta no seu Windows para você arrastar para a aba do Drive:")
        import subprocess
        subprocess.Popen(f'explorer.exe "{str(SHORTS_DIR)}"')


if __name__ == "__main__":
    main()
