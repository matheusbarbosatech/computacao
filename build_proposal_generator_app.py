import os

DESKTOP = r"C:\Users\matheus\Desktop"

generator_html = """<!DOCTYPE html>
<html lang="pt-BR">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Gerador de Propostas de Consultoria de TI — Baseado em Valor</title>
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&family=Outfit:wght@400;600;700;800;900&family=JetBrains+Mono:wght@400;600&display=swap" rel="stylesheet">
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css">
    <style>
        :root {
            --bg-base: #0a0d14;
            --bg-surface: #111722;
            --bg-card: rgba(22, 30, 46, 0.85);
            --border: rgba(255, 255, 255, 0.08);
            --primary: #38bdf8;
            --primary-gradient: linear-gradient(135deg, #38bdf8 0%, #818cf8 50%, #c084fc 100%);
            --accent-orange: #fb923c;
            --accent-emerald: #34d399;
            --text-main: #f1f5f9;
            --text-muted: #94a3b8;
            --text-dim: #64748b;
        }

        * { margin: 0; padding: 0; box-sizing: border-box; font-family: 'Inter', sans-serif; }

        body {
            background: radial-gradient(circle at 10% 20%, #0d1527 0%, var(--bg-base) 90%);
            color: var(--text-main);
            min-height: 100vh;
            padding: 2rem 1rem;
        }

        .container {
            max-width: 1400px;
            margin: 0 auto;
        }

        header {
            text-align: center;
            margin-bottom: 2.5rem;
        }

        .badge-brand {
            display: inline-flex;
            align-items: center;
            gap: 8px;
            padding: 6px 14px;
            border-radius: 20px;
            background: rgba(56, 189, 248, 0.15);
            border: 1px solid rgba(56, 189, 248, 0.3);
            color: #38bdf8;
            font-size: 0.82rem;
            font-weight: 700;
            text-transform: uppercase;
            letter-spacing: 1px;
            margin-bottom: 1rem;
        }

        h1 {
            font-family: 'Outfit', sans-serif;
            font-size: 2.5rem;
            font-weight: 900;
            background: var(--primary-gradient);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            margin-bottom: 0.5rem;
        }

        .grid-app {
            display: grid;
            grid-template-columns: 460px 1fr;
            gap: 2rem;
            align-items: start;
        }

        @media (max-width: 1080px) {
            .grid-app { grid-template-columns: 1fr; }
        }

        /* Glassmorphic Cards */
        .glass-card {
            background: var(--bg-card);
            border: 1px solid var(--border);
            border-radius: 18px;
            padding: 1.75rem;
            backdrop-filter: blur(16px);
        }

        .form-group {
            margin-bottom: 1.2rem;
        }

        label {
            display: block;
            font-size: 0.85rem;
            font-weight: 600;
            color: var(--text-muted);
            margin-bottom: 6px;
        }

        input, select, textarea {
            width: 100%;
            padding: 10px 14px;
            border-radius: 10px;
            background: rgba(10, 13, 20, 0.7);
            border: 1px solid var(--border);
            color: #fff;
            font-size: 0.9rem;
            outline: none;
            transition: border-color 0.2s;
        }

        input:focus, select:focus, textarea:focus {
            border-color: var(--primary);
            box-shadow: 0 0 10px rgba(56, 189, 248, 0.2);
        }

        .preset-btns {
            display: grid;
            grid-template-columns: repeat(2, 1fr);
            gap: 8px;
            margin-bottom: 1.5rem;
        }

        .btn-preset {
            background: rgba(255, 255, 255, 0.04);
            border: 1px solid var(--border);
            color: var(--text-muted);
            padding: 8px;
            border-radius: 8px;
            font-size: 0.78rem;
            font-weight: 600;
            cursor: pointer;
            transition: all 0.2s;
        }

        .btn-preset:hover {
            border-color: var(--primary);
            color: #fff;
            background: rgba(56, 189, 248, 0.1);
        }

        .btn-generate {
            width: 100%;
            padding: 14px;
            border-radius: 12px;
            background: var(--primary-gradient);
            border: none;
            color: #0f172a;
            font-family: 'Outfit', sans-serif;
            font-size: 1.1rem;
            font-weight: 800;
            cursor: pointer;
            transition: all 0.2s;
            box-shadow: 0 4px 20px rgba(56, 189, 248, 0.4);
            display: flex;
            align-items: center;
            justify-content: center;
            gap: 10px;
        }

        .btn-generate:hover {
            transform: translateY(-2px);
            box-shadow: 0 6px 25px rgba(56, 189, 248, 0.6);
        }

        /* Proposal Preview */
        .proposal-container {
            background: rgba(17, 23, 34, 0.95);
            border: 1px solid var(--border);
            border-radius: 18px;
            padding: 2.5rem;
            min-height: 700px;
            font-size: 0.95rem;
            line-height: 1.8;
            color: #cbd5e1;
        }

        .proposal-actions {
            display: flex;
            justify-content: flex-end;
            gap: 10px;
            margin-bottom: 1.5rem;
        }

        .btn-action {
            background: rgba(255, 255, 255, 0.05);
            border: 1px solid var(--border);
            color: #fff;
            padding: 8px 16px;
            border-radius: 8px;
            font-size: 0.85rem;
            font-weight: 600;
            cursor: pointer;
            transition: all 0.2s;
            display: flex;
            align-items: center;
            gap: 6px;
        }

        .btn-action:hover {
            border-color: var(--primary);
            background: rgba(56, 189, 248, 0.15);
        }

        /* Tables in Proposal */
        table.prop-table {
            width: 100%;
            border-collapse: collapse;
            margin: 1.5rem 0;
            font-size: 0.9rem;
        }

        table.prop-table th {
            background: rgba(56, 189, 248, 0.15);
            color: #38bdf8;
            font-weight: 700;
            text-align: left;
            padding: 10px 14px;
            border: 1px solid rgba(255, 255, 255, 0.08);
        }

        table.prop-table td {
            padding: 10px 14px;
            border: 1px solid rgba(255, 255, 255, 0.05);
            background: rgba(10, 13, 20, 0.4);
        }

        .callout-box {
            background: rgba(56, 189, 248, 0.08);
            border-left: 4px solid var(--primary);
            padding: 1.25rem;
            border-radius: 8px;
            margin: 1.5rem 0;
        }

        .callout-danger {
            background: rgba(239, 68, 68, 0.08);
            border-left: 4px solid #ef4444;
        }

        @media print {
            body { background: #fff; color: #000; padding: 0; }
            .grid-app { grid-template-columns: 1fr; }
            .glass-card, header, .proposal-actions { display: none; }
            .proposal-container { border: none; background: #fff; color: #000; padding: 0; }
            table.prop-table th { background: #eee; color: #000; }
            table.prop-table td { background: #fff; color: #000; }
            .callout-box { border-left-color: #000; background: #f9f9f9; color: #000; }
        }
    </style>
</head>
<body>

    <div class="container">
        <header>
            <div class="badge-brand">
                <i class="fa-solid fa-calculator"></i> Motor de Precificação Baseada em Valor
            </div>
            <h1>Gerador de Propostas de Consultoria de TI</h1>
            <p style="color: var(--text-muted);">Crie orçamentos executivos de alto valor (R$ 5.000 a R$ 20.000/mês) ancorados no risco de negócio e ROI.</p>
        </header>

        <div class="grid-app">
            <!-- PAINEL DE ENTRADA (DIAGNÓSTICO) -->
            <div class="glass-card">
                <div style="font-weight: 700; font-size: 1.1rem; margin-bottom: 0.75rem; color: #38bdf8;">
                    ⚡ Preenchimento Rápido por Nicho:
                </div>
                <div class="preset-btns">
                    <button class="btn-preset" onclick="loadPreset('clinica')"><i class="fa-solid fa-hospital"></i> Clínica Médica</button>
                    <button class="btn-preset" onclick="loadPreset('advocacia')"><i class="fa-solid fa-scale-balanced"></i> Escritório Advocacia</button>
                    <button class="btn-preset" onclick="loadPreset('contabilidade')"><i class="fa-solid fa-file-invoice-dollar"></i> Contabilidade</button>
                    <button class="btn-preset" onclick="loadPreset('distribuidora')"><i class="fa-solid fa-truck"></i> Distribuidora / Indústria</button>
                </div>

                <form id="proposalForm" onsubmit="generateProposal(event)">
                    <div class="form-group">
                        <label>1. Nome do Cliente & Setor:</label>
                        <input type="text" id="clientName" value="Clínica Médica Vida Saudável" required>
                    </div>

                    <div class="form-group">
                        <label>2. Seu Nome / Sua Consultoria:</label>
                        <input type="text" id="consultantName" value="Matheus Barbosa | Consultoria Estratégica de TI" required>
                    </div>

                    <div class="form-group">
                        <label>3. Porte da Empresa (Funcionários / PCs / Faturamento):</label>
                        <input type="text" id="clientSize" value="45 funcionários (30 computadores), faturamento R$ 600.000/mês" required>
                    </div>

                    <div class="form-group">
                        <label>4. Custo Estimado de 1 Hora da Empresa Parada:</label>
                        <input type="text" id="downtimeCost" value="R$ 15.000" required>
                    </div>

                    <div class="form-group">
                        <label>5. Dores & Histórico de Incidentes:</label>
                        <textarea id="painPoints" rows="3" required>Ataque de Ransomware recente com perda de 2 dias de faturamento (R$ 80.000 de prejuízo), backup manual em HD externo, Wi-Fi de pacientes sem isolamento de rede dos prontuários e lentidão no sistema PACS.</textarea>
                    </div>

                    <div class="form-group">
                        <label>6. Serviços Propostos no Escopo:</label>
                        <textarea id="servicesProposed" rows="3" required>1) Assessment de Vulnerabilidade e LGPD
2) Migração de Servidores Locais para Nuvem AWS/Azure
3) Backup em Nuvem Criptografado e Imutável
4) Gestão Contínua de TI, SOC e Monitoramento 24/7 (Retainer Mensal)</textarea>
                    </div>

                    <div class="form-group">
                        <label>7. Investimento de Entrada (Diagnóstico / Projeto):</label>
                        <input type="text" id="initialProjectPrice" value="R$ 25.000" required>
                    </div>

                    <div class="form-group">
                        <label>8. Mensalidade Proposta (Plano Anual):</label>
                        <input type="text" id="monthlyPrice" value="R$ 12.000" required>
                    </div>

                    <button type="submit" class="btn-generate">
                        <i class="fa-solid fa-wand-magic-sparkles"></i> Gerar Proposta Executiva
                    </button>
                </form>
            </div>

            <!-- PAINEL DE VISUALIZAÇÃO DA PROPOSTA GERADA -->
            <div>
                <div class="proposal-actions">
                    <button class="btn-action" onclick="copyProposal()"><i class="fa-regular fa-copy"></i> Copiar Texto</button>
                    <button class="btn-action" onclick="window.print()"><i class="fa-solid fa-print"></i> Imprimir / Salvar em PDF</button>
                </div>

                <div class="proposal-container" id="proposalOutput">
                    <!-- Gerado Dinamicamente -->
                </div>
            </div>
        </div>
    </div>

    <script>
        const presets = {
            clinica: {
                client: "Clínica Médica Vida Saudável (Saúde & Diagnósticos)",
                size: "45 funcionários (30 computadores), faturamento R$ 600.000/mês",
                downtime: "R$ 15.000",
                pains: "Ataque de Ransomware recente (prejuízo de R$ 80.000), backup manual em HD externo sem teste de restore, Wi-Fi de pacientes sem isolamento dos prontuários e lentidão no sistema PACS.",
                services: "1) Assessment de Cibersegurança e Conformidade LGPD Saúde\\n2) Migração de Servidores para Nuvem (AWS/Azure)\\n3) Backup Imutável com Retenção Contínua\\n4) Contrato Recorrente de Governança e Monitoramento 24/7",
                project: "R$ 25.000",
                monthly: "R$ 12.000"
            },
            advocacia: {
                client: "Mattos & Associados Advocacia Empresarial",
                size: "25 advogados (35 computadores), faturamento R$ 450.000/mês",
                downtime: "R$ 10.000",
                pains: "Vazamento de dados sigilosos de clientes em processos arbitrais, perda de prazos por instabilidade de servidores locais e falta de controle de acessos por perfil.",
                services: "1) Auditoria Forense e Adequação LGPD Jurídica\\n2) Implementação de VPN Segura e Autenticação Multifator (MFA)\\n3) Nuvem Privada para Documentos Sigilosos\\n4) Suporte Estratégico e Governança Mensal",
                project: "R$ 18.000",
                monthly: "R$ 8.500"
            },
            contabilidade: {
                client: "Ápice Contabilidade & BPO Financeiro",
                size: "30 colaboradores (40 computadores), faturamento R$ 380.000/mês",
                downtime: "R$ 12.000",
                pains: "Travamento de bancos de dados fiscais no fechamento de mês, computadores lentos sem padronização, risco de multas da Receita Federal por indisponibilidade de transmissão.",
                services: "1) Reestruturação de Banco de Dados e Servidor em Nuvem\\n2) Política de Backup Automatizado 3-2-1\\n3) Proteção de Endpoint contra Phishing Bancário\\n4) Gestão Recorrente de TI e Helpdesk Proativo",
                project: "R$ 15.000",
                monthly: "R$ 7.000"
            },
            distribuidora: {
                client: "Logisul Distribuição & Logística",
                size: "80 funcionários (50 coletores/PCs), faturamento R$ 1.800.000/mês",
                downtime: "R$ 35.000",
                pains: "Galpão parado por falha no link de internet e firewall desconfigurado, atraso no faturamento de caminhões e falta de redundância de links.",
                services: "1) Implantação de Firewall com Failover Automático de 2 Links\\n2) Segmentação de Rede Wi-Fi Industrial para Coletores\\n3) Monitoramento de Redes Zabbix 24/7\\n4) Contrato MSP com SLA de 30 minutos",
                project: "R$ 35.000",
                monthly: "R$ 16.000"
            }
        };

        function loadPreset(key) {
            const p = presets[key];
            document.getElementById('clientName').value = p.client;
            document.getElementById('clientSize').value = p.size;
            document.getElementById('downtimeCost').value = p.downtime;
            document.getElementById('painPoints').value = p.pains.replace(/\\\\n/g, '\\n');
            document.getElementById('servicesProposed').value = p.services.replace(/\\\\n/g, '\\n');
            document.getElementById('initialProjectPrice').value = p.project;
            document.getElementById('monthlyPrice').value = p.monthly;
            generateProposal();
        }

        function generateProposal(e) {
            if (e) e.preventDefault();

            const client = document.getElementById('clientName').value;
            const consultant = document.getElementById('consultantName').value;
            const size = document.getElementById('clientSize').value;
            const downtime = document.getElementById('downtimeCost').value;
            const pains = document.getElementById('painPoints').value;
            const services = document.getElementById('servicesProposed').value;
            const projectPrice = document.getElementById('initialProjectPrice').value;
            const monthlyPrice = document.getElementById('monthlyPrice').value;

            // Cálculos
            const numMonthly = parseFloat(monthlyPrice.replace(/[^0-9]/g, '')) || 10000;
            const numProject = parseFloat(projectPrice.replace(/[^0-9]/g, '')) || 25000;
            const numDowntime = parseFloat(downtime.replace(/[^0-9]/g, '')) || 15000;

            const biennialMonthly = (numMonthly * 0.9); // 10% desconto
            const annualTotal = (numMonthly * 12) + numProject;
            const biennialTotal = (biennialMonthly * 24) + numProject;
            const biennialSavings = (numMonthly * 24) - (biennialMonthly * 24);

            const annualCostOfInaction = (numDowntime * 12) + 80000;
            const estimatedRoi = Math.round(((annualCostOfInaction - annualTotal) / annualTotal) * 100);
            const paybackMonths = Math.max(2, Math.round((annualTotal / (annualCostOfInaction / 12))));

            const dateStr = new Date().toLocaleDateString('pt-BR', { day: '2-digit', month: 'long', year: 'numeric' });

            const html = `
                <div style="border-bottom: 2px solid var(--primary); padding-bottom: 1.5rem; margin-bottom: 2rem; display: flex; justify-content: space-between; align-items: flex-end;">
                    <div>
                        <span style="color: var(--primary); text-transform: uppercase; font-size: 0.8rem; font-weight: 800; letter-spacing: 1px;">Proposta Comercial Estratégica</span>
                        <h2 style="font-family: 'Outfit'; font-size: 1.8rem; color: #fff; margin-top: 4px;">Transformação, Segurança e Continuidade de TI</h2>
                        <div style="color: var(--text-muted); font-size: 0.9rem;">Preparado para: <strong style="color: #fff;">${client}</strong></div>
                    </div>
                    <div style="text-align: right; color: var(--text-dim); font-size: 0.85rem;">
                        <div>Data: ${dateStr}</div>
                        <div>Versão: 2.0 (Executiva)</div>
                    </div>
                </div>

                <!-- MÓDULO 1: CARTA AO EXECUTIVO -->
                <h3 style="color: #38bdf8; font-size: 1.25rem; margin-bottom: 0.75rem;">1. Carta ao Executivo</h3>
                <p>Prezada Diretoria da <strong>${client}</strong>,</p>
                <p>O objetivo deste documento não é vender tecnologia ou horas de suporte tradicional, mas apresentar uma <strong>estratégia blindada de continuidade de negócios, segurança da informação e previsibilidade operacional</strong>.</p>
                <p>Em empresas com a sua relevância e faturamento (${size}), a tecnologia deixou de ser um centro de suporte reativo e passou a ser o coração do faturamento. Uma hora de inatividade representa um impacto direto de <strong>${downtime}/hora</strong>, sem contar os danos reputacionais e regulatórios.</p>
                <p>Apresentamos a seguir nosso plano de ação definitivo para transformar a TI da sua empresa em uma fortaleza de crescimento.</p>

                <!-- MÓDULO 2: CENÁRIO ATUAL & CUSTO DA INAÇÃO -->
                <h3 style="color: #fb923c; font-size: 1.25rem; margin: 2rem 0 0.75rem;">2. Entendendo o Cenário Atual & O Custo da Inação</h3>
                <div class="callout-box callout-danger">
                    <strong style="color: #ef4444;"><i class="fa-solid fa-triangle-exclamation"></i> Diagnóstico de Vulnerabilidade Identificado:</strong>
                    <p style="margin-top: 6px;">${pains.replace(/\\n/g, '<br>')}</p>
                </div>
                <p><strong>O Custo de Não Agir (Cost of Inaction):</strong> Manter o modelo atual sem governança proativa gera um risco anual estimado de <strong>R$ ${annualCostOfInaction.toLocaleString('pt-BR')}</strong> (considerando paradas de sistema e vulnerabilidades críticas).</p>

                <!-- MÓDULO 3: OS 4 PILARES DO PROJETO -->
                <h3 style="color: #34d399; font-size: 1.25rem; margin: 2rem 0 0.75rem;">3. O que a sua Empresa Vai Conquistar</h3>
                <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 1rem; margin: 1rem 0;">
                    <div style="background: rgba(255,255,255,0.03); padding: 1rem; border-radius: 10px; border: 1px solid var(--border);">
                        <strong style="color: #38bdf8;">1. Transformação Operacional</strong>
                        <p style="font-size: 0.85rem; color: var(--text-muted); margin-top: 4px;">Estabilidade absoluta com servidores modernos e sem lentidões nos sistemas críticos.</p>
                    </div>
                    <div style="background: rgba(255,255,255,0.03); padding: 1rem; border-radius: 10px; border: 1px solid var(--border);">
                        <strong style="color: #fb923c;">2. Impacto Financeiro Direto</strong>
                        <p style="font-size: 0.85rem; color: var(--text-muted); margin-top: 4px;">Eliminação do risco de paradas operacionais que custam ${downtime}/hora.</p>
                    </div>
                    <div style="background: rgba(255,255,255,0.03); padding: 1rem; border-radius: 10px; border: 1px solid var(--border);">
                        <strong style="color: #34d399;">3. Segurança Jurídica & LGPD</strong>
                        <p style="font-size: 0.85rem; color: var(--text-muted); margin-top: 4px;">Blindagem de dados sensíveis de clientes e conformidade total com a ANPD.</p>
                    </div>
                    <div style="background: rgba(255,255,255,0.03); padding: 1rem; border-radius: 10px; border: 1px solid var(--border);">
                        <strong style="color: #c084fc;">4. Paz de Espírito para a Diretoria</strong>
                        <p style="font-size: 0.85rem; color: var(--text-muted); margin-top: 4px;">Monitoramento 24/7 com resolução proativa de incidentes antes que afetem a equipe.</p>
                    </div>
                </div>

                <!-- MÓDULO 4: ESCOPO & SERVIÇOS -->
                <h3 style="color: #c084fc; font-size: 1.25rem; margin: 2rem 0 0.75rem;">4. Escopo dos Serviços Estratégicos</h3>
                <div class="callout-box">
                    <strong>Serviços Inclusos na Proposta:</strong>
                    <div style="margin-top: 8px; line-height: 1.8;">${services.replace(/\\n/g, '<br>')}</div>
                </div>

                <!-- MÓDULO 5: MODELO FINANCEIRO & INVESTIMENTO -->
                <h3 style="color: #38bdf8; font-size: 1.25rem; margin: 2rem 0 0.75rem;">5. Proposta de Investimento e Retorno (ROI)</h3>
                
                <table class="prop-table">
                    <thead>
                        <tr>
                            <th>Item de Investimento</th>
                            <th>Plano Anual (12 Meses)</th>
                            <th>Plano Bienal (Incentivo de 10%)</th>
                        </tr>
                    </thead>
                    <tbody>
                        <tr>
                            <td><strong>Projeto de Entrada & Implantação</strong></td>
                            <td>${projectPrice} (Taxa Única)</td>
                            <td>${projectPrice} (Taxa Única)</td>
                        </tr>
                        <tr>
                            <td><strong>Governança Contínua (Retainer Mensal)</strong></td>
                            <td>R$ ${numMonthly.toLocaleString('pt-BR')} / mês</td>
                            <td><strong style="color: #34d399;">R$ ${biennialMonthly.toLocaleString('pt-BR')} / mês</strong></td>
                        </tr>
                        <tr>
                            <td><strong>Investimento Total no Período</strong></td>
                            <td>R$ ${annualTotal.toLocaleString('pt-BR')}</td>
                            <td>R$ ${biennialTotal.toLocaleString('pt-BR')}</td>
                        </tr>
                        <tr>
                            <td><strong>Economia Real no Plano Bienal</strong></td>
                            <td>—</td>
                            <td><strong style="color: #34d399;">Economia de R$ ${biennialSavings.toLocaleString('pt-BR')}</strong></td>
                        </tr>
                    </tbody>
                </table>

                <h4 style="font-size: 1.1rem; color: #34d399; margin: 1.5rem 0 0.5rem;">Indicadores de Retorno sobre o Investimento (ROI):</h4>
                <table class="prop-table">
                    <tbody>
                        <tr>
                            <td><strong>Economia Anual Estimada (Risco Evitado):</strong></td>
                            <td><strong>R$ ${annualCostOfInaction.toLocaleString('pt-BR')}</strong></td>
                        </tr>
                        <tr>
                            <td><strong>Retorno Estimado sobre Investimento (ROI):</strong></td>
                            <td><strong style="color: #38bdf8;">+${estimatedRoi}% ao ano</strong></td>
                        </tr>
                        <tr>
                            <td><strong>Payback Estimado do Projeto:</strong></td>
                            <td><strong style="color: #34d399;">${paybackMonths} meses</strong></td>
                        </tr>
                    </tbody>
                </table>

                <!-- MÓDULO 6: SLA & PRÓXIMOS PASSOS -->
                <h3 style="color: #fb923c; font-size: 1.25rem; margin: 2rem 0 0.75rem;">6. Acordos de Nível de Serviço (SLA) & Garantias</h3>
                <ul style="margin-left: 1.25rem; line-height: 1.8; color: var(--text-muted);">
                    <li><strong>Atendimento a Incidentes Críticos:</strong> Resposta garantida em até <strong>1 hora</strong>.</li>
                    <li><strong>Disponibilidade Garantida (Uptime):</strong> Meta de <strong>99,9%</strong> para serviços críticos.</li>
                    <li><strong>Relatórios Executivos Mensais:</strong> Transparência total com indicadores de saúde da infraestrutura.</li>
                </ul>

                <div style="margin-top: 2.5rem; padding-top: 1.5rem; border-top: 1px solid var(--border); display: flex; justify-content: space-between; align-items: flex-end;">
                    <div>
                        <div style="font-weight: 700; color: #fff;">${consultant}</div>
                        <div style="font-size: 0.85rem; color: var(--text-muted);">Consultor Estratégico de TI & Segurança</div>
                    </div>
                    <div style="text-align: right;">
                        <div style="font-size: 0.85rem; color: var(--text-dim);">Assinatura do Aceite / De Acordo:</div>
                        <div style="border-bottom: 1px solid #64748b; width: 220px; margin-top: 25px;"></div>
                        <div style="font-size: 0.8rem; color: var(--text-dim); margin-top: 4px;">Diretoria: ${client}</div>
                    </div>
                </div>
            `;

            document.getElementById('proposalOutput').innerHTML = html;
        }

        function copyProposal() {
            const text = document.getElementById('proposalOutput').innerText;
            navigator.clipboard.writeText(text).then(() => {
                alert('Proposta copiada para a área de transferência com sucesso!');
            });
        }

        // Gera na inicialização
        window.onload = () => {
            generateProposal();
        };
    </script>
</body>
</html>
"""

with open(os.path.join(DESKTOP, "GERADOR_DE_PROPOSTAS_CONSULTOR_TI.html"), "w", encoding="utf-8") as f:
    f.write(generator_html)

print("Gerador de Propostas HTML gerado no Desktop!")

# Criar o atalho .bat
bat_content = f"""@echo off
title Gerador de Propostas de Consultoria de TI
start "" "{os.path.join(DESKTOP, 'GERADOR_DE_PROPOSTAS_CONSULTOR_TI.html')}"
exit
"""

with open(os.path.join(DESKTOP, "ABRIR_GERADOR_PROPOSTAS.bat"), "w", encoding="utf-8") as f:
    f.write(bat_content)

print("Atalho .bat para o Gerador criado no Desktop!")
