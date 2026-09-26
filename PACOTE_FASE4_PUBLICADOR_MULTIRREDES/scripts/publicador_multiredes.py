#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
CENTRAL DE DISTRIBUIÇÃO MULTIRREDES — YOUTUBE, INSTAGRAM & TIKTOK (FASE 4)
IBPM CR Automation System — Publicação Omnichannel Automatizada

Permite auditar, simular, agendar e publicar simultaneamente em:
1. 🔴 YouTube (YouTube Data API v3): Shorts, Cortes Médios 16:9 e Pregação Completa Tier 3.
2. 🟣 Instagram (Meta Graph API v19.0): Reels 9:16 com gancho, copy e hashtags.
3. ⚫ TikTok (TikTok Content Posting API v2): Vídeos verticais 9:16 com títulos de alto impacto.

Uso:
  python scripts/fase4_publicacao/publicador_multiredes.py --status
  python scripts/fase4_publicacao/publicador_multiredes.py --simular
  python scripts/fase4_publicacao/publicador_multiredes.py --rede youtube --simular
  python scripts/fase4_publicacao/publicador_multiredes.py --rede instagram --simular
  python scripts/fase4_publicacao/publicador_multiredes.py --rede tiktok --simular
  python scripts/fase4_publicacao/publicador_multiredes.py --todas
