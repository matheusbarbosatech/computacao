# -*- coding: utf-8 -*-
"""
Gerador do Manual Executável em PDF para o PC Lenovo
Gera um documento PDF diagramado com todos os comandos, códigos e instruções de clonagem.
"""
import os
import sys
from fpdf import FPDF

BASE_DIR = r"c:\Users\matheus\Desktop\computacao"
PDF_OUTPUT = os.path.join(BASE_DIR, "MANUAL_EXECUTAVEL_LENOVO_CLONES_CYBER_E_AREAS.pdf")

# Cores do Layout
C_PRIMARY = (15, 23, 42)      # Azul Escuro Profundo (Slate 900)
C_ACCENT = (14, 165, 233)     # Ciano / Sky 500
C_CYBER = (16, 185, 129)      # Verde Esmeralda / Hacker
C_BG_CARD = (248, 250, 252)   # Cinza Claro Suave
C_BORDER = (226, 232, 240)    # Borda Suave
C_TEXT = (51, 65, 85)         # Texto Escuro (Slate 700)
C_CODE_BG = (241, 245, 249)   # Fundo de Bloco de Código

def sanitize(text):
    """Substitui caracteres fora do latin-1/standard para o fpdf2 core font"""
    if not isinstance(text, str):
        text = str(text)
    replacements = {
        "–": "-", "—": "-", "“": '"', "”": '"', "‘": "'", "’": "'",
        "•": "*", "🛡": "[CYBER]", "🚀": "[EXEC]", "☁": "[DRIVE]",
        "📡": "[TELEGRAM]", "🏛": "[CATEDRAL]", "✅": "[OK]", "⚡": "[FAST]",
        "⏸": "[PAUSE]", "🧠": "[INFO]", "💻": "[PC]", "📁": "[DIR]",
        "🔑": "[KEY]", "🎯": "[ALVO]", "💡": "[DICA]", "📌": "[NOTA]",
        "🏆": "[CONCLUIDO]", "📊": "[STATUS]", "🗺": "[MAPA]"
    }
    for k, v in replacements.items():
        text = text.replace(k, v)
    return text.encode('latin-1', 'replace').decode('latin-1')

class PDFManual(FPDF):
    def header(self):
        if self.page_no() > 1:
            self.set_font('Helvetica', 'B', 8)
            self.set_text_color(100, 116, 139)
            self.cell(0, 8, sanitize("CENTRAL DE COMANDO LENOVO - MANUAL DE CLONAGEM CYBER & ECOSSISTEMA"), 0, 0, 'L')
            self.set_font('Helvetica', '', 8)
            self.cell(0, 8, sanitize(f"Pagina {self.page_no()}"), 0, 1, 'R')
            self.set_draw_color(*C_BORDER)
            self.line(10, 15, 200, 15)
            self.ln(4)

    def footer(self):
        self.set_y(-12)
        self.set_font('Helvetica', 'I', 8)
        self.set_text_color(148, 163, 184)
        self.cell(0, 8, sanitize("Google Antigravity IDE | Workspace: matheusbarbosatech/computacao | Cota 750GB/Dia"), 0, 0, 'C')

    def chapter_title(self, title, tag=""):
        self.ln(3)
        self.set_fill_color(*C_PRIMARY)
        self.set_text_color(255, 255, 255)
        self.set_font('Helvetica', 'B', 11)
        self.cell(0, 8, f"  {sanitize(title)} {sanitize(tag)}", 0, 1, 'L', True)
        self.ln(2)

    def sub_title(self, title):
        self.set_font('Helvetica', 'B', 9.5)
        self.set_text_color(*C_PRIMARY)
        self.cell(0, 6, sanitize(title), 0, 1, 'L')
        self.ln(1)

    def body_p(self, text):
        self.set_font('Helvetica', '', 8.5)
        self.set_text_color(*C_TEXT)
        self.multi_cell(0, 4.2, sanitize(text))
        self.ln(1.5)

    def code_block(self, code_text):
        self.set_fill_color(*C_CODE_BG)
        self.set_draw_color(*C_BORDER)
        self.set_font('Courier', '', 7.5)
        self.set_text_color(15, 23, 42)
        
        # split lines and render inside border
        lines = code_text.strip().split('\n')
        h_total = len(lines) * 3.8 + 4
        
        # Check if page break is needed
        if self.get_y() + h_total > 275:
            self.add_page()
            
        cur_y = self.get_y()
        self.rect(10, cur_y, 190, h_total, 'DF')
        self.set_xy(12, cur_y + 2)
        for line in lines:
            self.cell(186, 3.8, sanitize(line), 0, 1, 'L')
            self.set_x(12)
        self.set_y(cur_y + h_total + 2)

    def info_card(self, title, items, color_border=C_ACCENT):
        if self.get_y() + 25 > 275:
            self.add_page()
        cur_y = self.get_y()
        h_est = len(items) * 4.2 + 8
        self.set_fill_color(*C_BG_CARD)
        self.set_draw_color(*color_border)
        self.set_line_width(0.5)
        self.rect(10, cur_y, 190, h_est, 'DF')
        
        # Title pill
        self.set_xy(12, cur_y + 2)
        self.set_font('Helvetica', 'B', 8.5)
        self.set_text_color(*C_PRIMARY)
        self.cell(0, 4.5, sanitize(f">> {title}"), 0, 1, 'L')
        
        self.set_font('Helvetica', '', 8)
        self.set_text_color(*C_TEXT)
        for it in items:
            self.set_x(14)
            self.cell(0, 4, sanitize(f"* {it}"), 0, 1, 'L')
        self.set_y(cur_y + h_est + 2)

