"""
=============================================================================
PIPELINE DE RENDERIZAÇÃO E COMPILAÇÃO DAS ESCOLAS RESTANTES
=============================================================================
Renderiza em alta resolução 1536x1024 300 DPI (Sketchnote Artesanal)
e compila os E-books A4 Paisagem prontos para encadernação/impressão gráfica.
=============================================================================
"""

import os
import sys
import time

if sys.platform == "win32":
    try:
        sys.stdout.reconfigure(encoding='utf-8', line_buffering=True)
        sys.stderr.reconfigure(encoding='utf-8', line_buffering=True)
    except Exception:
        pass

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

from organizar_acervo import ESCOLAS_CONFIG
from gerar_render_sketchnote_realista import renderizar_lote_escola
from compilar_ebook_para_impressao import gerar_ebook_escola

# Ordem otimizada de execução
ORDEM_ESCOLAS = [
    "08_ciberseguranca",
    "04_backend_e_apis",
    "07_devops_linux_e_nuvem",
    "05_frontend_e_mobile",
    "06_banco_dados_e_ia",
    "02_logica_e_algoritmos"
]

def executar():
    print("=" * 75, flush=True)
    print("🎨 INICIANDO PRODUÇÃO DAS ESCOLAS RESTANTES (SKETCHNOTE A4 PAISAGEM)", flush=True)
    print("=" * 75, flush=True)

    mapa_escolas = {e["pasta"]: e for e in ESCOLAS_CONFIG}
    inicio_geral = time.time()
    resumo_final = []

    for idx, pasta in enumerate(ORDEM_ESCOLAS, 1):
        info = mapa_escolas.get(pasta)
        if not info:
            continue

        nome = info["nome"]
        desc = info["descricao"]
        pasta_pdf = os.path.join(BASE_DIR, pasta, "pdf")
        nome_pdf = f"{pasta}_A4_PAISAGEM.pdf"
        caminho_pdf = os.path.join(pasta_pdf, nome_pdf)

        pasta_json = os.path.join(BASE_DIR, pasta, "json")
        pasta_img = os.path.join(BASE_DIR, pasta, "imagens")
        total_json = len([f for f in os.listdir(pasta_json) if f.endswith(".json")]) if os.path.exists(pasta_json) else 0
        total_img = len([f for f in os.listdir(pasta_img) if f.endswith(".png") and os.path.getsize(os.path.join(pasta_img, f)) > 10000]) if os.path.exists(pasta_img) else 0

        print(f"\n[{idx}/{len(ORDEM_ESCOLAS)}] >>> {nome.upper()}", flush=True)
        print(f"    Pasta: {pasta} | JSONs: {total_json} | Imagens prontas: {total_img}", flush=True)

        # Se o PDF já existe e tem tamanho grande (> 5MB) e todas as imagens estão prontas, pula
        if os.path.exists(caminho_pdf) and os.path.getsize(caminho_pdf) > 5 * 1024 * 1024 and total_img == total_json and total_json > 0:
            tam_mb = os.path.getsize(caminho_pdf) / (1024 * 1024)
            print(f"    ✅ E-book já compilado com alta fidelidade: {tam_mb:.1f} MB. Pulando.", flush=True)
            resumo_final.append({
                "escola": nome,
                "pasta": pasta,
                "pdf": caminho_pdf,
                "tamanho_mb": tam_mb,
                "status": "Já Existia"
            })
            continue

        # 1. Renderiza imagens que faltam com 3 workers
        t0 = time.time()
        renderizar_lote_escola(pasta, workers=3)
        t_render = time.time() - t0

        # 2. Compila o E-book A4 Paisagem
        print(f"    📦 Compilando PDF A4 Paisagem para {pasta}...", flush=True)
        pdf_gerado = gerar_ebook_escola(pasta, nome, desc)
        tam_mb = os.path.getsize(pdf_gerado) / (1024 * 1024) if pdf_gerado and os.path.exists(pdf_gerado) else 0

        print(f"    🎉 {nome} CONCLUÍDO COM SUCESSO! PDF: {tam_mb:.1f} MB em {t_render:.1f}s", flush=True)
        resumo_final.append({
            "escola": nome,
            "pasta": pasta,
            "pdf": pdf_gerado,
            "tamanho_mb": tam_mb,
            "status": "Recém Compilado"
        })

    tempo_total = time.time() - inicio_geral
    print("\n" + "=" * 75, flush=True)
    print("🏆 RELATÓRIO EXECUTIVO: TODAS AS ESCOLAS PROCESSADAS COM SUCESSO!", flush=True)
    print(f"⏱️ Tempo total de produção: {tempo_total / 60:.1f} minutos", flush=True)
    print("=" * 75, flush=True)
    for r in resumo_final:
        print(f"📄 [{r['status']:<15}] {r['escola'][:35]:<37} | {r['tamanho_mb']:5.1f} MB | {r['pdf']}", flush=True)
    print("=" * 75, flush=True)

if __name__ == "__main__":
    executar()
