"""
=============================================================================
GERADOR DE MAPAS MENTAIS VIA LINHA DE COMANDO (CLI)
=============================================================================
Uso simples:
  python gerar_mapa_cli.py --id 1
  python gerar_mapa_cli.py --topico "O que é Recursão?"
=============================================================================
"""

import argparse
import json
import os
import sys

if sys.platform == "win32":
    try:
        sys.stdout.reconfigure(encoding='utf-8')
        sys.stderr.reconfigure(encoding='utf-8')
    except Exception:
        pass

from matriz_uninter import TRILHA_INICIANTE_DO_ZERO, buscar_topico_por_id
from devworld_engine import gerar_mapa_devworld

def main():
    parser = argparse.ArgumentParser(description="Gerador de Mapas Mentais Sketchnote via DevWorld AI")
    parser.add_argument("--id", type=int, help="Número do tópico na Trilha UNINTER (1 a 57)")
    parser.add_argument("--topico", type=str, help="Nome livre de qualquer tópico para gerar")
    parser.add_argument("--foco", type=str, default="", help="Instrução ou analogia pedagógica adicional")
    parser.add_argument("--modelo", type=str, default=None, help="Modelo DevWorld (-f)")
    
    args = parser.parse_args()

    if args.id:
        info = buscar_topico_por_id(args.id)
        if not info:
            print(f"❌ Tópico #{args.id} não encontrado na trilha.")
            return
        topico = info["tema"]
        foco = info["foco"]
        id_mapa = info["id"]
    elif args.topico:
        topico = args.topico
        foco = args.foco
        id_mapa = 1
    else:
        print("💡 Informe --id <numero> (da matriz UNINTER) ou --topico \"Nome do Assunto\".")
        print("\nExemplos:")
        print("  python gerar_mapa_cli.py --id 1")
        print("  python gerar_mapa_cli.py --id 7")
        print("  python gerar_mapa_cli.py --topico \"O que é Recursão?\"")
        return

    print(f"🧠 Gerando mapa mental #{id_mapa}: '{topico}' via DevWorld AI...")
    try:
        resultado = gerar_mapa_devworld(topico, id_mapa=id_mapa, foco=foco, modelo=args.modelo)
        
        # Salva o arquivo JSON
        os.makedirs("output_mapas", exist_ok=True)
        nome_arquivo = f"output_mapas/mapa_{id_mapa:03d}_{topico.lower().replace(' ', '_')[:25]}.json"
        with open(nome_arquivo, "w", encoding="utf-8") as f:
            json.dump(resultado, f, indent=2, ensure_ascii=False)

        print(f"\n✅ Mapa gerado e salvo em: {nome_arquivo}")
        print(f"Título: {resultado.get('title')}")
        print(f"Definição: {resultado.get('definition')}")
        print(f"Modelo: {resultado.get('_modelo_usado')}")
    except Exception as e:
        print(f"❌ Erro ao gerar: {e}")

if __name__ == "__main__":
    main()
