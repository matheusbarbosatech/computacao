# -*- coding: utf-8 -*-
"""
ORQUESTRADOR MESTRE DE PROSPECÇÃO B2B PARA CIBERSEGURANÇA
1. Minera empresas com sites no Google Maps / OpenStreetMap
2. Analisa a postura de segurança passiva do site
3. Gera o Diagnóstico Preliminar em HTML/PDF de 1 página
4. Cria o Script de WhatsApp Personalizado baseado na falha encontrada
5. Exporta o Painel Geral em Markdown e CSV
"""
import os
import sys
import csv
import json
from datetime import datetime

sys.stdout.reconfigure(encoding='utf-8', errors='ignore')
sys.stderr.reconfigure(encoding='utf-8', errors='ignore')

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.append(BASE_DIR)

from minerador_leads_empresas import buscar_empresas_cidade
from analisador_postura_passiva import analisar_site
from gerador_diagnostico_cliente import gerar_html_diagnostico

def gerar_script_whatsapp(empresa, analise):
    nome = empresa["nome"]
    pontos = analise.get("pontos_criticos", [])
    
    # Filtrar exceções técnicas feias para uma mensagem natural e elegante
    falhas_humanas = [p for p in pontos if not p.lower().startswith("erro ao conectar")]
    if falhas_humanas:
        falha_destaque = falhas_humanas[0].lower()
    else:
        falha_destaque = "ausência de cabeçalhos modernos de proteção contra clonagem e diretrizes de criptografia da LGPD"
    
    return f"""Olá, equipe da {nome}, tudo bem?

Meu nome é Matheus, atuo com segurança digital e conformidade técnica para empresas da área de {empresa['nicho']}.

Estava realizando um levantamento preventivo na região e notei um detalhe importante no site de vocês: {falha_destaque}.

Para ajudar, elaborei um breve Diagnóstico Preliminar de 1 página com 3 pontos simples que a equipe de TI de vocês pode corrigir em menos de 1 hora para evitar riscos de invasão e adequar o portal às diretrizes da LGPD.

Gravei um vídeo rápido de 1 minuto apresentando o resumo do relatório. Posso te enviar o PDF e o link aqui pelo WhatsApp, sem nenhum compromisso?""".strip()


def executar_prospeccao(nicho="clinica", cidade="Curitiba", limite=5):
    print("=" * 65)
    print(f"💼 INICIANDO PROSPECÇÃO B2B: {nicho.upper()} EM {cidade.upper()}")
    print("=" * 65)

    print(f"🔍 1. Buscando empresas com sites ativos...")
    empresas = buscar_empresas_cidade(nicho, cidade, limite)
    print(f"📋 {len(empresas)} empresas localizadas para auditoria passiva.\n")

    relatorios_dir = os.path.join(BASE_DIR, "relatorios_clientes")
    os.makedirs(relatorios_dir, exist_ok=True)

    leads_processados = []

    for i, emp in enumerate(empresas, 1):
        nome = emp["nome"]
        site = emp["website"]
        print(f"[{i}/{len(empresas)}] 🛡️ Auditando: {nome} ({site})...")
        
        analise = analisar_site(site)
        print(f"   Nota: {analise['nota']} | Score: {analise['score']}/100")

        # Nome de arquivo seguro
        nome_arquivo = "".join([c if c.isalnum() else "_" for c in nome.lower()]).strip("_")[:40]
        html_path = os.path.join(relatorios_dir, f"diagnostico_{nome_arquivo}.html")
        gerar_html_diagnostico(nome, analise, html_path)
        print(f"   📄 Relatório gerado: {html_path}")

        script_wpp = gerar_script_whatsapp(emp, analise)

        leads_processados.append({
            "empresa": nome,
            "nicho": emp["nicho"],
            "cidade": emp["cidade"],
            "telefone": emp["telefone"],
            "website": site,
            "score": analise["score"],
            "nota": analise["nota"],
            "relatorio_html": html_path,
            "script_whatsapp": script_wpp,
            "pontos_criticos": " | ".join(analise["pontos_criticos"])
        })

    # 1. Exportar CSV para planilhas
    csv_path = os.path.join(BASE_DIR, "LEADS_PROSPECCAO_CYBER.csv")
    with open(csv_path, "w", encoding="utf-8-sig", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=[
            "empresa", "nicho", "cidade", "telefone", "website", "score", "nota", "relatorio_html", "pontos_criticos"
        ])
        writer.writeheader()
        for lp in leads_processados:
            row = {k: v for k, v in lp.items() if k != "script_whatsapp"}
            writer.writerow(row)

    # 2. Exportar Painel Markdown na Raiz
    project_dir = os.path.dirname(BASE_DIR)
    md_path = os.path.join(project_dir, "PAINEL_PROSPECCAO_B2B_CYBER.md")
    
    with open(md_path, "w", encoding="utf-8") as f:
        f.write(f"# 💼 Painel de Prospecção B2B: Leads & Diagnósticos de Cibersegurança\n\n")
        f.write(f"> **Nicho:** {nicho.title()} | **Cidade:** {cidade.title()} | **Data:** {datetime.now().strftime('%d/%m/%Y %H:%M')}\n\n---\n\n")
        
        f.write("## 📊 Tabela Geral de Oportunidades\n\n")
        f.write("| Empresa | Telefone | Score / Nota | Relatório do Cliente | Ação |\n")
        f.write("| :--- | :--- | :---: | :--- | :---: |\n")
        for lp in leads_processados:
            f.write(f"| **{lp['empresa']}** | `{lp['telefone']}` | **{lp['score']}/100** ({lp['nota']}) | [Abrir Diagnóstico](file:///{lp['relatorio_html'].replace(chr(92), '/')}) | [Copiar Script](#abordagem-{abs(hash(lp['empresa'])) % 1000}) |\n")

        f.write("\n---\n\n## 📩 Scripts Prontos para Enviar no WhatsApp\n\n")
        for lp in leads_processados:
            f.write(f"### <a id=\"abordagem-{abs(hash(lp['empresa'])) % 1000}\"></a>📲 {lp['empresa']} — Telefone: `{lp['telefone']}`\n\n")
            f.write(f"```text\n{lp['script_whatsapp']}\n```\n\n")
            f.write(f"* **Link do Relatório Local:** [Abrir Diagnóstico](file:///{lp['relatorio_html'].replace(chr(92), '/')})\n\n---\n\n")

    print("\n" + "=" * 65)
    print(f"🎉 PROSPECÇÃO CONCLUÍDA COM SUCESSO!")
    print(f"📊 Painel de Vendas: {md_path}")
    print(f"📁 Planilha de Leads: {csv_path}")
    print("=" * 65)

if __name__ == "__main__":
    nicho_input = sys.argv[1] if len(sys.argv) > 1 else "clinica"
    cidade_input = sys.argv[2] if len(sys.argv) > 2 else "Curitiba"
    limite_input = int(sys.argv[3]) if len(sys.argv) > 3 else 4
    executar_prospeccao(nicho_input, cidade_input, limite_input)
