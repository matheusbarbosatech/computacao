#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
PUBLICADOR E AGENDADOR OFICIAL — WHATSAPP STATUS (STORIES DO ZAP)
IBPM CR Automation System — Fase 4: Publicação Multirredes

O WhatsApp Status é o canal com maior taxa de abertura e retenção no Brasil:
- Audiência 100% quente (contatos, líderes, membros, amigos e familiares).
- Formato vertical nativo 9:16 (exatamente a proporção dos nossos 14 Micro-Shorts de 45s).
- Suporte a legendas com links e CTAs diretos.

Como funciona a automação do WhatsApp Status:
A API oficial da Meta (WhatsApp Cloud API) NÃO permite postar no Status (apenas conversas 1 a 1).
Por isso, este módulo implementa 3 opções profissionais e seguras:
1. Modo Navegador Persistente (Selenium / Chrome):
   - Abre o WhatsApp Web mantendo a sessão salva em 'data/whatsapp_session/'.
   - O usuário lê o QR Code uma única vez no celular.
   - O robô faz o upload do vídeo 9:16, insere a legenda com emojis e publica no Status.
2. Modo Gateway / REST API (Z-API / Evolution API / Baileys):
   - Envio direto para o JID 'status@broadcast'.
3. Modo Simulação (--simular / --dry-run):
   - Valida os 14 Micro-Shorts, formata copies curtas de alta conversão e gera o calendário.

Uso:
  python scripts/fase4_publicacao/whatsapp_status_uploader.py --simular
  python scripts/fase4_publicacao/whatsapp_status_uploader.py --conectar
  python scripts/fase4_publicacao/whatsapp_status_uploader.py --postar-corte 1
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
SESSION_DIR = BASE_DIR / "data" / "whatsapp_session"
SESSION_DIR.mkdir(parents=True, exist_ok=True)

CONFIG_FILE = BASE_DIR / "config" / "credentials" / "whatsapp_credentials.json"
TZ_BRT = timezone(timedelta(hours=-3))


def carregar_credenciais() -> dict:
    creds = {
        "api_url": os.environ.get("WHATSAPP_API_URL", ""),
        "api_token": os.environ.get("WHATSAPP_API_TOKEN", ""),
        "instance_id": os.environ.get("WHATSAPP_INSTANCE_ID", "")
    }
    if CONFIG_FILE.exists():
        try:
            with open(CONFIG_FILE, "r", encoding="utf-8") as f:
                creds.update(json.load(f))
        except Exception as e:
            print(f"⚠️ Erro ao ler {CONFIG_FILE.name}: {e}")
    return creds


def carregar_metadados(json_path: Path) -> dict:
    if not json_path.exists():
        raise FileNotFoundError(f"Arquivo de metadados não encontrado em: {json_path}")
    with open(json_path, "r", encoding="utf-8") as f:
        return json.load(f)


def formatar_legenda_whatsapp_status(copy_corte: dict, numero_corte: int) -> str:
    """Monta uma legenda concisa e impactante ideal para Status do WhatsApp (máx 150 caracteres para leitura rápida)."""
    tk_meta = copy_corte.get("tiktok_9x16", {})
    reels_meta = copy_corte.get("instagram_reels_9x16", {})
    
    gancho = tk_meta.get("titulo_gancho") or reels_meta.get("headline_gancho") or f"Mensagem Forte #{numero_corte}"
    # Legenda enxuta com chamada para ação
    legenda = f"🔥 {gancho}\n\n👉 Assista à mensagem completa no canal! Link nos comentários/bio."
    return legenda


