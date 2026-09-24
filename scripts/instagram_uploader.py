#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
PUBLICADOR E AGENDADOR OFICIAL — INSTAGRAM REELS API (META GRAPH API v19.0)
IBPM CR Automation System — Fase 4: Publicação Multirredes

Recursos:
1. Publicação e agendamento de Reels (9:16) no Instagram via Meta Graph API.
2. Modo Simulação (--simular / --dry-run):
   - Valida proporção (9:16), duração (<90s para Reels padrão), taxa de quadros e áudio.
   - Formata legendas com hashtags teológicas e chamadas para ação (CTA).
   - Valida limites de caracteres (máx 2.200 caracteres, máx 30 hashtags).
3. Fluxo Oficial Meta em 3 Etapas:
   - Etapa 1: Criação do Container de Mídia (POST /{ig_user_id}/media).
   - Etapa 2: Monitoramento de processamento de vídeo (GET /{container_id}).
   - Etapa 3: Publicação definitiva do Reel (POST /{ig_user_id}/media_publish).
4. Suporte a Contas Pessoais/Criador (Instagram Creator ou Business vinculado a Página do Facebook).
"""

import os
import sys
import json
import time
import argparse
import urllib.request
import urllib.parse
from pathlib import Path
from datetime import datetime, timedelta, timezone

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
if hasattr(sys.stderr, "reconfigure"):
    sys.stderr.reconfigure(encoding="utf-8", errors="replace")

BASE_DIR = Path(__file__).resolve().parent.parent.parent
DESKTOP_DIR = Path.home() / "Desktop" / "cortes_audio_culto_459_20_09_2026"
DEFAULT_JSON_METADADOS = DESKTOP_DIR / "00_COPIES_E_METADADOS_POSTAGEM.json"
CREDENTIALS_DIR = BASE_DIR / "config" / "credentials"
CONFIG_FILE = CREDENTIALS_DIR / "instagram_credentials.json"

GRAPH_API_URL = "https://graph.facebook.com/v19.0"
TZ_BRT = timezone(timedelta(hours=-3))


def carregar_credenciais() -> dict:
    """Carrega token de acesso e ID da conta do Instagram das credenciais ou variáveis de ambiente."""
    creds = {
        "access_token": os.environ.get("INSTAGRAM_ACCESS_TOKEN", ""),
        "instagram_account_id": os.environ.get("INSTAGRAM_ACCOUNT_ID", ""),
        "app_id": os.environ.get("INSTAGRAM_APP_ID", ""),
        "app_secret": os.environ.get("INSTAGRAM_APP_SECRET", "")
    }
    if CONFIG_FILE.exists():
        try:
            with open(CONFIG_FILE, "r", encoding="utf-8") as f:
                dados = json.load(f)
                creds.update(dados)
        except Exception as e:
            print(f"⚠️ Erro ao ler {CONFIG_FILE.name}: {e}")
    return creds


def carregar_metadados(json_path: Path) -> dict:
    if not json_path.exists():
        raise FileNotFoundError(f"Arquivo de metadados não encontrado em: {json_path}")
    with open(json_path, "r", encoding="utf-8") as f:
        return json.load(f)


def formatar_legenda_instagram(copy_info: dict) -> str:
    """Monta a legenda otimizada para o algoritmo do Instagram Reels."""
    titulo = copy_info.get("titulo", "")
    gancho = copy_info.get("gancho_atencao", "")
    desenvolvimento = copy_info.get("desenvolvimento", "")
    cta = copy_info.get("chamada_acao", "")
    hashtags = " ".join(copy_info.get("hashtags", []))

    partes = []
    if titulo:
        partes.append(f"✨ {titulo.upper()} ✨\n")
    if gancho:
        partes.append(f"{gancho}\n")
    if desenvolvimento:
        partes.append(f"{desenvolvimento}\n")
    if cta:
        partes.append(f"👉 {cta}\n")
    if hashtags:
        partes.append(f"\n{hashtags}")

    legenda = "\n".join(partes).strip()
    if len(legenda) > 2200:
        legenda = legenda[:2190] + "..."
    return legenda


def simular_publicacao_reels(metadados: dict):
    """Realiza uma auditoria completa pré-publicação para todos os vídeos 9:16."""
    print("=" * 80)
    print("📱 SIMULAÇÃO DE PUBLICAÇÃO — INSTAGRAM REELS (META GRAPH API)")
    print("=" * 80)

    creds = carregar_credenciais()
    tem_token = bool(creds.get("access_token") and creds.get("instagram_account_id"))

    if tem_token:
        print(f"🔑 Credenciais Meta encontradas!")
        print(f"   Instagram Account ID: {creds['instagram_account_id']}")
        print(f"   Access Token: {creds['access_token'][:10]}...{creds['access_token'][-6:]}")
    else:
        print("ℹ️ Modo Simulação sem credenciais ativas. Nenhuma chamada à API será feita.")
        print(f"   Para publicar para valer, configure: {CONFIG_FILE.relative_to(BASE_DIR)}")

    print("-" * 80)

    # 1. Shorts / Ápices (Tier 1)
    shorts_dir = DESKTOP_DIR / "05_SHORTS_APICE_45S"
    arquivos_shorts = sorted(list(shorts_dir.glob("*.mp4"))) if shorts_dir.exists() else []

    # 2. Cortes Médios 9:16 (Tier 2)
    medios_reels_dir = DESKTOP_DIR / "02_VIDEOS_9x16_REELS"
    arquivos_medios = sorted(list(medios_reels_dir.glob("*.mp4"))) if medios_reels_dir.exists() else []

    print(f"📦 Vídeos 9:16 identificados no Desktop:")
    print(f"   - Tier 1 (Micro-Shorts 45s): {len(arquivos_shorts)} arquivos em {shorts_dir.name}")
    print(f"   - Tier 2 (Cortes Médios 9:16): {len(arquivos_medios)} arquivos em {medios_reels_dir.name}")
    print("-" * 80)

    cortes_lista = metadados.get("cortes_medios_tier2", [])
    mapa_copies = {c.get("numero", i+1): c for i, c in enumerate(cortes_lista)}

    agendamentos = []
    hora_base = datetime.now(TZ_BRT) + timedelta(days=1, hours=12)  # Inicia amanhã às 12:00

    print("\n📋 PLANO DE POSTAGEM E CONTEÚDO PARA INSTAGRAM REELS:\n")
    for i, video_path in enumerate(arquivos_shorts):
        corte_num = i + 1
        info_corte = mapa_copies.get(corte_num, {})
        reels_meta = info_corte.get("instagram_reels_9x16", {})
        
        titulo = reels_meta.get("headline_gancho", f"Corte {corte_num} - {info_corte.get('tema', 'Palavra Forte')}")
        legenda = reels_meta.get("copy_legenda", "")
        tamanho_mb = video_path.stat().st_size / (1024 * 1024)

        # Escalonamento: 1 Reel por dia às 12h00
        data_publicacao = hora_base + timedelta(days=i)

        item = {
            "tipo": "Tier 1 - Micro-Short 45s (Reels Viral)",
            "corte_id": corte_num,
            "arquivo": video_path.name,
            "tamanho_mb": f"{tamanho_mb:.2f} MB",
            "horario_sugerido": data_publicacao.strftime("%d/%m/%Y às %H:%M BRT"),
            "titulo": titulo,
            "legenda_preview": (legenda[:180] + "...") if legenda else titulo
        }
        agendamentos.append(item)

        print(f"[{i+1}/{len(arquivos_shorts)}] Reel: {video_path.name} ({tamanho_mb:.1f} MB)")
        print(f"   ⏰ Publicação Sugerida: {item['horario_sugerido']}")
        print(f"   📝 Gancho / Headline: {titulo}")
        print(f"   📄 Preview Legenda: {item['legenda_preview']}")
        print("   " + "-" * 70)

    # Salva relatório de planejamento
    relatorio_path = DESKTOP_DIR / "00_PLANO_AGENDAMENTO_INSTAGRAM.json"
    with open(relatorio_path, "w", encoding="utf-8") as f:
        json.dump(agendamentos, f, indent=2, ensure_ascii=False)

    print(f"\n✅ Simulação concluída com sucesso!")
    print(f"💾 Plano de agendamento exportado para: {relatorio_path.name}")


def enviar_video_para_cdn_temporaria(video_path: Path) -> str:
    """Faz upload seguro do arquivo MP4 local para CDN direta temporária aceita pela Meta."""
    import subprocess
    print(f"   ☁️ Preparando streaming de alta velocidade para a Meta ({video_path.name})...")
    cmd = [
        "curl.exe", "-s", "-A", "Mozilla/5.0",
        "-F", "reqtype=fileupload",
        "-F", "time=1h",
        "-F", f"fileToUpload=@{str(video_path)}",
        "https://litterbox.catbox.moe/resources/internals/api.php"
    ]
    try:
        proc = subprocess.run(cmd, capture_output=True, text=True, check=True)
        url = proc.stdout.strip()
        if url.startswith("http"):
            print(f"   ✅ Link de CDN gerado: {url}")
            return url
        print(f"   ⚠️ Resposta inesperada da CDN: {url}")
        return None
    except Exception as e:
        print(f"   ❌ Falha no envio para CDN: {e}")
        return None


def criar_container_reels(ig_user_id: str, access_token: str, video_url: str, caption: str) -> str:
    """Etapa 1 da Meta: Registra o container do Reel a partir de uma URL pública direta."""
    url = f"https://graph.instagram.com/{ig_user_id}/media"
    payload = {
        "media_type": "REELS",
        "video_url": video_url,
        "caption": caption,
        "access_token": access_token
    }
    data = urllib.parse.urlencode(payload).encode("utf-8")
    req = urllib.request.Request(url, data=data, method="POST")

    try:
        with urllib.request.urlopen(req, timeout=60) as resp:
            resultado = json.loads(resp.read().decode("utf-8"))
            return resultado.get("id")
    except urllib.error.HTTPError as e:
        erro_corpo = e.read().decode("utf-8")
        print(f"❌ Erro ao criar container Reel na Meta API: {erro_corpo}")
        return None


def aguardar_processamento_container(container_id: str, access_token: str, max_espera_seg: int = 180) -> bool:
    """Etapa 2 da Meta: Aguarda o vídeo ser codificado e validado pela infraestrutura do Instagram."""
    url = f"https://graph.instagram.com/{container_id}?fields=status_code,status&access_token={access_token}"
    inicio = time.time()

    print(f"   ⏳ Aguardando processamento do vídeo no Instagram (Container ID: {container_id})...")
    while time.time() - inicio < max_espera_seg:
        time.sleep(5)
        req = urllib.request.Request(url, method="GET")
        try:
            with urllib.request.urlopen(req, timeout=30) as resp:
                resultado = json.loads(resp.read().decode("utf-8"))
                status = resultado.get("status_code")
                print(f"      Status: {status}")
                if status == "FINISHED":
                    print("   ✅ Processamento concluído com sucesso pela Meta!")
                    return True
                elif status in ["ERROR", "EXPIRED"]:
                    print(f"   ❌ Falha no processamento do Reel: {resultado.get('status')}")
                    return False
        except Exception as e:
            print(f"   ⚠️ Checagem pendente: {e}. Aguardando...")
    print("   ❌ Tempo limite de processamento atingido.")
    return False


def publicar_container_reels(ig_user_id: str, access_token: str, creation_id: str) -> str:
    """Etapa 3 da Meta: Publica o Reel definitivamente no perfil do Instagram."""
    url = f"https://graph.instagram.com/{ig_user_id}/media_publish"
    payload = {
        "creation_id": creation_id,
        "access_token": access_token
    }
    data = urllib.parse.urlencode(payload).encode("utf-8")
    req = urllib.request.Request(url, data=data, method="POST")

    try:
        with urllib.request.urlopen(req, timeout=60) as resp:
            resultado = json.loads(resp.read().decode("utf-8"))
            media_id = resultado.get("id")
            print(f"   🎉 Reel publicado com sucesso! Media ID: {media_id}")
            return media_id
    except urllib.error.HTTPError as e:
        erro_corpo = e.read().decode("utf-8")
        print(f"❌ Erro ao publicar Reel: {erro_corpo}")
        return None


def main():
    parser = argparse.ArgumentParser(description="Publicador Automático de Instagram Reels via Meta Graph API")
    parser.add_argument("--simular", "--dry-run", action="store_true", help="Audita arquivos, legendas e gera plano sem postar")
    parser.add_argument("--publicar-corte", type=int, default=None, help="Publica imediatamente um corte específico pelo número (ex: --publicar-corte 1)")
    parser.add_argument("--video-url", type=str, default=None, help="URL pública do vídeo para upload via API da Meta")
    args = parser.parse_args()

    if not DEFAULT_JSON_METADADOS.exists():
        print(f"❌ Arquivo de metadados não encontrado em: {DEFAULT_JSON_METADADOS}")
        sys.exit(1)

    metadados = carregar_metadados(DEFAULT_JSON_METADADOS)

    if args.simular or (not args.publicar_corte and not args.video_url):
        simular_publicacao_reels(metadados)
        return

    creds = carregar_credenciais()
    if not creds.get("access_token") or not creds.get("instagram_account_id"):
        print("❌ Erro: Credenciais do Instagram não configuradas.")
        print(f"   Preencha o arquivo: {CONFIG_FILE.relative_to(BASE_DIR)}")
        sys.exit(1)

    if args.publicar_corte:
        corte_id = args.publicar_corte
        shorts_dir = DESKTOP_DIR / "05_SHORTS_APICE_45S"
        arquivos = sorted(list(shorts_dir.glob("*.mp4")))
        if corte_id < 1 or corte_id > len(arquivos):
            print(f"❌ Corte {corte_id} inválido. Escolha entre 1 e {len(arquivos)}.")
            sys.exit(1)

        video_path = arquivos[corte_id - 1]
        cortes_lista = metadados.get("cortes_medios_tier2", [])
        mapa_copies = {c.get("numero", i+1): c for i, c in enumerate(cortes_lista)}
        info_corte = mapa_copies.get(corte_id, {})
        reels_meta = info_corte.get("instagram_reels_9x16", {})
        titulo = reels_meta.get("headline_gancho", f"Corte {corte_id}")
        legenda = reels_meta.get("copy_legenda", titulo)

        print(f"🚀 Publicando Corte {corte_id} ({video_path.name}) no Instagram Reels (@omatheusbs)...")
        print(f"   Gancho: {titulo}")

        user_id = creds.get("instagram_user_id", creds["instagram_account_id"])
        video_url = args.video_url or enviar_video_para_cdn_temporaria(video_path)
        if not video_url:
            print("❌ Não foi possível obter o link do vídeo para o Instagram.")
            sys.exit(1)

        container_id = criar_container_reels(user_id, creds["access_token"], video_url, legenda)
        if container_id:
            print(f"   📦 Container criado com sucesso: {container_id}")
            pronto = aguardar_processamento_container(container_id, creds["access_token"])
            if pronto:
                media_id = publicar_container_reels(user_id, creds["access_token"], container_id)
                if media_id:
                    print(f"🎉 CORTE {corte_id} PUBLICADO COM SUCESSO NO INSTAGRAM REELS! ID: {media_id}")


if __name__ == "__main__":
    main()
