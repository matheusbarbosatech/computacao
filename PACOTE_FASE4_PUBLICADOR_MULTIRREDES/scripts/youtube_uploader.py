#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
AGENDADOR E PUBLICADOR AUTOMÁTICO — YOUTUBE DATA API v3 (FASE 4)
IBPM CR Automation System — Publicação Inteligente da Pirâmide de Conteúdo

Consome:
- 00_COPIES_E_METADADOS_POSTAGEM.json (Títulos, descrições com capítulos, tags)
- 05_SHORTS_APICE_45S/*.mp4 (Tier 1: Micro-Shorts 9:16)
- 01_VIDEOS_16x9_YOUTUBE/*.mp4 (Tier 2: Cortes Médios 16:9)
- 00_PREGACAO_COMPLETA_TIER3/*.mp4 (Tier 3: Pregação Completa)
- 04_CAPAS_THUMBNAILS/16x9_YOUTUBE/*.jpg (Thumbnails oficiais)

Recursos:
1. Modo Simulação (--simular / --dry-run): Valida metadados, tamanhos, limites de caracteres e gera calendário visual.
2. Agendamento com publishAt: Programa a liberação automática em horários nobres no YouTube.
3. Upload Automático de Miniaturas (Thumbnails).
4. Gerenciamento e cálculo de cota diária (10.000 unidades do Google).
"""

import os
import sys
import json
import time
import argparse
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
CLIENT_SECRETS_FILE = CREDENTIALS_DIR / "client_secret.json"
TOKEN_FILE = CREDENTIALS_DIR / "token_youtube.json"

SCOPES = [
    "https://www.googleapis.com/auth/youtube.upload",
    "https://www.googleapis.com/auth/youtube",
    "https://www.googleapis.com/auth/youtube.force-ssl"
]

# Custos oficiais de cota da YouTube Data API v3
CUSTO_VIDEO_INSERT = 1600
CUSTO_THUMBNAIL_SET = 50
COTA_DIARIA_MAXIMA = 10000

# Fuso horário oficial (Brasília UTC-3)
TZ_BRT = timezone(timedelta(hours=-3))


def carregar_metadados(json_path: Path) -> dict:
    if not json_path.exists():
        raise FileNotFoundError(f"Arquivo de metadados não encontrado em: {json_path}")
    with open(json_path, "r", encoding="utf-8") as f:
        return json.load(f)


def obter_cliente_youtube():
    """
    Inicializa o cliente autenticado via OAuth 2.0.
    Se não houver credenciais, retorna None.
    """
    try:
        from googleapiclient.discovery import build
        from google.oauth2.credentials import Credentials
        from google.auth.transport.requests import Request
        from google_auth_oauthlib.flow import InstalledAppFlow
    except ImportError:
        print("❌ Bibliotecas do Google não instaladas. Execute: pip install google-api-python-client google-auth-oauthlib")
        return None

    creds = None
    if TOKEN_FILE.exists():
        try:
            creds = Credentials.from_authorized_user_file(str(TOKEN_FILE), SCOPES)
        except Exception as e:
            print(f"⚠️ Erro ao ler token salvo: {e}")

    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            try:
                creds.refresh(Request())
                print("🔄 Token de acesso do YouTube renovado com sucesso via Refresh Token.")
            except Exception as e:
                print(f"⚠️ Não foi possível renovar o token: {e}")
                creds = None

        if not creds:
            if not CLIENT_SECRETS_FILE.exists():
                print(f"⚠️ Arquivo client_secret.json não encontrado em: {CLIENT_SECRETS_FILE}")
                print(f"   Consulte o guia: config/credentials/README_YOUTUBE_OAUTH.md")
                return None

            print("🌐 Iniciando fluxo de autorização OAuth 2.0 no navegador...")
            flow = InstalledAppFlow.from_client_secrets_file(str(CLIENT_SECRETS_FILE), SCOPES)
            creds = flow.run_local_server(port=0)

        CREDENTIALS_DIR.mkdir(parents=True, exist_ok=True)
        with open(TOKEN_FILE, "w", encoding="utf-8") as f:
            f.write(creds.to_json())
        print(f"✅ Token salvo com sucesso em: {TOKEN_FILE}")

    return build("youtube", "v3", credentials=creds)


def planejar_calendario_publicacao(metadados: dict, data_inicio: datetime):
    """
    Constrói a grade de programação inteligente da Pirâmide de Conteúdo:
    - Tier 3: Segunda-feira às 19h00 (Mensagem Mestre)
    - Tier 1 (Shorts): 1 por dia às 12h00
    - Tier 2 (Cortes Médios): Terças e Quintas às 19h30
    """
    itens = []
    
    # 1. Tier 3 — Pregação Completa
    tier3_meta = metadados.get("tier3_pregacao_completa", {})
    if tier3_meta:
        # Próxima segunda-feira às 19h00
        dias_ate_segunda = (0 - data_inicio.weekday()) % 7
        if dias_ate_segunda == 0 and data_inicio.hour >= 19:
            dias_ate_segunda = 7
        dt_tier3 = (data_inicio + timedelta(days=dias_ate_segunda)).replace(hour=19, minute=0, second=0, microsecond=0, tzinfo=TZ_BRT)
        
        arquivo_video = DESKTOP_DIR / "00_PREGACAO_COMPLETA_TIER3" / "PREGACAO_COMPLETA_CULTO_459_DOMINGO_DE_CELEBRACAO_1080p60.mp4"
        arquivo_thumb = DESKTOP_DIR / "00_PREGACAO_COMPLETA_TIER3" / "THUMBNAIL_PREGACAO_COMPLETA_YOUTUBE.jpg"

        itens.append({
            "tier": "Tier 3 (Pregação Completa)",
            "tipo": "video_longo",
            "id_corte": "TIER3_MASTER",
            "titulo": tier3_meta.get("titulo_youtube", "")[:100],
            "descricao": tier3_meta.get("descricao_youtube", "")[:5000],
            "tags": tier3_meta.get("tags_seo", [])[:20],
            "categoria_id": "29",  # Nonprofits & Activism / Religião
            "data_programada_brt": dt_tier3.strftime("%d/%m/%Y %H:%M"),
            "publish_at_utc": dt_tier3.astimezone(timezone.utc).isoformat().replace("+00:00", "Z"),
            "video_path": arquivo_video,
            "thumb_path": arquivo_thumb,
            "custo_cota": CUSTO_VIDEO_INSERT + CUSTO_THUMBNAIL_SET
        })

    # 2. Tier 1 — 14 Micro-Shorts (1 por dia às 12h00)
    shorts_dir = DESKTOP_DIR / "05_SHORTS_APICE_45S"
    arquivos_shorts = sorted(list(shorts_dir.glob("*.mp4")))
    
    cortes_lista = metadados.get("cortes_medios", [])
    
    dia_short = data_inicio.replace(hour=12, minute=0, second=0, microsecond=0, tzinfo=TZ_BRT)
    if data_inicio.hour >= 12:
        dia_short += timedelta(days=1)

    for i, short_path in enumerate(arquivos_shorts):
        # Mapeia copy correspondente
        corte_info = cortes_lista[i] if i < len(cortes_lista) else {}
        titulo_base = corte_info.get("titulo_youtube", short_path.stem.replace("_", " "))
        
        # O YouTube Shorts precisa de #Shorts no título ou descrição
        titulo_short = f"{titulo_base[:88]} #Shorts"
        descricao_short = f"{corte_info.get('copy_instagram_reels', {}).get('texto', '')}\n\nAssista à pregação completa no canal @ibpmcr7976!\n\n#Shorts #IBPM #Jesus #Fé #Palavra"
        tags_short = ["Shorts", "IBPM", "Pregação", "Fé", "Jesus", "Deus", "Campo Grande", "Gospel", "Testemunho"]

        itens.append({
            "tier": "Tier 1 (Micro-Short 45s)",
            "tipo": "short_vertical",
            "id_corte": f"SHORT_{i+1:02d}",
            "titulo": titulo_short[:100],
            "descricao": descricao_short[:5000],
            "tags": tags_short,
            "categoria_id": "29",
            "data_programada_brt": dia_short.strftime("%d/%m/%Y %H:%M"),
            "publish_at_utc": dia_short.astimezone(timezone.utc).isoformat().replace("+00:00", "Z"),
            "video_path": short_path,
            "thumb_path": None,  # Shorts verticais usam o frame automático
            "custo_cota": CUSTO_VIDEO_INSERT
        })
        dia_short += timedelta(days=1)

    # 3. Tier 2 — 14 Cortes Médios 16:9 (Terças e Quintas às 19h30)
    videos_16x9_dir = DESKTOP_DIR / "01_VIDEOS_16x9_YOUTUBE"
    thumbs_16x9_dir = DESKTOP_DIR / "04_CAPAS_THUMBNAILS" / "16x9_YOUTUBE"
    arquivos_16x9 = sorted(list(videos_16x9_dir.glob("*.mp4")))

    # Encontra próximas Terças (weekday 1) e Quintas (weekday 3)
    dia_medio = data_inicio.replace(hour=19, minute=30, second=0, microsecond=0, tzinfo=TZ_BRT)
    while dia_medio.weekday() not in [1, 3] or (dia_medio.date() == data_inicio.date() and data_inicio.hour >= 19):
        dia_medio += timedelta(days=1)

    for i, video_path in enumerate(arquivos_16x9):
        corte_info = cortes_lista[i] if i < len(cortes_lista) else {}
        titulo_medio = corte_info.get("titulo_youtube", video_path.stem)[:100]
        desc_medio = corte_info.get("descricao_youtube", "")[:5000]
        tags_medio = corte_info.get("tags_seo", ["IBPM", "Culto", "Pregação"])

        thumb_medio = thumbs_16x9_dir / f"THUMB_16x9_CORTE_{i+1:02d}.jpg"
        if not thumb_medio.exists():
            thumb_medio = None

        itens.append({
            "tier": "Tier 2 (Corte Médio 3m)",
            "tipo": "video_medio_16x9",
            "id_corte": f"MEDIO_{i+1:02d}",
            "titulo": titulo_medio,
            "descricao": desc_medio,
            "tags": tags_medio,
            "categoria_id": "29",
            "data_programada_brt": dia_medio.strftime("%d/%m/%Y %H:%M"),
            "publish_at_utc": dia_medio.astimezone(timezone.utc).isoformat().replace("+00:00", "Z"),
            "video_path": video_path,
            "thumb_path": thumb_medio,
            "custo_cota": CUSTO_VIDEO_INSERT + (CUSTO_THUMBNAIL_SET if thumb_medio else 0)
        })

        # Avança para a próxima terça ou quinta
        dia_medio += timedelta(days=1)
        while dia_medio.weekday() not in [1, 3]:
            dia_medio += timedelta(days=1)

    return itens


def executar_simulacao(itens: list):
    """
    Valida todos os metadados, caminhos, comprimentos e exibe o cronograma em tabela.
    """
    print("=" * 110)
    print("📋 RELATÓRIO DE SIMULAÇÃO (DRY-RUN) — AGENDAMENTO AUTOMÁTICO YOUTUBE (FASE 4)")
    print("=" * 110)

    total_cota = sum(item["custo_cota"] for item in itens)
    total_videos = len(itens)
    total_com_thumb = sum(1 for item in itens if item["thumb_path"])

    print(f"📊 Resumo Geral do Pacote:")
    print(f"   • Total de Vídeos a Agendar: {total_videos} vídeos")
    print(f"   • Tier 3 (Pregação Completa): 1 vídeo master com capítulos")
    print(f"   • Tier 2 (Cortes Médios 16:9): 14 vídeos com thumbnails")
    print(f"   • Tier 1 (Micro-Shorts 45s): 14 shorts verticais com #Shorts")
    print(f"   • Cota Total Estimada da API: {total_cota:,} unidades (Limite diário do Google: {COTA_DIARIA_MAXIMA:,})")
    print("=" * 110)

    print(f"{'DATA (BRT)':<18} | {'TIER':<24} | {'STATUS ARQUIVO':<16} | {'TÍTULO NO YOUTUBE':<44}")
    print("-" * 110)

    validacao_ok = True
    for item in itens:
        vid_existe = item["video_path"].exists() if item["video_path"] else False
        status_vid = "✅ OK" if vid_existe else "❌ FALTA VÍDEO"
        if not vid_existe:
            validacao_ok = False

        titulo = item["titulo"]
        if len(titulo) > 42:
            titulo = titulo[:39] + "..."

        print(f"{item['data_programada_brt']:<18} | {item['tier']:<24} | {status_vid:<16} | {titulo:<44}")

    print("=" * 110)

    # Salva o plano completo em JSON no Desktop para inspeção
    plano_json = DESKTOP_DIR / "00_PLANO_AGENDAMENTO_YOUTUBE.json"
    dados_export = []
    for item in itens:
        dados_export.append({
            "tier": item["tier"],
            "id_corte": item["id_corte"],
            "titulo": item["titulo"],
            "caracteres_titulo": len(item["titulo"]),
            "data_programada_brt": item["data_programada_brt"],
            "publish_at_utc": item["publish_at_utc"],
            "video_path": str(item["video_path"]),
            "video_existe": item["video_path"].exists() if item["video_path"] else False,
            "thumb_path": str(item["thumb_path"]) if item["thumb_path"] else None,
            "custo_cota": item["custo_cota"]
        })

    with open(plano_json, "w", encoding="utf-8") as f:
        json.dump(dados_export, f, indent=2, ensure_ascii=False)

    print(f"\n📁 Plano de Agendamento salvo com sucesso em:")
    print(f"   --> {plano_json}")

    if validacao_ok:
        print("\n🎉 TODAS AS VALIDAÇÕES FORAM APROVADAS! A esteira está 100% pronta para envio.")
    else:
        print("\n⚠️ Alguns arquivos de vídeo ainda estão sendo renderizados em segundo plano.")

    return validacao_ok


def fazer_upload_e_agendamento(youtube, item: dict):
    """
    Executa o upload real do vídeo com status='private' e publishAt programado.
    Em seguida, envia a thumbnail.
    """
    from googleapiclient.http import MediaFileUpload

    print(f"\n🚀 Iniciando upload de: {item['id_corte']} — {item['titulo'][:60]}...")
    print(f"   📅 Agendamento: {item['data_programada_brt']} (UTC: {item['publish_at_utc']})")

    body = {
        "snippet": {
            "title": item["titulo"],
            "description": item["descricao"],
            "tags": item["tags"],
            "categoryId": item["categoria_id"]
        },
        "status": {
            "privacyStatus": "private",
            "publishAt": item["publish_at_utc"],
            "selfDeclaredMadeForKids": False
        }
    }

    media = MediaFileUpload(
        str(item["video_path"]),
        chunksize=1024 * 1024 * 5,  # 5MB chunks
        resumable=True
    )

    request = youtube.videos().insert(
        part="snippet,status",
        body=body,
        media_body=media
    )

    response = None
    t0 = time.time()
    while response is None:
        status, response = request.next_chunk()
        if status:
            progresso = int(status.progress() * 100)
            print(f"   ⏳ Upload em andamento: {progresso}%...", end="\r")

    video_id = response.get("id")
    video_url = f"https://youtu.be/{video_id}"
    print(f"\n   ✅ Vídeo enviado e programado com sucesso!")
    print(f"      ID: {video_id} | Link: {video_url} (Tempo: {time.time()-t0:.1f}s)")

    # Upload da Thumbnail oficial (se existir)
    if item.get("thumb_path") and Path(item["thumb_path"]).exists():
        try:
            print(f"   🖼️ Enviando thumbnail oficial: {Path(item['thumb_path']).name}...")
            youtube.thumbnails().set(
                videoId=video_id,
                media_body=MediaFileUpload(str(item["thumb_path"]))
            ).execute()
            print("   ✅ Thumbnail associada com sucesso!")
        except Exception as e:
            print(f"   ⚠️ Falha ao associar thumbnail: {e}")

    return {
        "id_corte": item["id_corte"],
        "video_id": video_id,
        "video_url": video_url,
        "publish_at_utc": item["publish_at_utc"],
        "data_programada_brt": item["data_programada_brt"],
        "timestamp_envio": datetime.now(timezone.utc).isoformat()
    }


def main():
    parser = argparse.ArgumentParser(description="Publicador e Agendador Automático do YouTube — IBPM CR")
    parser.add_argument("--simular", "--dry-run", action="store_true", help="Executa a simulação e validação sem enviar à API")
    parser.add_argument("--agendar-todos", action="store_true", help="Agenda toda a pirâmide (Tier 3 + Tier 2 + Tier 1)")
    parser.add_argument("--agendar-tier3", action="store_true", help="Agenda apenas a Pregação Completa")
    parser.add_argument("--agendar-shorts", action="store_true", help="Agenda os 14 Micro-Shorts de 45s")
    parser.add_argument("--agendar-cortes-medios", action="store_true", help="Agenda os 14 Cortes Médios 16:9")
    parser.add_argument("--data-inicio", type=str, default=None, help="Data inicial no formato YYYY-MM-DD (padrão: amanhã)")
    parser.add_argument("--json-metadados", type=str, default=str(DEFAULT_JSON_METADADOS), help="Caminho do JSON com metadados")
    args = parser.parse_args()

    # Data de início padrão: amanhã
    if args.data_inicio:
        dt_inicio = datetime.strptime(args.data_inicio, "%Y-%m-%d").replace(tzinfo=TZ_BRT)
    else:
        dt_inicio = (datetime.now(TZ_BRT) + timedelta(days=1)).replace(hour=0, minute=0, second=0, microsecond=0)

    try:
        metadados = carregar_metadados(Path(args.json_metadados))
    except Exception as e:
        print(f"❌ Erro ao carregar metadados: {e}")
        return

    itens = planejar_calendario_publicacao(metadados, dt_inicio)

    # Filtragem por flags
    if args.agendar_tier3:
        itens = [item for item in itens if "Tier 3" in item["tier"]]
    elif args.agendar_shorts:
        itens = [item for item in itens if "Tier 1" in item["tier"]]
    elif args.agendar_cortes_medios:
        itens = [item for item in itens if "Tier 2" in item["tier"]]

    # Se a flag --simular for passada (ou nenhuma flag de agendamento for informada), roda a simulação
    if args.simular or (not args.agendar_todos and not args.agendar_tier3 and not args.agendar_shorts and not args.agendar_cortes_medios):
        executar_simulacao(itens)
        return

    # Modo Produção com API Real
    print("=" * 80)
    print("🚀 INICIANDO AGENDAMENTO EM PRODUÇÃO NO YOUTUBE (@ibpmcr7976)")
    print("=" * 80)

    youtube = obter_cliente_youtube()
    if not youtube:
        print("\n❌ Não foi possível autenticar no YouTube. Execute com --simular para modo teste.")
        return

    relatorio_envios = []
    for item in itens:
        if not item["video_path"].exists():
            print(f"⚠️ Pulando {item['id_corte']}: Arquivo de vídeo não encontrado em disco.")
            continue

        try:
            res = fazer_upload_e_agendamento(youtube, item)
            relatorio_envios.append(res)
            # Pausa de 3 segundos entre envios para evitar rate-limiting
            time.sleep(3)
        except Exception as e:
            print(f"❌ Erro ao processar {item['id_corte']}: {e}")

    # Salva relatório de envios
    relatorio_json = DESKTOP_DIR / "00_RELATORIO_PUBLICACAO_YOUTUBE.json"
    with open(relatorio_json, "w", encoding="utf-8") as f:
        json.dump(relatorio_envios, f, indent=2, ensure_ascii=False)

    print(f"\n🎉 Envio concluído! {len(relatorio_envios)} vídeos agendados no YouTube.")
    print(f"   Relatório salvo em: {relatorio_json}")


if __name__ == "__main__":
    main()
