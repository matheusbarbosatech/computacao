import os
import subprocess
from generator import HTML_TEMPLATE, generate_pdf_from_html, build_html

pages = """
<!-- ========================================================================= -->
<!-- PÁGINA 1: CAPA                                                            -->
<!-- ========================================================================= -->
<div class="page cover-page">
    <div class="corner-tl"></div><div class="corner-tr"></div>
    <div class="corner-bl"></div><div class="corner-br"></div>

    <div class="cover-meta">
        01000011 01011001 01000010 01000101 01010010 &bull; SEC_LEVEL_05 &bull; EDICAO_2026
    </div>

    <h1 class="cover-main-title">
        $ CONSULTOR <span class="cover-highlight">[PREMIUM]</span> HACKER &gt;_
    </h1>
    
    <div class="cover-subtitle" style="max-width: 80%; margin: 0 auto 30px auto; font-size: 13px; color: #a3e635;">
        O m&eacute;todo ass&iacute;ncrono para transformar l&oacute;gica t&eacute;cnica em demanda constante e contratos recorrentes de R$ 5.000 a R$ 15.000/m&ecirc;s em Ciberseguran&ccedil;a.
    </div>

    <div class="terminal-box" style="width: 88%; margin: 25px auto; text-align: left;">
        <div class="terminal-header">
            <div class="terminal-buttons">
                <div class="terminal-btn btn-red"></div>
                <div class="terminal-btn btn-yellow"></div>
                <div class="terminal-btn btn-green"></div>
            </div>
            <span>root@consultoria:~# ./iniciar_posicionamento.sh</span>
        </div>
        <div class="terminal-content">
            <span class="prompt">&gt;$ _</span> <span class="cmd">status: pronto para execucao documental</span><br>
            <span class="comment">// Sem reunioes de alinhamento interminaveis. Sem "venda de labia".</span><br>
            <span class="comment">// Apenas prova tecnica de vulnerabilidade, laudo executivo e contratos blindados.</span>
        </div>
    </div>

    <div style="margin-top: 35px; display: flex; justify-content: center; gap: 15px;">
        <span class="cyber-badge badge-green">100% ASS&Iacute;NCRONO</span>
        <span class="cyber-badge badge-purple">SERVI&Ccedil;O PRODUTIZADO (SKU)</span>
        <span class="cyber-badge badge-amber">MICRO-MSSP RECORRENTE</span>
    </div>

    <div class="cover-logo-badge" style="margin-top: auto;">
        CYBER CONSULTANT <span>PREMIUM</span>
    </div>
</div>

<!-- ========================================================================= -->
<!-- PÁGINA 2: O MANIFESTO & O CHOQUE DE REALIDADE                             -->
<!-- ========================================================================= -->
<div class="page">
    <div class="corner-tl"></div><div class="corner-tr"></div>
    <div class="corner-bl"></div><div class="corner-br"></div>

    <div class="page-header">
        <span>CAP&Iacute;TULO 01 // FUNDAMENTOS</span>
        <span class="cyber-badge badge-green">STATUS: ESSENCIAL</span>
    </div>

    <h1 class="cyber-title">01. O FIM DA TI TRADICIONAL</h1>
    <h2 class="cyber-subtitle">&gt; Por que formatar PCs e dar suporte gen&eacute;rico &eacute; uma armadilha de exaust&atilde;o</h2>

    <p>
        A maioria dos profissionais de tecnologia com alta capacidade anal&iacute;tica comete o mesmo erro tr&aacute;gico: vender <strong>"tempo trabalhado"</strong> e <strong>"suporte t&eacute;cnico"</strong>. O resultado &eacute; sempre o mesmo: clientes leigos ligando no fim de semana, cobran&ccedil;a por hora humilhante e a sensa&ccedil;&atilde;o constante de desvaloriza&ccedil;&atilde;o.
    </p>

    <div class="cyber-grid" style="margin: 18px 0;">
        <div class="cyber-card alert">
            <h3 class="section-title" style="color: #ef4444; margin-top: 0; font-size: 13px;">&#10006; O Consultor de TI Comum</h3>
            <ul style="margin-left: 18px; margin-top: 8px; font-size: 12px; line-height: 1.6;">
                <li>Vende suporte, helpdesk e formata&ccedil;&atilde;o.</li>
                <li>Preso em reuni&otilde;es sociais exaustivas.</li>
                <li>Cobran&ccedil;a por hora (teto de ganhos r&iacute;gido).</li>
                <li>Cliente enxerga como "despesa chata".</li>
            </ul>
        </div>
        <div class="cyber-card success">
            <h3 class="section-title" style="color: #4ade80; margin-top: 0; font-size: 13px;">&#10004; O Consultor Premium Hacker</h3>
            <ul style="margin-left: 18px; margin-top: 8px; font-size: 12px; line-height: 1.6;">
                <li>Vende <strong>mitiga&ccedil;&atilde;o de risco jur&iacute;dico e financeiro (LGPD)</strong>.</li>
                <li>Comunica&ccedil;&atilde;o 100% ass&iacute;ncrona e documental.</li>
                <li>Cobran&ccedil;a por valor e escopo fixo (SKUs).</li>
                <li>Cliente enxerga como "blindagem estrat&eacute;gica".</li>
            </ul>
        </div>
    </div>

    <div class="cyber-card">
        <h3 class="section-title" style="margin-top: 0;">A Equa&ccedil;&atilde;o do Valor em Ciberseguran&ccedil;a</h3>
        <p style="font-size: 12px;">
            Uma empresa n&atilde;o contrata um Pentest porque gosta de tecnologia. Ela contrata porque o vazamento de sua base de clientes acarreta <strong>multas de at&eacute; R$ 50 milh&otilde;es pela LGPD</strong>, perda de reputa&ccedil;&atilde;o irrepar&aacute;vel e processos judiciais. O seu papel &eacute; identificar e documentar a falha antes que um invasor criminoso o fa&ccedil;a.
        </p>
    </div>

    <div class="terminal-box" style="margin-top: 10px;">
        <div class="terminal-header">
            <span>logica_de_precificacao.py</span>
        </div>
        <div class="terminal-content">
            <span class="cmd">custo_da_brecha</span> = <span class="output">R$ 150.000,00</span> <span class="comment">(multa + perda de operacao)</span><br>
            <span class="cmd">valor_do_seu_laudo</span> = <span class="output">R$ 3.500,00</span> <span class="comment">(2.3% do risco total)</span><br>
            <span class="prompt">&gt;&gt;&gt;</span> Para o empres&aacute;rio s&eacute;rio, seu servi&ccedil;o n&atilde;o &eacute; custo: &eacute; o seguro mais barato da empresa.
        </div>
    </div>

    <div class="page-footer">
        <span>CONSULTOR PREMIUM HACKER</span>
        <span>P&Aacute;GINA 02 // 08</span>
    </div>
</div>

<!-- ========================================================================= -->
<!-- PÁGINA 3: O PORTFÓLIO DE PRODUTOS FECHADOS (SKUS)                         -->
<!-- ========================================================================= -->
<div class="page">
    <div class="corner-tl"></div><div class="corner-tr"></div>
    <div class="corner-bl"></div><div class="corner-br"></div>

    <div class="page-header">
        <span>CAP&Iacute;TULO 02 // EMPACOTAMENTO</span>
        <span class="cyber-badge badge-purple">ARQUITETURA DE OFERTA</span>
    </div>

    <h1 class="cyber-title">02. OS 3 PRODUTOS DE PRATELEIRA (SKUs)</h1>
    <h2 class="cyber-subtitle">&gt; Nunca venda consultoria aberta; venda entreg&aacute;veis fechados</h2>

    <p>
        Para eliminar o atrito social e o desgaste de negociar escopos infinitos, o Consultor Premium Hacker opera com um cat&aacute;logo fechado de <strong>produtos com in&iacute;cio, meio e fim documentados</strong>:
    </p>

    <!-- SKU 1 -->
    <div class="cyber-card" style="border-left-color: #38bdf8;">
        <div style="display: flex; justify-content: space-between; align-items: center;">
            <strong style="color: #38bdf8; font-size: 14px; font-family: 'Orbitron';">SKU 1: Auditoria de Superf&iacute;cie Exposta (OSINT Passivo)</strong>
            <span class="cyber-badge badge-green">ENTRADA: R$ 1.500 a R$ 2.500</span>
        </div>
        <p style="margin-top: 6px; font-size: 12px;">
            <strong>O que &eacute;:</strong> Mapeamento 100% passivo e n&atilde;o-intrusivo. Varredura de subdom&iacute;nios, arquivos sens&iacute;veis abertos no Google (<code>.git</code>, <code>.env</code>, backups), portas expostas e credenciais de colaboradores vazadas na Dark Web.
        </p>
        <div style="font-family: 'Fira Code'; font-size: 11px; color: #94a3b8; margin-top: 4px;">
            &bull; Entrega: Relat&oacute;rio T&eacute;cnico em PDF (12 a 15 p&aacute;gs) &bull; Custo Social: ZERO reuni&otilde;es.
        </div>
    </div>

    <!-- SKU 2 -->
    <div class="cyber-card" style="border-left-color: #c084fc;">
        <div style="display: flex; justify-content: space-between; align-items: center;">
            <strong style="color: #c084fc; font-size: 14px; font-family: 'Orbitron';">SKU 2: Pentest Web &amp; API (Escopo Autorizado)</strong>
            <span class="cyber-badge badge-purple">PROJETO: R$ 3.500 a R$ 7.000</span>
        </div>
        <p style="margin-top: 6px; font-size: 12px;">
            <strong>O que &eacute;:</strong> Teste pr&aacute;tico de intrus&atilde;o direcionado a um sistema, e-commerce ou API espec&iacute;fica, focado no Top 10 OWASP (Inje&ccedil;&atilde;o SQL, IDOR, Broken Authentication, falhas de autoriza&ccedil;&atilde;o).
        </p>
        <div style="font-family: 'Fira Code'; font-size: 11px; color: #94a3b8; margin-top: 4px;">
            &bull; Entrega: Laudo de Vulnerabilidade com PoC (c&oacute;digo para reprodu&ccedil;&atilde;o) e guia t&eacute;cnico de corre&ccedil;&atilde;o.
        </div>
    </div>

    <!-- SKU 3 -->
    <div class="cyber-card" style="border-left-color: #bef264;">
        <div style="display: flex; justify-content: space-between; align-items: center;">
            <strong style="color: #bef264; font-size: 14px; font-family: 'Orbitron';">SKU 3: Micro-MSSP (Recorr&ecirc;ncia Mensal)</strong>
            <span class="cyber-badge badge-green">RECORR&Ecirc;NCIA: R$ 1.500 a R$ 3.000/M&Ecirc;S</span>
        </div>
        <p style="margin-top: 6px; font-size: 12px;">
            <strong>O que &eacute;:</strong> Gest&atilde;o cont&iacute;nua da postura de seguran&ccedil;a. 1 varredura automatizada mensal em novas atualiza&ccedil;&otilde;es do c&oacute;digo + monitoramento peri&oacute;dico de credenciais + laudo mensal de conformidade LGPD.
        </p>
        <div style="font-family: 'Fira Code'; font-size: 11px; color: #94a3b8; margin-top: 4px;">
            &bull; Entrega: 1 Laudo Mensal consolidado &bull; Esfor&ccedil;o operacional: 3 a 4 horas por m&ecirc;s.
        </div>
    </div>

    <div class="page-footer">
        <span>CONSULTOR PREMIUM HACKER</span>
        <span>P&Aacute;GINA 03 // 08</span>
    </div>
</div>

<!-- ========================================================================= -->
<!-- PÁGINA 4: PROSPECÇÃO FRIA SEM CONVERSA MOLE                               -->
<!-- ========================================================================= -->
<div class="page">
    <div class="corner-tl"></div><div class="corner-tr"></div>
    <div class="corner-bl"></div><div class="corner-br"></div>

    <div class="page-header">
        <span>CAP&Iacute;TULO 03 // CAPTA&Ccedil;&Atilde;O ASS&Iacute;NCRONA</span>
        <span class="cyber-badge badge-amber">M&Eacute;TODO PR&Aacute;TICO</span>
    </div>

    <h1 class="cyber-title">03. O "ATAQUE DE VALOR" &Eacute;TICO</h1>
    <h2 class="cyber-subtitle">&gt; Como abrir portas em empresas sem ligar para ningu&eacute;m e sem reuni&otilde;es de venda</h2>

    <p>
        Pessoas t&eacute;cnicas odeiam "fazer networking" ou fingir simpatia corporativa. O m&eacute;todo do <strong>Ataque de Valor &Eacute;tico</strong> substitui a l&aacute;bia pela for&ccedil;a incontest&aacute;vel dos fatos:
    </p>

    <div class="terminal-box">
        <div class="terminal-header">
            <span>email_template // abordagem_direta.eml</span>
        </div>
        <div class="terminal-content">
            <span class="prompt">Assunto:</span> <span class="cmd">[Aviso de Seguran&ccedil;a] Vulnerabilidade p&uacute;blica identificada no dom&iacute;nio [empresa.com.br]</span><br><br>
            Prezado [Nome do CTO / Fundador],<br><br>
            Durante uma rotina passiva de an&aacute;lise de seguran&ccedil;a em ativos web, identifiquei que o endpoint <strong>/admin/backup.tar.gz</strong> (ou diret&oacute;rio <code>.git</code>) do seu sistema est&aacute; indexado publicamente.<br><br>
            Isso exp&otilde;e credenciais de banco de dados e dados cobertos pela LGPD. Em anexo, envio um <strong>Laudo T&eacute;cnico Gratuito (PDF)</strong> com a Prova de Conceito e os 3 passos exatos para que sua equipe neutralize o risco hoje.<br><br>
            N&atilde;o realizei nenhum teste intrusivo. Se tiver interesse em um diagn&oacute;stico completo de superf&iacute;cie exposta em todos os ativos da empresa, o escopo est&aacute; detalhado no documento.<br><br>
            Atenciosamente,<br>
            <span class="prompt">[Seu Nome] &bull; Especialista em An&aacute;lise de Vulnerabilidades</span>
        </div>
    </div>

    <div class="cyber-grid">
        <div class="cyber-card">
            <strong style="color: #c084fc;">Por que esse m&eacute;todo converte?</strong>
            <p style="font-size: 11.5px; margin-top: 6px;">
                1. Voc&ecirc; n&atilde;o pede favor: voc&ecirc; entrega solu&ccedil;&atilde;o imediata.<br>
                2. Destr&oacute;i a barreira da desconfian&ccedil;a.<br>
                3. O CTO l&ecirc; o relat&oacute;rio e percebe que voc&ecirc; domina o assunto.
            </p>
        </div>
        <div class="cyber-card success">
            <strong style="color: #4ade80;">Canal White-Label (Ag&ecirc;ncias):</strong>
            <p style="font-size: 11.5px; margin-top: 6px;">
                Contate donos de ag&ecirc;ncias web: voc&ecirc; audita os softwares que eles constroem nos bastidores. A ag&ecirc;ncia coloca a marca dela e vende mais caro pro cliente; voc&ecirc; apenas entrega o PDF.
            </p>
        </div>
    </div>

    <div class="page-footer">
        <span>CONSULTOR PREMIUM HACKER</span>
        <span>P&Aacute;GINA 04 // 08</span>
    </div>
</div>

<!-- ========================================================================= -->
<!-- PÁGINA 5: A ANATOMIA DO LAUDO TÉCNICO PERFEITO                            -->
<!-- ========================================================================= -->
<div class="page">
    <div class="corner-tl"></div><div class="corner-tr"></div>
    <div class="corner-bl"></div><div class="corner-br"></div>

    <div class="page-header">
        <span>CAP&Iacute;TULO 04 // ENTREG&Aacute;VEL</span>
        <span class="cyber-badge badge-green">PADR&Atilde;O DE OURO</span>
    </div>

    <h1 class="cyber-title">04. A ANATOMIA DO LAUDO T&Eacute;CNICO</h1>
    <h2 class="cyber-subtitle">&gt; O documento em PDF &eacute; o seu verdadeiro produto</h2>

    <p>
        Em ciberseguran&ccedil;a, o seu cliente n&atilde;o v&ecirc; o c&oacute;digo rodando no seu terminal: ele v&ecirc; o <strong>Laudo T&eacute;cnico Formal</strong>. &Eacute; a qualidade desse documento que justifica cobrar R$ 3.500 a R$ 5.000 por avalia&ccedil;&atilde;o:
    </p>

    <div class="cyber-card" style="margin: 12px 0;">
        <h3 class="section-title" style="margin-top: 0; font-size: 13px;">1. Sum&aacute;rio Executivo (Para a Diretoria)</h3>
        <p style="font-size: 12px;">
            Linguagem s&oacute;bria e sem jarg&otilde;es t&eacute;cnicos. Traduz as falhas em <strong>risco financeiro, jur&iacute;dico e operacional</strong>. Um gr&aacute;fico de pizza visual (Cr&iacute;tico, Alto, M&eacute;dio) mostra exatamente onde a empresa est&aacute; exposta.
        </p>
    </div>

    <div class="cyber-card" style="margin: 12px 0;">
        <h3 class="section-title" style="margin-top: 0; font-size: 13px; color: #a3e635;">2. Matriz de Vulnerabilidades &amp; Pontua&ccedil;&atilde;o CVSS 3.1</h3>
        <p style="font-size: 12px;">
            Classifica&ccedil;&atilde;o matem&aacute;tica de gravidade (CVSS Score). N&atilde;o &eacute; a sua opini&atilde;o subjetiva; &eacute; o padr&atilde;o global da ind&uacute;stria.
        </p>
    </div>

    <div class="cyber-card alert" style="margin: 12px 0;">
        <h3 class="section-title" style="margin-top: 0; font-size: 13px; color: #ef4444;">3. Prova de Conceito T&eacute;cnica (PoC)</h3>
        <p style="font-size: 12px;">
            Passo a passo exato com prints e requisi&ccedil;&otilde;es HTTP para que os desenvolvedores internos consigam reproduzir o problema no laborat&oacute;rio deles.
        </p>
    </div>

    <div class="cyber-card success" style="margin: 12px 0;">
        <h3 class="section-title" style="margin-top: 0; font-size: 13px; color: #4ade80;">4. Guia Direto de Remedia&ccedil;&atilde;o &amp; Reteste</h3>
        <p style="font-size: 12px;">
            Snippets de c&oacute;digo e instru&ccedil;&otilde;es claras de configura&ccedil;&atilde;o (Apache, Nginx, c&oacute;digo-fonte). Inclui direito a <strong>1 reteste formal</strong> ap&oacute;s a corre&ccedil;&atilde;o para emitir o selo de conformidade.
        </p>
    </div>

    <div class="page-footer">
        <span>CONSULTOR PREMIUM HACKER</span>
        <span>P&Aacute;GINA 05 // 08</span>
    </div>
</div>

<!-- ========================================================================= -->
<!-- PÁGINA 6: A MATEMÁTICA DOS R$ 5.000 RECORRENTES                           -->
<!-- ========================================================================= -->
<div class="page">
    <div class="corner-tl"></div><div class="corner-tr"></div>
    <div class="corner-bl"></div><div class="corner-br"></div>

    <div class="page-header">
        <span>CAP&Iacute;TULO 05 // FINAN&Ccedil;AS &amp; RECORR&Ecirc;NCIA</span>
        <span class="cyber-badge badge-green">MICRO-MSSP</span>
    </div>

    <h1 class="cyber-title">05. A MATEM&Aacute;TICA DA RECORR&Ecirc;NCIA</h1>
    <h2 class="cyber-subtitle">&gt; Como construir R$ 5.000 a R$ 10.000 mensais com poucos clientes</h2>

    <p>
        O segredo da tranquilidade mental &eacute; n&atilde;o ter de ca&ccedil;ar clientes novos todos os meses. Voc&ecirc; constr&oacute;i uma base fixa de <strong>contratos recorrentes (retainers)</strong>:
    </p>

    <div class="terminal-box" style="margin: 16px 0;">
        <div class="terminal-header">
            <span>modelo_financeiro.sh</span>
        </div>
        <div class="terminal-content">
            <span class="comment"># Cen&aacute;rio 1: Alvo R$ 5.000/m&ecirc;s (Fase Inicial)</span><br>
            <span class="cmd">&bull; 2 clientes</span> a <span class="output">R$ 2.500,00/m&ecirc;s</span> = <span class="prompt">R$ 5.000,00 recorrentes</span><br>
            <span class="comment"># Cen&aacute;rio 2: Alvo R$ 7.500/m&ecirc;s (Fase de Tra&ccedil;&atilde;o)</span><br>
            <span class="cmd">&bull; 3 clientes</span> a <span class="output">R$ 2.500,00/m&ecirc;s</span> = <span class="prompt">R$ 7.500,00 recorrentes</span><br>
            <span class="comment"># Cen&aacute;rio 3: Alvo R$ 10.000/m&ecirc;s (Escala M&iacute;nima)</span><br>
            <span class="cmd">&bull; 4 clientes</span> a <span class="output">R$ 2.500,00/m&ecirc;s</span> = <span class="prompt">R$ 10.000,00 recorrentes</span>
        </div>
    </div>

    <div class="cyber-card">
        <h3 class="section-title" style="margin-top: 0;">Como entregar o servi&ccedil;o em apenas 3h/m&ecirc;s por cliente?</h3>
        <p style="font-size: 12px; line-height: 1.6;">
            Voc&ecirc; n&atilde;o fica na frente da tela o dia inteiro. Voc&ecirc; cria <strong>scripts de automa&ccedil;&atilde;o em Python</strong> que rodam em servidores agendados:
        </p>
        <ul style="margin-left: 20px; font-size: 12px; margin-top: 8px;">
            <li><strong>Semana 1:</strong> O script dispara uma varredura passiva de portas e certificados (Nmap/Nuclei).</li>
            <li><strong>Semana 2:</strong> Checagem autom&aacute;tica de novas credenciais vazadas com APIs de breach data.</li>
            <li><strong>Semana 3:</strong> Teste r&aacute;pido nos novos endpoints publicados pela equipe da empresa.</li>
            <li><strong>Semana 4:</strong> Compila&ccedil;&atilde;o do relat&oacute;rio mensal com o nosso rob&ocirc; de PDFs e envio por e-mail.</li>
        </ul>
    </div>

    <div class="cyber-card success" style="margin-top: 14px;">
        <strong style="color: #4ade80;">Custo Social Total:</strong> Praticamente nulo. Toda a rotina &eacute; executada no sil&ecirc;ncio do seu terminal, sem chamadas de voz e sem reuni&otilde;es desnecess&aacute;rias.
    </div>

    <div class="page-footer">
        <span>CONSULTOR PREMIUM HACKER</span>
        <span>P&Aacute;GINA 06 // 08</span>
    </div>
</div>

<!-- ========================================================================= -->
<!-- PÁGINA 7: BLINDAGEM JURÍDICA E OPERACIONAL                                -->
<!-- ========================================================================= -->
<div class="page">
    <div class="corner-tl"></div><div class="corner-tr"></div>
    <div class="corner-bl"></div><div class="corner-br"></div>

    <div class="page-header">
        <span>CAP&Iacute;TULO 06 // SEGURAN&Ccedil;A JUR&Iacute;DICA</span>
        <span class="cyber-badge badge-purple">BLINDAGEM TOTAL</span>
    </div>

    <h1 class="cyber-title">06. A BLINDAGEM JUR&Iacute;DICA &amp; BPC</h1>
    <h2 class="cyber-subtitle">&gt; Como proteger seu nome, sua seguran&ccedil;a legal e seus benef&iacute;cios</h2>

    <p>
        Trabalhar com seguran&ccedil;a ofensiva exige rigor documental absoluto para que seus testes jamais sejam confundidos com a&ccedil;&otilde;es maliciosas. Os 3 documentos inegoci&aacute;veis:
    </p>

    <div class="cyber-card" style="border-left-color: #38bdf8;">
        <strong style="color: #38bdf8; font-family: 'Orbitron'; font-size: 13px;">1. NDA (Non-Disclosure Agreement)</strong>
        <p style="font-size: 11.5px; margin-top: 4px;">
            Garante sigilo m&uacute;tuo estrito. Voc&ecirc; se compromete a n&atilde;o expor nenhuma vulnerabilidade do cliente publicamente, e ele se compromete a n&atilde;o divulgar valores e estrat&eacute;gias do seu contrato.
        </p>
    </div>

    <div class="cyber-card alert" style="border-left-color: #ef4444;">
        <strong style="color: #ef4444; font-family: 'Orbitron'; font-size: 13px;">2. RoE (Rules of Engagement - Regras de Engajamento)</strong>
        <p style="font-size: 11.5px; margin-top: 4px;">
            A sua maior prote&ccedil;&atilde;o jur&iacute;dica. Define exatamente <strong>quais IPs/URLs est&atilde;o autorizados</strong>, hor&aacute;rios de teste, proibi&ccedil;&atilde;o expressa de ataques de nega&ccedil;&atilde;o de servi&ccedil;o (DDoS) e procedimentos em caso de dados cr&iacute;ticos encontrados.
        </p>
    </div>

    <div class="cyber-card success" style="border-left-color: #4ade80;">
        <strong style="color: #4ade80; font-family: 'Orbitron'; font-size: 13px;">3. SOW (Statement of Work - Escopo Fechado)</strong>
        <p style="font-size: 11.5px; margin-top: 4px;">
            Elimina pedidos de favores fora de contrato ("olha meu computador aqui rapidinho"). Define que o trabalho se encerra ap&oacute;s a entrega do laudo e a realiza&ccedil;&atilde;o do reteste &uacute;nico acordado.
        </p>
    </div>

    <div class="cyber-card" style="margin-top: 14px; background: rgba(30, 20, 10, 0.7); border-color: rgba(245, 158, 11, 0.4); border-left-color: #f59e0b;">
        <strong style="color: #fbbf24;">Prote&ccedil;&atilde;o do Casulo e do BPC (Regra Estrat&eacute;gica):</strong>
        <p style="font-size: 11.5px; margin-top: 4px;">
            Durante o per&iacute;odo de estudos e estrutura&ccedil;&atilde;o t&eacute;cnica, voc&ecirc; <strong>n&atilde;o abre CNPJ nem MEI</strong>. Toda a capacita&ccedil;&atilde;o &eacute; feita em laborat&oacute;rio, Bug Bounty internacional (onde o pagamento pode ser gerido sem cruzamento imediato de sistemas do INSS) ou pessoa f&iacute;sica pontual, mantendo seu casulo intacto.
        </p>
    </div>

    <div class="page-footer">
        <span>CONSULTOR PREMIUM HACKER</span>
        <span>P&Aacute;GINA 07 // 08</span>
    </div>
</div>

<!-- ========================================================================= -->
<!-- PÁGINA 8: O ROADMAP PRÁTICO DOS 90 DIAS                                   -->
<!-- ========================================================================= -->
<div class="page">
    <div class="corner-tl"></div><div class="corner-tr"></div>
    <div class="corner-bl"></div><div class="corner-br"></div>

    <div class="page-header">
        <span>CAP&Iacute;TULO 07 // PLANO DE A&Ccedil;&Atilde;O</span>
        <span class="cyber-badge badge-green">EXECU&Ccedil;&Atilde;O IMEDIATA</span>
    </div>

    <h1 class="cyber-title">07. O ROADMAP DOS 90 DIAS</h1>
    <h2 class="cyber-subtitle">&gt; Cronograma direto de a&ccedil;&atilde;o passo a passo para sair do zero</h2>

    <div class="cyber-card" style="margin-bottom: 12px;">
        <strong style="color: #a855f7; font-family: 'Orbitron'; font-size: 13px;">M&Ecirc;S 1: FUNDA&Ccedil;&Atilde;O &amp; LABORATORIO (Dias 1 a 30)</strong>
        <ul style="margin-left: 20px; font-size: 11.5px; margin-top: 6px;">
            <li>Concluir trilhas b&aacute;sicas do <strong>TryHackMe</strong> (Pre-Security e Web Fundamentals).</li>
            <li>Praticar scripts de automa&ccedil;&atilde;o em Python (requisi&ccedil;&otilde;es HTTP e parsers de JSON).</li>
            <li>Personalizar seus modelos de Laudo em PDF no rob&ocirc; de ciberseguran&ccedil;a.</li>
        </ul>
    </div>

    <div class="cyber-card" style="margin-bottom: 12px;">
        <strong style="color: #38bdf8; font-family: 'Orbitron'; font-size: 13px;">M&Ecirc;S 2: MAPEAMENTO &amp; VALIDA&Ccedil;&Atilde;O (Dias 31 a 60)</strong>
        <ul style="margin-left: 20px; font-size: 11.5px; margin-top: 6px;">
            <li>Mapear 30 empresas alvo locais e 10 ag&ecirc;ncias de software/web design.</li>
            <li>Fazer an&aacute;lise passiva (OSINT) e identificar falhas evidentes sem tocar em nada invasivo.</li>
            <li>Disparar 10 e-mails de "Ataque de Valor &Eacute;tico" com relat&oacute;rios de amostra gr&aacute;tis.</li>
        </ul>
    </div>

    <div class="cyber-card" style="margin-bottom: 12px;">
        <strong style="color: #4ade80; font-family: 'Orbitron'; font-size: 13px;">M&Ecirc;S 3: CONVERS&Atilde;O &amp; RECORR&Ecirc;NCIA (Dias 61 a 90)</strong>
        <ul style="margin-left: 20px; font-size: 11.5px; margin-top: 6px;">
            <li>Fechar o primeiro contrato fechado (SKU 1 ou 2) ou fechar parceria White-Label com ag&ecirc;ncia.</li>
            <li>Entregar o laudo impec&aacute;vel e propor a transi&ccedil;&atilde;o para o <strong>Micro-MSSP Mensal (R$ 1.500 a R$ 2.500/m&ecirc;s)</strong>.</li>
            <li>Atingir a meta dos <strong>primeiros R$ 5.000 recorrentes</strong> com apenas 2 clientes fixos.</li>
        </ul>
    </div>

    <div class="terminal-box" style="margin-top: 15px;">
        <div class="terminal-header">
            <span>root@antigravity:~# conclusao</span>
        </div>
        <div class="terminal-content">
            <span class="prompt">&gt;$ _</span> <span class="cmd">Voc&ecirc; n&atilde;o precisa de carisma. Precisa de l&oacute;gica, m&eacute;todo e documenta&ccedil;&atilde;o.</span><br>
            <span class="output">[SISTEMA PRONTO PARA EXECU&Ccedil;&Atilde;O DOCUMENTAL]</span>
        </div>
    </div>

    <div class="page-footer">
        <span>CONSULTOR PREMIUM HACKER</span>
        <span>P&Aacute;GINA 08 // 08</span>
    </div>
</div>
"""

output_pdf = r"C:\Users\matheus\Desktop\Consultor_Premium_Hacker.pdf"
full_html = build_html("Consultor Premium Hacker", pages)
generate_pdf_from_html(full_html, output_pdf)
print(f"E-book completo gerado no Desktop: {output_pdf}")
