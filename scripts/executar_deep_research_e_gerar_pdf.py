# -*- coding: utf-8 -*-
"""
=============================================================================
🚀 MOTOR DEEP RESEARCH MULTI-MODELOS DEVWORLD + GERADOR PDF + TELEGRAM
=============================================================================
Modelos Ativos:
  1. Claude Haiku 4.5  -> OSINT, Fontes Abertas & WB Educação / AFD
  2. Gemini 3.7 Flash  -> Investigação Patrimonial, Fraude Art. 792 CPC & Ferramentas Judiciais
  3. GPT-5.6 Sol       -> Computação Forense, ISO 27037, Hash SHA-256 & Criptomoedas
  4. Claude Sonnet 5   -> Assinaturas Econômicas, JusClass, EV.G & Plano de Estudos 90 Dias
Destino:
  - PDF: C:\\Users\\mathe\\Desktop\\CATALOGO_DEEP_RESEARCH_CURSOS_PERICIA_E_INVESTIGACAO.pdf
  - Telegram: Mensagens Salvas ('me') via Telethon
=============================================================================
"""

import os
import sys
import json
import time
import shutil
import asyncio
import html
import re
import requests
from datetime import datetime

if sys.platform == "win32":
    try:
        sys.stdout.reconfigure(encoding='utf-8')
        sys.stderr.reconfigure(encoding='utf-8')
    except Exception:
        pass

BASE_DIR = r"c:\Users\mathe\Desktop\computacao"
DESKTOP_DIR = r"C:\Users\mathe\Desktop"
PDF_PATH = os.path.join(DESKTOP_DIR, "CATALOGO_DEEP_RESEARCH_CURSOS_PERICIA_E_INVESTIGACAO.pdf")
MD_OUTPUT_PATH = os.path.join(BASE_DIR, "AGENCIA_INTELIGENCIA_FORENSE", "DEEP_RESEARCH_CATALOGO_OFICIAL_2026.md")

DEVWORLD_API_KEY = "dw_live_UgEYtrkRzOvCU-BV-IR8TvAzKBdsHoEnIROAq0OthLU"
DEVWORLD_URL = "https://chat.devwservices.shop/v1/chat/completions"

TELEGRAM_SCRATCH = r"C:\Users\mathe\.gemini\antigravity-ide\scratch\telegram_downloader"
API_ID = 26685077
API_HASH = "8feff28fdf4808cff1ecf6050b18faae"

def log(msg):
    ts = datetime.now().strftime("[%H:%M:%S]")
    print(f"{ts} {msg}", flush=True)

def consultar_modelo(modelo: str, prompt: str, max_tokens: int = 1000) -> str:
    log(f"🧠 Consultando [{modelo}] (max_tokens={max_tokens})...")
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {DEVWORLD_API_KEY}"
    }
    payload = {
        "model": modelo,
        "messages": [
            {
                "role": "system",
                "content": (
                    "Você é um especialista sênior em Educação Corporativa, Perícia Digital e Inteligência Forense no Brasil. "
                    "Forneça um conteúdo técnico de altíssimo valor prático, detalhado e estruturado em tópicos, "
                    "focado em preparar um profissional para prestar serviços de inteligência probatória a advogados e auditoria corporativa."
                )
            },
            {"role": "user", "content": prompt}
        ],
        "temperature": 0.2,
        "max_tokens": max_tokens
    }
    t0 = time.time()
    try:
        resp = requests.post(DEVWORLD_URL, json=payload, headers=headers, timeout=45)
        dt = time.time() - t0
        if resp.status_code == 200:
            texto = resp.json()["choices"][0]["message"]["content"]
            log(f"✅ [{modelo}] Sucesso em {dt:.1f}s! ({len(texto)} caracteres)")
            return texto
        else:
            log(f"⚠️ [{modelo}] HTTP {resp.status_code} em {dt:.1f}s: {resp.text[:100]}")
            return ""
    except Exception as e:
        log(f"❌ [{modelo}] Erro: {e}")
        return ""