def simular_whatsapp_status(metadados: dict):
    """Audita os vídeos 9:16 e gera o calendário de postagem nos Status do WhatsApp."""
    print("=" * 80)
    print("🟢 SIMULAÇÃO DE PUBLICAÇÃO — WHATSAPP STATUS (STORIES DO ZAP)")
    print("=" * 80)
    print("ℹ️ Modo Simulação: Nenhum envio real será realizado agora.")
    print("   Os 14 Micro-Shorts (35-50s) têm formato vertical perfeito para Stories/Status.")
    print("-" * 80)

    shorts_dir = DESKTOP_DIR / "05_SHORTS_APICE_45S"
    arquivos_shorts = sorted(list(shorts_dir.glob("*.mp4"))) if shorts_dir.exists() else []

    print(f"📦 Vídeos 9:16 disponíveis no Desktop:")
    print(f"   - {len(arquivos_shorts)} Micro-Shorts Ápice em {shorts_dir.name}")
    print("-" * 80)

    cortes_lista = metadados.get("cortes_medios_tier2", [])
    mapa_copies = {c.get("numero", i+1): c for i, c in enumerate(cortes_lista)}

    agendamentos = []
    hora_base = datetime.now(TZ_BRT) + timedelta(days=1, hours=8)  # Inicia amanhã às 08:00 (Pico matinal do Zap)

    print("\n📋 PLANO DE POSTAGEM PARA O WHATSAPP STATUS (PICO DE AUDIÊNCIA):\n")
    for i, video_path in enumerate(arquivos_shorts):
        corte_num = i + 1
        info_corte = mapa_copies.get(corte_num, {})
        legenda = formatar_legenda_whatsapp_status(info_corte, corte_num)
        tamanho_mb = video_path.stat().st_size / (1024 * 1024)

        # Escalonamento: 1 ou 2 status por dia (ex: 08h00 e 19h00)
        data_publicacao = hora_base + timedelta(days=i)

        item = {
            "plataforma": "WhatsApp Status",
            "tipo": "Story / Vídeo 9:16",
            "corte_id": corte_num,
            "arquivo": video_path.name,
            "tamanho_mb": f"{tamanho_mb:.2f} MB",
            "horario_sugerido": data_publicacao.strftime("%d/%m/%Y às %H:%M BRT"),
            "legenda_status": legenda
        }
        agendamentos.append(item)

        print(f"[{i+1}/{len(arquivos_shorts)}] Status: {video_path.name} ({tamanho_mb:.1f} MB)")
        print(f"   ⏰ Horário Sugerido (Pico Matinal): {item['horario_sugerido']}")
        print(f"   💬 Texto do Status:\n{legenda}")
        print("   " + "-" * 70)

    relatorio_path = DESKTOP_DIR / "00_PLANO_AGENDAMENTO_WHATSAPP_STATUS.json"
    with open(relatorio_path, "w", encoding="utf-8") as f:
        json.dump(agendamentos, f, indent=2, ensure_ascii=False)

    print(f"\n✅ Simulação do WhatsApp Status concluída!")
    print(f"💾 Relatório salvo em: {relatorio_path.name}")


def conectar_whatsapp_web():
    """Abre uma janela persistente do Chrome com WhatsApp Web para leitura do QR Code."""
    print("=" * 80)
    print("📲 INICIALIZANDO CONEXÃO DO WHATSAPP WEB...")
    print("=" * 80)
    print("ℹ️ Uma janela do Chrome será aberta.")
    print("   1. Abra o WhatsApp no seu celular.")
    print("   2. Vá em Configurações > Aparelhos Conectados > Conectar Aparelho.")
    print("   3. Aponte a câmera para o QR Code na tela.")
    print(f"   A sessão ficará salva em: {SESSION_DIR.resolve()}")
    print("-" * 80)

    try:
        from selenium import webdriver
        from selenium.webdriver.chrome.options import Options
        from selenium.webdriver.chrome.service import Service

        chrome_options = Options()
        chrome_options.add_argument(f"--user-data-dir={SESSION_DIR.resolve()}")
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("--disable-dev-shm-usage")

        driver = webdriver.Chrome(options=chrome_options)
        driver.get("https://web.whatsapp.com")

        print("🚀 WhatsApp Web aberto. Aguardando você escanear o QR Code...")
        print("   (Você pode manter a janela aberta para publicar quando desejar)")
        
        # Mantém vivo para o usuário ler o QR code
        time.sleep(30)
        print("✅ Sessão inicializada. Feche a janela quando terminar o login.")
        input("Pressione ENTER após escanear o QR Code com sucesso...")
        driver.quit()
    except Exception as e:
        print(f"❌ Erro ao abrir navegador para WhatsApp: {e}")
        print("💡 Dica: Você também pode usar um gateway de API como Z-API ou Evolution API.")


