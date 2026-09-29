import os

DESKTOP = r"C:\Users\matheus\Desktop"

mindmap_html = """<!DOCTYPE html>
<html lang="pt-BR">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Mapa Mental Interativo — Clube do Consultor de TI</title>
    <link href="https://fonts.googleapis.com/css2?family=Outfit:wght@400;600;700;800;900&family=Inter:wght@400;500;600;700&display=swap" rel="stylesheet">
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css">
    <style>
        :root {
            --bg: #090d16;
            --surface: #111726;
            --card: rgba(22, 30, 48, 0.85);
            --border: rgba(255, 255, 255, 0.1);
            --primary: #38bdf8;
            --orange: #fb923c;
            --emerald: #34d399;
            --purple: #c084fc;
        }

        * { margin: 0; padding: 0; box-sizing: border-box; font-family: 'Inter', sans-serif; }

        body {
            background: radial-gradient(circle at 50% 10%, #172554 0%, var(--bg) 95%);
            color: #f8fafc;
            min-height: 100vh;
            padding: 2rem;
        }

        .header {
            text-align: center;
            margin-bottom: 3rem;
        }

        h1 {
            font-family: 'Outfit', sans-serif;
            font-size: 2.5rem;
            font-weight: 900;
            background: linear-gradient(135deg, #38bdf8, #818cf8, #c084fc);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            margin-bottom: 0.5rem;
        }

        .subtitle {
            color: #94a3b8;
            font-size: 1.05rem;
        }

        /* Central Node */
        .hub-center {
            max-width: 480px;
            margin: 0 auto 3rem;
            background: linear-gradient(135deg, rgba(56, 189, 248, 0.15) 0%, rgba(129, 140, 248, 0.15) 100%);
            border: 2px solid var(--primary);
            border-radius: 20px;
            padding: 1.5rem;
            text-align: center;
            box-shadow: 0 0 35px rgba(56, 189, 248, 0.3);
        }

        .hub-center h2 {
            font-family: 'Outfit', sans-serif;
            font-size: 1.5rem;
            color: #38bdf8;
            margin-bottom: 0.5rem;
        }

        /* Pillars Grid */
        .pillars-grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(320px, 1fr));
            gap: 2rem;
            max-width: 1400px;
            margin: 0 auto;
        }

        .pillar-card {
            background: var(--card);
            border: 1px solid var(--border);
            border-radius: 18px;
            padding: 1.8rem;
            backdrop-filter: blur(16px);
            transition: transform 0.3s ease, border-color 0.3s ease, box-shadow 0.3s ease;
            position: relative;
            overflow: hidden;
        }

        .pillar-card:hover {
            transform: translateY(-6px);
            box-shadow: 0 12px 36px rgba(0, 0, 0, 0.4);
        }

        .p1 { border-top: 4px solid var(--primary); }
        .p2 { border-top: 4px solid var(--orange); }
        .p3 { border-top: 4px solid var(--emerald); }
        .p4 { border-top: 4px solid var(--purple); }

        .pillar-header {
            display: flex;
            align-items: center;
            gap: 12px;
            margin-bottom: 1.25rem;
        }

        .pillar-icon {
            width: 44px;
            height: 44px;
            border-radius: 12px;
            display: flex;
            align-items: center;
            justify-content: center;
            font-size: 1.2rem;
        }

        .p1 .pillar-icon { background: rgba(56, 189, 248, 0.15); color: var(--primary); }
        .p2 .pillar-icon { background: rgba(251, 146, 60, 0.15); color: var(--orange); }
        .p3 .pillar-icon { background: rgba(52, 211, 153, 0.15); color: var(--emerald); }
        .p4 .pillar-icon { background: rgba(192, 132, 252, 0.15); color: var(--purple); }

        .pillar-title {
            font-family: 'Outfit', sans-serif;
            font-size: 1.25rem;
            font-weight: 800;
        }

        .nodes-list {
            list-style: none;
            display: flex;
            flex-direction: column;
            gap: 10px;
        }

        .node-item {
            background: rgba(10, 13, 20, 0.6);
            border: 1px solid rgba(255, 255, 255, 0.05);
            padding: 10px 14px;
            border-radius: 10px;
            font-size: 0.88rem;
            line-height: 1.5;
            color: #cbd5e1;
            transition: all 0.2s ease;
        }

        .node-item:hover {
            border-color: rgba(255, 255, 255, 0.2);
            color: #fff;
            transform: translateX(4px);
        }
    </style>
</head>
<body>

    <div class="header">
        <h1>MAPA MENTAL ESTRATÉGICO</h1>
        <p class="subtitle">Clube do Consultor de TI — As 32 Aulas Sintetizadas em Estrutura de Domínio</p>
    </div>

    <div class="hub-center">
        <i class="fa-solid fa-crown" style="font-size: 2rem; color: #38bdf8; margin-bottom: 0.75rem;"></i>
        <h2>CONSULTOR DE TI DE ALTO VALOR</h2>
        <p style="color: var(--text-muted); font-size: 0.9rem;">
            Meta: De 4 a 8 contratos de R$ 5.000 a R$ 20.000/mês (Faturamento de R$ 20k a R$ 80k/mês)
        </p>
    </div>

    <div class="pillars-grid">
        <!-- PILAR 1 -->
        <div class="pillar-card p1">
            <div class="pillar-header">
                <div class="pillar-icon"><i class="fa-solid fa-brain"></i></div>
                <div>
                    <span style="font-size: 0.75rem; text-transform: uppercase; font-weight: 700; color: var(--primary);">Pilar 1 • Aulas 01 a 08</span>
                    <div class="pillar-title">Mentalidade & Matrix do CLT</div>
                </div>
            </div>
            <ul class="nodes-list">
                <li class="node-item"><strong>Fim do Preço por Hora:</strong> Vender hora é ser punido por ser rápido e competente.</li>
                <li class="node-item"><strong>A Dor Real do Dono:</strong> CEOs temem perder vendas, paralisar fábricas e vazamento de dados.</li>
                <li class="node-item"><strong>Posicionamento de Autoridade:</strong> De suporte técnico reativo para conselheiro estratégico.</li>
                <li class="node-item"><strong>Desprogramação Operacional:</strong> Deixe o trabalho braçal para ferramentas e estagiários.</li>
            </ul>
        </div>

        <!-- PILAR 2 -->
        <div class="pillar-card p2">
            <div class="pillar-header">
                <div class="pillar-icon"><i class="fa-solid fa-file-invoice-dollar"></i></div>
                <div>
                    <span style="font-size: 0.75rem; text-transform: uppercase; font-weight: 700; color: var(--orange);">Pilar 2 • Aulas 09 a 14</span>
                    <div class="pillar-title">Engenharia de Ofertas</div>
                </div>
            </div>
            <ul class="nodes-list">
                <li class="node-item"><strong>Diagnóstico de Risco (R$ 2.500):</strong> A porta de entrada com quase 100% de conversão.</li>
                <li class="node-item"><strong>Contrato de Retainer (R$ 5k - R$ 15k/mês):</strong> Previsibilidade e receita recorrente (MRR).</li>
                <li class="node-item"><strong>Projetos de Migração & Cloud:</strong> Upsell de R$ 15.000 a R$ 50.000 na mesma base.</li>
                <li class="node-item"><strong>Precificação Ancorada no Risco:</strong> Compare o custo da consultoria com 3 dias de empresa parada.</li>
            </ul>
        </div>

        <!-- PILAR 3 -->
        <div class="pillar-card p3">
            <div class="pillar-header">
                <div class="pillar-icon"><i class="fa-solid fa-bullseye"></i></div>
                <div>
                    <span style="font-size: 0.75rem; text-transform: uppercase; font-weight: 700; color: var(--emerald);">Pilar 3 • Aulas 16 a 24</span>
                    <div class="pillar-title">Prospecção & Fechamento B2B</div>
                </div>
            </div>
            <ul class="nodes-list">
                <li class="node-item"><strong>Nicho Lucrativo Local:</strong> Empresas de 15 a 150 funcionários (Clínicas, Contabilidades, Advocacia).</li>
                <li class="node-item"><strong>Script Cirúrgico WhatsApp:</strong> Abordagem focada em vulnerabilidade invisível e sem venda agressiva.</li>
                <li class="node-item"><strong>Reunião Estratégica de 30min:</strong> Diagnóstico -> O Abismo -> Proposta Irresistível.</li>
                <li class="node-item"><strong>Quebra de Objeções:</strong> Destrua o "Já tenho o rapaz do TI" mostrando a diferença entre suporte e governança.</li>
            </ul>
        </div>

        <!-- PILAR 4 -->
        <div class="pillar-card p4">
            <div class="pillar-header">
                <div class="pillar-icon"><i class="fa-solid fa-chart-line"></i></div>
                <div>
                    <span style="font-size: 0.75rem; text-transform: uppercase; font-weight: 700; color: var(--purple);">Pilar 4 • Aulas 25 a 33</span>
                    <div class="pillar-title">Retenção & Escala de Contratos</div>
                </div>
            </div>
            <ul class="nodes-list">
                <li class="node-item"><strong>Relatório Executivo Mensal:</strong> 1 página provando ROI, ataques bloqueados e 100% de uptime.</li>
                <li class="node-item"><strong>Proatividade Total:</strong> Avise o cliente da falha após ter solucionado o problema.</li>
                <li class="node-item"><strong>Blindagem de Escopo:</strong> Contratos claros que impedem demandas extras fora do combinado.</li>
                <li class="node-item"><strong>Escala Automatizada:</strong> Use ferramentas de RMM/SOC para gerenciar múltiplos clientes simultaneamente.</li>
            </ul>
        </div>
    </div>

</body>
</html>
"""

with open(os.path.join(DESKTOP, "MAPA_MENTAL_CLUBE_DO_CONSULTOR.html"), "w", encoding="utf-8") as f:
    f.write(mindmap_html)

print("Mapa Mental Standalone HTML gerado no Desktop!")
