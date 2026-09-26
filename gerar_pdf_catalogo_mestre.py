# -*- coding: utf-8 -*-
"""
GERADOR DO CATÁLOGO MESTRE GERAL ABSOLUTO EM PDF
Compila TODO o universo do Google Drive Matriz (ID: 1cBDvRvFL4B5TmD7oXYfcTYvlHl40GXGG),
os Clones Pessoais e o Ecossistema do Telegram (59 Canais, 531 Cursos, 184 Livros).
"""
import os
import sys
import json
import re
from fpdf import FPDF
from fpdf.enums import XPos, YPos

BASE_DIR = r"c:\Users\matheus\Desktop\computacao"
PDF_OUTPUT = os.path.join(BASE_DIR, "CATALOGO_MESTRE_CURSOS_TELEGRAM_E_DRIVE.pdf")

# Paleta Executiva Premium
C_PRIMARY = (15, 23, 42)      # Slate 900
C_SECONDARY = (30, 41, 59)    # Slate 800
C_ACCENT = (14, 165, 233)     # Sky 500
C_CYBER = (16, 185, 129)      # Emerald 500
C_AMBER = (217, 119, 6)       # Amber 600
C_PURPLE = (147, 51, 234)     # Purple 600
C_ROSE = (225, 29, 72)        # Rose 600
C_BG_CARD = (248, 250, 252)   # Slate 50
C_BORDER = (226, 232, 240)    # Slate 200
C_TEXT = (51, 65, 85)         # Slate 700
C_TEXT_LIGHT = (100, 116, 139)# Slate 500

def clean_text(s):
    """Normaliza texto para PDF e substitui emojis por etiquetas legíveis"""
    if not s:
        return ""
    if not isinstance(s, str):
        s = str(s)
    
    replacements = {
        "—": "-", "–": "-", "“": '"', "”": '"', "‘": "'", "’": "'",
        "•": "*", "🎓": "[CURSO]", "🛡️": "[CYBER]", "🛡": "[CYBER]",
        "☁️": "[DRIVE]", "☁": "[DRIVE]", "📡": "[TG]", "🚀": "[PRO]",
        "💻": "[DEV]", "🔥": "[HOT]", "⭐": "*", "📚": "[LIVRO]",
        "🏛️": "[CATEDRAL]", "🏛": "[CATEDRAL]", "☕️": "", "☕": "",
        "👑": "", "💎": "[PREMIUM]", "🤿": "", "🦅": "", "🇧🇷": "[BR]",
        "📂": "[DIR]", "🆕": "[NOVO]", "🔎": "[BUSCA]", "📦": "[PKG]",
        "⚙️": "[CONFIG]", "⚙": "[CONFIG]", "🙂": "", "🤖": "[IA]",
        "💰": "[FIN]", "🧵": "-", "📍": "", "🔗": "",
        "✔": "[OK]", "✅": "[OK]", "❌": "[X]", "➡": "->", "⬅": "<-",
        "▶": ">", "◀": "<", "⚠": "[!]", "⚛": "[REACT]", "━": "-",
        "❤": "", "↳": "->", "☀": "", "►": ">", "🪼": "", "☀️": "",
        "🐦‍🔥": "", "🕊": "", "⚡": "[FAST]", "✨": "", "🎯": "[FOCO]",
        "⚔️": "[VS]", "⚔": "[VS]", "\ufe0f": "", "🌟": "[MKT]", "🎥": "[VIDEO]",
        "📊": "[FIN]", "🎵": "[SOM]", "🧠": "[NEURO]", "🎨": "[DESIGN]",
        "📖": "[EBOOK]", "🔁": "[OUTROS]"
    }
    for k, v in replacements.items():
        s = s.replace(k, v)
    
    # Filter printable BMP characters
    s = "".join(ch for ch in s if (32 <= ord(ch) <= 0xFFFF) or ch == '\n')
    # Collapse multiple spaces
    s = re.sub(r'[ \t]+', ' ', s)
    return s.strip()

