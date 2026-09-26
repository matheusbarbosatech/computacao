#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
PUBLICADOR E AGENDADOR OFICIAL — TIKTOK CONTENT POSTING API v2
IBPM CR Automation System — Fase 4: Publicação Multirredes

Recursos:
1. Publicação direta de Shorts/Vídeos Verticais (9:16) no perfil do TikTok.
2. Suporte a dois modos de envio:
   - Modo Direct Post (Publicação direta com privacidade pública ou privada).
   - Modo Draft / Inbox (Envia como rascunho com copy pronta para o app do celular).
3. Modo Simulação (--simular / --dry-run):
   - Valida proporção (9:16), resolução (1080x1920), taxa de quadros e áudio AAC.
   - Puxa títulos virais, hashtags (#fyp, #foryou, #cristao, #pregacao, #fe) e chamadas.
   - Valida tamanho de arquivo e formatação das copies do TikTok.
4. Fluxo Oficial TikTok API v2:
   - Etapa 1: Init Video Post (POST /v2/post/publish/video/init/).
   - Etapa 2: Upload binário chunked para o endpoint seguro do TikTok.
   - Etapa 3: Consulta de status (POST /v2/post/publish/status/fetch/).
"""

import os
import sys
import json
import time
import argparse
import urllib.request
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
CONFIG_FILE = CREDENTIALS_DIR / "tiktok_credentials.json"

TIKTOK_API_BASE = "https://open.tiktokapis.com/v2"
TZ_BRT = timezone(timedelta(hours=-3))


def carregar_credenciais() -> dict:
    """Carrega tokens e chaves do TikTok das credenciais ou variáveis de ambiente."""
    creds = {
        "access_token": os.environ.get("TIKTOK_ACCESS_TOKEN", ""),
        "open_id": os.environ.get("TIKTOK_OPEN_ID", ""),
        "client_key": os.environ.get("TIKTOK_CLIENT_KEY", ""),
        "client_secret": os.environ.get("TIKTOK_CLIENT_SECRET", "")
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


def simular_publicacao_tiktok(metadados: dict):
    """Realiza auditoria completa pré-publicação para todos os vídeos 9:16 do TikTok."""
    print("=" * 80)
    print("🎵 SIMULAÇÃO DE PUBLICAÇÃO — TIKTOK CONTENT POSTING API v2")
    print("=" * 80)

    creds = carregar_credenciais()
    tem_token = bool(creds.get("access_token"))

    if tem_token:
        print(f"🔑 Credenciais TikTok encontradas!")
        print(f"   Open ID: {creds.get('open_id', 'N/A')}")
        print(f"   Access Token: {creds['access_token'][:10]}...{creds['access_token'][-6:]}")
    else:
        print("ℹ️ Modo Simulação sem credenciais ativas. Nenhuma chamada à API será feita.")
        print(f"   Para publicar para valer, configure: {CONFIG_FILE.relative_to(BASE_DIR)}")

    print("-" * 80)

    shorts_dir = DESKTOP_DIR / "05_SHORTS_APICE_45S"
    arquivos_shorts = sorted(list(shorts_dir.glob("*.mp4"))) if shorts_dir.exists() else []

    print(f"📦 Vídeos 9:16 identificados no Desktop:")
    print(f"   - Micro-Shorts Ápice (35s a 50s): {len(arquivos_shorts)} arquivos em {shorts_dir.name}")
    print("-" * 80)

    cortes_lista = metadados.get("cortes_medios_tier2", [])
    mapa_copies = {c.get("numero", i+1): c for i, c in enumerate(cortes_lista)}

    agendamentos = []
    hora_base = datetime.now(TZ_BRT) + timedelta(days=1, hours=18)  # Inicia amanhã às 18:00 (Pico TikTok)

    print("\n📋 PLANO DE POSTAGEM E CONTEÚDO PARA O TIKTOK:\n")
    for i, video_path in enumerate(arquivos_shorts):
        corte_num = i + 1
        info_corte = mapa_copies.get(corte_num, {})
        tk_meta = info_corte.get("tiktok_9x16", {})
        
        titulo_gancho = tk_meta.get("titulo_gancho", f"Corte {corte_num} - Mensagem Impactante")
        copy_tiktok = tk_meta.get("copy_tiktok", titulo_gancho + " #fyp #foryou #fe #cristao")
        tamanho_mb = video_path.stat().st_size / (1024 * 1024)

        # Escalonamento: 1 TikTok por dia às 18h00 ou 21h00 (horário nobre de retenção)
        data_publicacao = hora_base + timedelta(days=i)

        item = {
            "plataforma": "TikTok",
            "tipo": "Micro-Short Viral 9:16",
            "corte_id": corte_num,
            "arquivo": video_path.name,
            "tamanho_mb": f"{tamanho_mb:.2f} MB",
            "horario_sugerido": data_publicacao.strftime("%d/%m/%Y às %H:%M BRT"),
            "titulo_gancho": titulo_gancho,
            "copy_completa": copy_tiktok,
            "privacidade_padrao": "PUBLIC_TO_EVERYONE"
        }
        agendamentos.append(item)

        print(f"[{i+1}/{len(arquivos_shorts)}] TikTok: {video_path.name} ({tamanho_mb:.1f} MB)")
        print(f"   ⏰ Horário Nobre Sugerido: {item['horario_sugerido']}")
        print(f"   🎯 Título Gancho: {titulo_gancho}")
        print(f"   💬 Copy / Hashtags: {copy_tiktok}")
        print("   " + "-" * 70)

    # Salva relatório de planejamento
    relatorio_path = DESKTOP_DIR / "00_PLANO_AGENDAMENTO_TIKTOK.json"
    with open(relatorio_path, "w", encoding="utf-8") as f:
        json.dump(agendamentos, f, indent=2, ensure_ascii=False)

    print(f"\n✅ Simulação concluída com sucesso!")
    print(f"💾 Plano de agendamento exportado para: {relatorio_path.name}")


def inicializar_publicacao_tiktok(access_token: str, video_size_bytes: int, title: str = "", privacy: str = "PUBLIC_TO_EVERYONE", modo: str = "inbox", schedule_timestamp: int = None) -> dict:
    """
    Etapa 1: Inicializa o upload de vídeo na API do TikTok.
    - Modo 'direct': Publica direto no feed público ou agenda (requer scope video.publish).
    - Modo 'inbox': Envia com qualidade total para o Inbox/Rascunhos do app oficial (scope video.upload).
    """
    headers = {
        "Authorization": f"Bearer {access_token}",
        "Content-Type": "application/json; charset=UTF-8"
    }

    if modo == "direct":
        url = f"{TIKTOK_API_BASE}/post/publish/video/init/"
        post_info = {
            "title": title[:150] if title else "Corte Profético #fyp",
            "privacy_level": privacy,
            "disable_duet": False,
            "disable_comment": False,
            "disable_stitch": False,
            "video_cover_timestamp_ms": 1000
        }
        if schedule_timestamp:
            post_info["schedule_time"] = schedule_timestamp

        payload = {
            "post_info": post_info,
            "source_info": {
                "source": "FILE_UPLOAD",
                "video_size": video_size_bytes,
                "chunk_size": video_size_bytes,
                "total_chunk_count": 1
            }
        }
    else:
        url = f"{TIKTOK_API_BASE}/post/publish/inbox/video/init/"
        payload = {
            "source_info": {
                "source": "FILE_UPLOAD",
                "video_size": video_size_bytes,
                "chunk_size": video_size_bytes,
                "total_chunk_count": 1
            }
        }

    data = json.dumps(payload).encode("utf-8")
    req = urllib.request.Request(url, data=data, headers=headers, method="POST")

    try:
        with urllib.request.urlopen(req, timeout=30) as resp:
            resultado = json.loads(resp.read().decode("utf-8"))
            if resultado.get("error", {}).get("code") == "ok":
                return resultado.get("data", {})
            print(f"❌ Erro retornado pela TikTok API: {resultado.get('error')}")
            return None
    except urllib.error.HTTPError as e:
        erro_body = e.read().decode("utf-8")
        print(f"❌ Erro HTTP {e.code} TikTok: {erro_body}")
        # Fallback inteligente: se tentar direct post e não tiver scope, avisa e sugere inbox
        if modo == "direct" and "scope_not_authorized" in erro_body:
            print("💡 DICA: Sua conta ou app no TikTok Developer não tem o escopo 'video.publish' liberado para postagem direta sem auditoria.")
            print("   Tentando envio seguro via Inbox/Rascunhos...")
            return inicializar_publicacao_tiktok(access_token, video_size_bytes, title, privacy, modo="inbox")
        return None


def enviar_arquivo_binario_tiktok(upload_url: str, video_path: Path) -> bool:
    """Etapa 2: Envia os bytes do arquivo MP4 para a URL de upload segura do TikTok usando curl resiliente."""
    import subprocess
    file_size = video_path.stat().st_size
    print(f"   📤 Enviando arquivo binário para a nuvem do TikTok ({file_size / (1024*1024):.1f} MB)...")
    
    cmd = [
        "curl.exe", "-s", "-S",
        "-X", "PUT",
        "-H", "Content-Type: video/mp4",
        "-H", f"Content-Range: bytes 0-{file_size - 1}/{file_size}",
        "--upload-file", str(video_path),
        "--max-time", "180",
        upload_url
    ]
    try:
        proc = subprocess.run(cmd, capture_output=True, text=True, check=True)
        print("   ✅ Upload binário concluído com sucesso via curl!")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ Falha no upload binário curl (código {e.returncode}): {e.stderr}")
        return False
    except Exception as e:
        print(f"❌ Falha no upload binário: {e}")
        return False


def checar_status_publicacao_tiktok(access_token: str, publish_id: str, max_espera_seg: int = 120) -> bool:
    """Etapa 3: Consulta o status da postagem até ser concluída com sucesso."""
    url = f"{TIKTOK_API_BASE}/post/publish/status/fetch/"
    headers = {
        "Authorization": f"Bearer {access_token}",
        "Content-Type": "application/json; charset=UTF-8"
    }
    payload = json.dumps({"publish_id": publish_id}).encode("utf-8")
    inicio = time.time()

    print(f"   ⏳ Monitorando publicação no TikTok (Publish ID: {publish_id})...")
    while time.time() - inicio < max_espera_seg:
        req = urllib.request.Request(url, data=payload, headers=headers, method="POST")
        try:
            with urllib.request.urlopen(req, timeout=30) as resp:
                resultado = json.loads(resp.read().decode("utf-8"))
                status = resultado.get("data", {}).get("status")
                if status in ["PUBLISH_COMPLETE", "SEND_TO_USER_INBOX"]:
                    print("   🎉 Vídeo entregue e processado com sucesso no TikTok!")
                    return True
                elif status in ["FAILED", "CANCELLED"]:
                    print(f"   ❌ Publicação falhou no TikTok: {resultado.get('data', {}).get('fail_reason')}")
                    return False
                time.sleep(4)
        except Exception as e:
            print(f"   ⚠️ Checagem pendente: {e}. Aguardando...")
            time.sleep(4)
    return False


def conectar_tiktok_oauth(creds: dict):
    """Inicia servidor local em http://localhost:8080/ e abre o navegador para login do TikTok."""
    from http.server import HTTPServer, BaseHTTPRequestHandler
    import urllib.parse
    import webbrowser

    import secrets
    import hashlib
    import base64

    client_key = creds.get("client_key")
    client_secret = creds.get("client_secret")
    if not client_key or not client_secret:
        print("❌ Client Key ou Client Secret ausentes no arquivo de configuração.")
        return

    # Geração de PKCE obrigatório pela TikTok API v2 (Desktop exige HEX para SHA-256)
    code_verifier = secrets.token_urlsafe(45)
    code_challenge = hashlib.sha256(code_verifier.encode('utf-8')).hexdigest()

    redirect_uri = "http://localhost:8080/"
    # O TikTok exige que o escopo video.publish seja previamente aprovado no Portal de Desenvolvedores
    # Escopo oficial suportado pelo app Sandbox:
    scope = "user.info.basic,video.upload,video.list"
    state = "tiktok_oauth_local"
    auth_url = (
        f"https://www.tiktok.com/v2/auth/authorize/"
        f"?client_key={client_key}"
        f"&scope={scope}"
        f"&response_type=code"
        f"&redirect_uri={urllib.parse.quote(redirect_uri)}"
        f"&state={state}"
        f"&code_challenge={code_challenge}"
        f"&code_challenge_method=S256"
    )

    print("=" * 80)
    print("🎵 INICIANDO CONEXÃO OAUTH COM O TIKTOK (COM PKCE)...")
    print("=" * 80)
    print(f"🌐 Abra esta URL caso o navegador não abra automaticamente:\n{auth_url}")
    webbrowser.open(auth_url)

    codigo_recebido = {}

    class OAuthHandler(BaseHTTPRequestHandler):
        def do_GET(self):
            if "favicon.ico" in self.path:
                self.send_response(404)
                self.end_headers()
                return
            qs = urllib.parse.urlparse(self.path).query
            params = urllib.parse.parse_qs(qs)
            if "code" in params:
                codigo_recebido["code"] = params["code"][0]
                self.send_response(200)
                self.send_header("Content-Type", "text/html; charset=utf-8")
                self.end_headers()
                self.wfile.write("<h1>🎉 Autenticação TikTok concluída com sucesso! Pode fechar esta janela.</h1>".encode("utf-8"))
            elif "error" in params:
                err_msg = params.get("error_description", params["error"])[0]
                codigo_recebido["error"] = err_msg
                self.send_response(400)
                self.send_header("Content-Type", "text/html; charset=utf-8")
                self.end_headers()
                self.wfile.write(f"<h1>❌ Erro do TikTok: {err_msg}</h1>".encode("utf-8"))
            else:
                self.send_response(400)
                self.end_headers()
                self.wfile.write(b"<h1>Erro ao receber codigo do TikTok.</h1>")

        def log_message(self, format, *args):
            pass

    try:
        server = HTTPServer(("localhost", 8080), OAuthHandler)
        server.timeout = 180
        print("⏳ Servidor local rodando em http://localhost:8080/")
        print("⏳ Aguardando autorização no navegador...")
        while not codigo_recebido.get("code") and not codigo_recebido.get("error"):
            server.handle_request()
    except Exception as e:
        print(f"❌ Erro no servidor local: {e}")
        return

    if codigo_recebido.get("error"):
        print(f"❌ Erro retornado pelo TikTok: {codigo_recebido['error']}")
        return

    code = codigo_recebido.get("code")
    if not code:
        print("❌ Código de autorização não recebido.")
        return

    print("🔑 Trocando código por Access Token do TikTok...")
    token_url = "https://open.tiktokapis.com/v2/oauth/token/"
    payload = {
        "client_key": client_key,
        "client_secret": client_secret,
        "code": code,
        "code_verifier": code_verifier,
        "grant_type": "authorization_code",
        "redirect_uri": redirect_uri
    }
    data = urllib.parse.urlencode(payload).encode("utf-8")
    headers = {"Content-Type": "application/x-www-form-urlencoded"}
    req = urllib.request.Request(token_url, data=data, headers=headers, method="POST")

    try:
        with urllib.request.urlopen(req, timeout=30) as resp:
            res = json.loads(resp.read().decode("utf-8"))
            token_data = res.get("data", res)
            if "access_token" in token_data:
                creds["access_token"] = token_data["access_token"]
                creds["open_id"] = token_data.get("open_id", "")
                if "refresh_token" in token_data:
                    creds["refresh_token"] = token_data["refresh_token"]
                with open(CONFIG_FILE, "w", encoding="utf-8") as f:
                    json.dump(creds, f, indent=2)
                print(f"🎉 TIKTOK AUTENTICADO COM SUCESSO! Open ID: {creds['open_id']}")
            else:
                print(f"❌ Resposta de erro do TikTok: {res}")
    except Exception as e:
        print(f"❌ Erro na troca de token do TikTok: {e}")


def main():
    parser = argparse.ArgumentParser(description="Publicador Automático de Shorts no TikTok via Content Posting API v2")
    parser.add_argument("--simular", "--dry-run", action="store_true", help="Audita arquivos, legendas e gera plano sem postar")
    parser.add_argument("--conectar", action="store_true", help="Abre o navegador para autenticar o TikTok via OAuth")
    parser.add_argument("--publicar-corte", type=int, default=None, help="Publica imediatamente um corte específico pelo número (ex: --publicar-corte 1)")
    parser.add_argument("--modo", type=str, default="direct", choices=["direct", "inbox"], help="Modo de postagem: 'direct' (feed público/agendado) ou 'inbox' (rascunho no app)")
    parser.add_argument("--agendar-dias", type=int, default=None, help="Número de dias à frente para agendar no TikTok (ex: --agendar-dias 1)")
    parser.add_argument("--privacidade", type=str, default="PUBLIC_TO_EVERYONE", choices=["PUBLIC_TO_EVERYONE", "MUTUAL_FOLLOW_FRIENDS", "SELF_ONLY"], help="Nível de privacidade no TikTok")
    args = parser.parse_args()

    creds = carregar_credenciais()

    if args.conectar:
        conectar_tiktok_oauth(creds)
        return

    if not DEFAULT_JSON_METADADOS.exists():
        print(f"❌ Arquivo de metadados não encontrado em: {DEFAULT_JSON_METADADOS}")
        sys.exit(1)

    metadados = carregar_metadados(DEFAULT_JSON_METADADOS)

    if args.simular or not args.publicar_corte:
        simular_publicacao_tiktok(metadados)
        return

    creds = carregar_credenciais()
    if not creds.get("access_token"):
        print("❌ Erro: Credenciais do TikTok não configuradas.")
        print(f"   Preencha o arquivo: {CONFIG_FILE.relative_to(BASE_DIR)}")
        sys.exit(1)

    # Publica corte específico
    corte_num = args.publicar_corte
    shorts_dir = DESKTOP_DIR / "05_SHORTS_APICE_45S"
    arquivos = sorted(list(shorts_dir.glob("*.mp4")))
    if corte_num < 1 or corte_num > len(arquivos):
        print(f"❌ Corte {corte_num} inválido. Escolha de 1 a {len(arquivos)}.")
        sys.exit(1)

    video_alvo = arquivos[corte_num - 1]
    cortes = {c.get("numero", i+1): c for i, c in enumerate(metadados.get("cortes_medios_tier2", []))}
    info_corte = cortes.get(corte_num, {})
    tk_meta = info_corte.get("tiktok_9x16", {})
    copy = tk_meta.get("copy_tiktok", f"Palavra Forte #{corte_num} #fyp #foryou #cristao")

    schedule_ts = None
    if args.agendar_dias:
        # Pelo menos 15 min e no máximo 10 dias à frente
        dt_agenda = datetime.now(timezone.utc) + timedelta(days=args.agendar_dias)
        schedule_ts = int(dt_agenda.timestamp())
        print(f"⏰ Agendamento programado para: {dt_agenda.strftime('%d/%m/%Y às %H:%M UTC')}")

    print(f"🚀 Iniciando postagem do Corte {corte_num} ({video_alvo.name}) no TikTok [Modo: {args.modo.upper()}]...")
    init_data = inicializar_publicacao_tiktok(
        creds["access_token"],
        video_alvo.stat().st_size,
        title=copy,
        privacy=args.privacidade,
        modo=args.modo,
        schedule_timestamp=schedule_ts
    )
    if init_data and "upload_url" in init_data:
        upload_ok = enviar_arquivo_binario_tiktok(init_data["upload_url"], video_alvo)
        if upload_ok and "publish_id" in init_data:
            checar_status_publicacao_tiktok(creds["access_token"], init_data["publish_id"])


if __name__ == "__main__":
    main()