"""

import os
import sys
import json
import argparse
from pathlib import Path

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
if hasattr(sys.stderr, "reconfigure"):
    sys.stderr.reconfigure(encoding="utf-8", errors="replace")

BASE_DIR = Path(__file__).resolve().parent.parent.parent
CREDENTIALS_DIR = BASE_DIR / "config" / "credentials"
DESKTOP_DIR = Path.home() / "Desktop" / "cortes_audio_culto_459_20_09_2026"

YOUTUBE_CLIENT_SECRET = CREDENTIALS_DIR / "client_secret.json"
YOUTUBE_TOKEN = CREDENTIALS_DIR / "token_youtube.json"
INSTAGRAM_CONFIG = CREDENTIALS_DIR / "instagram_credentials.json"
TIKTOK_CONFIG = CREDENTIALS_DIR / "tiktok_credentials.json"


def checar_status_credenciais():
    """Imprime o diagnóstico de conexão de cada rede social."""
    print("=" * 80)
    print("🌐 DIAGNÓSTICO DE CONEXÃO MULTIRREDES — REDES PESSOAIS")
    print("=" * 80)

    # 1. YouTube
    yt_ok = YOUTUBE_CLIENT_SECRET.exists() or YOUTUBE_TOKEN.exists()
    print(f"🔴 1. YOUTUBE (Data API v3):")
    if YOUTUBE_TOKEN.exists():
        print("   ✅ Status: AUTENTICADO (Token OAuth ativo em token_youtube.json)")
    elif YOUTUBE_CLIENT_SECRET.exists():
        print("   🟡 Status: CREDENCIAL PRESENTE (Aguardando primeiro login no navegador)")
    else:
        print(f"   ❌ Status: NÃO CONFIGURADO (Coloque client_secret.json em config/credentials/)")

    # 2. Instagram
    ig_ok = False
    if INSTAGRAM_CONFIG.exists():
        try:
            with open(INSTAGRAM_CONFIG, "r", encoding="utf-8") as f:
                d = json.load(f)
                ig_ok = bool(d.get("access_token") and d.get("instagram_account_id"))
        except Exception:
            pass
    print(f"\n🟣 2. INSTAGRAM REELS (Meta Graph API v19.0):")
    if ig_ok:
        print("   ✅ Status: AUTENTICADO (Token e Account ID configurados)")
    else:
        print(f"   ❌ Status: NÃO CONFIGURADO (Preencha instagram_credentials.json)")

    # 3. TikTok
    tk_ok = False
    if TIKTOK_CONFIG.exists():
        try:
            with open(TIKTOK_CONFIG, "r", encoding="utf-8") as f:
                d = json.load(f)
                tk_ok = bool(d.get("access_token"))
        except Exception:
            pass
    print(f"\n⚫ 3. TIKTOK (Content Posting API v2):")
    if tk_ok:
        print("   ✅ Status: AUTENTICADO (Access Token ativo)")
    else:
        print(f"   ❌ Status: NÃO CONFIGURADO (Preencha tiktok_credentials.json)")

    # 4. WhatsApp Status
    wa_session_dir = BASE_DIR / "data" / "whatsapp_session"
    wa_config = BASE_DIR / "config" / "credentials" / "whatsapp_credentials.json"
    wa_ok = any(wa_session_dir.glob("Default/*")) if wa_session_dir.exists() else False
    if not wa_ok and wa_config.exists():
        try:
            with open(wa_config, "r", encoding="utf-8") as f:
                d = json.load(f)
                wa_ok = bool(d.get("api_url") and d.get("api_token"))
        except Exception:
            pass
    nome_canal = "Matheus Barbosa"
    if wa_config.exists():
        try:
            with open(wa_config, "r", encoding="utf-8") as f:
                d = json.load(f)
                nome_canal = d.get("nome_canal", nome_canal)
        except Exception:
            pass

    print(f"\n🟢 4. WHATSAPP (Canal '{nome_canal}' & Status Silencioso):")
    if wa_ok:
        print("   ✅ Status: AUTENTICADO (Sessão Web em data/whatsapp_session)")
        print(f"   📁 Arquivo de Configuração: config/credentials/whatsapp_credentials.json")
    else:
        print(f"   🟡 Status: PRONTO PARA PAREAR (Execute: python scripts/fase4_publicacao/whatsapp_status_uploader.py --conectar)")

    print("-" * 80)
    print("📖 Guia completo de configuração das suas contas pessoais disponível em:")
    print(f"   config/credentials/GUIA_CONEXAO_REDES_PESSOAIS.md")
    print("=" * 80)


def executar_modulo(modulo_py: str, args_extras: list):
    """Executa um dos scripts especializados de publicação."""
    script_path = BASE_DIR / "scripts" / "fase4_publicacao" / modulo_py
    cmd = [sys.executable, str(script_path)] + args_extras
    import subprocess
    subprocess.run(cmd)


def main():
    parser = argparse.ArgumentParser(description="Central de Publicação Multirredes (YouTube, Instagram, TikTok, WhatsApp)")
    parser.add_argument("--status", action="store_true", help="Mostra status de conexão de todas as redes")
    parser.add_argument("--simular", action="store_true", help="Executa simulação de auditoria em todas as redes selecionadas")
    parser.add_argument("--rede", type=str, choices=["youtube", "instagram", "tiktok", "whatsapp", "todas"], default="todas", help="Rede social alvo")
    parser.add_argument("--todas", action="store_true", help="Dispara a simulação/publicação nas 4 redes em conjunto")
    args = parser.parse_args()

    if args.status:
        checar_status_credenciais()
        return

    rede_escolhida = "todas" if args.todas else args.rede
    simulacao_flag = ["--simular"] if args.simular else []

    if rede_escolhida in ["youtube", "todas"]:
        executar_modulo("youtube_uploader.py", simulacao_flag if simulacao_flag else ["--simular"])
        print("\n")

    if rede_escolhida in ["instagram", "todas"]:
        executar_modulo("instagram_uploader.py", simulacao_flag if simulacao_flag else ["--simular"])
        print("\n")

    if rede_escolhida in ["tiktok", "todas"]:
        executar_modulo("tiktok_uploader.py", simulacao_flag if simulacao_flag else ["--simular"])
        print("\n")

    if rede_escolhida in ["whatsapp", "todas"]:
        executar_modulo("whatsapp_canal_e_status.py", simulacao_flag if simulacao_flag else ["--simular"])
        print("\n")


if __name__ == "__main__":
    main()