class CatalogoAbsolutoPDF(FPDF):
    def __init__(self):
        super().__init__(orientation='P', unit='mm', format='A4')
        self.set_auto_page_break(auto=True, margin=15)
        self.add_font('ArialCustom', '', r'C:\Windows\Fonts\arial.ttf')
        self.add_font('ArialCustom', 'B', r'C:\Windows\Fonts\arialbd.ttf')
        self.add_font('ArialCustom', 'I', r'C:\Windows\Fonts\ariali.ttf')
        self.add_font('ArialCustom', 'BI', r'C:\Windows\Fonts\arialbi.ttf')
        self.set_font('ArialCustom', '', 9)

    def header(self):
        if self.page_no() > 1:
            self.set_font('ArialCustom', 'B', 8)
            self.set_text_color(*C_TEXT_LIGHT)
            self.cell(110, 7, clean_text("CATÁLOGO GERAL ABSOLUTO — DRIVE MATRIZ & TELEGRAM"), 0, new_x=XPos.RIGHT, new_y=YPos.TOP)
            self.set_font('ArialCustom', '', 8)
            self.cell(0, 7, clean_text(f"Página {self.page_no()}"), 0, new_x=XPos.LMARGIN, new_y=YPos.NEXT, align='R')
            self.set_draw_color(*C_BORDER)
            self.set_line_width(0.3)
            self.line(10, 13, 200, 13)
            self.ln(2)

    def footer(self):
        self.set_y(-12)
        self.set_font('ArialCustom', 'I', 7.5)
        self.set_text_color(*C_TEXT_LIGHT)
        self.cell(0, 7, clean_text("Matheus Barbosa | Acervo Completo em Nuvem | Drive Matriz Premium & Telegram Streaming"), 0, new_x=XPos.LMARGIN, new_y=YPos.NEXT, align='C')

    def section_banner(self, num, title, subtitle="", color=C_PRIMARY):
        if self.get_y() > 240:
            self.add_page()
        self.ln(4)
        cur_y = self.get_y()
        self.set_fill_color(*color)
        self.rect(10, cur_y, 190, 14, 'F')
        
        self.set_xy(14, cur_y + 1.5)
        self.set_font('ArialCustom', 'B', 12)
        self.set_text_color(255, 255, 255)
        self.cell(0, 6, clean_text(f"PARTE {num}: {title}"), 0, new_x=XPos.LMARGIN, new_y=YPos.NEXT)
        
        if subtitle:
            self.set_x(14)
            self.set_font('ArialCustom', 'I', 8)
            self.set_text_color(226, 232, 240)
            self.cell(0, 4.5, clean_text(subtitle), 0, new_x=XPos.LMARGIN, new_y=YPos.NEXT)
        
        self.set_y(cur_y + 17)

    def sub_header(self, title, count_tag=""):
        if self.get_y() > 255:
            self.add_page()
        self.ln(2.5)
        self.set_font('ArialCustom', 'B', 10)
        self.set_text_color(*C_PRIMARY)
        t = clean_text(title)
        if count_tag:
            t += f" ({clean_text(count_tag)})"
        self.cell(0, 6, t, 0, new_x=XPos.LMARGIN, new_y=YPos.NEXT)
        self.set_draw_color(*C_ACCENT)
        self.set_line_width(0.5)
        self.line(10, self.get_y(), 50, self.get_y())
        self.ln(2)

    def item_card(self, title, detail="", origin="", link="", border_color=C_ACCENT):
        if self.get_y() > 265:
            self.add_page()
        
        h = 7.5
        if detail:
            h += 3.8
        if origin or link:
            h += 3.8
            
        cur_y = self.get_y()
        self.set_fill_color(*C_BG_CARD)
        self.set_draw_color(*C_BORDER)
        self.set_line_width(0.2)
        self.rect(10, cur_y, 190, h, 'DF')
        
        # Border accent strip on left
        self.set_fill_color(*border_color)
        self.rect(10, cur_y, 2, h, 'F')
        
        self.set_xy(14, cur_y + 1.2)
        self.set_font('ArialCustom', 'B', 8.5)
        self.set_text_color(*C_PRIMARY)
        self.cell(182, 4, clean_text(title), 0, new_x=XPos.LMARGIN, new_y=YPos.NEXT)
        
        if detail:
            self.set_x(14)
            self.set_font('ArialCustom', '', 7.5)
            self.set_text_color(*C_TEXT)
            self.cell(182, 3.5, clean_text(detail), 0, new_x=XPos.LMARGIN, new_y=YPos.NEXT)
            
        if origin or link:
            self.set_x(14)
            self.set_font('ArialCustom', 'I', 7)
            self.set_text_color(*C_TEXT_LIGHT)
            meta = ""
            if origin:
                meta += f"Origem: {clean_text(origin)}"
            if link:
                if meta:
                    meta += "  |  Link: "
                else:
                    meta += "Link: "
                meta += clean_text(link)
            self.cell(182, 3.5, meta, 0, new_x=XPos.LMARGIN, new_y=YPos.NEXT)
            
        self.set_y(cur_y + h + 1.2)