def postar_status_via_selenium(video_path: Path, legenda: str) -> bool:
    """Abre o WhatsApp Web usando a sessão salva em data/whatsapp_session e posta o vídeo no Status."""
    from selenium import webdriver
    from selenium.webdriver.chrome.options import Options
    from selenium.webdriver.common.by import By
    from selenium.webdriver.support.ui import WebDriverWait
    from selenium.webdriver.support import expected_conditions as EC
    from selenium.webdriver.common.keys import Keys

    print("=" * 80)
    print(f"🚀 INICIANDO POSTAGEM NO WHATSAPP STATUS VIA SESSÃO SALVA")
    print(f"   Vídeo: {video_path.name}")
    print("=" * 80)

    chrome_options = Options()
    chrome_options.add_argument(f"--user-data-dir={SESSION_DIR.resolve()}")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    # Não usamos headless para garantir renderização de canvas de mídia e estabilidade do WhatsApp Web
    chrome_options.add_argument("--start-maximized")

    driver = None
    try:
        print("🌐 Abrindo WhatsApp Web com sua sessão salva...")
        driver = webdriver.Chrome(options=chrome_options)
        driver.get("https://web.whatsapp.com")

        # 1. Aguardar carregamento da sessão logada (até 45 segundos)
        wait = WebDriverWait(driver, 45)
        print("⏳ Verificando login do WhatsApp...")
        wait.until(EC.presence_of_element_located((By.XPATH, "//*[@id='pane-side'] | //div[contains(@data-testid, 'chat-list')] | //button[@aria-label='Status']")))
        print("✅ Sessão validada e ativa!")

        time.sleep(3)

        # 2. Clicar no botão de Status no topo/menu lateral
        print("📱 Acessando aba de Status...")
        wait.until(EC.element_to_be_clickable((By.XPATH, "//button[@aria-label='Status'] | //span[@data-icon='status-v3']/ancestor::button"))).click()
        time.sleep(3)

        # 3. Clicar no botão 'Foto e vídeo' para revelar o input de arquivo
        print("📸 Clicando na opção 'Foto e vídeo' do Status...")
        botoes_add = driver.find_elements(By.XPATH, "//button[contains(., 'Foto e v') or contains(., 'Foto')] | //button[@aria-label='Add Status']")
        if not botoes_add:
            # Fallback para o card 'Meu status'
            botoes_add = driver.find_elements(By.XPATH, "//button[contains(., 'Meu status')]")

        if botoes_add:
            botoes_add[0].click()
            time.sleep(2)

        # 4. Localizar o input de arquivo revelado
        print("📤 Anexando arquivo do vídeo no WhatsApp Status...")
        file_inputs = driver.find_elements(By.XPATH, "//input[@type='file' and contains(@accept, 'video')]")
        if not file_inputs:
            file_inputs = driver.find_elements(By.XPATH, "//input[@type='file']")

        if not file_inputs:
            raise Exception("Campo de upload de arquivo do Status não encontrado após clicar em 'Foto e vídeo'.")

        # Envia o caminho do arquivo MP4 para o input
        caminho_abs = str(video_path.resolve())
        file_inputs[0].send_keys(caminho_abs)
        print(f"   Arquivo '{video_path.name}' enviado para o WhatsApp! Aguardando editor de mídia...")

        # 5. Aguardar o editor de mídia carregar o vídeo e o campo de legenda
        time.sleep(6)
        caption_box = wait.until(EC.presence_of_element_located((By.XPATH, "//div[@contenteditable='true'] | //div[contains(@data-testid, 'caption-input')]")))
        
        # Digita a legenda
        print("✍️ Inserindo legenda no Status...")
        caption_box.click()
        time.sleep(1)
        caption_box.send_keys(legenda)
        time.sleep(2)

        # 6. Clicar no botão Enviar (verde)
        print("🚀 Clicando no botão verde de Enviar...")
        send_btn = None
        selectors_send = [
            "//span[@data-icon='send']/ancestor::button",
            "//span[@data-icon='send']/ancestor::div[@role='button']",
            "//button[contains(@aria-label, 'Enviar')]",
            "//div[contains(@aria-label, 'Enviar')]"
        ]
        for sel in selectors_send:
            elems = driver.find_elements(By.XPATH, sel)
            if elems:
                send_btn = elems[0]
                break

        if send_btn:
            send_btn.click()
        else:
            caption_box.send_keys(Keys.ENTER)

        print("⏳ Enviando vídeo para o Status do WhatsApp (aguardando 15s para upload completo)...")
        time.sleep(15)
        print("🎉 STATUS POSTADO NO WHATSAPP COM SUCESSO!")
        return True

    except Exception as e:
        print(f"❌ Falha ao postar Status via Selenium: {e}")
        return False
    finally:
        if driver:
            driver.quit()
            print("🔒 Navegador finalizado.")


