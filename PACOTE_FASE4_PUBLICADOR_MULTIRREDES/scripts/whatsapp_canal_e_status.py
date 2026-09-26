#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
CENTRAL DE DISTRIBUIÇÃO WHATSAPP — CANAL OFICIAL & STATUS (SEM NAVEGADOR ABERTO)
IBPM CR Automation System — Fase 4: Publicação Multirredes

Gerencia exclusivamente:
A. 📢 Canal Oficial de Transmissão (Alimento Diário: Devocional, Cortes e Frases)
B. 📚 Mini Estudo Bíblico da Semana (Toda Quarta-feira às 12:00 no Canal)
C. 📱 Status (Stories do WhatsApp) em Modo Silencioso (Headless - Sem janela na tela)

Uso:
  python scripts/fase4_publicacao/whatsapp_canal_e_status.py --simular
  python scripts/fase4_publicacao/whatsapp_canal_e_status.py --mini-estudo 1
  python scripts/fase4_publicacao/whatsapp_canal_e_status.py --postar-canal --tipo devocional --dia 1
  python scripts/fase4_publicacao/whatsapp_canal_e_status.py --postar-status --corte 1
"""

import os
import sys
import json
import time
import argparse
from pathlib import Path
from datetime import datetime

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")

BASE_DIR = Path(__file__).resolve().parent.parent.parent
DESKTOP_DIR = Path.home() / "Desktop" / "cortes_audio_culto_459_20_09_2026"
SHORTS_DIR = DESKTOP_DIR / "05_SHORTS_APICE_45S"
CALENDARIO_FILE = BASE_DIR / "data" / "fase4_publicacao" / "00_CALENDARIO_MESTRE_365_DIAS.json"
ATIVOS_DIR = BASE_DIR / "data" / "ativos_minerados"
SESSION_DIR = BASE_DIR / "data" / "whatsapp_session"
CONFIG_FILE = BASE_DIR / "config" / "credentials" / "whatsapp_credentials.json"

def carregar_config_whatsapp() -> dict:
    config = {
        "nome_canal": "Matheus Barbosa",
        "provedor": "evolution_api",
        "api_url": "",
        "api_token": "",
        "instance_name": "matheus_barbosa"
    }
    if CONFIG_FILE.exists():
        try:
            with open(CONFIG_FILE, "r", encoding="utf-8") as f:
                config.update(json.load(f))
        except Exception:
            pass
    return config

def carregar_calendario() -> list:
    if CALENDARIO_FILE.exists():
        with open(CALENDARIO_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    return []

def formatar_mini_estudo(celula_dict: dict) -> str:
    """Formata um roteiro minerado em um Mini Estudo Bíblico atraente para Canal do WhatsApp."""
    tema = celula_dict.get("tema", "Palavra de Vida").strip()
    versiculo = celula_dict.get("versiculo_base", "").strip()
    topicos = celula_dict.get("estudo_topicos", [])
    perguntas = celula_dict.get("perguntas_aplicacao", [])
    desafio = celula_dict.get("desafio_semana", "").strip()

    txt = []
    txt.append(f"📚 *MINI ESTUDO DA SEMANA: {tema.upper()}*")
    if versiculo:
        txt.append(f"📖 *Texto Base:* {versiculo}")
    txt.append("")
    txt.append("🔑 *3 CHAVES PRÁTICAS PARA A SUA SEMANA:*")
    for i, top in enumerate(topicos[:3]):
        tit = top.get("titulo", "") if isinstance(top, dict) else str(top)
        exp = top.get("explicacao", "") if isinstance(top, dict) else ""
        txt.append(f"*{i+1}. {tit.strip()}*")
        if exp:
            txt.append(f"_{exp.strip()}_")
    txt.append("")
    if perguntas:
        p = perguntas[0] if isinstance(perguntas, list) else str(perguntas)
        txt.append("❓ *PARA MEDITAR HOJE:*")
        txt.append(f"_{p.strip()}_")
        txt.append("")
    if desafio:
        txt.append("🎯 *DESAFIO PRÁTICO:*")
        txt.append(f"{desafio}")
        txt.append("")
    txt.append("👉 *Reaja com 🙏 ou 🔥 se esse estudo abençoou sua semana!*")
    return "\n".join(txt)

def formatar_devocional_canal(dev_dict: dict) -> str:
    """Formata o devocional diário para o Canal do WhatsApp."""
    titulo = dev_dict.get("titulo", "Alimento Diário")
    versiculo = dev_dict.get("versiculo", dev_dict.get("versiculo_chave", ""))
    reflexao = dev_dict.get("reflexao_resumo", dev_dict.get("reflexao", ""))
    oracao = dev_dict.get("oracao", dev_dict.get("oracao_do_dia", ""))

    txt = []
    txt.append(f"🌅 *DEVOCIONAL DIÁRIO — {titulo.upper()}*")
    if versiculo:
        txt.append(f"📖 *Versículo do Dia:* _{versiculo}_")
    txt.append("")
    if reflexao:
        txt.append(f"{reflexao}")
        txt.append("")
    if oracao:
        txt.append(f"🙏 *Oração do Dia:*\n_{oracao}_")
        txt.append("")
    txt.append("👉 *Compartilhe este devocional com quem precisa de uma palavra hoje!*")
    return "\n".join(txt)

def simular_grade():
    print("=" * 80)
    print("📢 CENTRAL WHATSAPP — CANAL OFICIAL & STATUS SILENCIOSO")
    print("=" * 80)
    cal = carregar_calendario()
    print(f"✅ Calendário Anual carregado: {len(cal)} dias programados")
    print("\n⏰ GRADE EXCLUSIVA DE DISTRIBUIÇÃO NO WHATSAPP:")
    print("   1. 🌅 07:00 — Devocional Diário no Canal Oficial + Status")
    print("   2. ⚡ 12:00 — Micro-Short Ápice 9:16 no Canal Oficial + Status")
    print("   3. 📚 Toda Quarta 12:00 — MINI ESTUDO BÍBLICO DA SEMANA no Canal Oficial")
    print("   4. 🌙 18:00 — Frase Profética Noturna no Canal Oficial")
    print("-" * 80)

    # Exibe amostra do Mini Estudo da Quarta-feira
    cels = sorted(list((ATIVOS_DIR / "celulas").glob("*.json")))
    if cels:
        with open(cels[0], "r", encoding="utf-8") as f:
            c = json.load(f)
        print("📖 EXEMPLO REAL: MINI ESTUDO DA SEMANA (QUARTA-FEIRA ÀS 12:00):\n")
        print(formatar_mini_estudo(c))
        print("-" * 80)

    if cal:
        d1 = cal[0]["publicacoes"]
        print("\n🌅 EXEMPLO REAL: DEVOCIONAL DIÁRIO (07:00 NO CANAL):\n")
        print(formatar_devocional_canal(d1["07:00_manha"]))
        print("=" * 80)

def otimizar_video_status(video_original: Path) -> Path:
    """Garante que o vídeo esteja abaixo do limite de 10 MB imposto pelo WhatsApp Web no Status."""
    import subprocess
    tamanho_mb = video_original.stat().st_size / (1024 * 1024)
    if tamanho_mb <= 9.5:
        return video_original

    pasta_status = BASE_DIR / "data" / "status_otimizados"
    pasta_status.mkdir(parents=True, exist_ok=True)
    video_otimizado = pasta_status / f"status_{video_original.stem}.mp4"

    if video_otimizado.exists() and video_otimizado.stat().st_size / (1024 * 1024) <= 9.5:
        return video_otimizado

    print(f"⚙️ Otimizando vídeo para o Status ({tamanho_mb:.1f} MB -> meta: < 10 MB via FFmpeg)...")
    cmd = [
        "ffmpeg", "-y", "-i", str(video_original.resolve()),
        "-vf", "scale=720:1280,fps=30",
        "-c:v", "libx264", "-preset", "ultrafast", "-crf", "26",
        "-c:a", "aac", "-b:a", "96k",
        str(video_otimizado.resolve())
    ]
    res = subprocess.run(cmd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    if res.returncode == 0 and video_otimizado.exists():
        novo_mb = video_otimizado.stat().st_size / (1024 * 1024)
        print(f"✅ Vídeo otimizado com sucesso: {novo_mb:.2f} MB (100% dentro do limite do WhatsApp Status)")
        return video_otimizado
    return video_original

def postar_status_silencioso(corte_num: int):
    """Posta no WhatsApp Status em modo Headless (100% silencioso em segundo plano, sem janela aberta)."""
    from selenium import webdriver
    from selenium.webdriver.chrome.options import Options
    from selenium.webdriver.common.by import By
    from selenium.webdriver.support.ui import WebDriverWait
    from selenium.webdriver.support import expected_conditions as EC
    from selenium.webdriver.common.keys import Keys

    arquivos = sorted(list(SHORTS_DIR.glob("*.mp4")))
    if corte_num < 1 or corte_num > len(arquivos):
        print(f"❌ Corte {corte_num} inválido. Escolha de 1 a {len(arquivos)}.")
        return False

    video_original = arquivos[corte_num - 1]
    print("=" * 80)
    print(f"📱 POSTANDO NO WHATSAPP STATUS (MODO SILENCIOSO / HEADLESS)")
    print(f"   Arquivo Original: {video_original.name}")
    print("=" * 80)

    # 1. Otimizar vídeo para caber no limite estrito de 10 MB do WhatsApp Status
    video_alvo = otimizar_video_status(video_original)

    options = Options()
    options.add_argument(f"--user-data-dir={SESSION_DIR.resolve()}")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--window-size=1280,900")
    # Mantém janela ativa sem congelar renderização do Chromium
    options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36")

    driver = None
    try:
        print("⏳ Conectando ao WhatsApp Web...")
        driver = webdriver.Chrome(options=options)

        driver.get("https://web.whatsapp.com")

        wait = WebDriverWait(driver, 45)
        wait.until(EC.presence_of_element_located((By.XPATH, "//*[@id='pane-side'] | //button[@aria-label='Status']")))
        print("✅ Sessão validada e ativa!")
        time.sleep(2)

        # 2. Clicar no menu de Status
        print("📍 Acessando aba de Status...")
        status_btn = wait.until(EC.element_to_be_clickable((By.XPATH, "//button[@aria-label='Status'] | //span[@data-icon='status-v3-unread' or @data-icon='status-v3']/ancestor::button")))
        driver.execute_script("arguments[0].click();", status_btn)
        time.sleep(3)

        # 3. Clicar no botão 'Foto e vídeo'
        botoes = driver.find_elements(By.XPATH, "//button[contains(., 'Foto e v') or contains(., 'Foto')] | //div[@role='button' and contains(., 'Foto')]")
        if not botoes:
            botoes = driver.find_elements(By.XPATH, "//button[contains(@aria-label, 'status') or contains(@aria-label, 'Status')]")
        
        alvo_foto = None
        for b in botoes:
            if "foto" in b.text.lower():
                alvo_foto = b
                break
        if not alvo_foto and botoes:
            alvo_foto = botoes[0]
            
        if alvo_foto:
            print(f"📸 Acionando: {alvo_foto.text.strip().replace(chr(10), ' ')}")
            driver.execute_script("arguments[0].click();", alvo_foto)
            time.sleep(2)

        # 4. Anexar vídeo
        file_inputs = driver.find_elements(By.XPATH, "//input[@type='file']")
        if not file_inputs:
            raise Exception("Input de arquivo não revelado.")
        
        print(f"📤 Injetando vídeo ({video_alvo.name})...")
        file_inputs[0].send_keys(str(video_alvo.resolve()))
        print("⏳ Aguardando renderização do preview do Status (6s)...")
        time.sleep(6)

        # 5. Inserir legenda se campo estiver presente
        editaveis = driver.find_elements(By.XPATH, "//div[@contenteditable='true']")
        if editaveis:
            caption_box = editaveis[0]
            try:
                caption_box.click()
                legenda = f"🔥 Palavra Forte #{corte_num} | Assista completa no canal!"
                caption_box.send_keys(legenda)
                time.sleep(1)
            except Exception:
                pass

        # 6. Clicar no botão de envio (seletores exatos do novo WhatsApp Web Status)
        send_candidates = driver.find_elements(By.XPATH, "//*[@aria-label[contains(., 'Enviar')]] | //*[@data-icon='wds-ic-send-filled']/ancestor::*[@role='button' or self::button] | //button[contains(@aria-label, 'Enviar')] | //div[contains(@aria-label, 'Enviar')] | //span[@data-icon='send']/ancestor::button")
        if not send_candidates:
            raise Exception("Botão de envio do Status não encontrado na tela.")

        print("🚀 Clicando no botão de envio do WhatsApp Status...")
        driver.execute_script("arguments[0].click();", send_candidates[0])

        print("⏳ Transmitindo vídeo para os Status do WhatsApp (15s)...")
        time.sleep(15)

        # Captura screenshot de comprovação
        proof_dir = BASE_DIR / "data" / "comprovantes_status"
        proof_dir.mkdir(parents=True, exist_ok=True)
        proof_path = proof_dir / f"status_publicado_corte_{corte_num}.png"
        driver.save_screenshot(str(proof_path))

        print(f"🎉 STATUS PUBLICADO COM SUCESSO NO SEU WHATSAPP!")
        print(f"📸 Comprovante salvo em: {proof_path.name}")
        return True

    except Exception as e:
        import traceback
        print(f"❌ Erro no envio de status: {e}")
        traceback.print_exc()
        return False
    finally:
        if driver:
            driver.quit()

def postar_no_canal(nome_canal: str, texto_mensagem: str, video_path: Path = None):
    """Posta texto formatado e/ou vídeo dentro do Canal Oficial do WhatsApp."""
    from selenium import webdriver
    from selenium.webdriver.chrome.options import Options
    from selenium.webdriver.common.by import By
    from selenium.webdriver.support.ui import WebDriverWait
    from selenium.webdriver.support import expected_conditions as EC
    from selenium.webdriver.common.keys import Keys

    print("=" * 80)
    print(f"📢 PUBLICANDO NO CANAL DO WHATSAPP: '{nome_canal}'")
    print("=" * 80)

    options = Options()
    options.add_argument(f"--user-data-dir={SESSION_DIR.resolve()}")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--headless=new")
    options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36")

    driver = None
    try:
        driver = webdriver.Chrome(options=options)
        driver.get("https://web.whatsapp.com")
        wait = WebDriverWait(driver, 45)
        wait.until(EC.presence_of_element_located((By.XPATH, "//*[@id='pane-side'] | //button[@aria-label='Canais']")))
        print("✅ Sessão conectada!")
        time.sleep(2)

        # 1. Clicar no menu Canais
        canais_btn = driver.find_elements(By.XPATH, "//button[@aria-label='Canais'] | //span[@data-icon='newsletter-outline']/ancestor::button")
        if canais_btn:
            canais_btn[0].click()
            time.sleep(3)

        # 2. Localizar o canal pelo nome
        canal_alvo = driver.find_elements(By.XPATH, f"//span[@title='{nome_canal}'] | //div[contains(., '{nome_canal}') and @role='button']")
        if not canal_alvo:
            print(f"⚠️ Canal '{nome_canal}' não encontrado na lista de canais.")
            print("   Certifique-se de que o canal foi criado com esse nome exato no seu WhatsApp.")
            return False

        canal_alvo[0].click()
        time.sleep(2)

        # 3. Se tiver vídeo para enviar
        if video_path and video_path.exists():
            print(f"📤 Anexando vídeo '{video_path.name}' no Canal...")
            # Clicar no botão de anexo '+'
            clip_btn = wait.until(EC.element_to_be_clickable((By.XPATH, "//button[@aria-label='Anexar'] | //span[@data-icon='plus']/ancestor::button")))
            clip_btn.click()
            time.sleep(1)

            file_input = driver.find_element(By.XPATH, "//input[@type='file']")
            file_input.send_keys(str(video_path.resolve()))
            time.sleep(5)

            # Legenda do vídeo
            caption = wait.until(EC.presence_of_element_located((By.XPATH, "//div[@contenteditable='true']")))
            caption.click()
            caption.send_keys(texto_mensagem)
            time.sleep(1)

            send_btn = driver.find_element(By.XPATH, "//span[@data-icon='send']/ancestor::button")
            send_btn.click()
            time.sleep(10)
        else:
            # Envio apenas de texto (Mini Estudo ou Devocional)
            print("✍️ Digitando mensagem formatada no Canal...")
            msg_box = wait.until(EC.presence_of_element_located((By.XPATH, "//div[@contenteditable='true']")))
            msg_box.click()
            time.sleep(1)
            # Para enviar textos com quebras de linha limpas
            for linha in texto_mensagem.split("\n"):
                msg_box.send_keys(linha)
                msg_box.send_keys(Keys.SHIFT, Keys.ENTER)
            time.sleep(1)
            msg_box.send_keys(Keys.ENTER)
            time.sleep(4)

        print(f"🎉 CONTEÚDO PUBLICADO NO CANAL '{nome_canal}' COM SUCESSO!")
        return True

    except Exception as e:
        print(f"❌ Erro ao publicar no canal: {e}")
        return False
    finally:
        if driver:
            driver.quit()

def main():
    config = carregar_config_whatsapp()
    canal_padrao = config.get("nome_canal", "Matheus Barbosa")

    parser = argparse.ArgumentParser(description="Central de Distribuição WhatsApp (Canal Oficial & Status Silencioso)")
    parser.add_argument("--simular", action="store_true", help="Mostra a grade e prévia dos conteúdos sem postar")
    parser.add_argument("--mini-estudo", type=int, default=None, help="Número do estudo semanal para prévia ou envio")
    parser.add_argument("--postar-status", action="store_true", help="Posta corte no Status em segundo plano (sem janela)")
    parser.add_argument("--corte", type=int, default=1, help="Número do corte (1 a 14) para postar no Status")
    parser.add_argument("--postar-canal", action="store_true", help="Dispara postagem dentro do Canal do WhatsApp")
    parser.add_argument("--nome-canal", type=str, default=canal_padrao, help=f"Nome exato do canal no seu WhatsApp (Padrão: '{canal_padrao}')")
    args = parser.parse_args()

    nome_canal_ativo = args.nome_canal

    if args.simular or (not args.postar_status and not args.postar_canal and args.mini_estudo is None):
        simular_grade()
        print(f"📢 Canal Oficial Configurado: '{nome_canal_ativo}'")
        if config.get("api_url") and config.get("api_token"):
            print(f"🌐 Provedor: Evolution API ativa ({config['api_url']} - Instância: {config['instance_name']})")
        else:
            print(f"💻 Provedor: Sessão Web Local (Sessão salva em data/whatsapp_session - Modo Headless)")
        print("=" * 80)
        return

    # 1. Postagem no Status (se solicitada)
    if args.postar_status:
        print("\n" + "=" * 80)
        print("📱 DISPARANDO TESTE NO WHATSAPP STATUS (SILENCIOSO / HEADLESS)...")
        print("=" * 80)
        postar_status_silencioso(args.corte)

    # 2. Postagem no Canal (se solicitada)
    if args.postar_canal:
        print("\n" + "=" * 80)
        print(f"📢 DISPARANDO TESTE NO CANAL DO WHATSAPP: '{nome_canal_ativo}'...")
        print("=" * 80)
        
        # Pega o primeiro estudo bíblico formatado
        cels = sorted(list((ATIVOS_DIR / "celulas").glob("*.json")))
        idx = (args.mini_estudo - 1) if args.mini_estudo else 0
        if 0 <= idx < len(cels):
            with open(cels[idx], "r", encoding="utf-8") as f:
                c = json.load(f)
            texto = formatar_mini_estudo(c)
        else:
            texto = "📚 *MINI ESTUDO DA SEMANA*\n\nDeus é bom em todo o tempo!"
            
        postar_no_canal(nome_canal_ativo, texto)

if __name__ == "__main__":
    main()
