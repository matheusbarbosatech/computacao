"""
=============================================================================
COMPILADOR DE E-BOOKS PARA IMPRESSÃO EM A4 PAISAGEM (300 DPI)
=============================================================================
Gera arquivos PDF profissionais de cada Escola em formato A4 Paisagem
(297 mm x 210 mm), prontos para encadernação Wire-o, fichário ou gráfica.
Inclui:
  1. Capa elegante da Escola
  2. Sumário / Índice analítico de páginas
  3. Páginas dos Mapas Mentais no layout Sketchnote diagramado
  4. Numeração e margens de sangria para encadernação
=============================================================================
"""

import os
import sys
import json
from fpdf import FPDF

if sys.platform == "win32":
    try:
        sys.stdout.reconfigure(encoding='utf-8')
        sys.stderr.reconfigure(encoding='utf-8')
    except Exception:
        pass

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# Paleta de Cores Sketchnote para Impressão CMYK-Friendly RGB
CORES = {
    "roxo": (126, 34, 206),
    "roxo_fundo": (243, 232, 255),
    "verde": (21, 128, 61),
    "verde_fundo": (240, 253, 244),
    "teal": (15, 118, 110),
    "teal_fundo": (240, 253, 250),
    "laranja": (194, 65, 12),
    "laranja_fundo": (255, 247, 237),
    "azul": (29, 78, 216),
    "azul_fundo": (239, 246, 255),
    "vermelho": (185, 28, 28),
    "vermelho_fundo": (254, 242, 242),
    "ambar": (180, 83, 9),
    "ambar_fundo": (255, 251, 235),
    "cinza_escuro": (30, 41, 59),
    "cinza_claro": (248, 250, 252),
    "borda_caixa": (203, 213, 225)
}

def sanitizar(texto: str) -> str:
    """Converte caracteres especiais e emojis para texto limpo suportado por fontes padrão."""
    if not texto:
        return ""
    # Substituições de emojis para texto elegante
    substituicoes = {
        "💡": "[ID] ",
        "🖥️": "[PC] ",
        "🖥": "[PC] ",
        "{ }": "{ } ",
        "</>": "</> ",
        "⚙️": "[FLUXO] ",
        "⚙": "[FLUXO] ",
        "⚠️": "[ALERTA] ",
        "⚠": "[ALERTA] ",
        "💬": "[RESUMO] ",
        "➔": "->",
        "→": "->",
        "•": "-",
        "✓": "[OK] ",
        "–": "-",
        "—": "-",
        "“": '"',
        "”": '"',
        "‘": "'",
        "’": "'"
    }
    for k, v in substituicoes.items():
        texto = texto.replace(k, v)
    
    # Remove qualquer outro caractere fora de latin-1
    return texto.encode('latin-1', 'replace').decode('latin-1')

class CadernoPDF(FPDF):
    def __init__(self, titulo_escola):
        super().__init__(orientation='L', unit='mm', format='A4') # 297 x 210 mm
        self.titulo_escola = sanitizar(titulo_escola)
        self.set_auto_page_break(auto=False)

    def header(self):
        if self.page_no() > 2: # Não desenha header na Capa nem no Sumário
            self.set_font('Helvetica', 'B', 8)
            self.set_text_color(100, 116, 139)
            # Margem superior de 8mm
            self.set_xy(15, 6)
            self.cell(150, 5, self.titulo_escola, 0, 0, 'L')
            self.set_xy(170, 6)
            self.cell(112, 5, "ENCICLOPÉDIA VISUAL DE COMPUTAÇÃO", 0, 0, 'R')
            self.set_draw_color(226, 232, 240)
            self.line(15, 12, 282, 12)

    def footer(self):
        if self.page_no() > 2:
            self.set_draw_color(226, 232, 240)
            self.line(15, 202, 282, 202)
            self.set_font('Helvetica', '', 8)
            self.set_text_color(148, 163, 184)
            self.set_xy(15, 203)
            self.cell(150, 5, "Material Didático para Estudo - Padrão A4 Paisagem", 0, 0, 'L')
            self.set_xy(230, 203)
            self.cell(52, 5, f"Página {self.page_no()}", 0, 0, 'R')

