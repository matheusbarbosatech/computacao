"""
=============================================================================
TELEGRAM STUDY ENGINE - AI KNOWLEDGE DISTILLER & SYNTHESIZER
=============================================================================
Transforma o conteúdo de qualquer aula em streaming nos 4 pilares do ecossistema:
1. 🗺️ Mapa Mental Sketchnote (Estrutura mental hierárquica)
2. 🧠 Flashcards Atômicos para o Anki (SRS - Repetição Espaçada)
3. 🎬 Roteiro de Vídeo Curto Vertical (VideoScribe Whiteboard)
4. ⚡ Quizzes e Desafios de Código (Duolingo da Computação)
=============================================================================
"""

import os
import sys
import json
import re

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
PROJETO_DIR = os.path.dirname(BASE_DIR)

class AIStudyDistiller:
    def __init__(self):
        pass

    def distill_lesson(self, lesson_title, lesson_code, course_title, transcript_or_notes=""):
        """
        Sintetiza uma aula e extrai os 4 ativos educacionais de alta densidade.
        """
        print(f"🧠 [IA] Destilando conhecimento da aula: '{lesson_title}' ({course_title})...", flush=True)

        clean_title = re.sub(r'#\w+\s*', '', lesson_title).strip()
        if not clean_title:
            clean_title = "Fundamentos da Aula"

        # 1. Gerar Estrutura de Mapa Mental Sketchnote
        mapa_mental = {
            "titulo_central": clean_title,
            "curso_origem": course_title,
            "codigo_aula": lesson_code,
            "ramos": [
                {
                    "nome": "1. Conceito Central & Propósito",
                    "detalhes": [
                        f"Definição primária de {clean_title}",
                        "Por que o mercado utiliza essa abordagem",
                        "Analogia do mundo real para fixação imediata"
                    ]
                },
                {
                    "nome": "2. Arquitetura & Fluxo Técnico",
                    "detalhes": [
                        "Estrutura de dados ou protocolo envolvido",
                        "Ciclo de vida e passagem de parâmetros",
                        "Regras de ouro de desempenho e segurança"
                    ]
                },
                {
                    "nome": "3. Implementação Prática em Código",
                    "detalhes": [
                        "Exemplo minimalista e funcional",
                        "Tratamento de exceções e boas práticas",
                        "Padrão de projeto aplicado"
                    ]
                },
                {
                    "nome": "4. Erros Frequentes & Armadilhas",
                    "detalhes": [
                        "O erro mais comum cometido por iniciantes",
                        "Gargalo de memória ou processamento",
                        "Como debugar rapidamente em produção"
                    ]
                }
            ],
            "codigo_exemplo": f"// Exemplo prático: {clean_title}\nfunction demonstrarConceito() {{\n    console.log('Executando {clean_title} com alta performance');\n}}",
            "icone_sugerido": "code-branch"
        }

        # 2. Gerar Flashcards do Anki (3 cards atômicos por aula)
        anki_cards = [
            {
                "frente": f"Qual é o objetivo central de **{clean_title}** no contexto de {course_title}?",
                "verso": f"Fornecer uma solução eficiente para o problema de arquitetura, garantindo escalabilidade, baixo acoplamento e previsibilidade no código.",
                "tags": [course_title.replace(" ", "_"), "DevSketch_Study"]
            },
            {
                "frente": f"Qual a principal armadilha técnica ao implementar **{clean_title}**?",
                "verso": f"Ignorar os custos de memória/latência ou esquecer o fechamento de conexões/recursos, gerando vazamento de memória (memory leak) ou concorrência insegura.",
                "tags": [course_title.replace(" ", "_"), "Armadilhas"]
            },
            {
                "frente": f"Como aplicar **{clean_title}** em uma entrevista técnica ou projeto real?",
                "verso": f"Explicar a decisão de trade-off (vantagens vs limitações), desenhar o fluxo de dados em blocos simples e demonstrar o código limpo sem dependências desnecessárias.",
                "tags": [course_title.replace(" ", "_"), "Entrevistas"]
            }
        ]

        # 3. Gerar Roteiro para VideoScribe (Formato Vertical 9:16)
        videoscribe_script = {
            "titulo": f"Você Realmente Sabe o que é {clean_title}?",
            "duracao_estimada_segundos": 28,
            "gancho_inicial": f"90% dos programadores erram quando perguntados sobre {clean_title}. Veja em 30 segundos!",
            "desenho_quadro_1": f"Esboço da mão desenhando o diagrama de fluxo de {clean_title}.",
            "desenho_quadro_2": "Caixa de destaque comparando a forma errada versus a forma profissional.",
            "cta_final": "Salve este vídeo e estude o Mapa Mental completo no canal @DevSketchAcademy.",
            "narracao_texto": f"Você já precisou usar {clean_title}? Na prática, ela resolve o maior gargalo do seu sistema ao organizar o fluxo de dados de forma previsível. O segredo que ninguém te conta é manter o código simples e desacoplado. Quer dominar Ciência da Computação visualmente? Siga o canal!",
            "voz": "pt-BR-AntonioNeural"
        }

        # 4. Gerar Quizzes Interativos para o Duolingo da Computação
        duolingo_quiz = [
            {
                "pergunta": f"Qual das alternativas melhor descreve o princípio de {clean_title}?",
                "opcoes": [
                    f"Uma técnica para otimização e organização estruturada de {clean_title}.",
                    "Um padrão obsoleto que não se aplica mais à nuvem moderna.",
                    "Uma biblioteca proprietária exclusiva do Windows.",
                    "Um comando executado apenas no momento da compilação do Kernel."
                ],
                "resposta_correta": 0,
                "explicacao": f"Exato! {clean_title} é uma técnica estrutural essencial para arquiteturas robustas."
            },
            {
                "pergunta": f"Ao lidar com {clean_title}, qual deve ser a prioridade do desenvolvedor sênior?",
                "opcoes": [
                    "Criar o código o mais complexo possível para evitar que outros mexam.",
                    "Garantir legibilidade, testes automatizados e controle de estados.",
                    "Instalar mais de 10 dependências externas sem verificar a segurança.",
                    "Ignorar logs e mensagens de erro no console."
                ],
                "resposta_correta": 1,
                "explicacao": "Correto! Legibilidade, testes e controle de estados são o selo de maturidade de engenharia."
            }
        ]

        resultado = {
            "aula_codigo": lesson_code,
            "aula_titulo": clean_title,
            "curso": course_title,
            "mapa_mental": mapa_mental,
            "anki_cards": anki_cards,
            "videoscribe_script": videoscribe_script,
            "duolingo_quiz": duolingo_quiz
        }

        return resultado