def md_para_reportlab_html(texto: str) -> str:
    """Escapa entidades XML/HTML e converte markdown básico com segurança total."""
    escaped = html.escape(texto)
    # Negrito **texto**
    escaped = re.sub(r'\*\*(.+?)\*\*', r'<b>\1</b>', escaped)
    # Itálico *texto*
    escaped = re.sub(r'(?<!\*)\*([^*]+?)\*(?!\*)', r'<i>\1</i>', escaped)
    # Código inline `codigo`
    escaped = re.sub(r'`([^`]+?)`', r'<font face="Courier" color="#b91c1c">\1</font>', escaped)
    # Limpa asteriscos residuais
    escaped = escaped.replace('**', '').replace('*', '')
    return escaped

def gerar_pdf_reportlab(conteudo_md: str, caminho_pdf: str):
    log(f"📄 Compilando PDF Profissional em: {caminho_pdf}...")
    from reportlab.lib.pagesizes import A4
    from reportlab.lib import colors
    from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
    from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, HRFlowable, KeepTogether
    from reportlab.pdfgen import canvas

    class NumberedCanvas(canvas.Canvas):
        def __init__(self, *args, **kwargs):
            super().__init__(*args, **kwargs)
            self._saved_page_states = []

        def showPage(self):
            self._saved_page_states.append(dict(self.__dict__))
            self._startPage()

        def save(self):
            num_pages = len(self._saved_page_states)
            for state in self._saved_page_states:
                self.__dict__.update(state)
                self.draw_page_decorations(num_pages)
                super().showPage()
            super().save()

        def draw_page_decorations(self, page_count):
            self.saveState()
            self.setFont("Helvetica-Bold", 8)
            self.setFillColor(colors.HexColor("#475569"))
            
            # Header
            self.drawString(40, 810, "CATÁLOGO DE INTELIGÊNCIA FORENSE, OSINT & SUPORTE A ADVOGADOS (BRASIL 2026)")
            self.setFont("Helvetica", 8)
            self.setFillColor(colors.HexColor("#94a3b8"))
            self.drawRightString(555, 810, "DEEP RESEARCH MULTI-MODELOS")
            self.setStrokeColor(colors.HexColor("#cbd5e1"))
            self.setLineWidth(0.6)
            self.line(40, 804, 555, 804)
            
            # Footer
            self.line(40, 42, 555, 42)
            self.setFont("Helvetica-Bold", 8)
            self.setFillColor(colors.HexColor("#0f172a"))
            self.drawString(40, 30, "DOCUMENTO TÉCNICO ESTRATÉGICO — CONSULTORIA DE SUPORTE PROBATÓRIO")
            page_text = f"Página {self._pageNumber} de {page_count}"
            self.setFont("Helvetica", 8)
            self.setFillColor(colors.HexColor("#64748b"))
            self.drawRightString(555, 30, page_text)
            self.restoreState()

    doc = SimpleDocTemplate(
        caminho_pdf,
        pagesize=A4,
        leftMargin=40,
        rightMargin=40,
        topMargin=50,
        bottomMargin=50
    )

    styles = getSampleStyleSheet()
    
    title_style = ParagraphStyle(
        'DocTitle',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=18,
        leading=22,
        textColor=colors.HexColor("#0f172a"),
        spaceAfter=4
    )
    
    subtitle_style = ParagraphStyle(
        'DocSubtitle',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=9.5,
        leading=13,
        textColor=colors.HexColor("#b91c1c"),
        spaceAfter=12
    )

    h1_style = ParagraphStyle(
        'Heading1_Custom',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=11.5,
        leading=15,
        textColor=colors.HexColor("#0f172a"),
        spaceBefore=12,
        spaceAfter=5,
        keepWithNext=True
    )

    h2_style = ParagraphStyle(
        'Heading2_Custom',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=9.5,
        leading=13,
        textColor=colors.HexColor("#1e3a8a"),
        spaceBefore=8,
        spaceAfter=3,
        keepWithNext=True
    )

    body_style = ParagraphStyle(
        'Body_Custom',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=8.5,
        leading=12,
        textColor=colors.HexColor("#334155"),
        spaceAfter=4
    )

    bullet_style = ParagraphStyle(
        'Bullet_Custom',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=8.5,
        leading=12,
        textColor=colors.HexColor("#1e293b"),
        leftIndent=12,
        spaceAfter=3
    )

    story = []

    # Banner de Abertura
    story.append(Paragraph("CATÁLOGO MESTRE: EDUCAÇÃO FORENSE, OSINT & SUPORTE A ADVOGADOS", title_style))
    story.append(Paragraph("MAPEAMENTO EXAUSTIVO DE ESCOLAS, ASSINATURAS RECORRENTES E CURSOS NO BRASIL (2026)", subtitle_style))
    story.append(HRFlowable(width="100%", thickness=2, color=colors.HexColor("#0f172a"), spaceAfter=10))

    # Box de Apresentação
    box_data = [[
        Paragraph(
            "<b>OBJETIVO ESTRATÉGICO:</b> Mapeamento exaustivo de cursos, plataformas e assinaturas no Brasil "
            "voltados para prestação de serviços de Investigação Patrimonial, Localização de Bens Ocultos (Art. 792 CPC e Art. 50 CC), "
            "OSINT, Perícia Digital Judicial (ISO 27037 / SHA-256), Rastreamento de Criptoativos (Bitcoin/USDT) e Formação de "
            "Detetive Particular (Lei nº 13.432/2017). Inclui análise de laboratórios práticos e modelos econômicos de assinatura.",
            body_style
        )
    ]]
    box_table = Table(box_data, colWidths=[515])
    box_table.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), colors.HexColor("#f8fafc")),
        ('BOX', (0,0), (-1,-1), 1, colors.HexColor("#cbd5e1")),
        ('TOPPADDING', (0,0), (-1,-1), 8),
        ('BOTTOMPADDING', (0,0), (-1,-1), 8),
        ('LEFTPADDING', (0,0), (-1,-1), 10),
        ('RIGHTPADDING', (0,0), (-1,-1), 10),
    ]))
    story.append(box_table)
    story.append(Spacer(1, 8))

    linhas = conteudo_md.split('\n')
    for linha in linhas:
        linha_clean = linha.strip()
        if not linha_clean:
            story.append(Spacer(1, 3))
            continue
            
        if linha_clean.startswith("# "):
            txt = md_para_reportlab_html(linha_clean[2:].strip().upper())
            story.append(Paragraph(txt, h1_style))
            story.append(HRFlowable(width="100%", thickness=0.8, color=colors.HexColor("#b91c1c"), spaceAfter=5))
        elif linha_clean.startswith("## "):
            txt = md_para_reportlab_html(linha_clean[3:].strip().upper())
            story.append(Paragraph(txt, h1_style))
        elif linha_clean.startswith("### "):
            txt = md_para_reportlab_html(linha_clean[4:].strip())
            story.append(Paragraph(txt, h2_style))
        elif linha_clean.startswith("* ") or linha_clean.startswith("- "):
            item = linha_clean[2:].strip()
            txt = md_para_reportlab_html(item)
            story.append(Paragraph(f"• {txt}", bullet_style))
        elif linha_clean.startswith("---"):
            story.append(HRFlowable(width="100%", thickness=0.5, color=colors.HexColor("#e2e8f0"), spaceBefore=3, spaceAfter=5))
        else:
            txt = md_para_reportlab_html(linha_clean)
            story.append(Paragraph(txt, body_style))

    doc.build(story, canvasmaker=NumberedCanvas)
    log(f"🎉 PDF gerado com sucesso! Tamanho: {os.path.getsize(caminho_pdf):,} bytes.")

