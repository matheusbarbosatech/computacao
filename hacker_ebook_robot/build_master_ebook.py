import os
import subprocess
from generator import HTML_TEMPLATE, generate_pdf_from_html, build_html

# ==============================================================================
# O CÓDIGO DA CONSULTORIA HACKER & CLOUD: O MANUAL DE R$ 50 MIL/MÊS
# Condensado e Modelado das 32 Aulas + 2 Livros do Diogo Molina
# Diagramação Moderna Cyber / High-Ticket (HackerHub Style)
# ==============================================================================

pages = """
<!-- ========================================================================= -->
<!-- PÁGINA 1: CAPA                                                            -->
<!-- ========================================================================= -->
<div class="page cover-page">
    <div class="corner-tl"></div><div class="corner-tr"></div>
    <div class="corner-bl"></div><div class="corner-br"></div>

    <div class="cover-meta">
        CYBER_SECURITY &bull; CLOUD_ARCHITECTURE &bull; MASTER_EDITION_2026
    </div>

    <h1 class="cover-main-title">
        O C&Oacute;DIGO DA <br>
        <span class="cover-highlight">CONSULTORIA HACKER</span> &gt;_
    </h1>
    
    <div class="cover-subtitle" style="max-width: 85%; margin: 15px auto 25px auto; font-size: 13px; color: #a3e635; line-height: 1.5;">
        O M&eacute;todo Pr&aacute;tico de 32 Aulas para Fechar Contratos Recorrentes de R$ 5.000 a R$ 50.000/m&ecirc;s &mdash; Sem Indica&ccedil;&atilde;o, Sem Reuni&otilde;es Longas e Sem Briga de Pre&ccedil;o.
    </div>

    <div class="terminal-box" style="width: 90%; margin: 20px auto; text-align: left;">
        <div class="terminal-header">
            <div class="terminal-buttons">
                <div class="terminal-btn btn-red"></div>
                <div class="terminal-btn btn-yellow"></div>
                <div class="terminal-btn btn-green"></div>
            </div>
            <span>root@consultor-hacker:~# ./executar_framework_50k.sh</span>
        </div>
        <div class="terminal-content">
            <span class="prompt">&gt;$ _</span> <span class="cmd">[STATUS: SISTEMA DE CONSULTORIA ESTRAT&Eacute;GICA ATIVADO]</span><br>
            <span class="comment">// 01. Posicionamento de Alto Valor (Fim da TI de R$ 150)</span><br>
            <span class="comment">// 02. Esteira de SKUs: Auditoria OSINT + FinOps + Cloud + Micro-MSSP</span><br>
            <span class="comment">// 03. Capta&ccedil;&atilde;o Ass&iacute;ncrona: Ataque de Valor &Eacute;tico e Canais White-Label</span><br>
            <span class="comment">// 04. Proposta de 1 P&aacute;gina com Fechamento de 80%</span>
        </div>
    </div>

    <div style="margin-top: 25px; display: flex; justify-content: center; gap: 12px; flex-wrap: wrap;">
        <span class="cyber-badge badge-green">FRAMEWORK 32 AULAS</span>
        <span class="cyber-badge badge-purple">MODELAGEM MOLINA + CYBER</span>
        <span class="cyber-badge badge-amber">RECORR&Ecirc;NCIA 100% ASS&Iacute;NCRONA</span>
    </div>

    <div class="cover-logo-badge" style="margin-top: auto;">
        PLAYBOOK EXECUTIVO <span>50K PREVIS&Iacute;VEL</span>
    </div>
</div>

<!-- ========================================================================= -->
<!-- PÁGINA 2: O CHOQUE DE REALIDADE & O FIM DA TI TRADICIONAL                -->
<!-- ========================================================================= -->
<div class="page">
    <div class="corner-tl"></div><div class="corner-tr"></div>
    <div class="corner-bl"></div><div class="corner-br"></div>

    <div class="page-header">
        <span>M&Oacute;DULO 01 // POSICIONAMENTO MATADOR</span>
        <span class="cyber-badge badge-green">FUNDAMENTO CR&Iacute;TICO</span>
    </div>

    <h1 class="cyber-title">01. O FIM DA TI COMMODITY</h1>
    <h2 class="cyber-subtitle">&gt; Por que formatar PCs e dar suporte gen&eacute;rico &eacute; uma armadilha de exaust&atilde;o</h2>

    <p>
        Nas primeiras aulas do curso, o choque de realidade &eacute; brutal: o profissional t&eacute;cnico passa anos acumulando certifica&ccedil;&otilde;es e conhecimentos dif&iacute;ceis, mas quando vai para o mercado, comete o erro de se vender como <em>"o cara que resolve tudo de TI"</em>.
    </p>

    <div class="cyber-grid" style="margin: 14px 0;">
        <div class="cyber-card alert">
            <h3 class="section-title" style="color: #ef4444; margin-top: 0; font-size: 12px;">&#10006; O T&eacute;cnico de R$ 150 (Guerra de Pre&ccedil;o)</h3>
            <ul style="margin-left: 15px; margin-top: 6px; font-size: 11px; line-height: 1.5;">
                <li>Vende horas trabalhadas e suporte gen&eacute;rico.</li>
                <li>Depende 100% de indica&ccedil;&atilde;o da boca a boca.</li>
                <li>Cliente enxerga como "despesa/custo inevit&aacute;vel".</li>
                <li>Precisa de 80 a 100 clientes para faturar R$ 20k.</li>
            </ul>
        </div>
        <div class="cyber-card success">
            <h3 class="section-title" style="color: #4ade80; margin-top: 0; font-size: 12px;">&#10004; O Consultor Estrat&eacute;gico de R$ 50k</h3>
            <ul style="margin-left: 15px; margin-top: 6px; font-size: 11px; line-height: 1.5;">
                <li>Vende <strong>elimina&ccedil;&atilde;o de preju&iacute;zo, LGPD e redu&ccedil;&atilde;o de custos</strong>.</li>
                <li>Capta&ccedil;&atilde;o ativa e previs&iacute;vel via esteira ass&iacute;ncrona.</li>
                <li>Cliente enxerga como "investimento estrat&eacute;gico".</li>
                <li>Fatura R$ 50k atendendo apenas <strong>5 a 8 clientes de alto valor</strong>.</li>
            </ul>
        </div>
    </div>

    <div class="cyber-card">
        <h3 class="section-title" style="margin-top: 0; font-size: 12px;">A Equa&ccedil;&atilde;o do Valor em Ciberseguran&ccedil;a & Nuvem</h3>
        <p style="font-size: 11.5px;">
            Um dono de empresa <strong>nunca contrata tecnologia pela tecnologia</strong>. Ele compra porque uma falha de seguran&ccedil;a ou servidor inoperante custa R$ 50.000/dia em preju&iacute;zo operacional e multas da ANPD. Quando voc&ecirc; quantifica o risco, o pre&ccedil;o da sua consultoria de R$ 3.000/m&ecirc;s se torna a decis&atilde;o mais barata da vida dele.
        </p>
    </div>

    <div class="terminal-box" style="margin-top: 8px;">
        <div class="terminal-header">
            <span>REGRA DE OURO // EXTRA&Iacute;DA DO LIVRO "POSICIONAMENTO MATADOR"</span>
        </div>
        <div class="terminal-content">
            <span class="prompt">LOGICA:</span> <span class="output">"Generalista compete por pre&ccedil;o e &eacute; tratado como servi&ccedil;al. Especialista dita o pre&ccedil;o, trabalha menos e &eacute; tratado como parceiro de neg&oacute;cios."</span>
        </div>
    </div>

    <div class="page-footer">
        <span>O CODIGO DA CONSULTORIA HACKER</span>
        <span>PAGINA 02</span>
    </div>
</div>

<!-- ========================================================================= -->
<!-- PÁGINA 3: AS 2 BRECHAS DE POSICIONAMENTO E NICHO                          -->
<!-- ========================================================================= -->
<div class="page">
    <div class="corner-tl"></div><div class="corner-tr"></div>
    <div class="corner-bl"></div><div class="corner-br"></div>

    <div class="page-header">
        <span>M&Oacute;DULO 01 // DEFINI&Ccedil;&Atilde;O DE NICHO & MERCADO</span>
        <span class="cyber-badge badge-purple">ALTA MARGEM</span>
    </div>

    <h1 class="cyber-title">02. AS 2 BRECHAS LUCRATIVAS</h1>
    <h2 class="cyber-subtitle">&gt; Como escolher um posicionamento que o mercado n&atilde;o consegue ignorar</h2>

    <p>
        O Molina detalha que existem apenas dois caminhos para se posicionar e cobrar caro imediatamente sem concorrentes:
    </p>

    <div class="cyber-grid" style="margin: 12px 0;">
        <div class="cyber-card">
            <div style="display: flex; align-items: center; gap: 8px; margin-bottom: 6px;">
                <span class="cyber-badge badge-green">BRECHA 1</span>
                <strong style="color: #ffffff; font-size: 12px;">Especializa&ccedil;&atilde;o Horizontal</strong>
            </div>
            <p style="font-size: 11px; margin-bottom: 6px;">
                <strong>(Foco no Problema Cr&iacute;tico):</strong> Voc&ecirc; resolve uma &uacute;nica dor profunda para v&aacute;rios tipos de empresas.
            </p>
            <div style="background: rgba(0,0,0,0.4); padding: 8px; border-radius: 4px; border-left: 2px solid #a3e635; font-size: 10.5px; font-style: italic;">
                "Especialista em detec&ccedil;&atilde;o de superf&iacute;cie exposta e blindagem LGPD para sistemas web e e-commerces."
            </div>
        </div>

        <div class="cyber-card">
            <div style="display: flex; align-items: center; gap: 8px; margin-bottom: 6px;">
                <span class="cyber-badge badge-purple">BRECHA 2</span>
                <strong style="color: #ffffff; font-size: 12px;">Especializa&ccedil;&atilde;o Vertical</strong>
            </div>
            <p style="font-size: 11px; margin-bottom: 6px;">
                <strong>(Foco no Mercado/Nicho):</strong> Voc&ecirc; domina a linguagem, regras e vulnerabilidades de um setor espec&iacute;fico de alto poder aquisitivo.
            </p>
            <div style="background: rgba(0,0,0,0.4); padding: 8px; border-radius: 4px; border-left: 2px solid #c084fc; font-size: 10.5px; font-style: italic;">
                "Consultor de Seguran&ccedil;a e Continuidade de Dados para Escrit&oacute;rios de Advocacia e Cl&iacute;nicas M&eacute;dicas."
            </div>
        </div>
    </div>

    <div class="cyber-card">
        <h3 class="section-title" style="margin-top: 0; font-size: 12px;">Por que nichos regulados pagam 3x mais sem pedir desconto?</h3>
        <p style="font-size: 11px;">
            Escrit&oacute;rios de advocacia e cl&iacute;nicas lidam com sigilo absoluto (processos jur&iacute;dicos, segredos industriais e prontu&aacute;rios m&eacute;dicos). O sequestro desses dados por <em>Ransomware</em> destr&oacute;i a banca da noite para o dia. Eles t&ecirc;m verba sobrando e n&atilde;o t&ecirc;m tempo a perder com curiosos.
        </p>
    </div>

    <div class="terminal-box" style="margin-top: 8px;">
        <div class="terminal-header">
            <span>FRAMEWORK // SELE&Ccedil;&Atilde;O DO SEU P&Uacute;BLICO ALVO</span>
        </div>
        <div class="terminal-content">
            <span class="prompt">[CRIT&Eacute;RIO 1]</span> Poder aquisitivo comprovado (empresas com mais de 10 funcion&aacute;rios).<br>
            <span class="prompt">[CRIT&Eacute;RIO 2]</span> Custo do erro alt&iacute;ssimo (multas, processos ou opera&ccedil;&atilde;o fora do ar).<br>
            <span class="prompt">[CRIT&Eacute;RIO 3]</span> Decisor direto acess&iacute;vel (s&oacute;cio, diretor de opera&ccedil;&otilde;es ou dono).
        </div>
    </div>

    <div class="page-footer">
        <span>O CODIGO DA CONSULTORIA HACKER</span>
        <span>PAGINA 03</span>
    </div>
</div>

<!-- ========================================================================= -->
<!-- PÁGINA 4: A ESTEIRA DE SERVIÇOS & SKUS PRODUTIZADOS                       -->
<!-- ========================================================================= -->
<div class="page">
    <div class="corner-tl"></div><div class="corner-tr"></div>
    <div class="corner-bl"></div><div class="corner-br"></div>

    <div class="page-header">
        <span>M&Oacute;DULO 02 // ESTEIRA DE PRODUTOS (AULAS 14 A 17)</span>
        <span class="cyber-badge badge-green">PRODUTIZA&Ccedil;&Atilde;O</span>
    </div>

    <h1 class="cyber-title">03. A ESTEIRA DE SERVI&Ccedil;OS (SKUs)</h1>
    <h2 class="cyber-subtitle">&gt; Como empacotar seguran&ccedil;a e nuvem em servi&ccedil;os de escopo e valor fixo</h2>

    <p>
        Nas aulas 14, 16 e 17, o Molina ensina a matar a proposta por hora e criar uma <strong>Esteira de SKUs (Stock Keeping Units)</strong> de entrada, entrega principal e recorr&ecirc;ncia:
    </p>

    <div class="cyber-card" style="border-left-color: #38bdf8; margin: 10px 0;">
        <div style="display: flex; justify-content: space-between; align-items: center;">
            <strong style="color: #38bdf8; font-size: 12.5px;">1. SETUP DE ENTRADA: Auditoria de Superf&iacute;cie Exposta (OSINT)</strong>
            <span class="cyber-badge badge-green">R$ 1.500 &mdash; R$ 2.500</span>
        </div>
        <p style="font-size: 11px; margin-top: 4px;">
            Varredura 100% passiva e n&atilde;o invasiva de credenciais vazadas, subdom&iacute;nios &oacute;rf&atilde;os, certificados expirados e portas abertas. Entrega: Relat&oacute;rio Executivo em PDF de 4 p&aacute;ginas com plano de a&ccedil;&atilde;o.
        </p>
    </div>

    <div class="cyber-card" style="border-left-color: #a855f7; margin: 10px 0;">
        <div style="display: flex; justify-content: space-between; align-items: center;">
            <strong style="color: #c084fc; font-size: 12.5px;">2. PROJETO CORE: Migra&ccedil;&atilde;o Cloud & Blindagem de Infra</strong>
            <span class="cyber-badge badge-purple">R$ 5.000 &mdash; R$ 25.000</span>
        </div>
        <p style="font-size: 11px; margin-top: 4px;">
            Migra&ccedil;&atilde;o estrat&eacute;gica de servidores locais para Azure/AWS, isolamento de rede, MFA compuls&oacute;rio, seguran&ccedil;a de endpoints e conformidade t&eacute;cnica com a LGPD.
        </p>
    </div>

    <div class="cyber-card" style="border-left-color: #f59e0b; margin: 10px 0;">
        <div style="display: flex; justify-content: space-between; align-items: center;">
            <strong style="color: #fbbf24; font-size: 12.5px;">3. RECORR&Ecirc;NCIA MENSAL: Micro-MSSP & FinOps Cont&iacute;nuo</strong>
            <span class="cyber-badge badge-amber">R$ 1.500 &mdash; R$ 3.500 / m&ecirc;s</span>
        </div>
        <p style="font-size: 11px; margin-top: 4px;">
            Monitoramento cont&iacute;nuo de novas vulnerabilidades, auditoria de logs de acesso, redu&ccedil;&atilde;o de faturas de cloud (FinOps) e envio de Laudo Mensal de Conformidade para a diretoria.
        </p>
    </div>

    <div class="terminal-box" style="margin-top: 8px;">
        <div class="terminal-header">
            <span>O MODELO DE ESCALA ENXUTA</span>
        </div>
        <div class="terminal-content">
            <span class="prompt">FATURAMENTO:</span> 6 clientes recorrentes a R$ 2.500/m&ecirc;s = <span class="cmd">R$ 15.000/m&ecirc;s</span><br>
            <span class="prompt">PROJETOS:</span> 2 setups/migra&ccedil;&otilde;es de entrada a R$ 7.500 = <span class="cmd">R$ 15.000/m&ecirc;s</span><br>
            <span class="prompt">TOTAL MENSAL:</span> <strong style="color: #a3e635;">R$ 30.000 a R$ 50.000 / m&ecirc;s com apenas 1 consultor operando!</strong>
        </div>
    </div>

    <div class="page-footer">
        <span>O CODIGO DA CONSULTORIA HACKER</span>
        <span>PAGINA 04</span>
    </div>
</div>

<!-- ========================================================================= -->
<!-- PÁGINA 5: CAPTAÇÃO ASSÍNCRONA E O ATAQUE DE VALOR ÉTICO                   -->
<!-- ========================================================================= -->
<div class="page">
    <div class="corner-tl"></div><div class="corner-tr"></div>
    <div class="corner-bl"></div><div class="corner-br"></div>

    <div class="page-header">
        <span>M&Oacute;DULO 03 // M&Aacute;QUINA DE ATRA&Ccedil;&Atilde;O ASS&Iacute;NCRONA</span>
        <span class="cyber-badge badge-green">PROSPEC&Ccedil;&Atilde;O FRIA</span>
    </div>

    <h1 class="cyber-title">04. O ATAQUE DE VALOR &Eacute;TICO</h1>
    <h2 class="cyber-subtitle">&gt; Como atrair decisores sem fazer liga&ccedil;&otilde;es chatas ou spam de vendas</h2>

    <p>
        O Molina ensina que o melhor jeito de fechar contratos de TI n&atilde;o &eacute; mandar uma mensagem dizendo <em>"vendo consultoria"</em>, mas sim **entregar uma amostra irrefut&aacute;vel de diagn&oacute;stico**.
    </p>

    <div class="cyber-card">
        <h3 class="section-title" style="margin-top: 0; font-size: 12px; color: #a3e635;">O Passo a Passo do Ataque de Valor Hacker:</h3>
        <ol style="margin-left: 18px; font-size: 11px; line-height: 1.6;">
            <li><strong>Reconhecimento Passivo:</strong> Voc&ecirc; roda o script de reconhecimento no dom&iacute;nio da empresa (DNS, registros SPF/DMARC mal configurados, e-mails de diretores vazados em breaches p&uacute;blicos).</li>
            <li><strong>Gera&ccedil;&atilde;o do Laudo Preliminar:</strong> Compila em 1 p&aacute;gina visual mostrando o risco real de phishing e sequestro.</li>
            <li><strong>Contato Formal e Educado:</strong> Envia um e-mail direto para o s&oacute;cio ou CEO alertando sobre a vulnerabilidade identificada.</li>
        </ol>
    </div>

    <div class="terminal-box" style="margin-top: 10px;">
        <div class="terminal-header">
            <span>TEMPLATE DE E-MAIL // ABORDAGEM DO ATAQUE DE VALOR</span>
        </div>
        <div class="terminal-content" style="font-size: 11px;">
            <span class="comment">Assunto: [Alerta de Seguran&ccedil;a] Risco de spoofing / exposi&ccedil;&atilde;o no dom&iacute;nio [Empresa.com.br]</span><br><br>
            Ol&aacute;, [Nome do Diretor], tudo bem?<br><br>
            Durante uma auditoria passiva de rotina em sistemas do setor [Setor da Empresa], identifiquei que o dom&iacute;nio <strong>[empresa.com.br]</strong> est&aacute; sem as pol&iacute;ticas DMARC/SPF configuradas, permitindo que terceiros enviem e-mails falsificados se passando pela diretoria da sua empresa.<br><br>
            Documentei essa falha e o passo a passo para corre&ccedil;&atilde;o em um relat&oacute;rio t&eacute;cnico de 1 p&aacute;gina (anexo em PDF sem custo algum).<br><br>
            Se fizer sentido para a sua equipe, posso orientar a corre&ccedil;&atilde;o r&aacute;pida dessa brecha.<br><br>
            Atenciosamente,<br>
            <span class="cmd">[Seu Nome] &bull; Especialista em Auditoria e Seguran&ccedil;a Web</span>
        </div>
    </div>

    <div class="page-footer">
        <span>O CODIGO DA CONSULTORIA HACKER</span>
        <span>PAGINA 05</span>
    </div>
</div>

<!-- ========================================================================= -->
<!-- PÁGINA 6: O CANAL WHITE-LABEL (O SEGREDO DAS AGÊNCIAS)                    -->
<!-- ========================================================================= -->
<div class="page">
    <div class="corner-tl"></div><div class="corner-tr"></div>
    <div class="corner-bl"></div><div class="corner-br"></div>

    <div class="page-header">
        <span>M&Oacute;DULO 03 // ESCALA POR PARCERIAS</span>
        <span class="cyber-badge badge-purple">CANAL WHITE-LABEL</span>
    </div>

    <h1 class="cyber-title">05. A PARCERIA COM AG&Ecirc;NCIAS</h1>
    <h2 class="cyber-subtitle">&gt; Como conseguir 10 a 20 clientes de bandeja sem precisar prospectar um por um</h2>

    <p>
        Uma das maiores sacadas do m&eacute;todo &eacute; a utiliza&ccedil;&atilde;o de **Canais de Distribui&ccedil;&atilde;o**. Em vez de ca&ccedil;ar cliente por cliente, voc&ecirc; faz parceria com quem j&aacute; tem a confian&ccedil;a das empresas.
    </p>

    <div class="cyber-grid" style="margin: 12px 0;">
        <div class="cyber-card">
            <h3 class="section-title" style="margin-top: 0; font-size: 12px; color: #38bdf8;">A Dor das Ag&ecirc;ncias Web</h3>
            <p style="font-size: 11px;">
                Ag&ecirc;ncias de marketing e software houses constroem sites e lojas virtuais para centenas de empresas. Por&eacute;m, elas **n&atilde;o entendem nada de seguran&ccedil;a t&eacute;cnica e LGPD**, vivendo com medo de seus clientes serem invadidos.
            </p>
        </div>
        <div class="cyber-card success">
            <h3 class="section-title" style="margin-top: 0; font-size: 12px; color: #4ade80;">A Sua Solu&ccedil;&atilde;o nos Bastidores</h3>
            <p style="font-size: 11px;">
                Voc&ecirc; atua como o **Bra&ccedil;o de Seguran&ccedil;a White-Label**. A ag&ecirc;ncia vende a auditoria/manuten&ccedil;&atilde;o de seguran&ccedil;a com a marca dela, coloca a margem de lucro em cima, e voc&ecirc; apenas roda seus scripts e envia os laudos em PDF.
            </p>
        </div>
    </div>

    <div class="terminal-box" style="margin-top: 10px;">
        <div class="terminal-header">
            <span>PROPOSTA DE PARCERIA // E-MAIL PARA DONOS DE AG&Ecirc;NCIA</span>
        </div>
        <div class="terminal-content" style="font-size: 11px;">
            <span class="comment">Assunto: Parceria t&eacute;cnica de seguran&ccedil;a e blindagem LGPD para os clientes da [Nome da Ag&ecirc;ncia]</span><br><br>
            Ol&aacute;, [Nome do Dono da Ag&ecirc;ncia], tudo bem?<br><br>
            Acompanho os projetos da sua ag&ecirc;ncia e vejo a qualidade das lojas e plataformas que voc&ecirc;s entregam.<br><br>
            Hoje atuo como especialista t&eacute;cnico em seguran&ccedil;a cibern&eacute;tica e auditoria de vulnerabilidades para ag&ecirc;ncias em formato <strong>White-Label</strong>. N&oacute;s realizamos a auditoria e o monitoramento nos bastidores para que voc&ecirc;s possam oferecer o <strong>Selo de Prote&ccedil;&atilde;o LGPD</strong> e seguran&ccedil;a cont&iacute;nua aos seus clientes, gerando uma nova receita recorrente sem que sua equipe precise gastar tempo com infraestrutura.<br><br>
            Podemos trocar 3 minutos de mensagens para eu te apresentar como funciona o modelo?
        </div>
    </div>

    <div class="page-footer">
        <span>O CODIGO DA CONSULTORIA HACKER</span>
        <span>PAGINA 06</span>
    </div>
</div>

<!-- ========================================================================= -->
<!-- PÁGINA 7: A PROPOSTA DE 1 PÁGINA QUE FECHA 80%                            -->
<!-- ========================================================================= -->
<div class="page">
    <div class="corner-tl"></div><div class="corner-tr"></div>
    <div class="corner-bl"></div><div class="corner-br"></div>

    <div class="page-header">
        <span>M&Oacute;DULO 04 // FECHAMENTO & PROPOSTAS</span>
        <span class="cyber-badge badge-amber">ALTA CONVERS&Atilde;O</span>
    </div>

    <h1 class="cyber-title">06. A PROPOSTA DE 1 P&Aacute;GINA</h1>
    <h2 class="cyber-subtitle">&gt; O formato que elimina a compara&ccedil;&atilde;o de pre&ccedil;o e fecha contratos de R$ 5k a R$ 25k</h2>

    <p>
        Nas aulas sobre propostas irresist&iacute;veis, o Molina mostra que propostas de 20 p&aacute;ginas cheias de "institucional" s&oacute; servem para travar a venda. A proposta que fecha possui exatamente **5 blocos cir&uacute;rgicos**:
    </p>

    <div class="cyber-card" style="margin: 10px 0;">
        <table style="width: 100%; border-collapse: collapse; font-size: 11px;">
            <tr style="border-bottom: 1px solid rgba(168, 85, 247, 0.3);">
                <td style="padding: 6px; width: 25%; color: #ccff00; font-family: 'Fira Code', monospace;"><strong>BLOCO 1: O Cen&aacute;rio</strong></td>
                <td style="padding: 6px; color: #cbd5e1;">Diagn&oacute;stico r&aacute;pido dos riscos atuais identificados na empresa (ex: 2 falhas cr&iacute;ticas de exposi&ccedil;&atilde;o e risco de multa LGPD).</td>
            </tr>
            <tr style="border-bottom: 1px solid rgba(168, 85, 247, 0.3);">
                <td style="padding: 6px; color: #38bdf8; font-family: 'Fira Code', monospace;"><strong>BLOCO 2: O Objetivo</strong></td>
                <td style="padding: 6px; color: #cbd5e1;">A meta clara em 1 frase: <em>"Blindagem completa do ambiente e elimina&ccedil;&atilde;o do risco de sequestro de dados."</em></td>
            </tr>
            <tr style="border-bottom: 1px solid rgba(168, 85, 247, 0.3);">
                <td style="padding: 6px; color: #c084fc; font-family: 'Fira Code', monospace;"><strong>BLOCO 3: O Escopo</strong></td>
                <td style="padding: 6px; color: #cbd5e1;">Lista de 3 a 5 entreg&aacute;veis t&eacute;cnicos fixos (sem men&ccedil;&atilde;o a horas ou tempo gasto).</td>
            </tr>
            <tr style="border-bottom: 1px solid rgba(168, 85, 247, 0.3);">
                <td style="padding: 6px; color: #f59e0b; font-family: 'Fira Code', monospace;"><strong>BLOCO 4: O Cronograma</strong></td>
                <td style="padding: 6px; color: #cbd5e1;">Prazo estimado de conclus&atilde;o do setup (ex: 10 dias &uacute;teis) e in&iacute;cio da recorr&ecirc;ncia.</td>
            </tr>
            <tr>
                <td style="padding: 6px; color: #4ade80; font-family: 'Fira Code', monospace;"><strong>BLOCO 5: O Investimento</strong></td>
                <td style="padding: 6px; color: #cbd5e1;">Valor do Setup (R$ 2.500) + Mensalidade do Micro-MSSP (R$ 1.500/m&ecirc;s), ancorado no valor do preju&iacute;zo evitado.</td>
            </tr>
        </table>
    </div>

    <div class="terminal-box" style="margin-top: 8px;">
        <div class="terminal-header">
            <span>RESPOSTA &Agrave; OBJE&Ccedil;&Atilde;O // "ACHEI CARO / FAZ POR MENOS?"</span>
        </div>
        <div class="terminal-content" style="font-size: 11px;">
            <span class="prompt">SCRIPT:</span> "Entendo perfeitamente, [Nome]. Nosso valor n&atilde;o reflete o tempo que passamos digitando comandos, mas sim a garantia de que sua empresa n&atilde;o sofrer&aacute; um preju&iacute;zo de R$ 50 mil por dia de parada ou vazamento. Se precisarmos ajustar o valor, precisaremos retirar a cobertura de monitoramento cont&iacute;nuo, deixando esse risco descoberto."
        </div>
    </div>

    <div class="page-footer">
        <span>O CODIGO DA CONSULTORIA HACKER</span>
        <span>PAGINA 07</span>
    </div>
</div>

<!-- ========================================================================= -->
<!-- PÁGINA 8: O CHECKLIST EXECUTIVO DE 30 DIAS                                -->
<!-- ========================================================================= -->
<div class="page">
    <div class="corner-tl"></div><div class="corner-tr"></div>
    <div class="corner-bl"></div><div class="corner-br"></div>

    <div class="page-header">
        <span>M&Oacute;DULO 05 // PLANO DE EXECU&Ccedil;&Atilde;O PR&Aacute;TICO</span>
        <span class="cyber-badge badge-green">CHECKLIST 30 DIAS</span>
    </div>

    <h1 class="cyber-title">07. PLANO DE A&Ccedil;&Atilde;O DE 30 DIAS</h1>
    <h2 class="cyber-subtitle">&gt; O roteiro para colocar sua consultoria hacker faturando este m&ecirc;s</h2>

    <p>
        Para n&atilde;o deixar o conhecimento preso no papel, execute rigorosamente este plano de 4 semanas:
    </p>

    <div class="cyber-grid" style="margin: 10px 0;">
        <div class="cyber-card">
            <h4 style="color: #a3e635; margin: 0 0 4px 0; font-size: 11.5px;">SEMANA 1: Posicionamento & SKU</h4>
            <ul style="margin-left: 14px; font-size: 10.5px; line-height: 1.45;">
                <li>Escolha 1 nicho (Horizontal ou Vertical).</li>
                <li>Defina o SKU de entrada (Auditoria OSINT R$ 1.500).</li>
                <li>Prepare seu modelo de Laudo Executivo em PDF.</li>
            </ul>
        </div>

        <div class="cyber-card">
            <h4 style="color: #38bdf8; margin: 0 0 4px 0; font-size: 11.5px;">SEMANA 2: Mapeamento de Alvos</h4>
            <ul style="margin-left: 14px; font-size: 10.5px; line-height: 1.45;">
                <li>Liste 30 ag&ecirc;ncias web e software houses da sua regi&atilde;o.</li>
                <li>Liste 20 empresas de m&eacute;dio porte com brechas p&uacute;blicas.</li>
                <li>Gere o relat&oacute;rio de demonstra&ccedil;&atilde;o pr&eacute;vio.</li>
            </ul>
        </div>

        <div class="cyber-card">
            <h4 style="color: #c084fc; margin: 0 0 4px 0; font-size: 11.5px;">SEMANA 3: Disparos & Abordagem</h4>
            <ul style="margin-left: 14px; font-size: 10.5px; line-height: 1.45;">
                <li>Envie 10 e-mails de Ataque de Valor &Eacute;tico por dia.</li>
                <li>Fa&ccedil;a o contato White-Label com donos de ag&ecirc;ncias.</li>
                <li>Mantenha a comunica&ccedil;&atilde;o 100% formal e ass&iacute;ncrona.</li>
            </ul>
        </div>

        <div class="cyber-card">
            <h4 style="color: #4ade80; margin: 0 0 4px 0; font-size: 11.5px;">SEMANA 4: Fechamento & Recorr&ecirc;ncia</h4>
            <ul style="margin-left: 14px; font-size: 10.5px; line-height: 1.45;">
                <li>Envie a Proposta de 1 P&aacute;gina para os interessados.</li>
                <li>Feche os 2 primeiros setups de R$ 2.500.</li>
                <li>Ative o contrato mensal de Micro-MSSP (R$ 1.500/m&ecirc;s).</li>
            </ul>
        </div>
    </div>

    <div class="terminal-box" style="margin-top: 10px;">
        <div class="terminal-header">
            <span>root@consultor-hacker:~# ./conclusao_master.sh</span>
        </div>
        <div class="terminal-content">
            <span class="prompt">[SISTEMA]</span> "Voc&ecirc; agora tem o mapa completo, a esteira de SKUs, os scripts de capta&ccedil;&atilde;o e o m&eacute;todo de fechamento. A diferen&ccedil;a entre o consultor de R$ 150 e o de R$ 50 mil &eacute; apenas a coragem de parar de vender horas e come&ccedil;ar a vender valor estrat&eacute;gico."
        </div>
    </div>

    <div class="page-footer">
        <span>O CODIGO DA CONSULTORIA HACKER</span>
        <span>PAGINA 08 // FIM DO MANUAL</span>
    </div>
</div>
"""

def generate_master_ebook():
    output_pdf = r"C:\Users\matheus\Desktop\O_Codigo_da_Consultoria_Hacker_e_Cloud.pdf"
    html = build_html("O Código da Consultoria Hacker - Manual 50k", pages)
    generate_pdf_from_html(html, output_pdf)
    print(f"Master E-book generated at: {output_pdf}")

if __name__ == "__main__":
    generate_master_ebook()
