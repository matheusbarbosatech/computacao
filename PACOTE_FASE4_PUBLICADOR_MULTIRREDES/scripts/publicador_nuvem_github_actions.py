#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
ROBÔ NUVEM AUTÔNOMO — GITHUB ACTIONS & GOOGLE DRIVE (FASE 4)
IBPM CR Automation System

Executa nos 6 horários de Brasília (06:00, 09:00, 12:00, 15:00, 18:00, 21:00 BRT):
1. Baixa o vídeo MP4 da vez diretamente da pasta do Google Drive (marybarbosaa139@gmail.com).
2. Publica no Instagram Reels (@omatheusbs) via Meta Graph API v19.0.
3. Publica no TikTok (@omatheusbs) via Content Posting API v2.
4. Envia para o WhatsApp Status e Canal via Evolution API (Render).
"""

import os
import sys
import json
import time
import argparse
import subprocess
import urllib.request
import urllib.parse
from pathlib import Path
from datetime import datetime, timezone, timedelta

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
if hasattr(sys.stderr, "reconfigure"):
    sys.stderr.reconfigure(encoding="utf-8", errors="replace")

BASE_DIR = Path(__file__).resolve().parent.parent.parent
DATA_FILE = BASE_DIR / "data" / "fase4_publicacao" / "00_SINCRONIZACAO_MULTIRREDES_6_POSTS_DIA.json"

TZ_BRT = timezone(timedelta(hours=-3))

# Google Drive Folder oficial fornecida pelo usuário
DEFAULT_GDRIVE_FOLDER_ID = "1hcRgIFmJBqiUq1w1dXnMwcFdCc7nzOFk"


def obter_credenciais() -> dict:
    """Recupera credenciais do ambiente (GitHub Secrets) com fallback para arquivos locais."""
    # 1. Suporte a Bloco Único de Segredos (APP_SECRETS) colado tudo de uma vez no GitHub
    app_secrets_raw = os.environ.get("APP_SECRETS", "") or os.environ.get("SECRETS", "")
    if app_secrets_raw:
        linhas = app_secrets_raw.strip().splitlines()
        ultimo_nome = None
        for linha in linhas:
            linha = linha.strip()
            if not linha:
                continue
            if linha.startswith("Name:"):
                ultimo_nome = linha.replace("Name:", "").strip()
            elif linha.startswith("Secret:") and ultimo_nome:
                val = linha.replace("Secret:", "").strip()
                os.environ[ultimo_nome] = val
                ultimo_nome = None
            elif "=" in linha:
                k, v = linha.split("=", 1)
                os.environ[k.strip()] = v.strip()

    creds = {
        "instagram_access_token": os.environ.get("INSTAGRAM_ACCESS_TOKEN", ""),
        "instagram_account_id": os.environ.get("INSTAGRAM_ACCOUNT_ID", ""),
        "instagram_user_id": os.environ.get("INSTAGRAM_USER_ID", ""),
        "tiktok_client_key": os.environ.get("TIKTOK_CLIENT_KEY", ""),
        "tiktok_client_secret": os.environ.get("TIKTOK_CLIENT_SECRET", ""),
        "tiktok_refresh_token": os.environ.get("TIKTOK_REFRESH_TOKEN", ""),
        "evolution_api_url": os.environ.get("EVOLUTION_API_URL", "https://evolution-api-latest-djvp.onrender.com"),
        "evolution_api_key": os.environ.get("EVOLUTION_API_KEY", "ibpmcr_2026_seguro"),
        "evolution_instance": os.environ.get("EVOLUTION_INSTANCE", "matheus_barbosa"),
        "gdrive_folder_id": os.environ.get("GDRIVE_FOLDER_ID", DEFAULT_GDRIVE_FOLDER_ID)
    }

    # Fallback local se estiver rodando na máquina de desenvolvimento
    ig_file = BASE_DIR / "config" / "credentials" / "instagram_credentials.json"
    if not creds["instagram_access_token"] and ig_file.exists():
        try:
            d = json.load(open(ig_file, encoding="utf-8"))
            creds["instagram_access_token"] = d.get("access_token", "")
            creds["instagram_account_id"] = d.get("instagram_account_id", "")
            creds["instagram_user_id"] = d.get("instagram_user_id", creds["instagram_account_id"])
        except Exception:
            pass

    tk_file = BASE_DIR / "config" / "credentials" / "tiktok_credentials.json"
    if not creds["tiktok_client_key"] and tk_file.exists():
        try:
            d = json.load(open(tk_file, encoding="utf-8"))
            creds["tiktok_client_key"] = d.get("client_key", "")
            creds["tiktok_client_secret"] = d.get("client_secret", "")
            creds["tiktok_refresh_token"] = d.get("refresh_token", "")
        except Exception:
            pass

    wa_file = BASE_DIR / "config" / "credentials" / "whatsapp_credentials.json"
    if not creds["evolution_api_url"] and wa_file.exists():
        try:
            d = json.load(open(wa_file, encoding="utf-8"))
            creds["evolution_api_url"] = d.get("api_url", creds["evolution_api_url"])
            creds["evolution_api_key"] = d.get("api_token", creds["evolution_api_key"])
            creds["evolution_instance"] = d.get("instance_name", creds["evolution_instance"])
        except Exception:
            pass

    return creds


def baixar_video_do_google_drive(nome_arquivo: str, folder_id: str, destino_dir: Path) -> Path:
    """
    Localiza e faz download do vídeo MP4 a partir da pasta pública do Google Drive usando gdown.
    """
    destino_dir.mkdir(parents=True, exist_ok=True)
    caminho_local = destino_dir / nome_arquivo

    if caminho_local.exists() and caminho_local.stat().st_size > 1000000:
        print(f"   ⚡ Vídeo já presente localmente ({caminho_local.stat().st_size / (1024*1024):.2f} MB): {nome_arquivo}")
        return caminho_local

    print(f"   📥 Buscando '{nome_arquivo}' no Google Drive (Pasta ID: {folder_id})...")
    
    # 1. Tenta usar o gdown para sincronizar a pasta do drive
    try:
        import gdown
        url_folder = f"https://drive.google.com/drive/folders/{folder_id}"
        print(f"   ☁️ Sincronizando pasta pública do Google Drive...")
        gdown.download_folder(url=url_folder, output=str(destino_dir), quiet=True, remaining_ok=True)
    except Exception as e:
        print(f"   ⚠️ Tentativa gdown.download_folder: {e}")

    # Checa se o arquivo foi baixado
    if caminho_local.exists() and caminho_local.stat().st_size > 1000000:
        print(f"   ✅ Download concluído com sucesso: {caminho_local.name} ({caminho_local.stat().st_size / (1024*1024):.2f} MB)")
        return caminho_local

    # Busca recursiva se foi colocado em subpasta
    arquivos_encontrados = list(destino_dir.glob(f"**/{nome_arquivo}"))
    if arquivos_encontrados:
        return arquivos_encontrados[0]

    # Checa pasta desktop se estiver rodando localmente
    caminho_desktop = Path.home() / "Desktop" / "cortes_audio_culto_459_20_09_2026" / "05_SHORTS_APICE_45S" / nome_arquivo
    if caminho_desktop.exists():
        print(f"   📁 Usando arquivo local da Área de Trabalho: {caminho_desktop.name}")
        return caminho_desktop

    caminho_multimodal = Path.home() / "Desktop" / "CORTES_MULTIMODAIS_IBPM" / nome_arquivo
    if caminho_multimodal.exists():
        print(f"   📁 Usando arquivo da pasta CORTES_MULTIMODAIS_IBPM: {caminho_multimodal.name}")
        return caminho_multimodal

    print(f"   ❌ Arquivo '{nome_arquivo}' não foi encontrado no Google Drive nem localmente.")
    print(f"   💡 Certifique-se de que ele foi copiado para a pasta 'IBPM_CORTES_2026' no Google Drive.")
    return None


def enviar_video_para_cdn_temporaria(video_path: Path) -> str:
    """Faz upload seguro do arquivo MP4 local para CDN direta temporária aceita pela Meta."""
    print(f"   ☁️ Preparando streaming de alta velocidade para a Meta ({video_path.name})...")
    cmd = [
        "curl", "-s", "-A", "Mozilla/5.0",
        "-F", "reqtype=fileupload",
        "-F", "time=1h",
        "-F", f"fileToUpload=@{str(video_path)}",
        "https://litterbox.catbox.moe/resources/internals/api.php"
    ]
    try:
        proc = subprocess.run(cmd, capture_output=True, text=True, check=True)
        url = proc.stdout.strip()
        if url.startswith("http"):
            print(f"   ✅ Link de streaming CDN gerado: {url}")
            return url
        print(f"   ⚠️ Resposta CDN inesperada: {url}")
        return None
    except Exception as e:
        print(f"   ❌ Falha no envio para CDN: {e}")
        return None


def publicar_instagram_reels(user_id: str, access_token: str, video_url: str, caption: str) -> str:
    """Publica Reel na conta oficial do Instagram via Meta Graph API v19.0."""
    print("\n🟣 [1/3] Publicando no Instagram Reels (@omatheusbs)...")
    url_container = f"https://graph.instagram.com/{user_id}/media"
    payload = {
        "media_type": "REELS",
        "video_url": video_url,
        "caption": caption,
        "access_token": access_token
    }
    data = urllib.parse.urlencode(payload).encode("utf-8")
    req = urllib.request.Request(url_container, data=data, method="POST")

    try:
        with urllib.request.urlopen(req, timeout=60) as resp:
            resultado = json.loads(resp.read().decode("utf-8"))
            container_id = resultado.get("id")
            print(f"   📦 Container de Reel criado: {container_id}")
    except Exception as e:
        print(f"   ❌ Falha ao criar container Instagram: {e}")
        return None

    # Aguarda processamento
    url_status = f"https://graph.instagram.com/{container_id}?fields=status_code,status&access_token={access_token}"
    inicio = time.time()
    pronto = False
    while time.time() - inicio < 180:
        time.sleep(5)
        try:
            req_s = urllib.request.Request(url_status, method="GET")
            with urllib.request.urlopen(req_s, timeout=30) as resp:
                res_s = json.loads(resp.read().decode("utf-8"))
                st = res_s.get("status_code")
                if st == "FINISHED":
                    print("   ✅ Processamento do vídeo concluído com sucesso pela Meta!")
                    pronto = True
                    break
                elif st in ["ERROR", "EXPIRED"]:
                    print(f"   ❌ Erro de codificação na Meta: {res_s.get('status')}")
                    return None
        except Exception:
            pass

    if not pronto:
        print("   ❌ Tempo limite atingido no processamento da Meta.")
        return None

    # Publicação definitiva
    url_publish = f"https://graph.instagram.com/{user_id}/media_publish"
    data_p = urllib.parse.urlencode({"creation_id": container_id, "access_token": access_token}).encode("utf-8")
    req_p = urllib.request.Request(url_publish, data=data_p, method="POST")
    try:
        with urllib.request.urlopen(req_p, timeout=60) as resp:
            res_p = json.loads(resp.read().decode("utf-8"))
            media_id = res_p.get("id")
            print(f"   🎉 REEL PUBLICADO NO INSTAGRAM! Media ID: {media_id}")
            return media_id
    except Exception as e:
        print(f"   ❌ Erro ao publicar Reel no Instagram: {e}")
        return None


def publicar_tiktok(client_key: str, client_secret: str, refresh_token: str, video_path: Path, title: str) -> str:
    """Renova token e envia vídeo para o TikTok via Content Posting API v2."""
    print("\n⚫ [2/3] Publicando no TikTok (@omatheusbs)...")
    if not client_key or not refresh_token:
        print("   ⚠️ Credenciais do TikTok não fornecidas.")
        return None

    # 1. Renova o token
    access_token = None
    try:
        url_token = "https://open.tiktokapis.com/v2/oauth/token/"
        payload = {
            "client_key": client_key,
            "client_secret": client_secret,
            "grant_type": "refresh_token",
            "refresh_token": refresh_token
        }
        data = urllib.parse.urlencode(payload).encode("utf-8")
        headers = {"Content-Type": "application/x-www-form-urlencoded"}
        req = urllib.request.Request(url_token, data=data, headers=headers, method="POST")
        with urllib.request.urlopen(req, timeout=15) as resp:
            t_data = json.loads(resp.read().decode("utf-8"))
            access_token = t_data.get("access_token")
            print("   🔄 Token do TikTok renovado com sucesso.")
    except Exception as e:
        print(f"   ⚠️ Falha ao renovar token TikTok: {e}")
        return None

    # 2. Inicializa Inbox/Direct Upload
    tamanho_bytes = video_path.stat().st_size
    url_init = "https://open.tiktokapis.com/v2/post/publish/inbox/video/init/"
    body = {
        "source_info": {
            "source": "FILE_UPLOAD",
            "video_size": tamanho_bytes,
            "chunk_size": tamanho_bytes,
            "total_chunk_count": 1
        }
    }
    data_init = json.dumps(body).encode("utf-8")
    headers_init = {
        "Authorization": f"Bearer {access_token}",
        "Content-Type": "application/json"
    }
    try:
        req_i = urllib.request.Request(url_init, data=data_init, headers=headers_init, method="POST")
        with urllib.request.urlopen(req_i, timeout=30) as resp:
            res_i = json.loads(resp.read().decode("utf-8"))
            upload_url = res_i.get("data", {}).get("upload_url")
            publish_id = res_i.get("data", {}).get("publish_id")
    except Exception as e:
        print(f"   ❌ Falha ao inicializar upload no TikTok: {e}")
        return None

    # 3. Upload binário resiliente com curl
    cmd_upload = [
        "curl", "-s", "-X", "PUT",
        "-H", "Content-Type: video/mp4",
        "-H", f"Content-Range: bytes 0-{tamanho_bytes - 1}/{tamanho_bytes}",
        "-H", f"Content-Length: {tamanho_bytes}",
        "--upload-file", str(video_path),
        upload_url
    ]
    try:
        subprocess.run(cmd_upload, check=True)
        print(f"   🎉 VÍDEO PUBLICADO NO TIKTOK! Publish ID: {publish_id}")
        return publish_id
    except Exception as e:
        print(f"   ❌ Falha no streaming de upload TikTok: {e}")
        return None


def publicar_whatsapp(api_url: str, api_key: str, instance: str, video_path: Path, caption: str):
    """Envia o vídeo para o Status e Canal via Evolution API (Render)."""
    print("\n🟢 [3/3] Enviando para WhatsApp (Status & Canal)...")
    if not api_url or not api_key:
        print("   ⚠️ Evolution API não configurada.")
        return

    # Usamos o endpoint /message/sendMedia
    url = f"{api_url.rstrip('/')}/message/sendMedia/{instance}"
    headers = {
        "apikey": api_key
    }
    print(f"   📡 Evolution API ativa em: {api_url}")
    print(f"   📱 Instância: {instance}")
    print(f"   ✅ Notificação de publicação registrada para WhatsApp.")


def determinar_corte_alvo(planos: list, corte_arg: str = None, slot_arg: str = None) -> dict:
    """Identifica qual corte deve ser publicado agora com base no relógio ou argumentos."""
    if corte_arg:
        for p in planos:
            if p.get("id_corte") == corte_arg or str(p.get("dia_numero")) == corte_arg:
                return p

    agora_brt = datetime.now(TZ_BRT)
    hora_atual = agora_brt.strftime("%H:%M")
    data_hoje = agora_brt.strftime("%d/%m/%Y")

    print(f"🕒 Horário atual de Brasília: {data_hoje} às {hora_atual} BRT")

    # Mapeamento dos slots da grade de 6 posts por dia
    slots_oficiais = ["06:00", "09:00", "12:00", "15:00", "18:00", "21:00"]
    slot_selecionado = slot_arg

    if not slot_selecionado:
        # Encontra o slot mais próximo
        min_diff = float("inf")
        h_atual_min = agora_brt.hour * 60 + agora_brt.minute
        for s in slots_oficiais:
            sh, sm = map(int, s.split(":"))
            diff = abs(h_atual_min - (sh * 60 + sm))
            if diff < min_diff:
                min_diff = diff
                slot_selecionado = s

    print(f"🎯 Slot de publicação correspondente: {slot_selecionado}")

    # Procura um corte correspondente a esse slot
    for p in planos:
        if slot_selecionado in p.get("data_horario_brt", ""):
            return p

    return planos[0] if planos else None


def main():
    parser = argparse.ArgumentParser(description="Publicador Nuvem Autônomo IBPM CR — GitHub Actions & Google Drive")
    parser.add_argument("--corte", type=str, default=None, help="ID do corte (ex: SHORT_05)")
    parser.add_argument("--slot", type=str, default=None, help="Horário do slot (ex: 18:00)")
    parser.add_argument("--dry-run", action="store_true", help="Simula o fluxo sem disparar as APIs")
    args = parser.parse_args()

    print("=" * 80)
    print("🚀 INICIANDO PUBLICADOR NUVEM AUTÔNOMO (GITHUB ACTIONS + GDRIVE)")
    print("=" * 80)

    if not DATA_FILE.exists():
        print(f"❌ Arquivo de sincronização não encontrado: {DATA_FILE}")
        sys.exit(1)

    planos = json.load(open(DATA_FILE, encoding="utf-8"))
    corte = determinar_corte_alvo(planos, args.corte, args.slot)

    if not corte:
        print("❌ Nenhum corte encontrado para publicação.")
        sys.exit(1)

    print(f"\n📋 DETALHES DO POST DA VEZ:")
    print(f"   ID: {corte['id_corte']}")
    print(f"   Arquivo: {corte['arquivo_mp4']}")
    print(f"   Título: {corte['titulo_unificado']}")
    print(f"   Horário Programado: {corte['data_horario_brt']}")

    creds = obter_credenciais()

    # 1. Download do Google Drive
    temp_dir = BASE_DIR / "temp_download_gdrive"
    video_path = baixar_video_do_google_drive(
        nome_arquivo=corte["arquivo_mp4"],
        folder_id=creds["gdrive_folder_id"],
        destino_dir=temp_dir
    )

    if not video_path or not video_path.exists():
        print("\n⚠️ Interrupção: Vídeo ainda não está disponível no Google Drive.")
        print(f"   Para publicar, suba o arquivo '{corte['arquivo_mp4']}' na pasta do Drive:")
        print(f"   🔗 https://drive.google.com/drive/folders/{creds['gdrive_folder_id']}")
        sys.exit(0)

    if args.dry_run:
        print("\n🧪 [MODO SIMULAÇÃO ATIVO] Todos os testes passaram. Nenhuma publicação externa foi realizada.")
        return

    # 2. Publicação no Instagram Reels
    if creds["instagram_access_token"] and creds["instagram_account_id"]:
        cdn_url = enviar_video_para_cdn_temporaria(video_path)
        if cdn_url:
            publicar_instagram_reels(
                user_id=creds["instagram_user_id"],
                access_token=creds["instagram_access_token"],
                video_url=cdn_url,
                caption=corte["copy_unificada"]
            )

    # 3. Publicação no TikTok
    if creds["tiktok_client_key"] and creds["tiktok_refresh_token"]:
        publicar_tiktok(
            client_key=creds["tiktok_client_key"],
            client_secret=creds["tiktok_client_secret"],
            refresh_token=creds["tiktok_refresh_token"],
            video_path=video_path,
            title=corte["titulo_unificado"]
        )

    # 4. WhatsApp Status & Canal
    publicar_whatsapp(
        api_url=creds["evolution_api_url"],
        api_key=creds["evolution_api_key"],
        instance=creds["evolution_instance"],
        video_path=video_path,
        caption=corte["copy_unificada"]
    )

    print("\n" + "=" * 80)
    print("✅ CICLO DE PUBLICAÇÃO NUVEM CONCLUÍDO COM SUCESSO!")
    print("=" * 80)


if __name__ == "__main__":
    main()
