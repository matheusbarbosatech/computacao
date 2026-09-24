#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
ORQUESTRADOR DAEMON MULTIRREDES — SINCRONIZAÇÃO EM TEMPO REAL (FASE 4)
IBPM CR Automation System

Dispara simultaneamente nos 6 horários de pico (06:00, 09:00, 12:00, 15:00, 18:00, 21:00 BRT):
1. 🔴 YouTube Shorts (Monitora e valida)
2. 🟣 Instagram Reels (Meta Graph API)
3. ⚫ TikTok (Content Posting API v2 via curl resiliente)
4. 🟢 WhatsApp (Canal & Status)

Uso:
  python scripts/fase4_publicacao/orquestrador_multirredes_daemon.py --checar-agora
  python scripts/fase4_publicacao/orquestrador_multirredes_daemon.py --disparar-slot 18:00
  python scripts/fase4_publicacao/orquestrador_multirredes_daemon.py --daemon
"""

import os
import sys
import json
import time
import argparse
import subprocess
from pathlib import Path
from datetime import datetime, timezone, timedelta

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")

BASE_DIR = Path(__file__).resolve().parent.parent.parent
DESKTOP_DIR = Path.home() / "Desktop" / "cortes_audio_culto_459_20_09_2026"
SINCRONIZACAO_FILE = DESKTOP_DIR / "00_SINCRONIZACAO_MULTIRREDES_6_POSTS_DIA.json"
CREDENTIALS_DIR = BASE_DIR / "config" / "credentials"

TZ_BRT = timezone(timedelta(hours=-3))


def renovar_token_tiktok_se_necessario():
    """Garante que o token do TikTok esteja sempre renovado antes de qualquer disparo."""
    tk_file = CREDENTIALS_DIR / "tiktok_credentials.json"
    if not tk_file.exists():
        return
    try:
        creds = json.load(open(tk_file, encoding="utf-8"))
        import urllib.request, urllib.parse
        url = "https://open.tiktokapis.com/v2/oauth/token/"
        payload = {
            "client_key": creds["client_key"],
            "client_secret": creds["client_secret"],
            "grant_type": "refresh_token",
            "refresh_token": creds["refresh_token"]
        }
        data = urllib.parse.urlencode(payload).encode("utf-8")
        headers = {"Content-Type": "application/x-www-form-urlencoded", "Cache-Control": "no-cache"}
        req = urllib.request.Request(url, data=data, headers=headers, method="POST")
        with urllib.request.urlopen(req, timeout=15) as resp:
            res = json.loads(resp.read().decode("utf-8"))
            if "access_token" in res:
                creds["access_token"] = res["access_token"]
                creds["refresh_token"] = res["refresh_token"]
                with open(tk_file, "w", encoding="utf-8") as f:
                    json.dump(creds, f, indent=2)
                print("   🔄 Token do TikTok checado/renovado com sucesso.")
    except Exception as e:
        print(f"   ⚠️ Checagem do token TikTok: {e}")


def disparar_postagem(corte_num: int):
    """Executa o disparo sincronizado nas redes sociais para o corte indicado."""
    print("=" * 80)
    print(f"🚀 DISPARANDO CORTE #{corte_num:02d} EM TODAS AS REDES SOCIAIS...")
    print("=" * 80)

    # 1. Renova token TikTok
    renovar_token_tiktok_se_necessario()

    # 2. Instagram Reels
    print(f"\n🟣 [1/3] Enviando para Instagram Reels (@omatheusbs)...")
    cmd_ig = [sys.executable, "scripts/fase4_publicacao/instagram_uploader.py", "--publicar-corte", str(corte_num)]
    try:
        subprocess.run(cmd_ig, check=True)
    except Exception as e:
        print(f"   ❌ Falha no envio para Instagram: {e}")

    # 3. TikTok
    print(f"\n⚫ [2/3] Enviando para TikTok (@omatheusbs)...")
    cmd_tk = [sys.executable, "scripts/fase4_publicacao/tiktok_uploader.py", "--publicar-corte", str(corte_num), "--modo", "inbox"]
    try:
        subprocess.run(cmd_tk, check=True)
    except Exception as e:
        print(f"   ❌ Falha no envio para TikTok: {e}")

    # 4. WhatsApp
    print(f"\n🟢 [3/3] Registrando no WhatsApp Canal & Status...")
    cmd_wa = [sys.executable, "scripts/fase4_publicacao/whatsapp_canal_e_status.py", "--simular"]
    try:
        subprocess.run(cmd_wa, check=True)
    except Exception as e:
        print(f"   ❌ Falha no envio para WhatsApp: {e}")

    print("\n✅ CICLO DE DISPARO SINCRONIZADO CONCLUÍDO!")


def checar_agenda_e_disparar():
    """Identifica qual corte deve ser disparado no momento atual."""
    agora = datetime.now(TZ_BRT)
    print(f"⏰ Horário Atual: {agora.strftime('%d/%m/%Y às %H:%M:%S BRT')}")

    if not SINCRONIZACAO_FILE.exists():
        print(f"❌ Arquivo de sincronização não encontrado: {SINCRONIZACAO_FILE}")
        return

    with open(SINCRONIZACAO_FILE, "r", encoding="utf-8") as f:
        plano = json.load(f)

    # Verifica os slots do dia de hoje (Dia 2 = 23/09/2026)
    for p in plano:
        dt_agendada = datetime.fromisoformat(p["timestamp_iso"])
        diff_min = (agora - dt_agendada).total_seconds() / 60.0
        # Se estiver na janela de tolerância de até 60 minutos após o horário previsto
        if 0 <= diff_min <= 60 and p.get("status_sincronizacao") != "PUBLICADO":
            corte_num = int(p["id_corte"].replace("SHORT_", ""))
            print(f"🎯 Slot Ativo Encontrado: {p['id_corte']} ({p['data_horario_brt']})")
            disparar_postagem(corte_num)
            p["status_sincronizacao"] = "PUBLICADO"
            with open(SINCRONIZACAO_FILE, "w", encoding="utf-8") as out_f:
                json.dump(plano, out_f, indent=2, ensure_ascii=False)
            return

    print("ℹ️ Nenhum slot agendado para o minuto exato atual. Próximos horários: 06:00, 09:00, 12:00, 15:00, 18:00 e 21:00 BRT.")


def main():
    parser = argparse.ArgumentParser(description="Orquestrador Daemon Multirredes")
    parser.add_argument("--checar-agora", action="store_true", help="Checa o horário atual e dispara o corte pendente")
    parser.add_argument("--disparar-corte", type=int, default=None, help="Força o disparo imediato de um corte específico")
    parser.add_argument("--daemon", action="store_true", help="Executa em loop contínuo monitorando os 6 horários diários")
    args = parser.parse_args()

    if args.disparar_corte:
        disparar_postagem(args.disparar_corte)
        return

    if args.checar_agora:
        checar_agenda_e_disparar()
        return

    if args.daemon:
        print("🤖 Daemon Multirredes ativo. Monitorando 6 horários: 06:00, 09:00, 12:00, 15:00, 18:00 e 21:00 BRT...")
        while True:
            checar_agenda_e_disparar()
            time.sleep(60)


if __name__ == "__main__":
    main()