def desenhar_card(pdf, x, y, w, h, titulo, bullets, cor_borda, cor_fundo, is_code=False):
    """Desenha um card de sketchnote com pílula de título e lista de pontos."""
    # Fundo do card
    pdf.set_fill_color(*cor_fundo)
    pdf.set_draw_color(*cor_borda)
    pdf.set_line_width(0.6)
    pdf.rect(x, y, w, h, 'DF')

    # Pílula de título
    pdf.set_fill_color(*cor_borda)
    pdf.set_text_color(255, 255, 255)
    pdf.set_font('Helvetica', 'B', 8)
    
    largura_pilula = min(pdf.get_string_width(titulo) + 6, w - 8)
    pdf.rect(x + 4, y - 3, largura_pilula, 6, 'F')
    pdf.set_xy(x + 5, y - 2.5)
    pdf.cell(largura_pilula - 2, 5, titulo, 0, 0, 'C')

    # Conteúdo / Bullets
    pdf.set_xy(x + 4, y + 5)
    pdf.set_text_color(30, 41, 59)
    pdf.set_font('Helvetica', '', 8)

    offset_y = y + 5
    for b in bullets:
        b_limpo = sanitizar(b)
        if offset_y > y + h - 6:
            break
        pdf.set_xy(x + 4, offset_y)
        
        if is_code and ("=" in b_limpo or "(" in b_limpo):
            pdf.set_fill_color(241, 245, 249)
            pdf.set_draw_color(148, 163, 184)
            pdf.set_font('Courier', 'B', 7.5)
            pdf.rect(x + 4, offset_y, w - 8, 5, 'DF')
            pdf.set_xy(x + 6, offset_y)
            pdf.cell(w - 12, 5, b_limpo, 0, 0, 'L')
            pdf.set_font('Helvetica', '', 8)
            offset_y += 6
        else:
            pdf.multi_cell(w - 8, 3.8, f"- {b_limpo}")
            offset_y = pdf.get_y() + 1.2