def build_pdf_absoluto():
    print("Iniciando compilação do Catálogo Geral Absoluto...")
    pdf = CatalogoAbsolutoPDF()
    pdf.set_margins(10, 10, 10)
    
    # Carregar dados
    with open(os.path.join(BASE_DIR, "matriz_drive_raw.json"), "r", encoding="utf-8") as f:
        matriz_items = json.load(f)
        
    with open(os.path.join(BASE_DIR, "drive_dump.json"), "r", encoding="utf-8") as f:
        drive_dump = json.load(f)

    base_tg = r"C:\Users\matheus\Desktop\#COMPUTAÇÃO\TelegramDownloader"
    with open(os.path.join(base_tg, "mapeamento_hashtags_computacao.json"), "r", encoding="utf-8") as f:
        tg_data = json.load(f)

    # Processar categorias da Matriz
    matriz_cats = {}
    for it in matriz_items:
        parts = it.split('/')
        cat = parts[0]
        if len(parts) == 2:
            matriz_cats.setdefault(cat, []).append(parts[1])
            
    total_cursos_matriz = sum(len(v) for v in matriz_cats.values())
    total_cursos_clonados = len(drive_dump['clonadas'])
    total_cursos_telegram = tg_data.get('total_cursos_encontrados', 531)
    
    # ==========================================
    # CAPA EXECUTIVA
    # ==========================================
    pdf.add_page()
    
    # Top banner dark
    pdf.set_fill_color(*C_PRIMARY)
    pdf.rect(0, 0, 210, 82, 'F')
    
    # Top emerald line
    pdf.set_fill_color(*C_CYBER)
    pdf.rect(0, 0, 210, 4, 'F')
    
    pdf.set_xy(12, 16)
    pdf.set_font('ArialCustom', 'B', 19)
    pdf.set_text_color(255, 255, 255)
    pdf.cell(0, 9, clean_text("CATÁLOGO GERAL ABSOLUTO"), 0, new_x=XPos.LMARGIN, new_y=YPos.NEXT)
    
    pdf.set_x(12)
    pdf.set_font('ArialCustom', 'B', 12.5)
    pdf.set_text_color(*C_ACCENT)
    pdf.cell(0, 7, clean_text("Google Drive Matriz Premium & Canais de Streaming do Telegram"), 0, new_x=XPos.LMARGIN, new_y=YPos.NEXT)
    
    pdf.set_x(12)
    pdf.set_font('ArialCustom', 'I', 9)
    pdf.set_text_color(203, 213, 225)
    pdf.cell(0, 6, clean_text("Inventário Mestre Unificado: Todas as Formações, Cursos, Plataformas e Livros"), 0, new_x=XPos.LMARGIN, new_y=YPos.NEXT)
    
    pdf.set_y(88)
    
    # Metadata Card
    pdf.set_fill_color(*C_BG_CARD)
    pdf.set_draw_color(*C_BORDER)
    pdf.rect(10, 86, 190, 34, 'DF')
    pdf.set_fill_color(*C_ACCENT)
    pdf.rect(10, 86, 3, 34, 'F')
    
    pdf.set_xy(16, 89)
    pdf.set_font('ArialCustom', 'B', 8.5)
    pdf.set_text_color(*C_PRIMARY)
    pdf.cell(38, 4.5, "Titular do Acervo:", 0, new_x=XPos.RIGHT, new_y=YPos.TOP)
    pdf.set_font('ArialCustom', '', 8.5)
    pdf.set_text_color(*C_TEXT)
    pdf.cell(0, 4.5, "Matheus Barbosa da Silva", 0, new_x=XPos.LMARGIN, new_y=YPos.NEXT)
    
    pdf.set_x(16)
    pdf.set_font('ArialCustom', 'B', 8.5)
    pdf.set_text_color(*C_PRIMARY)
    pdf.cell(38, 4.5, "Pasta Matriz Google Drive:", 0, new_x=XPos.RIGHT, new_y=YPos.TOP)
    pdf.set_font('ArialCustom', '', 8.5)
    pdf.set_text_color(*C_TEXT)
    pdf.cell(0, 4.5, clean_text("💎 DRIVE PREMIUM - MESTRE DOS CURSOS (ID: 1cBDvRvFL4B5TmD7oXYfcTYvlHl40GXGG)"), 0, new_x=XPos.LMARGIN, new_y=YPos.NEXT)

    pdf.set_x(16)
    pdf.set_font('ArialCustom', 'B', 8.5)
    pdf.set_text_color(*C_PRIMARY)
    pdf.cell(38, 4.5, "Acervo Pessoal Sincronizado:", 0, new_x=XPos.RIGHT, new_y=YPos.TOP)
    pdf.set_font('ArialCustom', '', 8.5)
    pdf.set_text_color(*C_TEXT)
    pdf.cell(0, 4.5, "meudrive:MEU_ACERVO_CLONADO/ (Solyd One, Hackone, Foco em SEC, etc.)", 0, new_x=XPos.LMARGIN, new_y=YPos.NEXT)

    pdf.set_x(16)
    pdf.set_font('ArialCustom', 'B', 8.5)
    pdf.set_text_color(*C_PRIMARY)
    pdf.cell(38, 4.5, "Ecossistema Telegram:", 0, new_x=XPos.RIGHT, new_y=YPos.TOP)
    pdf.set_font('ArialCustom', '', 8.5)
    pdf.set_text_color(*C_TEXT)
    pdf.cell(0, 4.5, "59 Canais Ativos • 531 Cursos de Computação • 184 Obras Hacker", 0, new_x=XPos.LMARGIN, new_y=YPos.NEXT)

    pdf.set_x(16)
    pdf.set_font('ArialCustom', 'B', 8.5)
    pdf.set_text_color(*C_PRIMARY)
    pdf.cell(38, 4.5, "Data da Auditoria Geral:", 0, new_x=XPos.RIGHT, new_y=YPos.TOP)
    pdf.set_font('ArialCustom', '', 8.5)
    pdf.set_text_color(*C_TEXT)
    pdf.cell(0, 4.5, "Setembro / 2026", 0, new_x=XPos.LMARGIN, new_y=YPos.NEXT)
    
    # 4 Metric Badges
    pdf.set_y(126)
    badges = [
        ("1.200+", "Cursos & Plataformas", C_ACCENT),
        ("16 Áreas", "Matriz Mestre dos Cursos", C_CYBER),
        ("59 Canais", "Streaming no Telegram", C_AMBER),
        ("+2.5 TB", "Conhecimento em Nuvem", C_PURPLE)
    ]
    
    bw = 45
    bh = 22
    for i, (val, label, col) in enumerate(badges):
        bx = 10 + i * 48
        pdf.set_fill_color(255, 255, 255)
        pdf.set_draw_color(*C_BORDER)
        pdf.rect(bx, 126, bw, bh, 'DF')
        
        pdf.set_fill_color(*col)
        pdf.rect(bx, 126, bw, 2.5, 'F')
        
        pdf.set_xy(bx, 131)
        pdf.set_font('ArialCustom', 'B', 13.5)
        pdf.set_text_color(*col)
        pdf.cell(bw, 6, val, 0, new_x=XPos.LMARGIN, new_y=YPos.NEXT, align='C')
        
        pdf.set_x(bx)
        pdf.set_font('ArialCustom', '', 7)
        pdf.set_text_color(*C_TEXT)
        pdf.cell(bw, 4, clean_text(label), 0, new_x=XPos.LMARGIN, new_y=YPos.NEXT, align='C')

    # Executive Text Box
    pdf.set_y(153)
    pdf.set_fill_color(*C_BG_CARD)
    pdf.set_draw_color(*C_BORDER)
    pdf.rect(10, 153, 190, 75, 'DF')
    
    pdf.set_xy(14, 156)
    pdf.set_font('ArialCustom', 'B', 10.5)
    pdf.set_text_color(*C_PRIMARY)
    pdf.cell(0, 5.5, clean_text("ECOSSISTEMA GERAL DE CONHECIMENTO & PLATAFORMAS"), 0, new_x=XPos.LMARGIN, new_y=YPos.NEXT)
    
    pdf.set_x(14)
    pdf.set_font('ArialCustom', '', 8)
    pdf.set_text_color(*C_TEXT)
    intro_txt = (
        "Este catálogo consolida o mapeamento definitivo e absoluto do seu acervo educacional. "
        "Ele reúne as 16 categorias completas da pasta Matriz '💎 DRIVE PREMIUM - MESTRE DOS CURSOS', "
        "as formações aprofundadas de cibersegurança e redes já clonadas na sua conta pessoal, "
        "e todos os 59 canais de tecnologia do Telegram com streaming ativo sem ocupação de disco local."
    )
    pdf.multi_cell(182, 4, clean_text(intro_txt))
    pdf.ln(1.5)
    
    pdf.set_x(14)
    pdf.set_font('ArialCustom', 'B', 8.5)
    pdf.set_text_color(*C_PRIMARY)
    pdf.cell(0, 4.5, clean_text("Distribuição dos Acervos:"), 0, new_x=XPos.LMARGIN, new_y=YPos.NEXT)
    
    pilares = [
        ("Matriz Drive Premium:", "97 plataformas de Programação (Alura, Rocketseat, Full Cycle, B7Web, FIAP), 60 formações de IA (Bruno Bracaioli, n8n, Vibe Coding, Lovable), Marketing, Concursos, Finanças, Design e Negócios."),
        ("Formações Ofensivas:", "Acervos mastodônticos dedicados: Solyd One Formação Pentest (38 módulos completos) e Hackone Academia Cyber (4 trilhas com 92 especializações em Cloud, Cyber, Mikrotik e Redes)."),
        ("Telegram Streaming:", "531 cursos de computação mapeados por hashtags com reprodução direta e zero bytes consumidos no seu SSD."),
        ("Biblioteca Universitária:", "184 manuais técnicos e livros clássicos de Ciência da Computação (Tanenbaum, Pressman, Norvig, Clean Code).")
    ]
    for p_title, p_desc in pilares:
        pdf.set_x(16)
        pdf.set_font('ArialCustom', 'B', 7.5)
        pdf.set_text_color(*C_ACCENT)
        pdf.cell(38, 4, clean_text(p_title), 0, new_x=XPos.RIGHT, new_y=YPos.TOP)
        pdf.set_font('ArialCustom', '', 7.5)
        pdf.set_text_color(*C_TEXT)
        pdf.cell(144, 4, clean_text(p_desc), 0, new_x=XPos.LMARGIN, new_y=YPos.NEXT)

    # Status box
    pdf.set_y(233)
    pdf.set_fill_color(240, 253, 244)
    pdf.set_draw_color(187, 247, 208)
    pdf.rect(10, 233, 190, 18, 'DF')
    pdf.set_xy(14, 235.5)
    pdf.set_font('ArialCustom', 'B', 8)
    pdf.set_text_color(*C_CYBER)
    pdf.cell(0, 4, clean_text("[STATUS: AUDITORIA COMPLETA DE TODAS AS VERTICAIS CONCLUÍDA]"), 0, new_x=XPos.LMARGIN, new_y=YPos.NEXT)
    pdf.set_x(14)
    pdf.set_font('ArialCustom', '', 7.5)
    pdf.set_text_color(22, 101, 52)
    pdf.cell(0, 4, clean_text("Documento com links clicáveis e caminhos de acesso direto no Google Drive e no Telegram."), 0, new_x=XPos.LMARGIN, new_y=YPos.NEXT)

    # ==========================================
    # PARTE 1: DRIVE MATRIZ - CATEGORIAS GERAIS
    # ==========================================
    pdf.add_page()
    pdf.section_banner(
        "1",
        "DRIVE MATRIZ PREMIUM (16 CATEGORIAS COMPLETAS)",
        "Pasta Mãe: 💎 DRIVE PREMIUM - MESTRE DOS CURSOS (ID: 1cBDvRvFL4B5TmD7oXYfcTYvlHl40GXGG)",
        C_PRIMARY
    )
    
    # Ordem das categorias a listar
    ordem_matriz = [
        ("02. 💻 Programação & Desenvolvimento", "97 Plataformas & Cursos Completos", C_ACCENT),
        ("03. 🤖 Inteligência Artificial & Automação ", "60 Formações de IA, n8n, Vibe Coding & Agentes", C_CYBER),
        ("04. 🌟 Marketing, Copy & Tráfego", "56 Formações de Tráfego Pago, Copywriting & Lançamentos", C_AMBER),
        ("06. 🎥 YouTube, TikTok & Conteúdo", "20 Cursos de Conteúdo Viral, Canais Dark & Edição", C_PURPLE),
        ("12. 🎨 Design, 3D & Edição", "17 Formações de Design Gráfico, Modelagem 3D & Motion", C_ROSE),
        ("07. 📚 Concursos & Vestibulares", "14 Grandes Pacotes de Concursos Públicos e Exames", C_PRIMARY),
        ("08. 📊 Investimentos & Finanças", "Formações de Mercado Financeiro, Opsec Cripto & Renda", C_CYBER),
        ("14. 🎯Desenvolvimento Pessoal", "16 Cursos de Alta Performance, Disciplina & Habilidades", C_ACCENT),
        ("11. 🧠 Neurociência, Psicologia & Saúde Mental", "Formações Clínicas, Terapia & Neurociência", C_PURPLE),
        ("05. 💰 Negócios & Empreendedorismo", "Gestão Empresarial, Vendas & Escala", C_AMBER),
        ("09. 🎵 Música & Instrumentos", "20 Cursos de Teoria Musical, Instrumentos & Produção", C_PRIMARY),
        ("10. ⚡Cursos Elétrica ", "Cursos Práticos de Eletricidade & Instalações", C_AMBER),
        ("13. 📖 Ebooks ", "10 Coleções e Bibliotecas de Livros Digitais", C_CYBER),
        ("15. 🔁 Outros", "31 Acervos Diversos e Especialidades Complementares", C_SECONDARY)
    ]
    
    for cat_key, sub_desc, cor in ordem_matriz:
        cursos_cat = matriz_cats.get(cat_key, [])
        if not cursos_cat:
            continue
            
        pdf.sub_header(cat_key, f"{len(cursos_cat)} itens • {sub_desc}")
        for c in sorted(cursos_cat):
            pdf.item_card(
                c,
                f"Matriz Drive: {cat_key}",
                f"Google Drive (ID: 1cBDvRvFL4B5TmD7oXYfcTYvlHl40GXGG)",
                border_color=cor
            )

    # ==========================================
    # PARTE 2: FORMAÇÕES OFENSIVAS & CYBER DEEP
    # ==========================================
    pdf.add_page()
    pdf.section_banner(
        "2",
        "FORMAÇÕES APROFUNDADAS DE CYBER & REDES",
        "Acervos Especiais Sincronizados na Conta Pessoal (meudrive:MEU_ACERVO_CLONADO/)",
        C_SECONDARY
    )
    
    # 2.1 Solyd One Formação Pentest
    solyd_mods = sorted([p.split('/')[1] for p in drive_dump['clonadas'] if p.startswith('SOLYD_ONE_FORMACAO_PENTEST_COMPLETA/') and p.count('/') == 1])
    pdf.sub_header("2.1 Solyd One — Formação Pentest Completa", f"{len(solyd_mods)} Módulos • 134.6 GB • 534 Aulas")
    pdf.set_font('ArialCustom', '', 8)
    pdf.set_text_color(*C_TEXT)
    pdf.multi_cell(0, 4, clean_text(
        "Formação definitiva do zero ao avançado cobrindo Linux, Redes, Web AppSec, Hardware Hacking, "
        "LLM Hacking, Evasão de EDR, Active Directory e desenvolvimento de exploits."
    ))
    pdf.ln(1)
    for mod in solyd_mods:
        pdf.item_card(
            f"Solyd One: {mod}",
            "Formação Pentest Completa do Zero ao Profissional",
            "meudrive:MEU_ACERVO_CLONADO/SOLYD_ONE_FORMACAO_PENTEST_COMPLETA",
            border_color=C_CYBER
        )

    # 2.2 Hackone Academia Cyber
    hackone_subs = sorted([p for p in drive_dump['clonadas'] if p.startswith('HACKONE_ACADEMIA_CYBER_COMPLETA/') and p.count('/') == 2])
    trilhas_hackone = {}
    for p in hackone_subs:
        parts = p.split('/')
        trilhas_hackone.setdefault(parts[1], []).append(parts[2])
        
    pdf.sub_header("2.2 Hackone — Academia Cyber Completa", f"4 Grandes Trilhas • {len(hackone_subs)} Especializações • 780.3 GB")
    for t_nome, modulos in trilhas_hackone.items():
        pdf.ln(1)
        pdf.set_font('ArialCustom', 'B', 8.5)
        pdf.set_text_color(*C_ACCENT)
        pdf.cell(0, 4.5, clean_text(f"► {t_nome} ({len(modulos)} especializações)"), 0, new_x=XPos.LMARGIN, new_y=YPos.NEXT)
        for m in modulos:
            pdf.item_card(
                f"{t_nome}: {m}",
                "Academia Cyber Hackone — Treinamento & Certificação",
                f"meudrive:MEU_ACERVO_CLONADO/HACKONE_ACADEMIA_CYBER_COMPLETA/{t_nome}",
                border_color=C_ACCENT
            )

    # 2.3 Foco em SEC, Geraldo Alcantara e Raiz
    pdf.sub_header("2.3 Outras Especializações & Cursos de Engenharia", "Acervos Práticos")
    outros_especiais = [
        ("Foco em SEC — 4 Pilares de Cyber e Investigação Digital", "Investigação Forense Digital, Perícia, Threat Intelligence e Segurança Prática.", "meudrive:MEU_ACERVO_CLONADO/FOCO_EM_SEC_INVESTIGACAO_DIGITAL"),
        ("Pentest Web Profissional — Geraldo Alcântara", "Do Reconhecimento Web Avançado à Exploração e Relatório Executivo.", "meudrive:MEU_ACERVO_CLONADO/PENTEST_WEB_PROFISSIONAL_GERALDO_ALCANTARA"),
        ("Especialista Python — Programador Aventureiro", "Trilha completa do zero à maestria com Python, OOP, arquitetura e automações.", "meudrive:Especialista Python - Programador Aventureiro"),
        ("Clone My SaaS ($399)", "Engenharia e desenvolvimento de sistemas SaaS modernos escaláveis.", "meudrive:CLONE MY SAAS $399")
    ]
    for t, d, orig in outros_especiais:
        pdf.item_card(t, d, orig, border_color=C_PURPLE)

    # 2.4 Catedral de Matemática
    mat_subs = sorted([p for p in drive_dump['clonadas'] if p.startswith('CATEDRAL_00_MATEMATICA_MASTER/') and p.count('/') == 1])
    pdf.sub_header("2.4 Catedral de Matemática & Fundamentos para Computação", f"{len(mat_subs)} Coleções")
    for m in mat_subs:
        m_nome = m.split('/')[1]
        pdf.item_card(
            f"Matemática: {m_nome}",
            "Treinamentos Olímpicos POTI IMPA, Iezzi, Pré-Cálculo e Livros Clássicos",
            "meudrive:MEU_ACERVO_CLONADO/CATEDRAL_00_MATEMATICA_MASTER",
            border_color=C_AMBER
        )

    # ==========================================
    # PARTE 3: CANAIS TELEGRAM
    # ==========================================
    pdf.add_page()
    pdf.section_banner(
        "3",
        "DIRETÓRIO DE 59 CANAIS DE STREAMING (TELEGRAM)",
        "Canais de Tecnologia e Cursos Conectados para Reprodução Direta em Nuvem",
        C_PRIMARY
    )
    
    pdf.set_font('ArialCustom', '', 8)
    pdf.set_text_color(*C_TEXT)
    pdf.multi_cell(0, 4, clean_text(
        "Abaixo estão os 59 canais identificados e integrados à sua conta do Telegram. "
        "Acesso direto via player de streaming na nuvem sem baixar nada no computador local."
    ))
    pdf.ln(2)
    
    # Table header
    pdf.set_fill_color(*C_PRIMARY)
    pdf.set_font('ArialCustom', 'B', 8)
    pdf.set_text_color(255, 255, 255)
    pdf.cell(10, 6, "#", 0, new_x=XPos.RIGHT, new_y=YPos.TOP, align='C', fill=True)
    pdf.cell(75, 6, "Nome do Canal", 0, new_x=XPos.RIGHT, new_y=YPos.TOP, align='L', fill=True)
    pdf.cell(45, 6, "ID / Identificador", 0, new_x=XPos.RIGHT, new_y=YPos.TOP, align='L', fill=True)
    pdf.cell(25, 6, "Cursos Mapeados", 0, new_x=XPos.RIGHT, new_y=YPos.TOP, align='C', fill=True)
    pdf.cell(35, 6, "Acesso Direto", 0, new_x=XPos.LMARGIN, new_y=YPos.NEXT, align='L', fill=True)
    
    canais_lista = [
        ("Mega Cursos", "@Mega_Curso", "39 itens", "https://t.me/Mega_Curso"),
        ("Voe Alto Antigo (Clone)", "-1001722206896", "34 itens", "https://t.me/c/1722206896/1"),
        ("Sathariel - Angel of Deception", "-1001697666550", "31 itens", "https://t.me/c/1697666550/1"),
        ("Mestre dos Cursos", "@Mestre_dos_Cursos", "28 itens", "https://t.me/Mestre_dos_Cursos"),
        ("Java Chat", "-1002093482981", "27 itens", "https://t.me/c/2093482981/1"),
        ("BKP - Zezao", "-1003285146096", "20 itens", "https://t.me/c/3285146096/1"),
        ("Aletheia Clone", "@aletheiaBR", "18 itens", "https://t.me/aletheiaBR"),
        ("DEFY SYSTEM ARCHIVES", "@DefySystemArchives", "17 itens", "https://t.me/DefySystemArchives"),
        ("Chat @conlinebr", "-1001860409528", "16 itens", "https://t.me/c/1860409528/1"),
        ("Cangaco Conteudo Backup", "-1001692070534", "16 itens", "https://t.me/c/1692070534/1"),
        ("< 404 Error >", "-1001985515257", "16 itens", "https://t.me/c/1985515257/1"),
        ("Cursos On Demand 24/7", "@ondemand24", "16 itens", "https://t.me/ondemand24"),
        ("Cattus Intellectualis", "-1002066589679", "16 itens", "https://t.me/c/2066589679/1"),
        ("Treasure cours chat", "@curs0seconteudos", "15 itens", "https://t.me/curs0seconteudos"),
        ("Courses - Online", "-1001668083861", "13 itens", "https://t.me/c/1668083861/1"),
        ("Apollyon - Templo de Delfos", "-1002100941446", "13 itens", "https://t.me/c/2100941446/1"),
        ("Kimera Society", "-1003945225095", "11 itens", "https://t.me/c/3945225095/1"),
        ("Tiger Eye | Cursos", "@TigerEyeDV", "11 itens", "https://t.me/TigerEyeDV"),
        ("DRAGON ACADEMY 2026", "-1002290046323", "11 itens", "https://t.me/c/2290046323/1"),
        ("CURSOS E CONTEUDOS GRATIS", "-1002058034320", "10 itens", "https://t.me/c/2058034320/1"),
        ("INFORMATICA FoxTech", "@FoxTechBR", "10 itens", "https://t.me/FoxTechBR"),
        ("DEV FoxDevs", "@Fox_Devs", "9 itens", "https://t.me/Fox_Devs"),
        ("Polemic Knowledge", "-1001910663694", "9 itens", "https://t.me/c/1910663694/1"),
        ("MINHA TRIBO DIGITAL", "-1001677408401", "9 itens", "https://t.me/c/1677408401/1"),
        ("Catalogo - Mestre dos Cursos", "@ListagemCursos", "8 itens", "https://t.me/ListagemCursos"),
        ("DevWorld - Cursos", "@DevWorldCBot", "8 itens", "https://t.me/DevWorldCBot"),
        ("Acervao Clone - El Gato", "-1002109379377", "7 itens", "https://t.me/c/2109379377/1"),
        ("Java Brasil - Receitass", "-1002056830228", "7 itens", "https://t.me/c/2056830228/1"),
        ("Devs Of Dragons", "-1002367740767", "6 itens", "https://t.me/c/2367740767/1"),
        ("Cursos Devs", "-1001909824548", "6 itens", "https://t.me/c/1909824548/1"),
        ("HACKING FoxHackers", "@FoxHackers", "6 itens", "https://t.me/FoxHackers"),
        ("Acervo Cursos online Backup", "@cursosonlinegratis1", "5 itens", "https://t.me/cursosonlinegratis1"),
        ("@Voo - Chat", "-1002937070831", "5 itens", "https://t.me/c/2937070831/1"),
        ("@Voo - Backup", "-1002781331111", "5 itens", "https://t.me/c/2781331111/1"),
        ("Polemic Knowledge - Clone", "-1001397713733", "4 itens", "https://t.me/c/1397713733/1"),
        ("Brasil Cursos", "@Brasil_Cursos5", "4 itens", "https://t.me/Brasil_Cursos5"),
        ("Cursos online", "-1002055797079", "3 itens", "https://t.me/c/2055797079/1"),
        ("ARSENAL DIGITAL 2.0 & MARKETING", "@arsenaldigital1", "3 itens", "https://t.me/arsenaldigital1"),
        ("Languages Chat", "-1003153030016", "3 itens", "https://t.me/c/3153030016/1"),
        ("CONCURSOS FoxConcursos", "@FoxConcursos", "3 itens", "https://t.me/FoxConcursos"),
        ("FROG DUCK", "-1003919455384", "3 itens", "https://t.me/c/3919455384/1"),
        ("Apollyon - Library", "-1001926854457", "3 itens", "https://t.me/c/1926854457/1"),
        ("Apollyon - Angel of the Void", "-1001923606985", "3 itens", "https://t.me/c/1923606985/1"),
        ("Polemic Knowledge Principal", "-1003589426937", "3 itens", "https://t.me/c/3589426937/1"),
        ("Guia do Uploader 2.0", "@guiadouploader20", "2 itens", "https://t.me/guiadouploader20"),
        ("Universidade Brasileira Livre", "@universidadebrasileiralivre", "2 itens", "https://t.me/universidadebrasileiralivre"),
        ("Bastiao Digital", "@bastiaodigital", "2 itens", "https://t.me/bastiaodigital"),
        ("Imperio Cursos", "-1001277777093", "2 itens", "https://t.me/c/1277777093/1"),
        ("Ovlon Hub", "@ovlonhub", "2 itens", "https://t.me/ovlonhub"),
        ("Cursos Populares Online - Gratis", "@popularcursosgratis", "2 itens", "https://t.me/popularcursosgratis"),
        ("Popular Cursos Oficial", "-1001887894832", "1 itens", "https://t.me/c/1887894832/1"),
        ("Lista Drive - DevWorldS", "@Drivecatalogo2", "1 itens", "https://t.me/Drivecatalogo2"),
        ("APOLLYON - DevSpace", "-1003812141549", "1 itens", "https://t.me/c/3812141549/1"),
        ("Acumuladores Digitais", "-1001532879558", "1 itens", "https://t.me/c/1532879558/1"),
        ("Raizen - O Trovao", "@raizentrovao", "1 itens", "https://t.me/raizentrovao"),
        ("Prompt Secreto", "@promptsecreto", "1 itens", "https://t.me/promptsecreto"),
        ("Little Demon", "@littledemonofc", "1 itens", "https://t.me/littledemonofc"),
        ("CURSOS DRIVE CATALOGO JAVABRASIL", "@cursoscatalogodrive", "1 itens", "https://t.me/cursoscatalogodrive"),
        ("Language C - Chat", "-1001914440397", "1 itens", "https://t.me/c/1914440397/1")
    ]
    
    for idx, (c_name, c_id, c_count, c_link) in enumerate(canais_lista, 1):
        if pdf.get_y() > 275:
            pdf.add_page()
            pdf.set_fill_color(*C_PRIMARY)
            pdf.set_font('ArialCustom', 'B', 8)
            pdf.set_text_color(255, 255, 255)
            pdf.cell(10, 6, "#", 0, new_x=XPos.RIGHT, new_y=YPos.TOP, align='C', fill=True)
            pdf.cell(75, 6, "Nome do Canal", 0, new_x=XPos.RIGHT, new_y=YPos.TOP, align='L', fill=True)
            pdf.cell(45, 6, "ID / Identificador", 0, new_x=XPos.RIGHT, new_y=YPos.TOP, align='L', fill=True)
            pdf.cell(25, 6, "Cursos Mapeados", 0, new_x=XPos.RIGHT, new_y=YPos.TOP, align='C', fill=True)
            pdf.cell(35, 6, "Acesso Direto", 0, new_x=XPos.LMARGIN, new_y=YPos.NEXT, align='L', fill=True)
            
        bg = (255, 255, 255) if idx % 2 != 0 else C_BG_CARD
        pdf.set_fill_color(*bg)
        pdf.set_font('ArialCustom', '', 7.5)
        pdf.set_text_color(*C_TEXT)
        
        pdf.cell(10, 5, str(idx), 0, new_x=XPos.RIGHT, new_y=YPos.TOP, align='C', fill=True)
        pdf.set_font('ArialCustom', 'B', 7.5)
        pdf.set_text_color(*C_PRIMARY)
        pdf.cell(75, 5, clean_text(c_name[:42]), 0, new_x=XPos.RIGHT, new_y=YPos.TOP, align='L', fill=True)
        pdf.set_font('ArialCustom', '', 7)
        pdf.set_text_color(*C_TEXT_LIGHT)
        pdf.cell(45, 5, clean_text(c_id[:25]), 0, new_x=XPos.RIGHT, new_y=YPos.TOP, align='L', fill=True)
        pdf.set_font('ArialCustom', 'B', 7)
        pdf.set_text_color(*C_CYBER)
        pdf.cell(25, 5, clean_text(c_count), 0, new_x=XPos.RIGHT, new_y=YPos.TOP, align='C', fill=True)
        pdf.set_font('ArialCustom', '', 6.5)
        pdf.set_text_color(*C_ACCENT)
        pdf.cell(35, 5, clean_text(c_link[:30]), 0, new_x=XPos.LMARGIN, new_y=YPos.NEXT, align='L', fill=True)

    # ==========================================
    # PARTE 4: CURSOS TELEGRAM POR TRILHA
    # ==========================================
    pdf.add_page()
    pdf.section_banner(
        "4",
        "CATÁLOGO DE 531 CURSOS DE STREAMING (TELEGRAM)",
        "Indexados por Grandes Áreas e Hashtags com Links Diretos de Reprodução",
        C_SECONDARY
    )
    
    macro_areas = [
        ("Linguagens de Programação & Lógica", ["#programacao", "#python", "#javascript", "#typescript", "#java", "#csharp", "#cplusplus", "#linguagemc", "#logica", "#algoritmos"], C_ACCENT),
        ("Desenvolvimento Web, Frontend, Backend & Mobile", ["#backend", "#frontend", "#fullstack", "#react", "#nodejs", "#node"], C_CYBER),
        ("DevOps, Infraestrutura, Linux & Cloud", ["#devops", "#docker", "#kubernetes", "#linux", "#aws", "#cloud", "#nuvem"], C_PRIMARY),
        ("Cibersegurança, Hacking Ético, Red Team & Pentest", ["#ciberseguranca", "#hacking", "#pentest", "#segurancadainformacao"], C_ROSE),
        ("Inteligência Artificial, Machine Learning & Data Science", ["#ia", "#inteligenciaartificial", "#machinelearning", "#datascience"], C_PURPLE),
        ("Redes de Computadores, Cisco, CCNA & Telecom", ["#redes", "#redesdecomputadores", "#cisco", "#ccna"], C_AMBER),
        ("Banco de Dados, SQL & Engenharia de Dados", ["#bancodedados", "#sql", "#mysql"], C_CYBER),
        ("Arquitetura de Software & Ciência da Computação", ["#arquitetura", "#engenharia", "#computacao"], C_SECONDARY)
    ]
    
    seen_links = set()
    for area_title, tags, cor in macro_areas:
        cursos_area = []
        for tag in tags:
            items = tg_data.get('cursos_por_hashtag', {}).get(tag, [])
            for it in items:
                link = it.get('link_mensagem', '')
                titulo = it.get('titulo', '').strip()
                if titulo.startswith('Nome: '):
                    titulo = titulo[6:].strip()
                elif titulo.startswith('Nome : '):
                    titulo = titulo[7:].strip()
                
                titulo = clean_text(titulo)
                k = (titulo, link)
                if k not in seen_links:
                    seen_links.add(k)
                    cursos_area.append({
                        'titulo': titulo,
                        'canal': it.get('canal', ''),
                        'link': link,
                        'tag': tag
                    })
                    
        pdf.sub_header(f"Trilha: {area_title}", f"{len(cursos_area)} cursos indexados")
        for c in cursos_area:
            pdf.item_card(
                c['titulo'],
                f"Especialidade: {c['tag']}",
                c['canal'],
                c['link'],
                border_color=cor
            )

    # ==========================================
    # PARTE 5: BIBLIOTECA HACKER & LIVROS CLÁSSICOS
    # ==========================================
    pdf.add_page()
    pdf.section_banner(
        "5",
        "BIBLIOTECA HACKER & LIVROS CLÁSSICOS DE COMPUTAÇÃO",
        "184 Obras Técnicas, Manuais Universitários e Livros de Referência",
        C_PRIMARY
    )
    
    acervo_md_path = os.path.join(BASE_DIR, "ACERVO_HACKER_TELEGRAM_CONSOLIDADO.md")
    if os.path.exists(acervo_md_path):
        with open(acervo_md_path, 'r', encoding='utf-8') as f:
            lines = f.readlines()
            
        cur_sub = "Manuais Técnicos"
        for l in lines:
            l = l.strip()
            if l.startswith("## "):
                cur_sub = l.replace("## ", "").strip()
                pdf.sub_header(clean_text(cur_sub))
            elif l.startswith("* **"):
                parts = l.split("**")
                if len(parts) >= 2:
                    item_name = parts[1].strip()
                    extra = ""
                    if len(parts) >= 3:
                        extra = parts[2].strip()
                    pdf.item_card(clean_text(item_name), clean_text(extra), "Telegram Acervo Consolidado Hacker", border_color=C_CYBER)

    # ==========================================
    # PARTE 6: CENTRAL DE COMANDOS
    # ==========================================
    pdf.add_page()
    pdf.section_banner(
        "6",
        "CENTRAL DE COMANDOS & ATUALIZAÇÃO AUTOMÁTICA",
        "Scripts Executáveis Prontos para Gerenciamento dos Acervos",
        C_SECONDARY
    )
    
    pdf.set_font('ArialCustom', '', 8.5)
    pdf.set_text_color(*C_TEXT)
    pdf.multi_cell(0, 4.2, clean_text(
        "Rotinas criadas no repositório local para executar, clonar e sincronizar os materiais:"
    ))
    pdf.ln(2)
    
    comandos_uteis = [
        ("GERAR_CATALOGO_PDF.bat", "Gera e atualiza este catálogo completo em PDF em poucos segundos com 1 clique duplo."),
        ("CLONAR_DRIVE_01_NOVIDADES.bat", "Executa a cópia Cloud-to-Cloud dos cursos novos adicionados ao Google Drive com controle de cota 750GB/dia."),
        ("CLONAR_SOLYD_ONE_PENTEST.bat", "Clona os 38 módulos da formação completa Solyd One Pentest diretamente para o seu Drive."),
        ("CLONAR_HACKONE_E_CYBER.bat", "Clona as 4 trilhas de Cibersegurança, Cloud, Mikrotik e Redes da Hackone (780 GB)."),
        ("ESTUDAR_CURSOS_TELEGRAM.bat", "Abre o motor de streaming do Telegram para assistir aos 531 cursos sem baixar arquivos no SSD."),
        ("VARREDURA_HACKER_TELEGRAM_GLOBAL.bat", "Varre automaticamente novas mensagens em todos os canais e atualiza a base de cursos.")
    ]
    
    for c_bat, c_desc in comandos_uteis:
        pdf.item_card(f"Script: {c_bat}", c_desc, "Local: c:\\Users\\matheus\\Desktop\\computacao", border_color=C_ACCENT)

    # Salvar PDF
    print(f"Salvando PDF em: {PDF_OUTPUT}")
    pdf.output(PDF_OUTPUT)
    print(f"Sucesso absoluto! PDF gerado com {pdf.page_no()} páginas.")
    return pdf.page_no()

if __name__ == '__main__':
    pags = build_pdf_absoluto()
    print(f"Compilação concluída com sucesso! Total: {pags} páginas.")