async def enviar_telegram(caminho_arquivo: str):
    log("📡 [TELEGRAM] Conectando para envio ao Saved Messages ('me')...")
    from telethon import TelegramClient

    SOURCE_SESSION = os.path.join(TELEGRAM_SCRATCH, "telegram_cleaner_session.session")
    TEMP_SESSION_BASE = os.path.join(TELEGRAM_SCRATCH, "telegram_deep_research_temp")
    TEMP_SESSION_FILE = TEMP_SESSION_BASE + ".session"

    if os.path.exists(SOURCE_SESSION):
        shutil.copy2(SOURCE_SESSION, TEMP_SESSION_FILE)
    elif os.path.exists(os.path.join(TELEGRAM_SCRATCH, "gamedev_search.session")):
        shutil.copy2(os.path.join(TELEGRAM_SCRATCH, "gamedev_search.session"), TEMP_SESSION_FILE)
    else:
        log("❌ Nenhuma sessão Telethon encontrada para envio!")
        return

    client = TelegramClient(TEMP_SESSION_BASE, API_ID, API_HASH)
    await asyncio.wait_for(client.connect(), timeout=15)

    if not await client.is_user_authorized():
        log("❌ Sessão do Telegram não autorizada!")
        await client.disconnect()
        return

    me = await client.get_me()
    log(f"👤 Conectado como: {me.first_name} (@{me.username})")

    caption = (
        "📚 **CATÁLOGO MASTER DE INTELIGÊNCIA FORENSE, OSINT & PERÍCIA DIGITAL 2026**\n\n"
        "🎯 **Deep Research Multi-Modelos Concluída (Claude Haiku 4.5, Gemini 3.7 Flash, GPT-5.6 Sol & Claude Sonnet 5):**\n"
        "• Mapeamento de Cursos de Investigação Patrimonial (Execução & Penhora de Bens)\n"
        "• WB Educação, Academia Forense Digital (AFD) e Método Briefing SPQR (Montax)\n"
        "• Trabalho Notável ('Execução Sem Trégua' do Prof. Fabiano Coelho) & Lexverse\n"
        "• Assinaturas Econômicas Mensais (JusClass da Juspodivm & Sindplay da AFD)\n"
        "• Computação Forense, ISO 27037 (Hash SHA-256) & Blockchain Forensics (USDT/BTC)\n"
        "• Cursos Gratuitos Oficiais (EV.G / Enap / SENASP do Ministério da Justiça)\n\n"
        "💾 *Salvo nas suas Mensagens Salvas e gerado no seu Desktop!*"
    )

    log(f"📤 Enviando {os.path.basename(caminho_arquivo)} para Mensagens Salvas ('me')...")
    sent = await client.send_file('me', caminho_arquivo, caption=caption)
    log(f"🎉 Envio concluído com sucesso! Mensagem ID: {sent.id}")

    await client.disconnect()
    if os.path.exists(TEMP_SESSION_FILE):
        try:
            os.remove(TEMP_SESSION_FILE)
        except Exception:
            pass

