# -*- coding: utf-8 -*-
"""
Script para gerar os Atalhos de Desktop e Painel de Acesso Rápido aos Cursos de Criação de Produto.
"""
import os
import sys

sys.stdout.reconfigure(encoding='utf-8')
sys.stderr.reconfigure(encoding='utf-8')

DESKTOP_DIR = r"C:\Users\matheus\Desktop"
FOLDER_CURSOS = os.path.join(DESKTOP_DIR, "🎓 CURSOS - CRIACAO DE PRODUTO")

os.makedirs(FOLDER_CURSOS, exist_ok=True)

CURSOS = [
    {
        "num": "01",
        "nome": "PM3 - Curso de Product Management",
        "icone": "🎓",
        "categoria": "Product Discovery & Métricas",
        "id": "1APzYTMyc6MnB0-waSnpegwYfzdOocQ2d",
        "url": "https://drive.google.com/drive/folders/1APzYTMyc6MnB0-waSnpegwYfzdOocQ2d",
        "desc": "O padrão-ouro nacional. Aprenda Product Discovery, entrevistas de validação, mapeamento de dores reais e definição de MVP."
    },
    {
        "num": "02",
        "nome": "Dev de Oferta | O Roadmap",
        "icone": "🎯",
        "categoria": "Engenharia de Oferta & Valor",
        "id": "12uZn8GQqV7YRy9H8MwE910rTO-F1bvqF",
        "url": "https://drive.google.com/drive/folders/12uZn8GQqV7YRy9H8MwE910rTO-F1bvqF",
        "desc": "Como transformar sua competência técnica em uma proposta irresistível que clientes corporativos ou finais compram com facilidade."
    },
    {
        "num": "03",
        "nome": "MVP ao SaaS - Gustavo Sextaro",
        "icone": "🤖",
        "categoria": "Micro-SaaS & Ferramentas",
        "id": "1DbTpTqIQsan7Ua-5CfopIe8PfMQgjxMs",
        "url": "https://drive.google.com/drive/folders/1DbTpTqIQsan7Ua-5CfopIe8PfMQgjxMs",
        "desc": "Como construir softwares enxutos, ferramentas resolutivas e micro-SaaS que resolvem problemas pontuais e geram receita recorrente."
    },
    {
        "num": "04",
        "nome": "PM3 - Curso de Product Marketing",
        "icone": "📢",
        "categoria": "Go-to-Market & Posicionamento",
        "id": "1B2qIUalRgqRQMeMCQFHZsRzUKPs93kAp",
        "url": "https://drive.google.com/drive/folders/1B2qIUalRgqRQMeMCQFHZsRzUKPs93kAp",
        "desc": "Estratégia de lançamento, proposta única de valor (UVP), diferenciação de concorrentes e conquista dos primeiros usuários pagantes."
    },
    {
        "num": "05",
        "nome": "No Code Start Up [Formações & Cursos]",
        "icone": "🧩",
        "categoria": "Construção Ágil de Produtos",
        "id": "1h9F9BNG2eQO0ndB1xpFFwhm-36k1119w",
        "url": "https://drive.google.com/drive/folders/1h9F9BNG2eQO0ndB1xpFFwhm-36k1119w",
        "desc": "Crie ferramentas web, painéis administrativos e aplicativos completos sem precisar perder 6 meses codando do zero."
    },
    {
        "num": "06",
        "nome": "Comunidade sem Codar - Renato Asse",
        "icone": "💻",
        "categoria": "Sistemas Web & Low-Code",
        "id": "1o2jnecoxp01WLh_FQCApt1kyK-zpQzC8",
        "url": "https://drive.google.com/drive/folders/1o2jnecoxp01WLh_FQCApt1kyK-zpQzC8",
        "desc": "Construção de plataformas completas e funcionais que atendem empresas e usuários finais com estabilidade e design."
    },
    {
        "num": "07",
        "nome": "Meu Sistema Lucrativo - Paulo Borges",
        "icone": "💰",
        "categoria": "Sistemas de Alto Valor",
        "id": "1nnZNfaLVDhYiqMpD8jEya_mUykLS13Z7",
        "url": "https://drive.google.com/drive/folders/1nnZNfaLVDhYiqMpD8jEya_mUykLS13Z7",
        "desc": "Modelagem de produtos e softwares para venda direta com altas margens para o mercado corporativo e prestadores de serviço."
    },
    {
        "num": "08",
        "nome": "IA Saas Club - Victor Demarco",
        "icone": "🧠",
        "categoria": "IA Aplicada a Produtos",
        "id": "12PU_SFWfgnwgj4EjjmA8MWg4LtAPhDTM",
        "url": "https://drive.google.com/drive/folders/12PU_SFWfgnwgj4EjjmA8MWg4LtAPhDTM",
        "desc": "Desenvolvimento de produtos e agentes inteligentes que resolvem tarefas humanas complexas com cobrança por mensalidade."
    },
    {
        "num": "09",
        "nome": "Fórmula Negócio Online 2026",
        "icone": "📦",
        "categoria": "Infoprodutos & Métodos Didáticos",
        "id": "1llt8Eh2WljYDXHzKdfmCK3y2pII9pxaj",
        "url": "https://drive.google.com/drive/folders/1llt8Eh2WljYDXHzKdfmCK3y2pII9pxaj",
        "desc": "O guia mais aprofundado do Brasil em pesquisa de nichos lucrativos, validação de demanda e esteira didática estruturada."
    },
    {
        "num": "10",
        "nome": "Código do Produto Viral",
        "icone": "🔥",
        "categoria": "Produtos com Viralidade Nativa",
        "id": "1lO629VzW7cRfcdBxu8XhVEM1XpXCTpI-",
        "url": "https://drive.google.com/drive/folders/1lO629VzW7cRfcdBxu8XhVEM1XpXCTpI-",
        "desc": "Workshop e vitrine com análise reversa de produtos que viralizam organicamente e se vendem pela própria utilidade."
    },
    {
        "num": "11",
        "nome": "Venda Todo Santo Dia 2026",
        "icone": "⚡",
        "categoria": "Produtos Perpétuos",
        "id": "1DIh_cw4PP2QN9iLrSRXLRDEL1M34Vzwx",
        "url": "https://drive.google.com/drive/folders/1DIh_cw4PP2QN9iLrSRXLRDEL1M34Vzwx",
        "desc": "Engenharia de produtos para venda diária contínua e estável no tráfego sem a pressão de lançamentos semestrais."
    },
    {
        "num": "12",
        "nome": "Formação Funnel Builder - Thiago Finch",
        "icone": "🚀",
        "categoria": "Arquitetura de Conversão",
        "id": "1m5-o9cNs56jxDoGRnNgdApHQv7AoRJoS",
        "url": "https://drive.google.com/drive/folders/1m5-o9cNs56jxDoGRnNgdApHQv7AoRJoS",
        "desc": "Estruturação das páginas, vídeos de vendas e jornada completa do usuário para máxima taxa de conversão."
    }
]

