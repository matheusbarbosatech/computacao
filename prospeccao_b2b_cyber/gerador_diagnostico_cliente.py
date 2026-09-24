# -*- coding: utf-8 -*-
"""
GERADOR DE RELATÓRIO EXECUTIVO EM HTML/PDF (DIAGNÓSTICO PRELIMINAR DE SEGURANÇA)
Produz um documento visual elegante de 1 página pronto para impressão ou envio digital.
"""
import os
from datetime import datetime

def gerar_html_diagnostico(empresa, analise, output_path):
    score = analise["score"]
    nota = analise["nota"]
    
    # Cor do termômetro
    if score >= 75:
        cor_badge = "#10b981" # Verde
        status_texto = "Postura Adequada"
    elif score >= 50:
        cor_badge = "#f59e0b" # Amarelo
        status_texto = "Atenção Necessária"
    else:
        cor_badge = "#ef4444" # Vermelho
        status_texto = "Risco Elevado de Exposição"

    pontos_criticos_html = "".join([f"<li>⚠️ {p}</li>" for p in analise["pontos_criticos"]])
    pontos_positivos_html = "".join([f"<li>✅ {p}</li>" for p in analise["pontos_positivos"]])

    html = f"""<!DOCTYPE html>
<html lang="pt-BR">
<head>
  <meta charset="UTF-8">
  <title>Diagnóstico Preliminar de Segurança — {empresa}</title>
  <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&family=Outfit:wght@600;700;800&display=swap');
    
    * {{ box-sizing: border-box; margin: 0; padding: 0; }}
    body {{
      font-family: 'Inter', sans-serif;
      background: #f8fafc;
      color: #0f172a;
      padding: 40px;
      line-height: 1.5;
    }}
    .sheet {{
      background: #ffffff;
      max-width: 850px;
      margin: 0 auto;
      padding: 45px 50px;
      border-radius: 16px;
      box-shadow: 0 10px 25px rgba(0,0,0,0.05);
      border: 1px solid #e2e8f0;
    }}
    header {{
      display: flex;
      justify-content: space-between;
      align-items: center;
      border-bottom: 2px solid #e2e8f0;
      padding-bottom: 25px;
      margin-bottom: 30px;
    }}
    .logo-area h1 {{
      font-family: 'Outfit', sans-serif;
      font-size: 22px;
      font-weight: 800;
      color: #0f172a;
      letter-spacing: -0.5px;
    }}
    .logo-area span {{
      color: #3b82f6;
    }}
    .doc-meta {{
      text-align: right;
      font-size: 13px;
      color: #64748b;
    }}
    .target-box {{
      background: #f1f5f9;
      border-radius: 12px;
      padding: 18px 24px;
      margin-bottom: 30px;
      display: flex;
      justify-content: space-between;
      align-items: center;
    }}
    .target-info h2 {{
      font-size: 18px;
      font-weight: 700;
      color: #1e293b;
    }}
    .target-info p {{
      font-size: 13px;
      color: #64748b;
    }}
    .score-badge {{
      background: {cor_badge};
      color: #ffffff;
      padding: 10px 20px;
      border-radius: 10px;
      font-weight: 800;
      font-size: 20px;
      text-align: center;
    }}
    .score-badge small {{
      display: block;
      font-size: 11px;
      font-weight: 600;
      text-transform: uppercase;
      letter-spacing: 0.5px;
    }}
    .grid-2 {{
      display: grid;
      grid-template-columns: 1fr 1fr;
      gap: 25px;
      margin-bottom: 30px;
    }}
    .card {{
      background: #ffffff;
      border: 1px solid #e2e8f0;
      border-radius: 12px;
      padding: 20px;
    }}
    .card h3 {{
      font-size: 15px;
      font-weight: 700;
      margin-bottom: 14px;
      display: flex;
      align-items: center;
      gap: 8px;
    }}
    .card ul {{
      list-style: none;
      font-size: 13px;
    }}
    .card li {{
      margin-bottom: 10px;
      line-height: 1.4;
    }}
    .recommendations {{
      background: #eff6ff;
      border: 1px solid #bfdbfe;
      border-radius: 12px;
      padding: 22px;
      margin-bottom: 30px;
    }}
    .recommendations h3 {{
      color: #1d4ed8;
      font-size: 16px;
      margin-bottom: 12px;
      font-weight: 700;
    }}
    .recommendations ol {{
      margin-left: 20px;
      font-size: 13px;
      color: #1e3a8a;
    }}
    .recommendations li {{
      margin-bottom: 8px;
    }}
    footer {{
      border-top: 1px solid #e2e8f0;
      padding-top: 20px;
      display: flex;
      justify-content: space-between;
      align-items: center;
      font-size: 12px;
      color: #64748b;
    }}
    .contact-btn {{
      background: #0f172a;
      color: #ffffff;
      padding: 8px 16px;
      border-radius: 6px;
      text-decoration: none;
      font-weight: 600;
      font-size: 12px;
    }}
    @media print {{
      body {{ background: #ffffff; padding: 0; }}
      .sheet {{ border: none; box-shadow: none; padding: 0; max-width: 100%; }}
      .contact-btn {{ display: none; }}
    }}
  </style>
</head>
<body>

  <div class="sheet">
    <header>
      <div class="logo-area">
        <h1>Cyber<span>Shield</span> Consultoria</h1>
        <p style="font-size: 12px; color: #64748b;">Auditoria Técnica de Segurança da Informação & LGPD</p>
      </div>
      <div class="doc-meta">
        <p><strong>Relatório Técnico:</strong> #{abs(hash(empresa)) % 100000:05d}</p>
        <p>Data: {datetime.now().strftime("%d/%m/%Y")}</p>
        <p>Status: <span style="color: {cor_badge}; font-weight: 700;">{status_texto}</span></p>
      </div>
    </header>

    <div class="target-box">
      <div class="target-info">
        <h2>{empresa}</h2>
        <p>Domínio Auditado: <strong>{analise['url']}</strong></p>
        <p>Tipo de Avaliação: Análise Passiva Externa de Cabeçalhos e Transporte</p>
      </div>
      <div class="score-badge">
        {score} / 100
        <small>{nota}</small>
      </div>
    </div>

    <div class="grid-2">
      <div class="card" style="border-left: 4px solid #ef4444;">
        <h3 style="color: #b91c1c;">Vulnerabilidades & Pontos de Risco</h3>
        <ul>
          {pontos_criticos_html if pontos_criticos_html else "<li>Nenhum risco crítico externo identificado.</li>"}
        </ul>
      </div>

      <div class="card" style="border-left: 4px solid #10b981;">
        <h3 style="color: #047857;">Mecanismos Ativos de Proteção</h3>
        <ul>
          {pontos_positivos_html if pontos_positivos_html else "<li>Nenhum cabeçalho avançado de defesa detectado.</li>"}
        </ul>
      </div>
    </div>

    <div class="recommendations">
      <h3>📋 3 Ações Imediatas de Remediação Recomendadas:</h3>
      <ol>
        <li><strong>Implementar Cabeçalhos Anti-Clonagem (X-Frame-Options & CSP):</strong> Impede que golpistas criem réplicas da sua página dentro de iframes para capturar senhas de clientes e funcionários.</li>
        <li><strong>Ocultar Assinaturas de Versão do Servidor:</strong> Evita que invasores identifiquem a versão exata do seu servidor web e explorem brechas públicas conhecidas.</li>
        <li><strong>Ativar Política HSTS Rigorosa:</strong> Assegura que nenhum usuário navegue em versão insegura (HTTP), garantindo conformidade com as diretrizes de criptografia da LGPD.</li>
      </ol>
    </div>

    <footer>
      <div>
        <p><strong>Auditor Responsável:</strong> Matheus Barbosa | Especialista em Segurança Digital</p>
        <p>Avaliação preliminar não-invasiva baseada nas diretrizes OWASP e LGPD (Lei nº 13.709/2018).</p>
      </div>
      <a href="https://wa.me/5541999999999?text=Ol%C3%A1%20Matheus,%20recebi%20o%20diagn%C3%B3stico%20de%20seguran%C3%A7a%20e%20gostaria%20de%20conversar" class="contact-btn" target="_blank">Agendar Consultoria</a>
    </footer>
  </div>

</body>
</html>
"""
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    with open(output_path, "w", encoding="utf-8") as f:
        f.write(html)
    return output_path
