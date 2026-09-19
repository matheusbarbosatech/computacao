"""
=============================================================================
GERADOR EM LOTE: TODOS OS 200 MAPAS MENTAIS (DEVWORLD AI)
=============================================================================
Gera o conteúdo pedagógico estruturado para todos os 200 mapas da trilha,
salvando cada um em 'output_mapas/mapa_XXX.json'.
Possui suporte a retomada automática (não regera o que já foi salvo)
e controle de concorrência suave com retry.
=============================================================================
"""

import os
import sys
import json
import time
from concurrent.futures import ThreadPoolExecutor, as_completed

if sys.platform == "win32":
    try:
        sys.stdout.reconfigure(encoding='utf-8')
        sys.stderr.reconfigure(encoding='utf-8')
    except Exception:
        pass

from matriz_uninter import TODOS_OS_200_MAPAS
from devworld_engine import gerar_mapa_devworld

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
OUTPUT_DIR = os.path.join(BASE_DIR, "output_mapas")

def gerar_um_mapa(item: dict) -> dict:
    map_id = item["id"]
    tema = item["tema"]
    foco = item["foco"]
    
    arquivo_json = os.path.join(OUTPUT_DIR, f"mapa_{map_id:03d}.json")

    # Se já existir e for válido, reaproveita
    if os.path.exists(arquivo_json):
        try:
            with open(arquivo_json, "r", encoding="utf-8") as f:
                dados = json.load(f)
                if dados.get("id") == map_id and (dados.get("topLeft") or dados.get("top_left")):
                    return {"id": map_id, "tema": tema, "status": "existente"}
        except Exception:
            pass

    # Chama a API da DevWorld com até 3 tentativas
    for tentativa in range(1, 4):
        try:
            resultado = gerar_mapa_devworld(
                topico=tema,
                id_mapa=map_id,
                foco=foco,
                modelo=None
            )

            # Garante integridade do id e metadados
            resultado["id"] = map_id
            resultado["modulo"] = item.get("modulo", "")
            resultado["foco_pedagogico"] = foco

            with open(arquivo_json, "w", encoding="utf-8") as f:
                json.dump(resultado, f, indent=2, ensure_ascii=False)

            return {"id": map_id, "tema": tema, "status": "gerado"}
        except Exception as e:
            time.sleep(1.5 * tentativa)
            if tentativa == 3:
                return {"id": map_id, "tema": tema, "status": "erro", "erro": str(e)}

def main():
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    total = len(TODOS_OS_200_MAPAS)

    print("=" * 70)
    print("🚀 INICIANDO PRODUÇÃO EM LOTE DOS 200 MAPAS MENTAIS")
    print(f"📁 Destino dos arquivos: {OUTPUT_DIR}")
    print("⚡ Motor: DevWorld AI (devworld/gemini-3.7-flash-f - Ilimitado)")
    print("=" * 70)

    # Verifica quantos já foram gerados anteriormente
    existentes = 0
    for item in TODOS_OS_200_MAPAS:
        p = os.path.join(OUTPUT_DIR, f"mapa_{item['id']:03d}.json")
        if os.path.exists(p):
            existentes += 1

    print(f"📊 Progresso inicial: {existentes}/{total} mapas já concluídos.")
    print("Iniciando workers paralelos para processar a fila com velocidade máxima...\n")

    concluidos = existentes
    erros = 0
    inicio = time.time()

    # Processa usando pool de 3 threads (velocidade ideal sem estourar rate limit)
    with ThreadPoolExecutor(max_workers=2) as executor:
        futuros = {executor.submit(gerar_um_mapa, item): item for item in TODOS_OS_200_MAPAS}

        for futuro in as_completed(futuros):
            res = futuro.result()
            if res["status"] in ("gerado", "existente"):
                concluidos += 1 if res["status"] == "gerado" else 0
                tag = "✅ GERADO" if res["status"] == "gerado" else "⏩ JÁ EXISTIA"
                pct = (concluidos / total) * 100
                print(f"[{concluidos:03d}/{total:03d} - {pct:5.1f}%] {tag} #{res['id']:03d}: {res['tema']}")
            else:
                erros += 1
                print(f"❌ ERRO #{res['id']:03d}: {res['tema']} -> {res.get('erro')}")

    tempo_total = time.time() - inicio
    print("\n" + "=" * 70)
    print(f"🏁 PROCESSAMENTO FINALIZADO EM {tempo_total:.1f} SEGUNDOS!")
    print(f"✅ Mapas disponíveis: {concluidos}/{total}")
    if erros > 0:
        print(f"⚠️ Erros encontrados: {erros} (basta rodar novamente para retentar apenas os que faltam)")
    print(f"📁 Todos os arquivos estão salvos em: {OUTPUT_DIR}")
    print("=" * 70)

if __name__ == "__main__":
    main()
