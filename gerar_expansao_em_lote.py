"""
=============================================================================
GERADOR EM LOTE DA EXPANSÃO (MAPAS 201 AO 700) — DEVWORLD AI
=============================================================================
Gera os 500 mapas mentais adicionais para completar o catálogo de 700 mapas
das 8 Escolas da Computação.
Salva tanto em 'output_mapas/mapa_XXX.json' quanto diretamente na pasta da Escola
específica ('03_python_especialista/json/mapa_XXX.json').
Suporta retomada transparente (ignora o que já foi gerado).
=============================================================================
"""

import os
import sys
import json
import time
import argparse
from concurrent.futures import ThreadPoolExecutor, as_completed

if sys.platform == "win32":
    try:
        sys.stdout.reconfigure(encoding='utf-8')
        sys.stderr.reconfigure(encoding='utf-8')
    except Exception:
        pass

from matriz_expansao_700 import obter_todos_os_mapas_expansao
from devworld_engine import gerar_mapa_devworld

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
OUTPUT_DIR = os.path.join(BASE_DIR, "output_mapas")

def processar_um_mapa(item: dict) -> dict:
    map_id = item["id"]
    tema = item["tema"]
    foco = item["foco"]
    escola = item["escola"]
    
    arquivo_geral = os.path.join(OUTPUT_DIR, f"mapa_{map_id:03d}.json")
    pasta_escola_json = os.path.join(BASE_DIR, escola, "json")
    os.makedirs(pasta_escola_json, exist_ok=True)
    arquivo_escola = os.path.join(pasta_escola_json, f"mapa_{map_id:03d}.json")

    # 1. Verifica se já existe e está completo
    if os.path.exists(arquivo_geral) and os.path.exists(arquivo_escola):
        try:
            with open(arquivo_geral, "r", encoding="utf-8") as f:
                d = json.load(f)
                if d.get("id") == map_id and (d.get("topLeft") or d.get("top_left")):
                    return {"id": map_id, "tema": tema, "escola": escola, "status": "existente"}
        except Exception:
            pass

    # 2. Gera via DevWorld com até 3 tentativas
    for tentativa in range(1, 4):
        try:
            resultado = gerar_mapa_devworld(
                topico=tema,
                id_mapa=map_id,
                foco=foco
            )

            # Enriquece metadados
            resultado["id"] = map_id
            resultado["modulo"] = item.get("modulo", "")
            resultado["escola"] = escola
            resultado["foco_pedagogico"] = foco

            # Salva na pasta geral
            with open(arquivo_geral, "w", encoding="utf-8") as f:
                json.dump(resultado, f, indent=2, ensure_ascii=False)

            # Salva diretamente na pasta da Escola
            with open(arquivo_escola, "w", encoding="utf-8") as f:
                json.dump(resultado, f, indent=2, ensure_ascii=False)

            return {"id": map_id, "tema": tema, "escola": escola, "status": "gerado"}
        except Exception as e:
            time.sleep(2.0 * tentativa)
            if tentativa == 3:
                return {"id": map_id, "tema": tema, "escola": escola, "status": "erro", "erro": str(e)}

def main():
    parser = argparse.ArgumentParser(description="Gerador em Lote da Expansão 700 Mapas")
    parser.add_argument("--escola", type=str, default=None, help="Filtrar por escola específica (ex: 03_python_especialista)")
    parser.add_argument("--limite", type=int, default=None, help="Limitar quantidade de mapas a gerar nesta rodada")
    parser.add_argument("--workers", type=int, default=2, help="Número de workers paralelos (default: 2)")
    args = parser.parse_args()

    os.makedirs(OUTPUT_DIR, exist_ok=True)
    todos = obter_todos_os_mapas_expansao()

    if args.escola:
        todos = [item for item in todos if args.escola.lower() in item["escola"].lower()]

    if args.limite:
        todos = todos[:args.limite]

    total = len(todos)
    if total == 0:
        print("Nenhum mapa encontrado com os filtros informados.")
        return

    print("=" * 75)
    print("🚀 INICIANDO PRODUÇÃO DA EXPANSÃO (DEVWORLD AI)")
    print(f"📊 Fila de Processamento: {total} mapas mentais")
    if args.escola:
        print(f"🎯 Filtro de Escola: {args.escola}")
    print(f"⚡ Workers Concorrentes: {args.workers}")
    print("=" * 75)

    inicio = time.time()
    concluidos = 0
    erros = 0

    with ThreadPoolExecutor(max_workers=args.workers) as executor:
        futuros = {executor.submit(processar_um_mapa, item): item for item in todos}

        for futuro in as_completed(futuros):
            res = futuro.result()
            if res["status"] in ("gerado", "existente"):
                concluidos += 1
                tag = "✅ GERADO" if res["status"] == "gerado" else "⏩ JÁ EXISTIA"
                pct = (concluidos / total) * 100
                print(f"[{concluidos:03d}/{total:03d} - {pct:5.1f}%] {tag} #{res['id']:03d} [{res['escola'][:12]}]: {res['tema']}")
            else:
                erros += 1
                print(f"❌ ERRO #{res['id']:03d}: {res['tema']} -> {res.get('erro')}")

    tempo_total = time.time() - inicio
    print("\n" + "=" * 75)
    print(f"🏁 RODADA CONCLUÍDA EM {tempo_total:.1f} SEGUNDOS!")
    print(f"✅ Mapas processados: {concluidos}/{total}")
    if erros > 0:
        print(f"⚠️ Erros encontrados: {erros} (basta executar novamente para retentar)")
    print("=" * 75)

if __name__ == "__main__":
    main()