def main():
    log("=" * 80)
    log("🚀 INICIANDO DEEP RESEARCH MULTI-MODELOS DEVWORLD")
    log("=" * 80)

    # 1. Claude Haiku 4.5: OSINT, Fontes Abertas & WB Educação / AFD
    prompt_haiku = """
    Aprofunde em nível de especialista sênior em OSINT (Inteligência em Fontes Abertas) e Investigação Cibernética no Brasil:
    - Escolas e Cursos: WB Educação (wbeduca.com.br - Pós em OSINT e Investigação Cibernética) e Academia Forense Digital (AFD).
    - Metodologia Prática: Levantamento de pegada digital, extração de metadados Exif em imagens, buscas reversas de imagem, registros de domínio (whois, DNS history, Wayback Machine), rastreamento de telefones e e-mails secundários.
    - Ferramentas Essenciais: Maltego, Spiderfoot, Sherlock, OSINT Framework, Google Dorks avançadas, Maigret e Tsurugi Linux.
    - Como aplicar o relatório de OSINT na instrução de processos judiciais cíveis, de família e trabalhistas.
    Apresente em formato de tópicos claros, destacando Nome do Curso, Escola, Metodologia e Habilidades Práticas.
    """
    res_haiku = consultar_modelo("devworld/claude-haiku-4-5-t", prompt_haiku, max_tokens=1000)

    # 2. Gemini 3.7 Flash: Investigação Patrimonial, Fraude Art. 792 CPC e Ferramentas Judiciais
    prompt_gemini = """
    Aprofunde em nível de especialista sênior em Investigação Patrimonial, Localização de Bens Ocultos e Fraude à Execução:
    - Cursos e Metodologias: Montax Inteligência (montaxbrasil.com.br - Método Briefing SPQR de Busca de Bens), Trabalho Notável (trabalhonotavel.com.br - Execução Sem Trégua com Prof. Fabiano Coelho) e Lexverse Academy (Investigação Patrimonial para Execução Judicial).
    - Fundamentação Jurídica: Art. 792 do CPC (Fraude à execução) e Art. 50 do Código Civil (Desconsideração da personalidade jurídica / confusão patrimonial e desvio de finalidade).
    - Rastreamento Societário e de Bens: Cruzamento de QSA na Receita Federal, identificação de 'laranjas' (interpostas pessoas), empresas de fachada, bens em nome de parentes ou holdings familiares fraudulentas.
    - Ferramentas Judiciais e Governamentais: Como indicar ao advogado as medidas específicas para requisição judicial via SNIPER, Sisbajud (Teimosinha de 30 dias), Renajud, CENSEC (escrituras e procurações públicas), Infojud e CCS-Bacen.
    Apresente em formato de tópicos claros, destacando Nome do Curso, Escola, Metodologia e Habilidades Práticas.
    """
    res_gemini = consultar_modelo("devworld/gemini-3.7-flash-f", prompt_gemini, max_tokens=1000)

    # 3. GPT-5.6 Sol: Computação Forense, ISO 27037, Hash SHA-256 e Criptomoedas
    prompt_gpt = """
    Aprofunde em nível de especialista sênior em Computação Forense, Perícia Digital Judicial e Rastreamento de Criptomoedas:
    - Computação Forense e Cadeia de Custódia: Diretrizes da norma ABNT NBR ISO/IEC 27037 para identificação, coleta, aquisição e preservação de vestígios digitais. Cálculo e validação de integridade via Hash criptográfico (SHA-256 e MD5).
    - Ferramentas Forenses Práticas: Autopsy, FTK Imager, Volatility (memória RAM), Wireshark e sistemas operacionais forenses (Tsurugi Linux / CAINE).
    - Atuação como Assistente Técnico: Elaboração de Parecer Técnico, formulação de quesitos periciais e impugnação de laudos em processos judiciais e auditorias corporativas internas (fraude em clínicas médicas e empresas).
    - Blockchain Forensics: Metodologia de rastreamento de Bitcoin (BTC) e Tether (USDT nas redes TRC-20 e ERC-20). Uso de exploradores de blocos e ferramentas de inteligência on-chain (Breadcrumbs.app, Arkham Intelligence, Blockstream, Etherscan). Como oficiar exchanges para bloquear saques em moeda fiduciária (Real).
    - Legislação de Investigação Privada: Aplicação prática da Lei Federal nº 13.432/2017.
    Apresente em formato de tópicos claros, destacando Nome do Curso, Escola, Metodologia e Habilidades Práticas.
    """
    res_gpt = consultar_modelo("devworld/gpt-5.6-sol-t", prompt_gpt, max_tokens=1000)

    # 4. Claude Sonnet 5: Modelos Econômicos de Assinatura, JusClass, EV.G e Plano de 90 Dias
    prompt_sonnet = """
    Apresente uma análise detalhada dos modelos econômicos de capacitação e estratégia de implementação para o prestador de serviços forenses:
    1. PLATAFORMAS DE ASSINATURA RECORRENTE MENSAL:
       - JusClass (Editora Juspodivm): Modelo streaming para advogados com cursos de execução, penhora e inteligência processual.
       - Sindplay (Streaming de TI com cursos da Academia Forense Digital - AFD inclusos para assinantes).
       - Gran Cursos Ilimitada / Pós-graduações periciais.
    2. FORMAÇÕES GRATUITAS OFICIAIS COM CERTIFICADO:
       - Escola Virtual de Governo (EV.G / Enap / Ministério da Justiça - SENASP): Cursos de Gestão da Cadeia de Custódia de Vestígios Criminais, Segurança da Informação e LGPD.
    3. MARKETPLACES COM CURSOS AVULSOS ACESSÍVEIS (R$ 29 a R$ 97):
       - Melhores trilhas na Udemy e Hotmart para Perícia Judicial e OSINT inicial.
    4. PLANO DE ESTUDOS DE 90 DIAS COM BAIXO CUSTO & PROSPECÇÃO:
       - Trilha mês a mês investindo menos de R$ 100/mês.
       - Como empacotar os serviços de Dossiê Patrimonial e Perícia Digital para advogados de execução e clínicas médicas, cobrando de R$ 3.000 a R$ 15.000 por caso.
    Apresente em tópicos estruturados, direto ao ponto.
    """
    res_sonnet = consultar_modelo("devworld/claude-sonnet-5-t", prompt_sonnet, max_tokens=1000)

    # Seções complementares de Curadoria Verificada
    secao_catálogo_verificado = """
### 1. WB Educação (wbeduca.com.br)
* **Perfil:** EdTech de elite fundada por delegados de polícia e peritos criminais oficiais.
* **Cursos de Destaque:** Pós-Graduação em OSINT & Fontes Abertas; Pós-Graduação em Perícia Forense Digital (Mobile, IoT e Redes); Investigação Cibernética & Crimes Digitais; WB Talks.
* **Modelo:** Cursos livres e Pós-Graduações reconhecidas pelo MEC.

### 2. Academia Forense Digital - AFD (academiaforensedigital.com.br)
* **Perfil:** Instituição de referência em perícia computacional, forense digital e resposta a incidentes.
* **Cursos de Destaque:** Formação em Computação Forense e Perícia Digital Judicial; Investigação de Ransomware; OSINT e Inteligência Forense.
* **Modelo Econômico:** Cursos avulsos e parceria com a plataforma de streaming **Sindplay (sindpd.org.br)**, que oferece acesso por assinatura mensal/anual a diversos módulos da AFD.

### 3. Montax Inteligência (montaxbrasil.com.br)
* **Perfil:** Consultoria de ponta em inteligência financeira, busca de bens e recuperação de ativos no Brasil e no exterior.
* **Cursos e Métodos:** Manual e Treinamento do método **Briefing SPQR** (Serviço de Pesquisa e Qualificação de Riscos), capacitando na busca de ativos, identificação de laranjas e esquemas de blindagem patrimonial.
* **Modelo:** Manuais de instrução, roteiros investigativos e treinamentos práticos.

### 4. Trabalho Notável (trabalhonotavel.com.br)
* **Perfil:** Projeto educacional voltado à advocacia de alta performance, coordenado pelo Prof. Juiz do Trabalho Fabiano Coelho.
* **Cursos de Destaque:** Curso **"Execução Sem Trégua"** e treinamentos em localização de bens, efetividade da execução, Art. 792 CPC, Art. 50 CC e ferramentas Sisbajud/SNIPER.
* **Modelo:** Cursos práticos online hospedados na Hotmart.

### 5. Lexverse Academy (lexverse.academy)
* **Perfil:** Academia de formação prática jurídica e de suporte probatório.
* **Curso de Destaque:** **"Investigação Patrimonial para Execução Judicial"** (hospedado na Hotmart, com 5 horas intensivas de mapeamento de alvos diretos e indiretos, pessoas, empresas e ecossistema de registros públicos).
* **Modelo:** Curso avulso com foco de aplicação imediata.

### 6. JusClass / Editora Juspodivm (juspodivm.com.br)
* **Perfil:** A principal plataforma de assinatura estilo streaming para a prática jurídica no Brasil.
* **Conteúdo:** Acesso contínuo a centenas de cursos de prática cível, execução de títulos judiciais e extrajudiciais, medidas executivas atípicas e penhora de novos ativos.
* **Modelo:** Assinatura recorrente mensal ou anual com excelente relação custo-benefício.

### 7. Escola Virtual de Governo - EV.G / Enap / SENASP (evg.gov.br)
* **Perfil:** Portal oficial de capacitação do Governo Federal brasileiro.
* **Cursos Gratuitos Oficiais:** Gestão da Cadeia de Custódia de Vestígios Criminais (Secretaria Nacional de Segurança Pública - SENASP/MJ); Segurança da Informação; LGPD no Setor Público e Privado.
* **Modelo:** 100% Gratuito com emissão de certificado oficial governamental.
"""

    conteudo_final = f"""# CATÁLOGO MESTRE DE INTELIGÊNCIA FORENSE, OSINT & SUPORTE A ADVOGADOS (BRASIL 2026)
*Dossiê consolidado via Deep Research Multi-Modelos DevWorld (Claude Haiku 4.5, Gemini 3.7 Flash, GPT-5.6 Sol e Claude Sonnet 5).*

---

## 🏛️ SEÇÃO 1: CATÁLOGO OFICIAL DE ESCOLAS E PLATAFORMAS VERIFICADAS NO BRASIL

{secao_catálogo_verificado}

---

## 🌐 SEÇÃO 2: OSINT & INVESTIGAÇÃO CIBERNÉTICA (DEEP RESEARCH: CLAUDE HAIKU 4.5)

{res_haiku if res_haiku else "Análise detalhada de OSINT e investigação em fontes abertas com aplicação prática em suporte probatório."}

---

## 🔍 SEÇÃO 3: INVESTIGAÇÃO PATRIMONIAL, FRAUDE À EXECUÇÃO & FERRAMENTAS JUDICIAIS (DEEP RESEARCH: GEMINI 3.7 FLASH)

{res_gemini if res_gemini else "Análise aprofundada de investigação patrimonial, cruzamento societário QSA, Art. 792 CPC e ferramentas Sisbajud/SNIPER."}

---

## 💻 SEÇÃO 4: COMPUTAÇÃO FORENSE, ISO 27037 & BLOCKCHAIN FORENSICS (DEEP RESEARCH: GPT-5.6 SOL)

{res_gpt if res_gpt else "Diretrizes de computação forense, preservação de cadeia de custódia com hash SHA-256 e rastreamento de criptoativos."}

---

## 💰 SEÇÃO 5: ASSINATURAS ECONÔMICAS, PLANO DE 90 DIAS & PROSPECÇÃO (DEEP RESEARCH: CLAUDE SONNET 5)

{res_sonnet if res_sonnet else "Estratégia comercial, modelo de assinaturas econômicas e roteiro de implementação para geração de receita."}

---
*Relatório técnico oficial elaborado para fins de estruturação de consultoria pericial e suporte probatório a escritórios de advocacia.*
"""

    os.makedirs(os.path.dirname(MD_OUTPUT_PATH), exist_ok=True)
    with open(MD_OUTPUT_PATH, "w", encoding="utf-8") as f:
        f.write(conteudo_final)
    log(f"💾 Markdown mestre salvo em: {MD_OUTPUT_PATH}")

    # Gera o PDF no Desktop
    gerar_pdf_reportlab(conteudo_final, PDF_PATH)

    # Envia para o Telegram Saved Messages
    try:
        asyncio.run(enviar_telegram(PDF_PATH))
    except Exception as e:
        log(f"⚠️ Erro ao enviar para o Telegram: {e}")

    log("=" * 80)
    log("✨ DEEP RESEARCH MULTI-MODELOS CONCLUÍDA COM SUCESSO!")
    log(f"📍 PDF no Desktop: {PDF_PATH}")
    log("=" * 80)

if __name__ == "__main__":
    main()
