# -*- coding: utf-8 -*-
"""
🚀 ORQUESTRADOR SUPREMO DE CIBERSEGURANÇA & HACKING ÉTICO (LENOVO MASTER)
Coordena a clonagem e consolidação total de:
1. Google Drive (Cloud-to-Cloud): Hackone, Foco em SEC, Pentest Web, AI Cyber
2. Telegram (FoxHackers Supergrupo & Tópicos)
3. Telegram Catedral Hacker (-1003810610080 - 10 Tópicos Atômicos)
"""
import subprocess
import os
import sys
import json
import time

sys.stdout.reconfigure(encoding='utf-8', line_buffering=True)
sys.stderr.reconfigure(encoding='utf-8', line_buffering=True)

BASE_COMPUTACAO = r"c:\Users\matheus\Desktop\computacao"
BASE_TELEGRAM = r"C:\Users\matheus\Desktop\#COMPUTAÇÃO\TelegramDownloader"

def banner():
    print("=" * 75)
    print("🛡️  CENTRAL DE COMANDO SUPREMO DE CYBERSECURITY & HACKING (LENOVO)")
    print("🎯  MISSÃO: Consolidação Total de Cursos, Livros, Canais e Laboratórios")
    print("=" * 75)
    print("1. [DRIVE]    Finalizar Hackone + Cursos de Pentest e Forense")
    print("2. [TELEGRAM] Clonar Supergrupo FoxHackers com Tópicos")
    print("3. [TELEGRAM] Alimentar Catedral Hacker (-1003810610080)")
    print("4. [TUDO]     Executar Pipeline Completo Automatizado")
    print("=" * 75)

def executar_drive_cyber():
    print("\n☁️ [FASE 1] INICIANDO CLONAGEM DO GOOGLE DRIVE (CLOUD-TO-CLOUD)...")
    script = os.path.join(BASE_COMPUTACAO, "clonar_hackone_e_cyber.py")
    if os.path.exists(script):
        subprocess.run([sys.executable, script], cwd=BASE_COMPUTACAO)
    else:
        print(f"⚠️ Script não encontrado: {script}")

def executar_telegram_supergrupos():
    print("\n📡 [FASE 2] INICIANDO CLONAGEM DO SUPERGRUPO FOXHACKERS...")
    script = os.path.join(BASE_TELEGRAM, "clonar_supergrupos_completos.py")
    if os.path.exists(script):
        subprocess.run([sys.executable, script], cwd=BASE_TELEGRAM)
    else:
        print(f"⚠️ Script não encontrado: {script}")

def executar_varredura_hacker():
    print("\n🔍 [FASE 3] VARREDURA GLOBAL DE LIVROS, CURSOS E CANAIS DE HACKING...")
    script = os.path.join(BASE_COMPUTACAO, "varredura_hacker_telegram_global.py")
    if os.path.exists(script):
        subprocess.run([sys.executable, script], cwd=BASE_COMPUTACAO)
    else:
        print(f"⚠️ Script não encontrado: {script}")

def main():
    banner()
    if len(sys.argv) > 1:
        opcao = sys.argv[1]
    else:
        print("\nEscolha a operação:")
        print(" [1] Executar Tudo em Sequência (Recomendado)")
        print(" [2] Somente Google Drive Cyber")
        print(" [3] Somente Telegram FoxHackers & Catedrais")
        print(" [4] Somente Varredura & Catálogo de Livros/Canais")
        try:
            opcao = input("\n👉 Digite a opção (1-4) [Padrão: 1]: ").strip() or "1"
        except Exception:
            opcao = "1"

    if opcao == "1":
        print("\n🚀 Disparando Pipeline Completo de Cibersegurança...")
        executar_drive_cyber()
        executar_telegram_supergrupos()
        executar_varredura_hacker()
    elif opcao == "2":
        executar_drive_cyber()
    elif opcao == "3":
        executar_telegram_supergrupos()
    elif opcao == "4":
        executar_varredura_hacker()
    else:
        print("Opção inválida.")

    print("\n" + "=" * 75)
    print("🏆 PIPELINE DE CIBERSEGURANÇA FINALIZADO!")
    print("=" * 75)

if __name__ == "__main__":
    main()
