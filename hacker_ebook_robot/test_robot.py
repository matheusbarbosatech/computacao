import os
from generator import build_html, generate_pdf_from_html

body_pages = """
<!-- PÁGINA 1: CAPA -->
<div class="page cover-page">
    <div class="corner-tl"></div><div class="corner-tr"></div>
    <div class="corner-bl"></div><div class="corner-br"></div>

    <div class="cover-meta">
        01001001 01001110 01000101 &bull; SYSTEM_OK &bull; SEC_LEVEL_01
    </div>

    <h1 class="cover-main-title">
        $ C&Oacute;DIGO <span class="cover-highlight">[EXPOSTO]</span> &gt;_
    </h1>
    <div class="cover-subtitle">
        Guia Pr&aacute;tico de Ciberseguran&ccedil;a &amp; Pentest em APIs
    </div>

    <div class="terminal-box" style="width: 85%; margin: 30px auto; text-align: left;">
        <div class="terminal-header">
            <div class="terminal-buttons">
                <div class="terminal-btn btn-red"></div>
                <div class="terminal-btn btn-yellow"></div>
                <div class="terminal-btn btn-green"></div>
            </div>
            <span>root@kernel:~# audit</span>
        </div>
        <div class="terminal-content">
            <span class="prompt">&gt;$ _</span> <span class="cmd">conhecimento &eacute; a melhor firewall.</span><br>
            <span class="comment">// Mapeamento automatizado de falhas l&oacute;gicas e vetores de invas&atilde;o</span>
        </div>
    </div>

    <div class="cover-logo-badge">
        HACKER <span>HUB</span>
    </div>
</div>

<!-- PÁGINA 2: CONTEÚDO TÉCNICO -->
<div class="page">
    <div class="corner-tl"></div><div class="corner-tr"></div>
    <div class="corner-bl"></div><div class="corner-br"></div>

    <div class="page-header">
        <span>MOD_01 // FUNDAMENTOS</span>
        <span class="cyber-badge badge-green">STATUS: ATIVO</span>
    </div>

    <h1 class="cyber-title">01. INVAS&Atilde;O DE APIs: IDOR</h1>
    <h2 class="cyber-subtitle">&gt; Insecure Direct Object References em Endpoints Modernos</h2>

    <p>
        O <strong>IDOR (Insecure Direct Object Reference)</strong> ocorre quando uma aplica&ccedil;&atilde;o web ou API fornece acesso direto a objetos internos com base na entrada fornecida pelo usu&aacute;rio, sem valida&ccedil;&atilde;o pr&eacute;via de autoriza&ccedil;&atilde;o.
    </p>

    <div class="terminal-box">
        <div class="terminal-header">
            <div class="terminal-buttons">
                <div class="terminal-btn btn-red"></div>
                <div class="terminal-btn btn-yellow"></div>
                <div class="terminal-btn btn-green"></div>
            </div>
            <span>burp_suite // repeater_request.http</span>
        </div>
        <div class="terminal-content">
            <span class="cmd">GET /api/v1/users/account/1042 HTTP/1.1</span><br>
            Host: target-empresa.com.br<br>
            Authorization: Bearer eyJhbGciOi... <span class="comment">(Token do usu&aacute;rio 1041)</span><br><br>
            <span class="prompt">HTTP/1.1 200 OK</span><br>
            <span class="output">{ "user_id": 1042, "nome": "Diretor Financeiro", "saldo_pix": 85400.00 }</span>
        </div>
    </div>

    <div class="cyber-card alert">
        <h3 class="section-title" style="color: #ef4444; margin-top: 0;">&#9888; IMPACTO CR&Iacute;TICO (CVSS 8.6)</h3>
        <p>
            Uma falha l&oacute;gica de IDOR permite que qualquer usu&aacute;rio autenticado acesse dados sens&iacute;veis de outros clientes, gerando vazamento em massa de dados protegidos pela LGPD.
        </p>
    </div>

    <div class="cyber-grid">
        <div class="cyber-card">
            <strong style="color: #c084fc;">Vetores de Detec&ccedil;&atilde;o:</strong>
            <ul style="margin-left: 18px; margin-top: 6px;">
                <li>Sequenciamento num&eacute;rico de IDs</li>
                <li>Par&acirc;metros em URLs e headers</li>
                <li>UUIDs previs&iacute;veis ou hashes MD5</li>
            </ul>
        </div>
        <div class="cyber-card success">
            <strong style="color: #4ade80;">M&eacute;todo de Remedia&ccedil;&atilde;o:</strong>
            <ul style="margin-left: 18px; margin-top: 6px;">
                <li>Checagem rigorosa de sess&atilde;o no backend</li>
                <li>Uso de GUIDs criptogr&aacute;ficos</li>
                <li>Pol&iacute;ticas de RBAC / ABAC</li>
            </ul>
        </div>
    </div>

    <div class="page-footer">
        <span>HACKERHUB // E-BOOK SERIES</span>
        <span>P&Aacute;GINA 02 // 61</span>
    </div>
</div>
"""

output_pdf = r"C:\Users\matheus\Desktop\computacao\hacker_ebook_robot\sample_ebook.pdf"
full_html = build_html("HackerHub Sample", body_pages)
generate_pdf_from_html(full_html, output_pdf)