def gerar_pdf():
    pdf = PDFManual(orientation='P', unit='mm', format='A4')
    pdf.set_auto_page_break(auto=True, margin=15)
    
    # -------------------------------------------------------------
    # PÁGINA 1: CAPA & SUMÁRIO EXECUTIVO
    # -------------------------------------------------------------
    pdf.add_page()
    
    # Cabeçalho da Capa
    pdf.set_fill_color(*C_PRIMARY)
    pdf.rect(10, 10, 190, 36, 'F')
    
    pdf.set_xy(15, 14)
    pdf.set_font('Helvetica', 'B', 16)
    pdf.set_text_color(255, 255, 255)
    pdf.cell(0, 8, sanitize("MANUAL MESTRE DE CLONAGEM & OPERACOES"), 0, 1, 'L')
    
    pdf.set_xy(15, 23)
    pdf.set_font('Helvetica', 'B', 10)
    pdf.set_text_color(*C_ACCENT)
    pdf.cell(0, 6, sanitize("CENTRALIZACAO SUPREMA NO PC LENOVO | CYBERSECURITY + ECOSSISTEMA"), 0, 1, 'L')
    
    pdf.set_xy(15, 30)
    pdf.set_font('Helvetica', '', 8)
    pdf.set_text_color(203, 213, 225)
    pdf.cell(0, 5, sanitize("Google Drive (750GB/Dia Nuvem-a-Nuvem) + Telegram Supergrupos e 5 Catedrais"), 0, 1, 'L')
    
    pdf.set_y(50)
    
    pdf.chapter_title("1. RESUMO EXECUTIVO & ESTADO ATUAL DOS CLONES")
    pdf.body_p("Este manual consolida todos os scripts, fluxos e instrucoes para que o PC Lenovo execute a clonagem integral dos acervos. O processo prioriza 100% a area de Ciberseguranca, Pentest e Defesa, sem esquecer as demais areas tecnologicas.")
    
    pdf.info_card("ESTADO ATUAL DOS ACERVOS", [
        "Google Drive - Solyd One Pentest (134.6 GB / 534 itens): 100% CONCLUIDO COM SUCESSO.",
        "Google Drive - Hackone Academia Cyber (780 GB): 1.354+ itens transferidos (Em andamento).",
        "Google Drive - Cursos Complementares: Foco em SEC + Pentest Geraldo Alcantara (Prontos na fila).",
        "Telegram - 5 Catedrais Master: Supergrupos criados com modo Forum/Topicos ativado com sucesso.",
        "Telegram - FoxHackers, Fox_Devs, FoxTechBR: Filas prontas para replicacao automatica."
    ], C_CYBER)
    
    pdf.chapter_title("2. COMANDO RAPIDO DE 1-CLIQUE NO LENOVO")
    pdf.body_p("Para iniciar a execucao completa no PC Lenovo, abra a pasta do projeto no terminal ou de duplo clique no inicializador:")
    
    pdf.code_block("""# Opcao 1: Executavel direto (Basta dar duplo clique)
EXECUTAR_MASTER_LENOVO_CYBER.bat

# Opcao 2: Via Terminal no Google Antigravity IDE
cd c:\\Users\\matheus\\Desktop\\computacao
python orquestrador_master_lenovo_cyber.py""")

    pdf.info_card("MODOS DE EXECUCAO DISPONIVEIS NO MENU", [
        "[1] Pipeline Completo (Recomendado): Executa Drive Cyber -> Telegram FoxHackers -> Catedrais.",
        "[2] Somente Google Drive: Foca em esgotar a cota de 750GB/dia com os cursos de Cyber e Dev.",
        "[3] Somente Telegram: Clona supergrupos e replica os topicos nos clones sem gastar cota do Drive.",
        "[4] Somente Varredura & Catalogo: Organiza e gera lista de livros, manuais e canais."
    ])

    # -------------------------------------------------------------
    # PÁGINA 2: GOOGLE DRIVE CLOUD-TO-CLOUD & COTA 750GB
    # -------------------------------------------------------------
    pdf.add_page()
    pdf.chapter_title("3. ARQUITETURA GOOGLE DRIVE: REGRAS DA COTA DE 750 GB/DIA")
    
    pdf.body_p("A clonagem do Google Drive funciona via 'Server-Side Copy' pelo Rclone. Isso significa que os dados trafegam diretamente entre os servidores do Google Cloud, sem baixar nenhum byte para o disco rigido do Lenovo e sem consumir a franquia da sua internet.")
    
    pdf.info_card("PARAMETROS CRITICOS DO RCLONE UTILIZADOS", [
        "--server-side-across-configs : Obriga a transferencia 100% nuvem-a-nuvem.",
        "--fast-list                  : Acelera listagem e reduz requisicoes a API.",
        "--transfers 4 --checkers 8   : 4 downloads paralelos com 8 verificadores simultaneos.",
        "--tpslimit 3                 : Limita a 3 transacoes/s para EVITAR Erro 403 (Rate Limit).",
        "--drive-pacer-min-sleep 100ms: Intervalo minimo de seguranca entre chamadas.",
        "--drive-stop-on-upload-limit : Se atingir os 750GB, pausa graciosamente sem corromper.",
        "--retries 10                 : Tolera oscilacoes temporarias e retoma automaticamente."
    ], C_PRIMARY)
    
    pdf.sub_title("Codigo Completo do Script do Google Drive (clonar_hackone_e_cyber.py):")
    pdf.code_block("""# clonar_hackone_e_cyber.py
import subprocess, sys, os, time, json

LOG_FILE = "clonagem_hackone.log"
PROGRESSO_FILE = "progresso_hackone.json"
ORIGEM_HACKONE = "meudrive,shared_with_me:DRIVE PREMIUM/02. Programacao/Hackone"
DESTINO_HACKONE = "meudrive:MEU_ACERVO_CLONADO/HACKONE_ACADEMIA_CYBER_COMPLETA"

CURSOS_EXTRAS = [
    {"nome": "Foco em SEC - 4 Pilares", "origem": ".../Foco em SEC", "destino": "meudrive:MEU_ACERVO_CLONADO/FOCO_EM_SEC"},
    {"nome": "Pentest Web Geraldo", "origem": ".../Pentest Web", "destino": "meudrive:MEU_ACERVO_CLONADO/PENTEST_GERALDO"}
]

def clonar(origem, destino, nome):
    cmd = ["rclone", "copy", origem, destino, "--server-side-across-configs",
           "--fast-list", "--transfers", "4", "--checkers", "8", "--tpslimit", "3",
           "--drive-pacer-min-sleep", "100ms", "--drive-stop-on-upload-limit",
           "--retries", "10", "--log-file", LOG_FILE, "--log-level", "INFO", "-P"]
    print(f">> CLONANDO: {nome}")
    return subprocess.run(cmd).returncode""")

    pdf.sub_title("Outras Pastas do Google Drive Mapeadas (Todas as Areas):")
    pdf.body_p("Alem de Cyber, a fila sequencial contempla as pastas de Desenvolvimento Geral ('01. NOVIDADES - CURSOS ADICIONADOS RECENTEMENTE' e 'Fox_Devs') atraves do script 'clonar_drive_com_monitor_cota.py'.")

    # -------------------------------------------------------------
    # PÁGINA 3: TELEGRAM CLONER & AS 5 CATEDRAIS MASTER
    # -------------------------------------------------------------
    pdf.add_page()
    pdf.chapter_title("4. TELEGRAM: AS 5 CATEDRAIS MASTER & TOPICOS ATOMICOS")
    
    pdf.body_p("No Telegram, o ecossistema esta estruturado em 5 Supergrupos Master com Modo Forum/Topicos ativado, garantindo organizacao impecavel:")

    pdf.info_card("AS 5 CATEDRAIS MASTER CRIADAS (IDs Salvos em catedrais_master_supergrupos.json)", [
        "1. CIBERSEGURANCA & DEVOPS   : ID -1003810610080 (10 Topicos Especializados)",
        "2. PROGRAMACAO & DEV          : ID -1003743629393 (Backend, Frontend, Mobile, DBs)",
        "3. IA, DADOS & AUTOMACAO      : ID -1004306202844 (Machine Learning, LLMs, Scripts)",
        "4. AUDIOVISUAL & DESIGN       : ID -1004446501310 (Edicao de Video, After, VFX, Design)",
        "5. MARKETING & NEGOCIOS       : ID -1004365977260 (Copywriting, Trafego, SaaS, Vendas)"
    ], C_CYBER)

    pdf.sub_title("Os 10 Topicos Estruturados na Catedral de Ciberseguranca (-1003810610080):")
    topicos_cyber = [
        "Topico 01: Fundamentos, Linux para Pentesters & Terminal",
        "Topico 02: Red Team, Web AppSec & OWASP Top 10",
        "Topico 03: Infraestrutura, Redes & Ataques em Protocolos",
        "Topico 04: Active Directory & Pentest Corporativo Windows",
        "Topico 05: Engenharia Reversa, Binarios & Malware Dev",
        "Topico 06: Blue Team, SOC, SIEM & Deteccao de Intrusao",
        "Topico 07: Pericia Forense Digital & Resposta a Incidentes (DFIR)",
        "Topico 08: Hardware Hacking, IoT & Radio-Frequencia (RF)",
        "Topico 09: Certificacoes Internacionais (Security+, CEH, OSCP)",
        "Topico 10: Biblioteca Mestre de Livros, Manuais & CheatSheets"
    ]
    pdf.info_card("ESTRUTURA DOS 10 TOPICOS DE CYBER", topicos_cyber, C_ACCENT)

    pdf.sub_title("Codigo do Robô de Supergrupos (clonar_supergrupos_completos.py):")
    pdf.code_block("""# clonar_supergrupos_completos.py (Resumo do Core)
async def clonar_supergrupo(app, orig_id, dest_id, nome):
    topicos = await obter_topicos(app, orig_id)
    for t_id, t_title in topicos.items():
        dest_topic_id = await criar_ou_obter_topico_clone(app, dest_id, t_title)
        msgs = await obter_mensagens_topico(app, orig_id, t_id)
        for msg in msgs:
            await app.copy_message(chat_id=dest_id, from_chat_id=orig_id, 
                                   message_id=msg.id, message_thread_id=dest_topic_id)
            await asyncio.sleep(0.5) # Anti-Flood""")

    # -------------------------------------------------------------
    # PÁGINA 4: RADAR DE CANAIS & ARSENAL DE FERRAMENTAS
    # -------------------------------------------------------------
    pdf.add_page()
    pdf.chapter_title("5. RADAR DE RECURSOS: CANAIS, LIVROS & ARSENAL OPEN-SOURCE")

    pdf.body_p("O orquestrador varre os canais publicos e privados catalogados no banco de dados e roteia as midias e arquivos para seus devidos topicos:")

    pdf.info_card("CANAIS & COMUNIDADES CATALOGADAS (BR & GLOBAL)", [
        "Mente Binaria (BR)       : Engenharia Reversa, Assembly x86/x64, Analise de Malware.",
        "HackerSec & Desec (BR)   : Labs de Pentest, Exploitation, Red Team e Certificacoes.",
        "Foco em SEC (BR)         : Investigacao Digital, Cadeia de Custodia e Pericia Forense.",
        "The Hacker News (Global) : Zero-Days, Vulnerabilidades Criticas e Inteligencia de Ameacas.",
        "Offensive Security (GL)  : Labs de Kali Linux, OSCP, Proving Grounds e Evasion.",
        "OWASP Global             : Seguranca em Aplicacoes Web, APIs REST/GraphQL e Top 10.",
        "Cyber Books Library      : Acervo com 250+ Livros (No Starch Press, O'Reilly, Sybex)."
    ], C_PRIMARY)

    pdf.sub_title("Arsenal de Ferramentas Open-Source Classificadas por Dominio:")
    pdf.info_card("ARSENAL HACKER & BLUE TEAM", [
        "Recon & OSINT        : Nmap, Subfinder, Amass, TheHarvester, Shodan CLI",
        "Web AppSec Pentest   : Burp Suite, SQLMap, FFUF, Nuclei, OWASP ZAP, Nikto",
        "Redes & Wi-Fi        : Wireshark, Bettercap, Scapy, Aircrack-ng, Responder",
        "Active Directory     : BloodHound, Impacket, CrackMapExec, Mimikatz, Rubeus",
        "Engenharia Reversa   : Ghidra, IDA Free, Cutter, x64dbg, Radare2, GDB",
        "Blue Team & SOC      : Wazuh XDR, Suricata, Zeek, Sigma Rules, Velociraptor",
        "Pericia Forense      : Autopsy, Volatility 3, FTK Imager, RegRipper, YARA"
    ], C_CYBER)

    pdf.chapter_title("6. GUIA DE CONTINGENCIA & TRATAMENTO DE ERROS")
    pdf.info_card("COMO AGIR EM CASO DE ERROS OU PAUSAS", [
        "Erro 403 Google Drive (Rate Limit) : O script aguarda 5 minutos e retoma sozinho.",
        "Telegram FloodWait (Ex: 300s)       : O Pyrogram dorme o tempo exato e prossegue sem crash.",
        "Queda de Energia / Reinicializacao  : Basta executar o BAT novamente; ele checa o que ja",
        "                                      foi clonado e continua exatamente de onde parou."
    ], (239, 68, 68))

    # Salva o arquivo
    pdf.output(PDF_OUTPUT)
    print(f"[OK] PDF gerado com sucesso em: {PDF_OUTPUT}")


if __name__ == "__main__":
    sys.stdout.reconfigure(encoding='utf-8', errors='replace')
    sys.stderr.reconfigure(encoding='utf-8', errors='replace')
    gerar_pdf()

