"""
=============================================================================
COMPILADOR GERAL DE ARTBOOKS EM A4 PAISAGEM (TODAS AS 8 ESCOLAS)
=============================================================================
Renderiza em alta velocidade (multithreaded Chrome Headless) e compila os
8 E-books completos prontos para gráfica/impressão Wire-o com todas as
700 lâminas no novo padrão visual Sketchnote realista.
=============================================================================
"""

import os
import sys
import time
from organizar_acervo import ESCOLAS_CONFIG
from gerar_render_sketchnote_realista import renderizar_lote_escola
from compilar_ebook_para_impressao import gerar_ebook_escola

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

def processar_tudo():
    print("=" * 75)
    print("🚀 INICIANDO PRODUÇÃO COMPLETA DOS 8 ARTBOOKS EM A4 PAISAGEM (300 DPI)")
    print(f"📚 Catálogo Geral: 700 Mapas Mentais Sketchnote")
    print("=" * 75)

    inicio_geral = time.time()
    resultados = []

    for idx, esc in enumerate(ESCOLAS_CONFIG, 1):
        pasta = esc["pasta"]
        nome = esc["nome"]
        descricao = esc["descricao"]

        print(f"\n[{idx}/8] -------------------------------------------------------------")
        print(f"🏛️ Processando Escola: {nome}")
        print(f"📁 Pasta: {pasta}")
        print("---------------------------------------------------------------------")

        # 1. Renderiza artes pendentes com 3 workers paralelos
        t0 = time.time()
        renderizar_lote_escola(pasta, workers=3)
        t_render = time.time() - t0

        # 2. Compila o E-book em PDF A4 Paisagem
        pdf_path = gerar_ebook_escola(pasta, nome, descricao)
        tam_mb = os.path.getsize(pdf_path) / (1024 * 1024) if pdf_path and os.path.exists(pdf_path) else 0

        resultados.append({
            "escola": nome,
            "pasta": pasta,
            "pdf": pdf_path,
            "tamanho_mb": tam_mb,
            "tempo": t_render
        })

    tempo_total = time.time() - inicio_geral

    print("\n" + "=" * 75)
    print("🏆 PRODUÇÃO DOS 8 E-BOOKS FINALIZADA COM SUCESSO!")
    print(f"⏱️ Tempo total: {tempo_total / 60:.1f} minutos")
    print("=" * 75)
    for r in resultados:
        print(f"📄 {r['escola'][:38]:<40} | {r['tamanho_mb']:5.1f} MB | {r['pdf']}")
    print("=" * 75)

if __name__ == "__main__":
    processar_tudo()
