# -*- coding: utf-8 -*-
"""
🔍 VARREDURA DE ELITE: ACERVO HACKER & CIBERSEGURANÇA GLOBAL NO TELEGRAM
Varre todos os bancos de dados JSON, mapeamentos de canais e mensagens do Telegram
Classificando por categorias de Red Team, Blue Team, Forense, Malware e Livros.
"""
import os
import sys
import json
import glob
from datetime import datetime

sys.stdout.reconfigure(encoding='utf-8', errors='replace')
sys.stderr.reconfigure(encoding='utf-8', errors='replace')

BASE_DIR = r"C:\Users\matheus\Desktop\#COMPUTAÇÃO\TelegramDownloader"
PROJECT_DIR = r"c:\Users\matheus\Desktop\computacao"
OUTPUT_MD = os.path.join(PROJECT_DIR, "ACERVO_HACKER_TELEGRAM_CONSOLIDADO.md")
OUTPUT_JSON = os.path.join(BASE_DIR, "fila_hacker_catedral_telegram.json")

# Palavras-chave refinadas por categoria
CATEGORIAS_HACKER = {
    "red_team_e_pentest": [
        "pentest", "ethical hacking", "hackersec", "solyd", "hackone", "metasploit", 
        "nmap", "burp suite", "sqlmap", "owasp", "xss", "sqli", "exploit", "red team", 
        "bug bounty", "wireshark", "aircrack", "desec"
    ],
    "engenharia_reversa_e_malware": [
        "reverse engineering", "engenharia reversa", "malware", "ghidra", "ida pro", 
        "x64dbg", "assembly", "shellcode", "edr bypass", "rootkit", "c++", "sektor7"
    ],
    "active_directory_e_windows": [
        "active directory", "impacket", "bloodhound", "kerberos", "pass the hash", 
        "powershell", "mimikatz", "windows hacking", "ad security"
    ],
    "blue_team_soc_e_forense": [
        "blue team", "soc", "siem", "wazuh", "suricata", "zeek", "sigma", "forense", 
        "perícia", "volatility", "autopsy", "incident response", "dfir", "threat hunting"
    ],
    "hardware_hacking_e_iot": [
        "hardware hacking", "iot", "proxmark", "rfid", "nfc", "badusb", "rubber ducky", 
        "flipper zero", "sdr", "esp32", "arduino"
    ],
    "certificacoes_internacionais": [
        "security+", "pentest+", "ceh", "cissp", "oscp", "comptia", "isc2", "ccna security"
    ],
    "livros_e_manuais_pdf": [
        "pdf", "epub", "livro", "book", "manual", "guia", "cheatsheet"
    ]
}

def scan_all():
    print("=" * 70)
    print("🛡️ VARREDURA PROFUNDA DE CIBERSEGURANÇA & HACKING NO TELEGRAM")
    print("=" * 70)
    
    arquivos_json = glob.glob(os.path.join(BASE_DIR, "*.json"))
    print(f"📂 Analisando {len(arquivos_json)} bancos de dados de mensagens e canais...")
    
    resultados = {cat: [] for cat in CATEGORIAS_HACKER}
    titulos_vistos = set()
    total_encontrados = 0

    for jf in arquivos_json:
        nome_base = os.path.basename(jf)
        try:
            with open(jf, "r", encoding="utf-8") as f:
                data = json.load(f)
                
            def processar(obj):
                nonlocal total_encontrados
                if isinstance(obj, dict):
                    title = obj.get("title") or obj.get("titulo") or obj.get("nome") or ""
                    if isinstance(title, str) and title.strip():
                        t_clean = title.strip()
                        t_lower = t_clean.lower()
                        chave = t_lower[:65]
                        
                        if chave not in titulos_vistos:
                            item = {
                                "titulo": t_clean,
                                "origem": nome_base,
                                "id": obj.get("id"),
                                "tamanho_mb": obj.get("tamanho_mb"),
                                "tipo": obj.get("type") or obj.get("tipo"),
                                "link": obj.get("link") or obj.get("url") or obj.get("chat_link")
                            }
                            
                            enquadrado = False
                            for cat, kw_list in CATEGORIAS_HACKER.items():
                                if any(k in t_lower for k in kw_list):
                                    resultados[cat].append(item)
                                    titulos_vistos.add(chave)
                                    total_encontrados += 1
                                    enquadrado = True
                                    break
                                    
                elif isinstance(obj, list):
                    for elem in obj:
                        processar(elem)

            processar(data)
        except Exception:
            continue

    print(f"✅ Total de Ativos Únicos de Cibersegurança Encontrados: {total_encontrados}")
    
    # Salva JSON para alimentação automática da Catedral
    with open(OUTPUT_JSON, "w", encoding="utf-8") as f:
        json.dump(resultados, f, ensure_ascii=False, indent=2)
        
    # Gera Markdown formatado
    with open(OUTPUT_MD, "w", encoding="utf-8") as f:
        f.write("# 🛡️ ACERVO CONSOLIDADO DE HACKING & CIBERSEGURANÇA (TELEGRAM)\n\n")
        f.write(f"> **Última Atualização:** {datetime.now().strftime('%d/%m/%Y %H:%M:%S')}\n")
        f.write(f"> **Total de Ativos Mapeados:** {total_encontrados} materiais e cursos\n\n---\n\n")
        
        nomes_bonitos = {
            "red_team_e_pentest": "⚔️ 1. Red Team, Pentest & Web Security",
            "engenharia_reversa_e_malware": "🔬 2. Engenharia Reversa & Análise de Malware",
            "active_directory_e_windows": "🏢 3. Active Directory & Pentest Corporativo",
            "blue_team_soc_e_forense": "🛡️ 4. Blue Team, SOC, SIEM & Perícia Forense",
            "hardware_hacking_e_iot": "🔌 5. Hardware Hacking, IoT & RF",
            "certificacoes_internacionais": "🏆 6. Certificações Globais (CompTIA, CEH, OSCP)",
            "livros_e_manuais_pdf": "📚 7. Livros, Manuais & CheatSheets"
        }
        
        for cat, itens in resultados.items():
            f.write(f"## {nomes_bonitos.get(cat, cat)} ({len(itens)} itens)\n\n")
            if not itens:
                f.write("*Nenhum item específico nesta categoria ainda.*\n\n")
            for it in itens[:40]: # Top 40 por categoria
                sz = f" ({it['tamanho_mb']:.1f} MB)" if it.get('tamanho_mb') else ""
                lnk = f" | [Acessar Link]({it['link']})" if it.get('link') else ""
                f.write(f"* **{it['titulo']}**{sz}{lnk}\n")
            f.write("\n---\n\n")
            
    print(f"📝 Catálogo gerado com sucesso em: {OUTPUT_MD}")

if __name__ == "__main__":
    scan_all()
