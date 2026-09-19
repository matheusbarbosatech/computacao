"""
=============================================================================
CATÁLOGO MESTRE DAS 8 ESCOLAS DA COMPUTAÇÃO (~700 MAPAS MENTAIS)
=============================================================================
Estrutura completa das Escolas, Carreiras e Tópicos individuais,
fundindo a base teórica da UNINTER, as demandas práticas da ALURA e a didática
visual de primeiros princípios de FEYNMAN / CS50.
=============================================================================
"""

from typing import List, Dict

ESCOLAS_METADATA = [
    {
        "id": "01",
        "codigo": "uninter",
        "icone": "🏛️",
        "nome": "Ciência da Computação UNINTER",
        "pasta": "01_ciencia_computacao_uninter",
        "descricao": "Arquitetura Von Neumann, Sistemas Operacionais, Compiladores e Teoria da Computação",
        "carreiras": [
            "Arquitetura de Computadores & Hardware",
            "Sistemas Operacionais & Concorrência",
            "Estruturas de Dados Avançadas & Complexidade Big-O",
            "Teoria da Computação, Autômatos & Compiladores"
        ]
    },
    {
        "id": "02",
        "codigo": "logica",
        "icone": "💻",
        "nome": "Lógica de Programação & Algoritmos",
        "pasta": "02_logica_e_algoritmos",
        "descricao": "Fundamentos do zero absoluto, tomada de decisão, loops, funções, arrays, objetos e Git",
        "carreiras": [
            "Fundamentos da Computação & Pensamento Lógico",
            "Lógica de Decisão e Estruturas de Repetição",
            "Funções, Modularização & Escopo",
            "Coleções de Dados (Arrays, Objetos & JSON)",
            "Git & GitHub Profissional"
        ]
    },
    {
        "id": "03",
        "codigo": "python",
        "icone": "🐍",
        "nome": "Python Especialista",
        "pasta": "03_python_especialista",
        "descricao": "Do básico à automação de tarefas, web scraping, manipulação de dados e scripts inteligentes",
        "carreiras": [
            "Sintaxe Moderna & Estruturas de Dados Pythonicas",
            "Automação de Tarefas & Manipulação de Arquivos",
            "Web Scraping & Coleta Automatizada de Dados",
            "Programação Orientada a Objetos com Python",
            "Desenvolvimento de APIs com FastAPI & Flask"
        ]
    },
    {
        "id": "04",
        "codigo": "backend",
        "icone": "⚙️",
        "nome": "Back-end & Microsserviços",
        "pasta": "04_backend_e_apis",
        "descricao": "Orientação a Objetos, Design Patterns, Arquitetura de APIs RESTful, Java/Spring, C# e Node.js",
        "carreiras": [
            "Programação Orientada a Objetos (POO) & Princípios SOLID",
            "Arquitetura de APIs RESTful & Protocolo HTTP",
            "Java & Ecossistema Spring Boot",
            "C# & Ecossistema .NET Moderno",
            "Node.js, TypeScript & NestJS",
            "Padrões de Microsserviços & Mensageria"
        ]
    },
    {
        "id": "05",
        "codigo": "frontend",
        "icone": "📱",
        "nome": "Front-end, Mobile & UX/UI",
        "pasta": "05_frontend_e_mobile",
        "descricao": "HTML5 semântico, CSS3 Flexbox/Grid, JavaScript moderno, React, Next.js, Flutter e Design UX",
        "carreiras": [
            "HTML5 Semântico, CSS3 Moderno & Design Responsivo",
            "JavaScript Moderno (ES6+) & Manipulação do DOM",
            "React.js & Next.js para Aplicações Web",
            "Desenvolvimento Mobile Multiplataforma com Flutter",
            "Fundamentos de UX/UI Design & Ergonomia Cognitiva"
        ]
    },
    {
        "id": "06",
        "codigo": "dados_ia",
        "icone": "🗄️",
        "nome": "Banco de Dados SQL/NoSQL & IA",
        "pasta": "06_banco_dados_e_ia",
        "descricao": "Modelagem relacional, consultas SQL avançadas, JOINS, ACID, NoSQL, Machine Learning e LLMs",
        "carreiras": [
            "Modelagem Relacional & Comandos SQL (SELECT, INSERT, UPDATE)",
            "Consultas Avançadas, Agrupamentos (GROUP BY) & JOINS",
            "Otimização, Índices, Transações ACID & Triggers",
            "Bancos NoSQL (MongoDB, Redis) & Big Data",
            "Machine Learning & Aprendizado Profundo",
            "Engenharia de LLMs, Prompts, Embeddings & RAG"
        ]
    },
    {
        "id": "07",
        "codigo": "devops",
        "icone": "☁️",
        "nome": "DevOps, Linux & Nuvem",
        "pasta": "07_devops_linux_e_nuvem",
        "descricao": "Administração Linux, Shell Scripting, Redes de Computadores, Docker, Kubernetes, CI/CD e AWS",
        "carreiras": [
            "Linux Essencial & Shell Scripting para Desenvolvedores",
            "Redes de Computadores & Protocolos de Comunicação",
            "Containers com Docker & Docker Compose",
            "Orquestração de Containers com Kubernetes (K8s)",
            "Computação em Nuvem (AWS / GCP / Azure)",
            "Pipelines de CI/CD com GitHub Actions"
        ]
    },
    {
        "id": "08",
        "codigo": "ciberseguranca",
        "icone": "🛡️",
        "nome": "Cibersegurança & Ethical Hacking",
        "pasta": "08_ciberseguranca",
        "descricao": "Criptografia, Segurança Web OWASP Top 10, Red Team (Pentest), Blue Team (Defesa) e Segurança Cloud",
        "carreiras": [
            "Fundamentos de Segurança da Informação & Criptografia",
            "Segurança em Aplicações Web (OWASP Top 10)",
            "Red Team: Metodologias de Pentest & Invasão Ética",
            "Blue Team: Defesa, Monitoramento SOC & Resposta a Incidentes",
            "Governança, Privacidade (LGPD) & Engenharia Social"
        ]
    }
]

def obter_escolas():
    return ESCOLAS_METADATA

def obter_escola_por_codigo(codigo: str):
    for e in ESCOLAS_METADATA:
        if e["codigo"] == codigo or e["pasta"] == codigo:
            return e
    return None
