"""
=============================================================================
ORGANIZADOR DO ACERVO DAS 8 ESCOLAS DE COMPUTAÇÃO
=============================================================================
Cria as 8 pastas temáticas na Área de Trabalho com subpastas padronizadas
(json, imagens, pdf) e distribui os 200 mapas já existentes para suas
respectivas escolas.
=============================================================================
"""

import os
import sys
import json
import shutil

if sys.platform == "win32":
    try:
        sys.stdout.reconfigure(encoding='utf-8')
        sys.stderr.reconfigure(encoding='utf-8')
    except Exception:
        pass

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
OUTPUT_MAPAS_DIR = os.path.join(BASE_DIR, "output_mapas")

ESCOLAS_CONFIG = [
    {
        "id": "01",
        "pasta": "01_ciencia_computacao_uninter",
        "nome": "Ciência da Computação UNINTER (Teoria & Hardware)",
        "descricao": "Arquitetura Von Neumann, Sistemas Operacionais, Estruturas de Dados Clássicas e Teoria da Computação",
        "faixa_ids": [135, 136, 137, 138, 139, 140, 141, 142, 143, 144, 145, 146, 147] + list(range(411, 461))
    },
    {
        "id": "02",
        "pasta": "02_logica_e_algoritmos",
        "nome": "Lógica de Programação & Algoritmos",
        "descricao": "Fundamentos do zero, variáveis, tipos de dados, operadores, loops, funções, arrays, objetos e Git",
        "faixa_ids": list(range(1, 96)) + list(range(641, 701))
    },
    {
        "id": "03",
        "pasta": "03_python_especialista",
        "nome": "Python Especialista (Do Zero à Automação)",
        "descricao": "Sintaxe moderna de Python, scripts de automação, web scraping, manipulação de arquivos e ecossistema Python",
        "faixa_ids": list(range(201, 261))
    },
    {
        "id": "04",
        "pasta": "04_backend_e_apis",
        "nome": "Back-end, APIs RESTful & Microsserviços",
        "descricao": "Programação Orientada a Objetos (POO), arquitetura de APIs, autenticação, microsserviços e Java/C#/Node",
        "faixa_ids": list(range(96, 116)) + list(range(461, 521))
    },
    {
        "id": "05",
        "pasta": "05_frontend_e_mobile",
        "nome": "Front-end, Mobile & UX/UI",
        "descricao": "DOM, eventos no navegador, JavaScript assíncrono, Promises, fetch, HTML5/CSS3, React e Flutter",
        "faixa_ids": list(range(116, 135)) + list(range(521, 581))
    },
    {
        "id": "06",
        "pasta": "06_banco_dados_e_ia",
        "nome": "Banco de Dados SQL & NoSQL, Big Data & IA",
        "descricao": "Modelagem relacional, comandos SQL, JOINS, ACID, NoSQL, Inteligência Artificial, Machine Learning e LLMs",
        "faixa_ids": [149, 150] + list(range(151, 201)) + list(range(581, 641))
    },
    {
        "id": "07",
        "pasta": "07_devops_linux_e_nuvem",
        "nome": "DevOps, Linux & Nuvem",
        "descricao": "Administração Linux, Shell Script, redes de computadores, Docker, Kubernetes, CI/CD e Cloud AWS",
        "faixa_ids": list(range(261, 341))
    },
    {
        "id": "08",
        "pasta": "08_ciberseguranca",
        "nome": "Cibersegurança & Ethical Hacking",
        "descricao": "Criptografia clássica e moderna, segurança web OWASP Top 10, Red Team (Pentest) e Blue Team (Defesa)",
        "faixa_ids": [148] + list(range(341, 411))
    }
]

def organizar():
    print("=" * 70)
    print("📁 ORGANIZANDO O ACERVO NAS 8 ESCOLAS DA COMPUTAÇÃO...")
    print("=" * 70)

    # 1. Cria a estrutura de pastas padronizada
    for esc in ESCOLAS_CONFIG:
        caminho_escola = os.path.join(BASE_DIR, esc["pasta"])
        pasta_json = os.path.join(caminho_escola, "json")
        pasta_imagens = os.path.join(caminho_escola, "imagens")
        pasta_pdf = os.path.join(caminho_escola, "pdf")

        os.makedirs(pasta_json, exist_ok=True)
        os.makedirs(pasta_imagens, exist_ok=True)
        os.makedirs(pasta_pdf, exist_ok=True)

        # Cria README informativo na pasta da escola
        readme_path = os.path.join(caminho_escola, "README.md")
        with open(readme_path, "w", encoding="utf-8") as f:
            f.write(f"# 🎓 Escola {esc['id']}: {esc['nome']}\n\n")
            f.write(f"> {esc['descricao']}\n\n")
            f.write("## 📁 Estrutura desta pasta:\n")
            f.write("- **`json/`**: Arquivos de dados estruturados de cada mapa mental.\n")
            f.write("- **`imagens/`**: Mapas mentais renderizados em PNG de alta resolução (300 DPI).\n")
            f.write("- **`pdf/`**: E-book diagramado em formato A4 Paisagem pronto para impressão.\n")

        print(f"✅ Estrutura criada: {esc['pasta']}/")

    # 2. Distribui os 200 mapas gerados para as pastas correspondentes
    mapas_copiados = 0
    for esc in ESCOLAS_CONFIG:
        pasta_json = os.path.join(BASE_DIR, esc["pasta"], "json")
        for map_id in esc["faixa_ids"]:
            origem = os.path.join(OUTPUT_MAPAS_DIR, f"mapa_{map_id:03d}.json")
            if os.path.exists(origem):
                destino = os.path.join(pasta_json, f"mapa_{map_id:03d}.json")
                shutil.copy2(origem, destino)
                mapas_copiados += 1

    print(f"\n📦 {mapas_copiados} mapas mentais organizados nas pastas das escolas!")
    print("=" * 70)

if __name__ == "__main__":
    organizar()
