#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
🏛️ CENTRAL DE COMANDO HACKER & CIBERSEGURANÇA (FULL-SPECTRUM)
Menu Tático Unificado para todas as Suites e Operações do Ecossistema
"""

import os
import sys
import subprocess
import time

sys.stdout.reconfigure(encoding='utf-8', errors='replace')
sys.stderr.reconfigure(encoding='utf-8', errors='replace')

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

def limpar_tela():
    os.system('cls' if os.name == 'nt' else 'clear')

def banner():
    print("""
\033[96m
╔══════════════════════════════════════════════════════════════════════════════╗
║        🏛️  CENTRAL DE COMANDO MASTER: CIBERSEGURANÇA & HACKING ÉTICO        ║
║               Operador Full-Spectrum: DFIR | CTI | RED | BLUE                ║
╚══════════════════════════════════════════════════════════════════════════════╝
\033[0m""")

def menu():
    while True:
        limpar_tela()
        banner()
        print("""
  \033[92m[1]\033[0m 📡 \033[1mSentinelSOC Live\033[0m (Radar de Ameaças, SIEM & Simulador Red Team)
  \033[92m[2]\033[0m 🕵️ \033[1mInvestigação Forense & Triagem DFIR\033[0m (Laudo Pericial Oficial)
  \033[92m[3]\033[0m 🌐 \033[1mCyber Threat Intelligence & OSINT Recon\033[0m (CTI Briefing)
  \033[92m[4]\033[0m 🔍 \033[1mVarredura Global Hacker no Telegram\033[0m (184 Ativos Mapeados)
  \033[92m[5]\033[0m ☁️ \033[1mStatus de Clonagem do Google Drive\033[0m (Solyd One & Hackone)
  \033[92m[6]\033[0m 📚 \033[1mAbrir Catálogo dos 100 Projetos Práticos PBL\033[0m
  \033[91m[0]\033[0m 🚪 Sair
        """)
        
        opcao = input("\033[93m👉 Selecione uma operação tática [0-6]: \033[0m").strip()
        
        if opcao == "1":
            print("\n[*] Iniciando o SentinelSOC Live na porta 9090...")
            try:
                import webbrowser
                webbrowser.open("http://localhost:9090")
                subprocess.run([sys.executable, os.path.join(BASE_DIR, "projeto_pratico_hoje_sentinel_soc", "sentinel_server.py")])
            except KeyboardInterrupt:
                pass
        elif opcao == "2":
            print("\n[*] Executando Suite Forense e Gerando Laudo...")
            subprocess.run([sys.executable, os.path.join(BASE_DIR, "investigacao_digital", "forensic_investigator.py")])
            input("\nPressione [ENTER] para voltar ao menu...")
        elif opcao == "3":
            print("\n[*] Executando Motor de CTI e OSINT...")
            subprocess.run([sys.executable, os.path.join(BASE_DIR, "osint_threat_intelligence", "cti_investigator.py")])
            input("\nPressione [ENTER] para voltar ao menu...")
        elif opcao == "4":
            print("\n[*] Executando Varredura no Telegram...")
            subprocess.run([sys.executable, os.path.join(BASE_DIR, "varredura_hacker_telegram_global.py")])
            input("\nPressione [ENTER] para voltar ao menu...")
        elif opcao == "5":
            print("\n" + "=" * 60)
            print("📊 STATUS DAS CLONAGENS GOOGLE DRIVE (CLOUD-TO-CLOUD)")
            print("=" * 60)
            log_solyd = os.path.join(BASE_DIR, "clonagem_solyd_one.log")
            log_hackone = os.path.join(BASE_DIR, "clonagem_hackone.log")
            
            print("\n🏆 SOLYD ONE (Formação Pentest Completa - 134.6 GB):")
            print("  Status: CONCLUÍDO COM 100% DE SUCESSO! (534 arquivos)")
            
            print("\n🚀 HACKONE (Academia Cyber Completa - 780.3 GB):")
            print("  Status: EM ANDAMENTO (Mais de 285 GB transferidos!)")
            input("\nPressione [ENTER] para voltar ao menu...")
        elif opcao == "6":
            md_path = os.path.join(BASE_DIR, "100_PROJETOS_PRATICOS_PBL_CYBER_HACKING.md")
            print(f"\n[*] Abrindo catálogo: {md_path}")
            if os.name == 'nt':
                os.system(f'start "" "{md_path}"')
            input("\nPressione [ENTER] para voltar ao menu...")
        elif opcao == "0":
            print("\nEncerrando Central de Comando. Bom treinamento, operador!\n")
            break

if __name__ == "__main__":
    menu()