def gerar_ebook_escola(pasta_escola, nome_escola, descricao_escola):
    caminho_escola = os.path.join(BASE_DIR, pasta_escola)
    pasta_json = os.path.join(caminho_escola, "json")
    pasta_pdf = os.path.join(caminho_escola, "pdf")

    if not os.path.exists(pasta_json):
        return None

    arquivos = sorted([f for f in os.listdir(pasta_json) if f.endswith(".json")])
    if not arquivos:
        return None

    print(f"\n📖 Compilando E-book: {nome_escola} ({len(arquivos)} mapas)...")

    pdf = CadernoPDF(nome_escola)

    # -------------------------------------------------------------------------
    # PÁGINA 1: CAPA PROFISSIONAL
    # -------------------------------------------------------------------------
    pdf.add_page()
    # Fundo escuro premium
    pdf.set_fill_color(15, 23, 42)
    pdf.rect(0, 0, 297, 210, 'F')

    # Borda decorativa azul
    pdf.set_draw_color(56, 189, 248)
    pdf.set_line_width(1.5)
    pdf.rect(10, 10, 277, 190, 'D')

    # Título da Capa
    pdf.set_text_color(56, 189, 248)
    pdf.set_font('Helvetica', 'B', 14)
    pdf.set_xy(20, 35)
    pdf.cell(257, 10, "ENCICLOPÉDIA VISUAL DE COMPUTAÇÃO", 0, 1, 'C')

    pdf.set_text_color(255, 255, 255)
    pdf.set_font('Helvetica', 'B', 24)
    pdf.set_xy(20, 52)
    pdf.multi_cell(257, 12, sanitizar(nome_escola.upper()), 0, 'C')

    pdf.set_text_color(148, 163, 184)
    pdf.set_font('Helvetica', '', 11)
    pdf.set_xy(35, 90)
    pdf.multi_cell(227, 7, sanitizar(descricao_escola), 0, 'C')

    # Badge de Metodologia
    pdf.set_fill_color(30, 41, 59)
    pdf.set_draw_color(71, 85, 105)
    pdf.rect(60, 130, 177, 24, 'DF')
    pdf.set_text_color(255, 255, 255)
    pdf.set_font('Helvetica', 'B', 10)
    pdf.set_xy(60, 134)
    pdf.cell(177, 6, "METODOLOGIA TRÍPLICE", 0, 1, 'C')
    pdf.set_font('Helvetica', '', 9)
    pdf.set_text_color(203, 213, 225)
    pdf.cell(177, 6, "UNINTER (Base Acadêmica) + ALURA (Mercado) + FEYNMAN (Didática Visual)", 0, 1, 'C')

    pdf.set_font('Helvetica', 'B', 10)
    pdf.set_text_color(56, 189, 248)
    pdf.set_xy(20, 175)
    pdf.cell(257, 6, f"VOLUME COM {len(arquivos)} MAPAS MENTAIS ESTRUTURADOS EM A4 PAISAGEM", 0, 1, 'C')

    # -------------------------------------------------------------------------
    # PÁGINA 2+: SUMÁRIO ANALÍTICO (Com paginação dinâmica se > 65 mapas)
    # -------------------------------------------------------------------------
    pdf.add_page()
    pdf.set_fill_color(248, 250, 252)
    pdf.rect(0, 0, 297, 210, 'F')

    pdf.set_font('Helvetica', 'B', 16)
    pdf.set_text_color(15, 23, 42)
    pdf.set_xy(15, 16)
    pdf.cell(267, 10, "SUMÁRIO DO VOLUME", 0, 1, 'L')
    pdf.set_draw_color(15, 23, 42)
    pdf.set_line_width(0.8)
    pdf.line(15, 26, 282, 26)

    mapas_dados = []
    itens_sumario = []
    for idx, arq in enumerate(arquivos):
        with open(os.path.join(pasta_json, arq), "r", encoding="utf-8") as f:
            d = json.load(f)
            mapas_dados.append(d)
            itens_sumario.append((d.get('id', idx+1), sanitizar(d.get('title', arq))))

    # Calcula quantas páginas de sumário teremos
    itens_por_pagina = 64 # 32 por coluna
    pag_sumario_extras = 1 if len(itens_sumario) > itens_por_pagina else 0

    col1_x, col2_x = 15, 150
    y_start = 32
    col_y = y_start
    coluna_atual = 1

    pdf.set_font('Helvetica', '', 8.5)
    for idx, (id_item, tit_item) in enumerate(itens_sumario):
        if idx > 0 and idx % itens_por_pagina == 0:
            # Nova página de continuação do sumário
            pdf.add_page()
            pdf.set_fill_color(248, 250, 252)
            pdf.rect(0, 0, 297, 210, 'F')
            pdf.set_font('Helvetica', 'B', 16)
            pdf.set_text_color(15, 23, 42)
            pdf.set_xy(15, 16)
            pdf.cell(267, 10, "SUMÁRIO DO VOLUME (CONTINUAÇÃO)", 0, 1, 'L')
            pdf.set_draw_color(15, 23, 42)
            pdf.set_line_width(0.8)
            pdf.line(15, 26, 282, 26)
            pdf.set_font('Helvetica', '', 8.5)
            col_y = y_start
            coluna_atual = 1

        elif idx > 0 and idx % (itens_por_pagina // 2) == 0:
            coluna_atual = 2
            col_y = y_start

        x_pos = col1_x if coluna_atual == 1 else col2_x
        num_pag_mapa = idx + 3 + pag_sumario_extras
        titulo_formatado = f"#{id_item:03d} - {tit_item}"[:54]

        pdf.set_xy(x_pos, col_y)
        pdf.cell(115, 4.6, titulo_formatado, 0, 0, 'L')
        pdf.cell(15, 4.6, f"pág. {num_pag_mapa}", 0, 1, 'R')
        col_y += 4.6

    # -------------------------------------------------------------------------
    # PÁGINAS DOS MAPAS MENTAIS (1 Mapa Artístico Sketchnote por Página A4)
    # -------------------------------------------------------------------------
    from gerar_render_sketchnote_realista import renderizar_mapa_direto, obter_navegador_headless
    try:
        nav = obter_navegador_headless()
    except Exception:
        nav = None

    pasta_imagens = os.path.join(caminho_escola, "imagens")
    os.makedirs(pasta_imagens, exist_ok=True)

    for idx, d in enumerate(mapas_dados, 1):
        id_num = d.get('id', idx)
        nome_png = f"mapa_{id_num:03d}.png"
        caminho_png = os.path.join(pasta_imagens, nome_png)

        # Se a imagem em alta resolução ainda não existir ou for inválida, gera na hora
        if not os.path.exists(caminho_png) or os.path.getsize(caminho_png) < 10000:
            try:
                renderizar_mapa_direto(d, caminho_png, navegador=nav)
            except Exception as e:
                print(f"  ⚠️ Aviso: não foi possível renderizar PNG para #{id_num}: {e}")

        # Insere a lâmina artística completa na folha A4 Paisagem (297 x 210 mm)
        if os.path.exists(caminho_png) and os.path.getsize(caminho_png) > 10000:
            pdf.add_page()
            pdf.image(caminho_png, x=0, y=0, w=297, h=210)
        else:
            # Fallback de segurança se headless falhar
            pdf.add_page()
            pdf.set_fill_color(250, 248, 245)
            pdf.rect(0, 0, 297, 210, 'F')
            titulo_central = sanitizar(d.get('title', 'TEMA')).upper()
            pdf.set_xy(20, 95)
            pdf.set_font('Helvetica', 'B', 16)
            pdf.set_text_color(15, 23, 42)
            pdf.cell(257, 10, f"#{id_num}. {titulo_central}", 0, 1, 'C')

    # Salva o arquivo PDF final
    nome_pdf_limpo = pasta_escola.replace("/", "_") + "_A4_PAISAGEM.pdf"
    saida_pdf = os.path.join(pasta_pdf, nome_pdf_limpo)
    pdf.output(saida_pdf)
    print(f"✅ E-book gerado com sucesso: {saida_pdf} ({pdf.page_no()} páginas)")
    return saida_pdf

def compilar_todos():
    from organizar_acervo import ESCOLAS_CONFIG
    print("=" * 70)
    print("🚀 COMPILANDO E-BOOKS DAS ESCOLAS EM A4 PAISAGEM PARA IMPRESSÃO...")
    print("=" * 70)
    
    total_gerados = 0
    for esc in ESCOLAS_CONFIG:
        res = gerar_ebook_escola(esc["pasta"], esc["nome"], esc["descricao"])
        if res:
            total_gerados += 1

    print("\n" + "=" * 70)
    print(f"🏁 COMPILAÇÃO FINALIZADA! {total_gerados} E-books em PDF prontos para envio à gráfica!")
    print("=" * 70)

if __name__ == "__main__":
    compilar_todos()
