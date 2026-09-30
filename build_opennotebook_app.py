import os
import json
import glob

DESKTOP = r"C:\Users\matheus\Desktop"
TRANS_DIR = os.path.join(DESKTOP, "Clube_do_Consultor_Transcricoes")

# Carregar as 32 transcrições
trans_files = sorted(glob.glob(os.path.join(TRANS_DIR, "aula_*.txt")))
lessons_list = []

for f in trans_files:
    fname = os.path.basename(f)
    num = fname.replace("aula_", "").replace(".txt", "")
    with open(f, "r", encoding="utf-8", errors="ignore") as fp:
        raw_text = fp.read().strip()
    
    # Extrair título ou resumo
    summary = raw_text[:280].replace("\n", " ").strip()
    lessons_list.append({
        "id": f"aula_{num}",
        "num": num,
        "title": f"Aula {num} — Módulo de Consultoria Estratégica",
        "size": len(raw_text),
        "text": raw_text,
        "summary": summary
    })

lessons_json = json.dumps(lessons_list, ensure_ascii=False)

# Criar o HTML da aplicação OpenNotebook
html_content = f"""<!DOCTYPE html>
<html lang="pt-BR" class="dark">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>OpenNotebook — Clube do Consultor de TI (32 Aulas)</title>
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&family=Outfit:wght@400;600;700;800;900&family=JetBrains+Mono:wght@400;600&display=swap" rel="stylesheet">
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css">
    <style>
        :root {{
            --bg-base: #0a0d14;
            --bg-surface: #111722;
            --bg-card: rgba(22, 30, 46, 0.75);
            --bg-card-hover: rgba(30, 41, 63, 0.9);
            --border: rgba(255, 255, 255, 0.08);
            --border-glow: rgba(56, 189, 248, 0.3);
            --primary: #38bdf8;
            --primary-gradient: linear-gradient(135deg, #38bdf8 0%, #818cf8 50%, #c084fc 100%);
            --accent-orange: #fb923c;
            --accent-emerald: #34d399;
            --text-main: #f1f5f9;
            --text-muted: #94a3b8;
            --text-dim: #64748b;
        }}

        * {{
            margin: 0;
            padding: 0;
            box-sizing: border-box;
            font-family: 'Inter', sans-serif;
        }}

        body {{
            background: radial-gradient(circle at 10% 20%, #0d1527 0%, var(--bg-base) 90%);
            color: var(--text-main);
            min-height: 100vh;
            display: flex;
            flex-direction: column;
            overflow-x: hidden;
        }}

        /* Header */
        header {{
            background: rgba(10, 13, 20, 0.85);
            backdrop-filter: blur(16px);
            border-bottom: 1px solid var(--border);
            padding: 1rem 2rem;
            display: flex;
            justify-content: space-between;
            align-items: center;
            position: sticky;
            top: 0;
            z-index: 100;
        }}

        .brand {{
            display: flex;
            align-items: center;
            gap: 12px;
        }}

        .brand-icon {{
            width: 42px;
            height: 42px;
            border-radius: 12px;
            background: var(--primary-gradient);
            display: flex;
            align-items: center;
            justify-content: center;
            font-size: 20px;
            color: #fff;
            box-shadow: 0 0 20px rgba(56, 189, 248, 0.4);
        }}

        .brand-title {{
            font-family: 'Outfit', sans-serif;
            font-size: 1.35rem;
            font-weight: 800;
            letter-spacing: -0.5px;
            background: var(--primary-gradient);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
        }}

        .brand-subtitle {{
            font-size: 0.78rem;
            color: var(--text-muted);
            text-transform: uppercase;
            letter-spacing: 1px;
            font-weight: 600;
        }}

        /* Navigation Tabs */
        nav.nav-tabs {{
            display: flex;
            gap: 8px;
            background: rgba(17, 23, 34, 0.8);
            padding: 6px;
            border-radius: 14px;
            border: 1px solid var(--border);
        }}

        .nav-btn {{
            background: transparent;
            border: none;
            color: var(--text-muted);
            padding: 8px 16px;
            border-radius: 10px;
            font-size: 0.88rem;
            font-weight: 600;
            cursor: pointer;
            transition: all 0.2s ease;
            display: flex;
            align-items: center;
            gap: 8px;
        }}

        .nav-btn:hover {{
            color: var(--text-main);
            background: rgba(255, 255, 255, 0.05);
        }}

        .nav-btn.active {{
            background: var(--primary-gradient);
            color: #0f172a;
            font-weight: 700;
            box-shadow: 0 4px 12px rgba(56, 189, 248, 0.3);
        }}

        /* Main Container */
        main {{
            flex: 1;
            padding: 2rem;
            max-width: 1440px;
            margin: 0 auto;
            width: 100%;
        }}

        .tab-pane {{
            display: none;
            animation: fadeIn 0.3s ease;
        }}

        .tab-pane.active {{
            display: block;
        }}

        @keyframes fadeIn {{
            from {{ opacity: 0; transform: translateY(8px); }}
            to {{ opacity: 1; transform: translateY(0); }}
        }}

        /* Glassmorphic Cards */
        .glass-card {{
            background: var(--bg-card);
            border: 1px solid var(--border);
            border-radius: 16px;
            padding: 1.5rem;
            backdrop-filter: blur(12px);
            transition: all 0.3s ease;
        }}

        .glass-card:hover {{
            border-color: rgba(56, 189, 248, 0.2);
            box-shadow: 0 8px 32px rgba(0, 0, 0, 0.3);
        }}

        /* Grid Layouts */
        .grid-2 {{
            display: grid;
            grid-template-columns: 1fr 1fr;
            gap: 1.5rem;
        }}

        .grid-3 {{
            display: grid;
            grid-template-columns: repeat(3, 1fr);
            gap: 1.5rem;
        }}

        .grid-4 {{
            display: grid;
            grid-template-columns: repeat(4, 1fr);
            gap: 1rem;
        }}

        @media (max-width: 1024px) {{
            .grid-2, .grid-3, .grid-4 {{
                grid-template-columns: 1fr;
            }}
            header {{
                flex-direction: column;
                gap: 1rem;
            }}
        }}

        /* Audio Deep Dive / Podcast Player */
        .podcast-header {{
            background: linear-gradient(135deg, rgba(56, 189, 248, 0.15) 0%, rgba(129, 140, 248, 0.1) 100%);
            border: 1px solid rgba(56, 189, 248, 0.3);
            border-radius: 20px;
            padding: 2rem;
            margin-bottom: 2rem;
            display: flex;
            justify-content: space-between;
            align-items: center;
            position: relative;
            overflow: hidden;
        }}

        .podcast-info h2 {{
            font-family: 'Outfit', sans-serif;
            font-size: 1.8rem;
            font-weight: 800;
            margin-bottom: 0.5rem;
        }}

        .podcast-controls {{
            display: flex;
            align-items: center;
            gap: 14px;
        }}

        .btn-play {{
            width: 56px;
            height: 56px;
            border-radius: 50%;
            background: var(--primary-gradient);
            border: none;
            color: #0f172a;
            font-size: 22px;
            display: flex;
            align-items: center;
            justify-content: center;
            cursor: pointer;
            box-shadow: 0 0 25px rgba(56, 189, 248, 0.6);
            transition: transform 0.2s ease;
        }}

        .btn-play:hover {{
            transform: scale(1.08);
        }}

        .podcast-dialogue {{
            display: flex;
            flex-direction: column;
            gap: 1.25rem;
        }}

        .dialogue-bubble {{
            display: flex;
            gap: 1rem;
            padding: 1.25rem;
            border-radius: 14px;
            background: rgba(17, 23, 34, 0.6);
            border: 1px solid var(--border);
            transition: all 0.2s ease;
        }}

        .dialogue-bubble.active {{
            background: rgba(56, 189, 248, 0.12);
            border-color: var(--primary);
            box-shadow: 0 0 20px rgba(56, 189, 248, 0.2);
        }}

        .avatar {{
            width: 44px;
            height: 44px;
            border-radius: 12px;
            display: flex;
            align-items: center;
            justify-content: center;
            font-weight: 800;
            font-size: 1rem;
            flex-shrink: 0;
        }}

        .avatar-lucas {{
            background: linear-gradient(135deg, #38bdf8, #2563eb);
            color: #fff;
        }}

        .avatar-sofia {{
            background: linear-gradient(135deg, #f472b6, #db2777);
            color: #fff;
        }}

        /* Mind Map Visual Tree */
        .mindmap-container {{
            background: var(--bg-surface);
            border: 1px solid var(--border);
            border-radius: 18px;
            padding: 2rem;
            min-height: 650px;
            position: relative;
            overflow: auto;
        }}

        .mindmap-node {{
            background: rgba(22, 30, 46, 0.95);
            border: 1px solid var(--border);
            border-radius: 12px;
            padding: 1rem 1.25rem;
            margin-bottom: 1rem;
            cursor: pointer;
            transition: all 0.2s ease;
        }}

        .mindmap-node:hover {{
            border-color: var(--primary);
            transform: translateX(6px);
        }}

        .node-pilar {{
            border-left: 5px solid var(--primary);
            font-weight: 700;
            font-size: 1.1rem;
        }}

        .node-pilar-2 {{
            border-left: 5px solid var(--accent-orange);
        }}

        .node-pilar-3 {{
            border-left: 5px solid var(--accent-emerald);
        }}

        .node-pilar-4 {{
            border-left: 5px solid #c084fc;
        }}

        /* Flashcards */
        .flashcard-wrapper {{
            perspective: 1000px;
            min-height: 320px;
            cursor: pointer;
        }}

        .flashcard {{
            width: 100%;
            height: 320px;
            border-radius: 20px;
            position: relative;
            transform-style: preserve-3d;
            transition: transform 0.6s cubic-bezier(0.4, 0.2, 0.2, 1);
        }}

        .flashcard.flipped {{
            transform: rotateY(180deg);
        }}

        .card-front, .card-back {{
            position: absolute;
            width: 100%;
            height: 100%;
            backface-visibility: hidden;
            border-radius: 20px;
            padding: 2.5rem;
            display: flex;
            flex-direction: column;
            justify-content: center;
            align-items: center;
            text-align: center;
            border: 1px solid var(--border);
        }}

        .card-front {{
            background: linear-gradient(135deg, rgba(22, 30, 46, 0.95) 0%, rgba(15, 23, 42, 0.95) 100%);
        }}

        .card-back {{
            background: linear-gradient(135deg, rgba(30, 41, 59, 0.98) 0%, rgba(15, 23, 42, 0.98) 100%);
            border-color: var(--primary);
            transform: rotateY(180deg);
        }}

        /* Source Explorer & Chat */
        .source-item {{
            background: rgba(17, 23, 34, 0.7);
            border: 1px solid var(--border);
            border-radius: 12px;
            padding: 1rem;
            cursor: pointer;
            transition: all 0.2s ease;
        }}

        .source-item:hover, .source-item.selected {{
            border-color: var(--primary);
            background: rgba(56, 189, 248, 0.1);
        }}

        /* Custom Scrollbar */
        ::-webkit-scrollbar {{
            width: 8px;
            height: 8px;
        }}
        ::-webkit-scrollbar-track {{
            background: var(--bg-base);
        }}
        ::-webkit-scrollbar-thumb {{
            background: #1e293b;
            border-radius: 4px;
        }}
        ::-webkit-scrollbar-thumb:hover {{
            background: #334155;
        }}

        .badge {{
            display: inline-block;
            padding: 4px 10px;
            border-radius: 8px;
            font-size: 0.75rem;
            font-weight: 700;
            text-transform: uppercase;
        }}
        .badge-blue {{ background: rgba(56, 189, 248, 0.15); color: #38bdf8; }}
        .badge-orange {{ background: rgba(251, 146, 60, 0.15); color: #fb923c; }}
        .badge-green {{ background: rgba(52, 211, 153, 0.15); color: #34d399; }}
        .badge-purple {{ background: rgba(192, 132, 252, 0.15); color: #c084fc; }}
    </style>
</head>
<body>

    <header>
        <div class="brand">
            <div class="brand-icon">
                <i class="fa-solid fa-brain"></i>
            </div>
            <div>
                <div class="brand-title">OpenNotebook AI</div>
                <div class="brand-subtitle">Clube do Consultor de TI — 32 Aulas Master</div>
            </div>
        </div>

        <nav class="nav-tabs">
            <button class="nav-btn active" onclick="switchTab('tab-podcast')">
                <i class="fa-solid fa-headphones-simple"></i> Audio Deep Dive
            </button>
            <button class="nav-btn" onclick="switchTab('tab-mindmap')">
                <i class="fa-solid fa-diagram-project"></i> Mapa Mental
            </button>
            <button class="nav-btn" onclick="switchTab('tab-study')">
                <i class="fa-solid fa-book-open"></i> Guia de Estudos
            </button>
            <button class="nav-btn" onclick="switchTab('tab-flashcards')">
                <i class="fa-solid fa-layer-group"></i> Flashcards
            </button>
            <button class="nav-btn" onclick="switchTab('tab-sources')">
                <i class="fa-solid fa-database"></i> 32 Transcrições
            </button>
            <button class="nav-btn" onclick="switchTab('tab-calc')">
                <i class="fa-solid fa-calculator"></i> Calculadora R$
            </button>
        </nav>
    </header>

    <main>
        <!-- ABA 1: AUDIO DEEP DIVE (PODCAST NOTEBOOKLM) -->
        <div id="tab-podcast" class="tab-pane active">
            <div class="podcast-header">
                <div class="podcast-info">
                    <span class="badge badge-blue">NotebookLM Style Audio Deep Dive</span>
                    <h2>Episódio Especial: A Transição do Técnico ao Consultor de R$ 20k/mês</h2>
                    <p style="color: var(--text-muted); max-width: 700px;">
                        Uma conversa dinâmica e aprofundada entre dois hosts de IA (Lucas & Sofia) dissecando todo o método ensinado nas 32 aulas do Clube do Consultor de TI.
                    </p>
                </div>
                <div class="podcast-controls">
                    <button class="btn-play" id="podcastPlayBtn" onclick="togglePodcastSpeech()">
                        <i class="fa-solid fa-play" id="podcastPlayIcon"></i>
                    </button>
                </div>
            </div>

            <div class="podcast-dialogue" id="dialogueContainer">
                <div class="dialogue-bubble" data-index="0">
                    <div class="avatar avatar-lucas">L</div>
                    <div>
                        <div style="font-weight: 700; color: #38bdf8; margin-bottom: 4px;">Lucas (Co-Host)</div>
                        <p style="line-height: 1.7;">Fala pessoal! Sejam muito bem-vindos a este mergulho profundo no acervo das 32 aulas do Clube do Consultor de TI. Sofia, eu fiquei chocado com o primeiro pilar: o cara mostra que 95% dos profissionais de TI estão presos na 'Matrix do CLT' e do técnico que só apaga incêndio.</p>
                    </div>
                </div>

                <div class="dialogue-bubble" data-index="1">
                    <div class="avatar avatar-sofia">S</div>
                    <div>
                        <div style="font-weight: 700; color: #f472b6; margin-bottom: 4px;">Sofia (Co-Host)</div>
                        <p style="line-height: 1.7;">Exatamente, Lucas! E o ponto central que ele bate desde a aula 1 é brutal: o dono de empresa NÃO quer comprar Linux, Docker, firewall ou pentest. Ele quer saber de duas coisas: 'Quanto isso vai me economizar?' e 'Como isso impede a minha empresa de parar por 3 dias e tomar um prejuízo de 100 mil reais?'.</p>
                    </div>
                </div>

                <div class="dialogue-bubble" data-index="2">
                    <div class="avatar avatar-lucas">L</div>
                    <div>
                        <div style="font-weight: 700; color: #38bdf8; margin-bottom: 4px;">Lucas (Co-Host)</div>
                        <p style="line-height: 1.7;">E é aí que entra a esteira de produtos de alto valor. Em vez de cobrar R$ 100 por hora pra consertar impressora, o consultor vende um Diagnóstico de Risco Inicial por R$ 2.500, e já engata um contrato de retenção mensal de R$ 5.000 a R$ 15.000 recorrente.</p>
                    </div>
                </div>

                <div class="dialogue-bubble" data-index="3">
                    <div class="avatar avatar-sofia">S</div>
                    <div>
                        <div style="font-weight: 700; color: #f472b6; margin-bottom: 4px;">Sofia (Co-Host)</div>
                        <p style="line-height: 1.7;">E a prospecção B2B ativa é o segredo ensinado a partir da aula 16! Nada de ficar esperando cliente cair do céu. Você aborda empresas de médio porte locais (contabilidades, clínicas, distribuidoras) com um script cirúrgico no WhatsApp, focado no risco invisível da operação deles.</p>
                    </div>
                </div>

                <div class="dialogue-bubble" data-index="4">
                    <div class="avatar avatar-lucas">L</div>
                    <div>
                        <div style="font-weight: 700; color: #38bdf8; margin-bottom: 4px;">Lucas (Co-Host)</div>
                        <p style="line-height: 1.7;">E na reunião de 30 minutos, você não abre terminal nem mostra código. Você faz perguntas estratégicas que fazem o empresário perceber que está sentado em cima de uma bomba-relógio sem backup testado. Com 4 a 5 clientes, você fatura mais de R$ 25.000/mês com previsibilidade total!</p>
                    </div>
                </div>
            </div>
        </div>

        <!-- ABA 2: MAPA MENTAL INTERATIVO -->
        <div id="tab-mindmap" class="tab-pane">
            <h2 style="font-family: 'Outfit'; font-size: 1.8rem; margin-bottom: 1.5rem;">🧠 Mapa Mental dos 4 Pilares da Consultoria de TI</h2>
            
            <div class="grid-2">
                <!-- PILAR 1 -->
                <div class="mindmap-node node-pilar">
                    <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 8px;">
                        <span class="badge badge-blue">Pilar 01 • Aulas 01 a 08</span>
                        <i class="fa-solid fa-unlock-keyhole" style="color: #38bdf8;"></i>
                    </div>
                    <h3 style="font-size: 1.25rem; margin-bottom: 8px;">Quebra da Matrix & Desprogramação do Técnico</h3>
                    <ul style="color: var(--text-muted); font-size: 0.9rem; line-height: 1.8; margin-left: 1.2rem;">
                        <li>A armadilha de vender horas vs. vender impacto nos negócios</li>
                        <li>Como o CEO enxerga TI: de 'centro de custo' a 'garantia de receita'</li>
                        <li>Eliminação da síndrome do impostor técnica</li>
                        <li>Construção do Posicionamento Matador de Consultor</li>
                    </ul>
                </div>

                <!-- PILAR 2 -->
                <div class="mindmap-node node-pilar node-pilar-2">
                    <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 8px;">
                        <span class="badge badge-orange">Pilar 02 • Aulas 09 a 14</span>
                        <i class="fa-solid fa-gem" style="color: #fb923c;"></i>
                    </div>
                    <h3 style="font-size: 1.25rem; margin-bottom: 8px;">Engenharia de Ofertas de R$ 5k a R$ 20k</h3>
                    <ul style="color: var(--text-muted); font-size: 0.9rem; line-height: 1.8; margin-left: 1.2rem;">
                        <li>A oferta 'Cavalo de Troia': Diagnóstico de Vulnerabilidade e Risco</li>
                        <li>Contrato de Retainer Recorrente (MRR de R$ 3.000 a R$ 15.000)</li>
                        <li>Projetos de Migração & Infraestrutura (Ticket de R$ 10k a R$ 50k)</li>
                        <li>Precificação ancorada no custo da inoperância do cliente</li>
                    </ul>
                </div>

                <!-- PILAR 3 -->
                <div class="mindmap-node node-pilar node-pilar-3">
                    <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 8px;">
                        <span class="badge badge-green">Pilar 03 • Aulas 16 a 24</span>
                        <i class="fa-solid fa-crosshairs" style="color: #34d399;"></i>
                    </div>
                    <h3 style="font-size: 1.25rem; margin-bottom: 8px;">Prospecção Ativa B2B & Fechamento em 30min</h3>
                    <ul style="color: var(--text-muted); font-size: 0.9rem; line-height: 1.8; margin-left: 1.2rem;">
                        <li>Mineração de tomadores de decisão (Sócios, Diretores, CEOs)</li>
                        <li>Scripts cirúrgicos de abordagem no WhatsApp e LinkedIn</li>
                        <li>O roteiro de 30 minutos: Diagnóstico, Abismo e Apresentação</li>
                        <li>Como quebrar as 4 objeções clássicas sem dar desconto</li>
                    </ul>
                </div>

                <!-- PILAR 4 -->
                <div class="mindmap-node node-pilar node-pilar-4">
                    <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 8px;">
                        <span class="badge badge-purple">Pilar 04 • Aulas 25 a 33</span>
                        <i class="fa-solid fa-infinity" style="color: #c084fc;"></i>
                    </div>
                    <h3 style="font-size: 1.25rem; margin-bottom: 8px;">Entrega Estratégica, SLA & Retenção Infinita</h3>
                    <ul style="color: var(--text-muted); font-size: 0.9rem; line-height: 1.8; margin-left: 1.2rem;">
                        <li>Relatório Executivo Mensal de 1 página que renova contratos</li>
                        <li>Governança proativa: resolver antes do cliente perceber</li>
                        <li>Proteção contra Scope Creep (pedidos fora do contrato)</li>
                        <li>Escala com processos e contratação de técnicos operacionais</li>
                    </ul>
                </div>
            </div>
        </div>

        <!-- ABA 3: GUIA DE ESTUDOS & RESUMO EXECUTIVO -->
        <div id="tab-study" class="tab-pane">
            <div class="glass-card" style="margin-bottom: 1.5rem;">
                <h2 style="font-family: 'Outfit'; font-size: 1.8rem; margin-bottom: 1rem; color: #38bdf8;">
                    📖 Resumo Executivo & Playbooks Práticos
                </h2>
                <p style="color: var(--text-muted); line-height: 1.8; font-size: 1rem; margin-bottom: 1.5rem;">
                    Este guia condensa as mais de 25 horas de aula em princípios acionáveis que você pode aplicar imediatamente no mercado corporativo.
                </p>

                <h3 style="font-size: 1.3rem; margin: 1.5rem 0 0.75rem; color: #fb923c;">🎯 Script de Abordagem WhatsApp / LinkedIn</h3>
                <div style="background: rgba(10, 13, 20, 0.9); padding: 1.25rem; border-radius: 12px; border: 1px solid var(--border); font-family: 'JetBrains Mono', monospace; font-size: 0.88rem; line-height: 1.7; color: #34d399;">
                    "Olá [Nome do Sócio], tudo bem? Acompanho a atuação da [Nome da Empresa] no setor de [Nicho].<br><br>
                    Notei que muitas empresas do seu porte estão enfrentando paradas inesperadas de sistema e vulnerabilidades críticas que custam dias de faturamento travado.<br><br>
                    Desenvolvi uma auditoria de risco de 15 minutos que identifica exatamente onde estão os gargalos e pontos de falha que a TI tradicional não enxerga.<br><br>
                    Você teria 15 minutos nesta quinta-feira às 14h para eu te apresentar esse panorama sem custo?"
                </div>

                <h3 style="font-size: 1.3rem; margin: 2rem 0 0.75rem; color: #38bdf8;">💡 A Regra de Ouro da Precificação</h3>
                <div class="grid-3" style="margin-top: 1rem;">
                    <div style="background: rgba(255,255,255,0.03); padding: 1.2rem; border-radius: 12px; border: 1px solid var(--border);">
                        <strong style="color: #38bdf8;">Diagnóstico de Entrada</strong>
                        <div style="font-size: 1.5rem; font-weight: 800; margin: 0.5rem 0;">R$ 1.500 - R$ 3.500</div>
                        <p style="font-size: 0.82rem; color: var(--text-muted);">Auditoria inicial de segurança, backup e servidores em 48h.</p>
                    </div>
                    <div style="background: rgba(255,255,255,0.03); padding: 1.2rem; border-radius: 12px; border: 1px solid var(--border);">
                        <strong style="color: #34d399;">Retainer Mensal (MRR)</strong>
                        <div style="font-size: 1.5rem; font-weight: 800; margin: 0.5rem 0;">R$ 4.000 - R$ 12.000/mês</div>
                        <p style="font-size: 0.82rem; color: var(--text-muted);">Governança contínua, resposta a incidentes e proatividade.</p>
                    </div>
                    <div style="background: rgba(255,255,255,0.03); padding: 1.2rem; border-radius: 12px; border: 1px solid var(--border);">
                        <strong style="color: #c084fc;">Projetos Estratégicos</strong>
                        <div style="font-size: 1.5rem; font-weight: 800; margin: 0.5rem 0;">R$ 15.000 - R$ 45.000</div>
                        <p style="font-size: 0.82rem; color: var(--text-muted);">Migração para nuvem, reestruturação de firewall e SOC.</p>
                    </div>
                </div>
            </div>
        </div>

        <!-- ABA 4: FLASHCARDS INTERATIVOS -->
        <div id="tab-flashcards" class="tab-pane">
            <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 1.5rem;">
                <h2 style="font-family: 'Outfit'; font-size: 1.8rem;">🃏 Flashcards de Repetição Espaçada</h2>
                <div style="color: var(--text-muted); font-size: 0.9rem;">
                    Card <span id="currentCardNum" style="color: #38bdf8; font-weight: 700;">1</span> de <span id="totalCardsNum">10</span>
                </div>
            </div>

            <div class="flashcard-wrapper" onclick="flipCard()">
                <div class="flashcard" id="activeFlashcard">
                    <div class="card-front">
                        <span class="badge badge-blue" style="margin-bottom: 1.5rem;" id="cardCategory">Mentalidade</span>
                        <h3 id="cardQuestion" style="font-size: 1.4rem; font-weight: 700; line-height: 1.6;">
                            Por que vender 'horas técnicas' é a pior estratégia para um profissional de TI?
                        </h3>
                        <p style="margin-top: 1.5rem; font-size: 0.85rem; color: var(--text-dim);">
                            <i class="fa-solid fa-hand-pointer"></i> Clique para revelar a resposta
                        </p>
                    </div>
                    <div class="card-back">
                        <span class="badge badge-green" style="margin-bottom: 1rem;">Resposta & Princípio</span>
                        <p id="cardAnswer" style="font-size: 1.15rem; line-height: 1.7; color: #e2e8f0;">
                            Porque o dia só tem 24 horas, criando um teto de ganhos. Além disso, o cliente associa hora a 'custo operacional'. O consultor estratégico vende **Impacto, Redução de Risco e Continuidade do Negócio**, cobrando pelo valor gerado e não pelo tempo gasto.
                        </p>
                    </div>
                </div>
            </div>

            <div style="display: flex; justify-content: center; gap: 1rem; margin-top: 2rem;">
                <button class="nav-btn" onclick="prevCard()" style="background: rgba(255,255,255,0.05); padding: 10px 20px;">
                    <i class="fa-solid fa-arrow-left"></i> Anterior
                </button>
                <button class="nav-btn" onclick="nextCard()" style="background: var(--primary-gradient); color: #0f172a; padding: 10px 24px; font-weight: 700;">
                    Próximo Card <i class="fa-solid fa-arrow-right"></i>
                </button>
            </div>
        </div>

        <!-- ABA 5: EXPLORADOR DAS 32 TRANSCRIÇÕES -->
        <div id="tab-sources" class="tab-pane">
            <div class="grid-2">
                <div class="glass-card" style="height: 680px; display: flex; flex-direction: column;">
                    <h3 style="font-size: 1.2rem; margin-bottom: 1rem;">📚 As 32 Aulas do Acervo</h3>
                    <input type="text" id="searchLessonsInput" placeholder="Filtrar por palavra-chave..." oninput="filterLessonsList()" style="width: 100%; padding: 10px 14px; border-radius: 10px; background: rgba(0,0,0,0.4); border: 1px solid var(--border); color: #fff; margin-bottom: 1rem;">
                    <div id="lessonsListContainer" style="flex: 1; overflow-y: auto; display: flex; flex-direction: column; gap: 8px;">
                        <!-- Populado via JS -->
                    </div>
                </div>

                <div class="glass-card" style="height: 680px; display: flex; flex-direction: column;">
                    <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 1rem; padding-bottom: 0.5rem; border-bottom: 1px solid var(--border);">
                        <h3 id="selectedLessonTitle" style="font-size: 1.15rem; color: #38bdf8;">Selecione uma aula</h3>
                        <span id="selectedLessonSize" style="font-size: 0.8rem; color: var(--text-dim);">0 bytes</span>
                    </div>
                    <div id="lessonContentDisplay" style="flex: 1; overflow-y: auto; font-family: 'JetBrains Mono', monospace; font-size: 0.85rem; line-height: 1.8; color: #cbd5e1; white-space: pre-wrap; background: rgba(0,0,0,0.3); padding: 1.25rem; border-radius: 10px;">
                        Clique em uma aula à esquerda para carregar a transcrição integral e os detalhes.
                    </div>
                </div>
            </div>
        </div>

        <!-- ABA 6: CALCULADORA DE PRECIFICAÇÃO E MRR -->
        <div id="tab-calc" class="tab-pane">
            <div class="glass-card" style="max-width: 800px; margin: 0 auto;">
                <h2 style="font-family: 'Outfit'; font-size: 1.8rem; margin-bottom: 1rem; color: #34d399;">
                    💰 Calculadora de Faturamento do Consultor
                </h2>
                <p style="color: var(--text-muted); margin-bottom: 2rem;">
                    Simule seu faturamento mensal recorrente (MRR) e faturamento anual com base no método do Clube do Consultor:
                </p>

                <div style="display: flex; flex-direction: column; gap: 1.5rem;">
                    <div>
                        <label style="font-weight: 600; display: block; margin-bottom: 6px;">Número de Clientes Recorrentes (Retainer):</label>
                        <input type="range" id="calcClients" min="1" max="20" value="5" oninput="updateCalculator()" style="width: 100%;">
                        <div style="display: flex; justify-content: space-between; color: #38bdf8; font-weight: 700; font-size: 1.1rem; margin-top: 4px;">
                            <span id="calcClientsVal">5 clientes</span>
                        </div>
                    </div>

                    <div>
                        <label style="font-weight: 600; display: block; margin-bottom: 6px;">Ticket Médio Mensal por Cliente:</label>
                        <input type="range" id="calcTicket" min="2000" max="20000" step="500" value="5000" oninput="updateCalculator()" style="width: 100%;">
                        <div style="display: flex; justify-content: space-between; color: #fb923c; font-weight: 700; font-size: 1.1rem; margin-top: 4px;">
                            <span id="calcTicketVal">R$ 5.000 / mês</span>
                        </div>
                    </div>

                    <div>
                        <label style="font-weight: 600; display: block; margin-bottom: 6px;">Diagnósticos / Auditorias de Entrada por Mês:</label>
                        <input type="range" id="calcAudits" min="0" max="10" value="2" oninput="updateCalculator()" style="width: 100%;">
                        <div style="display: flex; justify-content: space-between; color: #c084fc; font-weight: 700; font-size: 1.1rem; margin-top: 4px;">
                            <span id="calcAuditsVal">2 auditorias (R$ 2.500 cada)</span>
                        </div>
                    </div>
                </div>

                <hr style="border-color: var(--border); margin: 2rem 0;">

                <div class="grid-2">
                    <div style="background: rgba(56, 189, 248, 0.1); border: 1px solid var(--primary); padding: 1.5rem; border-radius: 14px; text-align: center;">
                        <span style="font-size: 0.85rem; text-transform: uppercase; letter-spacing: 1px; color: var(--text-muted); font-weight: 700;">Faturamento Mensal (MRR)</span>
                        <div id="calcMonthlyTotal" style="font-size: 2.2rem; font-family: 'Outfit'; font-weight: 900; color: #38bdf8; margin-top: 6px;">
                            R$ 30.000 / mês
                        </div>
                    </div>

                    <div style="background: rgba(52, 211, 153, 0.1); border: 1px solid var(--accent-emerald); padding: 1.5rem; border-radius: 14px; text-align: center;">
                        <span style="font-size: 0.85rem; text-transform: uppercase; letter-spacing: 1px; color: var(--text-muted); font-weight: 700;">Faturamento Anual Projetado</span>
                        <div id="calcYearlyTotal" style="font-size: 2.2rem; font-family: 'Outfit'; font-weight: 900; color: #34d399; margin-top: 6px;">
                            R$ 360.000 / ano
                        </div>
                    </div>
                </div>
            </div>
        </div>
    </main>

    <script>
        const lessonsData = {lessons_json};

        const flashcardsData = [
            {{
                category: "Mentalidade",
                q: "Por que vender 'horas técnicas' é a pior estratégia para um profissional de TI?",
                a: "Porque você tem um teto biológico de 24h/dia. Além disso, o cliente associa hora a custo. O consultor cobra pelo IMPACTO e RISCO EVITADO."
            }},
            {{
                category: "Precificação",
                q: "Qual a estrutura do Tripé da Consultoria de TI de Alto Valor?",
                a: "1) Diagnóstico de Entrada (R$ 1.5k a R$ 3.5k) -> 2) Retainer Mensal Recorrente (R$ 4k a R$ 12k/mês) -> 3) Projetos de Transformação/Nuvem (R$ 15k a R$ 45k)."
            }},
            {{
                category: "Prospecção B2B",
                q: "Qual é o perfil ideal de empresa para abordar no início?",
                a: "Empresas locais de 15 a 150 funcionários (Clínicas, Contabilidades, Escritórios de Advocacia, Distribuidoras) que dependem 100% do sistema para faturar."
            }},
            {{
                category: "Vendas & Reunião",
                q: "Como conduzir uma reunião de 30 minutos sem falar de termos técnicos?",
                a: "Foque no Diagnóstico e no Abismo: faça perguntas sobre o custo da empresa parada, risco de perda de dados e multas da LGPD em vez de mostrar comandos de terminal."
            }},
            {{
                category: "Objeção Clássica",
                q: "Como quebrar a objeção 'Já tenho um rapaz do TI que cuida disso'?",
                a: "Diga que o seu trabalho não concorre com o suporte dele: você é a governança e segurança estratégica que impede que a empresa seja paralisada por ataques cibernéticos."
            }},
            {{
                category: "Retenção & SLA",
                q: "Como deve ser o Relatório Executivo Mensal para garantir a renovação do contrato?",
                a: "Um resumo executivo de 1 página focado em negócios: quantos ataques foram bloqueados, testes de restore de backup realizados e tempo de 100% de operação no ar."
            }}
        ];

        let currentCardIndex = 0;

        function switchTab(tabId) {{
            document.querySelectorAll('.tab-pane').forEach(el => el.classList.remove('active'));
            document.querySelectorAll('.nav-btn').forEach(el => el.classList.remove('active'));
            
            document.getElementById(tabId).classList.add('active');
            event.currentTarget.classList.add('active');
        }}

        // Flashcards Logic
        function updateCardDisplay() {{
            const card = flashcardsData[currentCardIndex];
            document.getElementById('cardCategory').innerText = card.category;
            document.getElementById('cardQuestion').innerText = card.q;
            document.getElementById('cardAnswer').innerText = card.a;
            document.getElementById('currentCardNum').innerText = currentCardIndex + 1;
            document.getElementById('totalCardsNum').innerText = flashcardsData.length;
            document.getElementById('activeFlashcard').classList.remove('flipped');
        }}

        function flipCard() {{
            document.getElementById('activeFlashcard').classList.toggle('flipped');
        }}

        function nextCard() {{
            currentCardIndex = (currentCardIndex + 1) % flashcardsData.length;
            updateCardDisplay();
        }}

        function prevCard() {{
            currentCardIndex = (currentCardIndex - 1 + flashcardsData.length) % flashcardsData.length;
            updateCardDisplay();
        }}

        // Sources List
        function renderLessonsList(filter = '') {{
            const container = document.getElementById('lessonsListContainer');
            container.innerHTML = '';
            
            lessonsData.filter(l => l.title.toLowerCase().includes(filter.toLowerCase()) || l.text.toLowerCase().includes(filter.toLowerCase()))
                .forEach((l, idx) => {{
                    const div = document.createElement('div');
                    div.className = 'source-item';
                    div.innerHTML = `
                        <div style="font-weight: 700; font-size: 0.95rem; margin-bottom: 4px; color: #f8fafc;">${{l.title}}</div>
                        <div style="font-size: 0.78rem; color: var(--text-dim); line-height: 1.4;">${{l.summary.substring(0, 110)}}...</div>
                    `;
                    div.onclick = () => selectLesson(l, div);
                    container.appendChild(div);
                    if (idx === 0 && !filter) {{
                        selectLesson(l, div);
                    }}
                }});
        }}

        function selectLesson(lesson, elem) {{
            document.querySelectorAll('.source-item').forEach(el => el.classList.remove('selected'));
            if (elem) elem.classList.add('selected');
            document.getElementById('selectedLessonTitle').innerText = lesson.title;
            document.getElementById('selectedLessonSize').innerText = (lesson.size / 1024).toFixed(1) + ' KB';
            document.getElementById('lessonContentDisplay').innerText = lesson.text;
        }}

        function filterLessonsList() {{
            const val = document.getElementById('searchLessonsInput').value;
            renderLessonsList(val);
        }}

        // Calculator
        function updateCalculator() {{
            const clients = parseInt(document.getElementById('calcClients').value);
            const ticket = parseInt(document.getElementById('calcTicket').value);
            const audits = parseInt(document.getElementById('calcAudits').value);

            document.getElementById('calcClientsVal').innerText = clients + ' clientes';
            document.getElementById('calcTicketVal').innerText = 'R$ ' + ticket.toLocaleString('pt-BR') + ' / mês';
            document.getElementById('calcAuditsVal').innerText = audits + ' auditorias (R$ 2.500 cada)';

            const mrr = (clients * ticket) + (audits * 2500);
            const yearly = mrr * 12;

            document.getElementById('calcMonthlyTotal').innerText = 'R$ ' + mrr.toLocaleString('pt-BR') + ' / mês';
            document.getElementById('calcYearlyTotal').innerText = 'R$ ' + yearly.toLocaleString('pt-BR') + ' / ano';
        }}

        // Podcast Speech Synthesis (Web Speech API)
        let isSpeaking = false;
        let speechIndex = 0;
        const dialogueLines = [
            "Fala pessoal! Sejam muito bem-vindos a este mergulho profundo no acervo das 32 aulas do Clube do Consultor de TI. Sofia, eu fiquei chocado com o primeiro pilar: o cara mostra que 95% dos profissionais de TI estão presos na Matrix do CLT e do técnico que só apaga incêndio.",
            "Exatamente, Lucas! E o ponto central que ele bate desde a aula 1 é brutal: o dono de empresa NÃO quer comprar Linux, Docker, firewall ou pentest. Ele quer saber de redução de custos e garantia de que a empresa não vai parar.",
            "E é aí que entra a esteira de produtos de alto valor. Em vez de cobrar 100 reais por hora pra consertar impressora, o consultor vende um Diagnóstico de Risco Inicial por 2.500 reais, e já engata um contrato de retenção mensal de 5.000 a 15.000 reais recorrente.",
            "E a prospecção B2B ativa é o segredo ensinado a partir da aula 16! Nada de ficar esperando cliente. Você aborda empresas de médio porte locais com um script cirúrgico no WhatsApp, focado no risco invisível da operação deles.",
            "E na reunião de 30 minutos, você não abre terminal nem mostra código. Você faz perguntas estratégicas que fazem o empresário perceber que está sentado em cima de uma bomba-relógio sem backup testado. Com 4 a 5 clientes, você fatura mais de 25 mil reais por mês com previsibilidade total!"
        ];

        function togglePodcastSpeech() {{
            if (!('speechSynthesis' in window)) {{
                alert('Seu navegador não suporta sintetizador de voz nativo.');
                return;
            }}

            if (isSpeaking) {{
                window.speechSynthesis.cancel();
                isSpeaking = false;
                document.getElementById('podcastPlayIcon').className = 'fa-solid fa-play';
                document.querySelectorAll('.dialogue-bubble').forEach(el => el.classList.remove('active'));
            }} else {{
                isSpeaking = true;
                speechIndex = 0;
                document.getElementById('podcastPlayIcon').className = 'fa-solid fa-pause';
                playNextDialogueLine();
            }}
        }}

        function playNextDialogueLine() {{
            if (!isSpeaking || speechIndex >= dialogueLines.length) {{
                isSpeaking = false;
                document.getElementById('podcastPlayIcon').className = 'fa-solid fa-play';
                document.querySelectorAll('.dialogue-bubble').forEach(el => el.classList.remove('active'));
                return;
            }}

            document.querySelectorAll('.dialogue-bubble').forEach((el, idx) => {{
                if (idx === speechIndex) el.classList.add('active');
                else el.classList.remove('active');
            }});

            const utterance = new SpeechSynthesisUtterance(dialogueLines[speechIndex]);
            utterance.lang = 'pt-BR';
            utterance.rate = 1.05;
            utterance.pitch = speechIndex % 2 === 0 ? 0.95 : 1.15; // Alterna pitch para Lucas e Sofia

            utterance.onend = () => {{
                speechIndex++;
                playNextDialogueLine();
            }};

            window.speechSynthesis.speak(utterance);
        }}

        // Inicialização
        window.onload = () => {{
            updateCardDisplay();
            renderLessonsList();
            updateCalculator();
        }};
    </script>
</body>
</html>
"""

with open(os.path.join(DESKTOP, "OPENNOTEBOOK_CLUBE_DO_CONSULTOR.html"), "w", encoding="utf-8") as f:
    f.write(html_content)

print("OpenNotebook App HTML gerado no Desktop!")

# Criar o atalho .bat no Desktop para abrir com 1 clique
bat_content = f"""@echo off
title OpenNotebook — Clube do Consultor de TI
start "" "{os.path.join(DESKTOP, 'OPENNOTEBOOK_CLUBE_DO_CONSULTOR.html')}"
exit
"""

with open(os.path.join(DESKTOP, "ABRIR_OPENNOTEBOOK_CONSULTOR.bat"), "w", encoding="utf-8") as f:
    f.write(bat_content)

print("Atalho .bat criado no Desktop!")
