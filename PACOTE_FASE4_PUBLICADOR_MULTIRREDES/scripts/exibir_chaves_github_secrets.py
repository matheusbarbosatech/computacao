#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
EXIBIDOR E GERADOR DE GITHUB SECRETS (FASE 4)
IBPM CR Automation System

Lê as credenciais já configuradas localmente e formata no padrão exato
para copiar e colar no GitHub:
Settings > Secrets and variables > Actions > New repository secret
"""

import sys
import json
from pathlib import Path

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")

BASE_DIR = Path(__file__).resolve().parent.parent.parent
CREDENTIALS_DIR = BASE_DIR / "config" / "credentials"

IG_FILE = CREDENTIALS_DIR / "instagram_credentials.json"
TK_FILE = CREDENTIALS_DIR / "tiktok_credentials.json"
WA_FILE = CREDENTIALS_DIR / "whatsapp_credentials.json"

DEFAULT_GDRIVE_ID = "1hcRgIFmJBqiUq1w1dXnMwcFdCc7nzOFk"


def main():
    print("=" * 80)
    print("🔐 GITHUB SECRETS — CHAVES PRONTAS PARA O ROBÔ NA NUVEM")
    print("=" * 80)
    print("\nPara o robô funcionar no GitHub Actions com seu PC desligado, adicione estas")
    print("chaves no seu repositório no GitHub:")
    print("👉 Acesse: https://github.com/matheusbarbosatech/ibpmcr-automation/settings/secrets/actions")
    print("👉 Clique no botão verde: 'New repository secret'\n")
    print("-" * 80)

    secrets = {}

    # 1. Instagram
    if IG_FILE.exists():
        try:
            ig = json.load(open(IG_FILE, encoding="utf-8"))
            secrets["INSTAGRAM_ACCESS_TOKEN"] = ig.get("access_token", "")
            secrets["INSTAGRAM_ACCOUNT_ID"] = ig.get("instagram_account_id", "")
            secrets["INSTAGRAM_USER_ID"] = ig.get("instagram_user_id", ig.get("instagram_account_id", ""))
        except Exception as e:
            print(f"⚠️ Erro ao ler Instagram: {e}")

    # 2. TikTok
    if TK_FILE.exists():
        try:
            tk = json.load(open(TK_FILE, encoding="utf-8"))
            secrets["TIKTOK_CLIENT_KEY"] = tk.get("client_key", "")
            secrets["TIKTOK_CLIENT_SECRET"] = tk.get("client_secret", "")
            secrets["TIKTOK_REFRESH_TOKEN"] = tk.get("refresh_token", "")
        except Exception as e:
            print(f"⚠️ Erro ao ler TikTok: {e}")

    # 3. WhatsApp (Render Evolution API)
    if WA_FILE.exists():
        try:
            wa = json.load(open(WA_FILE, encoding="utf-8"))
            secrets["EVOLUTION_API_URL"] = wa.get("api_url", "https://evolution-api-latest-djvp.onrender.com")
            secrets["EVOLUTION_API_KEY"] = wa.get("api_token", "ibpmcr_2026_seguro")
            secrets["EVOLUTION_INSTANCE"] = wa.get("instance_name", "matheus_barbosa")
        except Exception as e:
            print(f"⚠️ Erro ao ler WhatsApp: {e}")

    # 4. Google Drive Folder
    secrets["GDRIVE_FOLDER_ID"] = DEFAULT_GDRIVE_ID

    for nome, valor in secrets.items():
        print(f"📌 Nome do Secret:  {nome}")
        # Mostra valor mascarado para preview e valor completo
        if len(valor) > 30:
            preview = valor[:12] + "..." + valor[-10:]
        else:
            preview = valor
        print(f"   Prévia do Valor: {preview}")
        print("   " + "-" * 40)

    print("\n" + "=" * 80)
    print("✅ TODAS AS CHAVES FORAM MAPEADAS COM SUCESSO!")
    print("=" * 80)


if __name__ == "__main__":
    main()
