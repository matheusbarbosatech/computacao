import os
import sys
import time
from pathlib import Path
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

BASE_DIR = Path(__file__).resolve().parent.parent.parent
SESSION_DIR = BASE_DIR / "data" / "whatsapp_session"
DESKTOP_DIR = Path.home() / "Desktop" / "cortes_audio_culto_459_20_09_2026"
SHORTS_DIR = DESKTOP_DIR / "05_SHORTS_APICE_45S"
DEBUG_DIR = BASE_DIR / "data" / "debug_status"
DEBUG_DIR.mkdir(parents=True, exist_ok=True)

video = BASE_DIR / "data" / "status_teste_compactado.mp4"
print(f"Vídeo de teste (comprimido < 10MB): {video.name} ({video.stat().st_size / (1024*1024):.2f} MB)")

options = Options()
options.add_argument(f"--user-data-dir={SESSION_DIR.resolve()}")
options.add_argument("--no-sandbox")
options.add_argument("--disable-dev-shm-usage")
options.add_argument("--window-size=1280,900")
# Não minimizar para permitir o Chrome renderizar o canvas/video
options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36")

driver = webdriver.Chrome(options=options)
try:
    print("Navegando para o WhatsApp Web...")
    driver.get("https://web.whatsapp.com")
    
    wait = WebDriverWait(driver, 45)
    wait.until(EC.presence_of_element_located((By.XPATH, "//*[@id='pane-side'] | //button[@aria-label='Status']")))
    print("WhatsApp Web carregado!")
    time.sleep(3)

    # 1. Clicar no ícone de Status
    print("Clicando no botão de Status...")
    status_btn = wait.until(EC.element_to_be_clickable((By.XPATH, "//button[@aria-label='Status'] | //span[@data-icon='status-v3-unread' or @data-icon='status-v3']/ancestor::button")))
    status_btn.click()
    time.sleep(3)
    driver.save_screenshot(str(DEBUG_DIR / "01_status_tab.png"))

    # 2. Clicar no botão 'Foto e vídeo'
    print("Procurando botão 'Foto e vídeo'...")
    botoes = driver.find_elements(By.XPATH, "//button[contains(., 'Foto e v') or contains(., 'Foto')] | //div[@role='button' and contains(., 'Foto')]")
    if not botoes:
        # tentar achar o botão '+' ou câmera
        botoes = driver.find_elements(By.XPATH, "//button[contains(@aria-label, 'status') or contains(@aria-label, 'Status')]")
    
    alvo = None
    for b in botoes:
        if "foto" in b.text.lower():
            alvo = b
            break
    if not alvo and botoes:
        alvo = botoes[0]

    print(f"Clicando no botão: {alvo.text if alvo else 'Nenhum'}")
    if alvo:
        driver.execute_script("arguments[0].click();", alvo)
        time.sleep(2)
    driver.save_screenshot(str(DEBUG_DIR / "02_after_click_photo.png"))

    # 3. Localizar input[type='file']
    inputs = driver.find_elements(By.XPATH, "//input[@type='file']")
    print(f"Inputs encontrados: {len(inputs)}")
    for i, inp in enumerate(inputs):
        print(f"Input {i}: accept={inp.get_attribute('accept')}")

    if inputs:
        inp = inputs[0]
        print(f"Injetando vídeo: {video.resolve()}")
        inp.send_keys(str(video.resolve()))
        time.sleep(5)
        driver.save_screenshot(str(DEBUG_DIR / "03_after_send_keys.png"))

        # Inspecionar elementos na tela após anexar
        print("--- ELEMENTOS NA TELA ---")
        icons = driver.find_elements(By.XPATH, "//*[@data-icon]")
        for ic in icons:
            icon_name = ic.get_attribute("data-icon")
            tag = ic.find_element(By.XPATH, "..").tag_name
            print(f"Icon: {icon_name} (Parent: {tag})")

        buttons = driver.find_elements(By.XPATH, "//button | //div[@role='button']")
        for b in buttons:
            aria = b.get_attribute("aria-label") or ""
            txt = b.text.strip()
            if aria or txt:
                print(f"Button: text='{txt}' aria='{aria}'")

        contenteditables = driver.find_elements(By.XPATH, "//*[@contenteditable='true']")
        print(f"Contenteditables: {len(contenteditables)}")

        # Verificar se apareceu o botão de enviar (send)
        send_candidates = driver.find_elements(By.XPATH, "//*[@data-icon='send']/ancestor::*[@role='button' or self::button] | //span[@data-icon='send-inverted']/ancestor::*[@role='button' or self::button] | //div[@aria-label='Enviar' or @aria-label='Send']")
        print(f"Send candidates: {len(send_candidates)}")
        if send_candidates:
            print("Botão de envio encontrado! Clicando no envio do Status...")
            driver.execute_script("arguments[0].click();", send_candidates[0])
            print("Clicado no botão de envio! Aguardando 15 segundos para upload...")
            time.sleep(15)
            driver.save_screenshot(str(DEBUG_DIR / "04_after_send_click.png"))
            print("Upload finalizado!")
        else:
            print("Botão de envio NÃO encontrado após send_keys.")

except Exception as e:
    print(f"Erro: {e}")
    driver.save_screenshot(str(DEBUG_DIR / "error.png"))
finally:
    driver.quit()