def postar_status_via_api(video_path: Path, legenda: str, creds: dict) -> bool:
    """Envia o vídeo para o WhatsApp Status via endpoint REST (ex: Evolution API ou Z-API)."""
    import urllib.request
    import urllib.parse

    api_url = creds.get("api_url")
    token = creds.get("api_token")

    if not api_url or not token:
        print("❌ Credenciais de API do WhatsApp não configuradas.")
        print(f"   Configure: {CONFIG_FILE}")
        return False

    print(f"🚀 Enviando '{video_path.name}' para o WhatsApp Status via API...")
    # Exemplo genérico Evolution/Z-API para status@broadcast
    url = f"{api_url}/message/sendMediaStatus"
    payload = {
        "media": str(video_path.resolve()),
        "caption": legenda,
        "type": "video"
    }
    headers = {
        "apikey": token,
        "Content-Type": "application/json"
    }
    data = json.dumps(payload).encode("utf-8")
    req = urllib.request.Request(url, data=data, headers=headers, method="POST")

    try:
        with urllib.request.urlopen(req, timeout=60) as resp:
            resultado = json.loads(resp.read().decode("utf-8"))
            print(f"   🎉 Status postado com sucesso! Resposta: {resultado}")
            return True
    except Exception as e:
        print(f"   ❌ Erro ao enviar status via API: {e}")
        return False


def main():
    parser = argparse.ArgumentParser(description="Publicador de Shorts no WhatsApp Status")
    parser.add_argument("--simular", action="store_true", help="Audita arquivos, legendas e gera plano sem postar")
    parser.add_argument("--conectar", action="store_true", help="Abre o WhatsApp Web para você escanear o QR Code uma única vez")
    parser.add_argument("--postar-corte", type=int, default=None, help="Número do corte a ser postado no Status (1 a 14)")
    args = parser.parse_args()

    if not DEFAULT_JSON_METADADOS.exists():
        print(f"❌ Metadados não encontrados em: {DEFAULT_JSON_METADADOS}")
        sys.exit(1)

    metadados = carregar_metadados(DEFAULT_JSON_METADADOS)

    if args.conectar:
        conectar_whatsapp_web()
        return

    if args.simular or args.postar_corte is None:
        simular_whatsapp_status(metadados)
        return

    # Postagem real
    corte_num = args.postar_corte
    shorts_dir = DESKTOP_DIR / "05_SHORTS_APICE_45S"
    arquivos = sorted(list(shorts_dir.glob("*.mp4")))
    if corte_num < 1 or corte_num > len(arquivos):
        print(f"❌ Corte {corte_num} inválido. Escolha de 1 a {len(arquivos)}.")
        sys.exit(1)

    video_alvo = arquivos[corte_num - 1]
    cortes = {c.get("numero", i+1): c for i, c in enumerate(metadados.get("cortes_medios_tier2", []))}
    info_corte = cortes.get(corte_num, {})
    legenda = formatar_legenda_whatsapp_status(info_corte, corte_num)

    creds = carregar_credenciais()
    if creds.get("api_url"):
        postar_status_via_api(video_alvo, legenda, creds)
    else:
        print("📲 Nenhuma REST API configurada. Usando automação direta do WhatsApp Web com sua sessão salva...")
        postar_status_via_selenium(video_alvo, legenda)


if __name__ == "__main__":
    main()