def criar_atalho_url(caminho, url):
    conteudo = f"[InternetShortcut]\nURL={url}\n"
    with open(caminho, "w", encoding="utf-8") as f:
        f.write(conteudo)

def main():
    print("Gerando atalhos na pasta de Criação de Produto...")
    for c in CURSOS:
        nome_arquivo = f"{c['num']}. {c['nome']}.url"
        # Limpar caracteres inválidos para Windows
        for char in [':', '*', '?', '"', '<', '>', '|']:
            nome_arquivo = nome_arquivo.replace(char, '')
        caminho = os.path.join(FOLDER_CURSOS, nome_arquivo)
        criar_atalho_url(caminho, c['url'])
        print(f" -> Criado: {nome_arquivo}")

    # Criar também os 3 atalhos principais diretamente na raiz do Desktop para acesso instantâneo
    destaques = [
        ("🎓 01. PM3 - Product Management.url", "https://drive.google.com/drive/folders/1APzYTMyc6MnB0-waSnpegwYfzdOocQ2d"),
        ("🎯 02. Dev de Oferta.url", "https://drive.google.com/drive/folders/12uZn8GQqV7YRy9H8MwE910rTO-F1bvqF"),
        ("🤖 03. MVP ao SaaS.url", "https://drive.google.com/drive/folders/1DbTpTqIQsan7Ua-5CfopIe8PfMQgjxMs"),
        ("☁️ Drive Matriz (Completo).url", "https://drive.google.com/drive/folders/1cBDvRvFL4B5TmD7oXYfcTYvlHl40GXGG")
    ]
    for nome, url in destaques:
        caminho = os.path.join(DESKTOP_DIR, nome)
        criar_atalho_url(caminho, url)
        print(f" -> Criado no Desktop: {nome}")

    print("\nTodos os atalhos criados com sucesso!")

if __name__ == "__main__":
    main()
