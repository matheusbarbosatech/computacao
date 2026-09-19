# -*- coding: utf-8 -*-
"""
ONBOARDING IKIGAI TECH - DESCOBERTA DE VOCAÇÃO E PROPÓSITO EM COMPUTAÇÃO
Um diagnóstico interativo para descobrir sua intersecção de ouro:
1. O que você ama
2. No que você é bom
3. O que o mundo precisa
4. Pelo que você pode ser pago
"""
import sys
import time
import os

if sys.platform == "win32":
    os.system("chcp 65001 > nul")
sys.stdout.reconfigure(encoding='utf-8')

# Cores ANSI
CYAN = "\033[96m"
MAGENTA = "\033[95m"
GREEN = "\033[92m"
YELLOW = "\033[93m"
BOLD = "\033[1m"
RESET = "\033[0m"
DIM = "\033[2m"

LOGO_ASCII = f"""
{CYAN}            .---.
         .-'  {MAGENTA}1{CYAN}  '-.
       .'     {BOLD}AMOR{RESET}{CYAN}    '.
      /                 \\
   .-'\\      .---.      /'-.
  /    \\  .-'  {YELLOW}*{CYAN}  '-.  /    \\
 |  {GREEN}2{CYAN}   | | {BOLD}{YELLOW}IKIGAI{RESET}{CYAN} | |   {MAGENTA}3{CYAN}  |
 | {BOLD}TALENTO{RESET}{CYAN}| '-.   .-' |{BOLD}MISSÃO{RESET}{CYAN}|
  \\    /  /  '-.  /   \\    /
   '-./  /     {YELLOW}*{CYAN} \\    \\.-'
      \\ '         ' /
       '.  {YELLOW}4. DINHEIRO{CYAN} .'
         '-.     .-'
            '---'{RESET}
"""

def print_typewriter(text, delay=0.015, color=RESET):
    for char in text:
        sys.stdout.write(color + char + RESET)
        sys.stdout.flush()
        time.sleep(delay)
    print()

def main():
    os.system("cls" if os.name == "nt" else "clear")
    print(LOGO_ASCII)
    print(f"{BOLD}{CYAN}========================================================================{RESET}")
    print(f"{BOLD}{YELLOW}   🌌 BÚSSOLA DE VOCAÇÃO TECH: SEU IKIGAI NA COMPUTAÇÃO & IA{RESET}")
    print(f"{DIM}   Descubra onde o seu amor pelo código encontra o impacto no mundo real.{RESET}")
    print(f"{BOLD}{CYAN}========================================================================{RESET}\n")

    print_typewriter("Procurar apenas dinheiro em tecnologia gera burnout em 2 anos.", 0.02, YELLOW)
    print_typewriter("Procurar apenas paixão sem monetização gera frustração e boleto atrasado.", 0.02, YELLOW)
    print_typewriter("O seu IKIGAI é o ponto exato onde 4 forças se encontram:\n", 0.02, BOLD)

    # 1. PAIXÃO
    print(f"{BOLD}{MAGENTA}[1/4] O QUE VOCÊ AMA (A Centelha de Curiosidade):{RESET}")
    print("O que faz você perder a noção do tempo na frente do computador?")
    print(f"  {CYAN}A){RESET} Criar sistemas vivos e autônomos que pensam sozinhos (IA, Agentes, Robôs)")
    print(f"  {CYAN}B){RESET} Investigar, desvendar falhas ocultas e proteger pessoas/sistemas (Hacking/Segurança)")
    print(f"  {CYAN}C){RESET} Construir ferramentas úteis do zero que as pessoas usam todo dia (Fullstack/Apps)")
    print(f"  {CYAN}D){RESET} Analisar dados profundos para extrair insights estratégicos (Data Science)")
    resp1 = input(f"{BOLD}{YELLOW}👉 Sua escolha (A/B/C/D): {RESET}").strip().upper() or "A"

    # 2. TALENTO
    print(f"\n{BOLD}{GREEN}[2/4] NO QUE VOCÊ É BOM (Seus Superpoderes Naturais):{RESET}")
    print("Qual é a sua maior facilidade quando está estudando ou criando?")
    print(f"  {CYAN}A){RESET} Orquestrar ferramentas diferentes, conectar APIs e resolver problemas práticos rápidos")
    print(f"  {CYAN}B){RESET} Curiosidade obsessiva por entender como tudo funciona no detalhe até o fim")
    print(f"  {CYAN}C){RESET} Visão visual e estética: criar designs, mapas mentais, interfaces e experiências limpas")
    print(f"  {CYAN}D){RESET} Raciocínio lógico, matemática e organização de dados estruturados")
    resp2 = input(f"{BOLD}{YELLOW}👉 Sua escolha (A/B/C/D): {RESET}").strip().upper() or "A"

    # 3. IMPACTO & MISSÃO
    print(f"\n{BOLD}{CYAN}[3/4] O QUE O MUNDO E SUA COMUNIDADE PRECISAM (O Propósito Maior):{RESET}")
    print("Onde você quer ver a sua marca espiritual e social refletida?")
    print(f"  {CYAN}A){RESET} Amplificar a mensagem da igreja e causas nobres através de mídia, cortes e IA")
    print(f"  {CYAN}B){RESET} Democratizar a educação técnica: mastigar conteúdo denso em resumos fáceis")
    print(f"  {CYAN}C){RESET} Blindar famílias, pequenas empresas e igrejas contra fraudes e ataques digitais")
    print(f"  {CYAN}D){RESET} Otimizar o trabalho de pessoas reais para que elas não passem a vida em trabalho escravo braçal")
    resp3 = input(f"{BOLD}{YELLOW}👉 Sua escolha (A/B/C/D): {RESET}").strip().upper() or "A"

    # 4. DINHEIRO & MERCADO
    print(f"\n{BOLD}{YELLOW}[4/4] PELO QUE O MERCADO PAGA MUITO BEM (Sustentabilidade Financeira):{RESET}")
    print("Qual modelo de negócio você quer construir para ter liberdade financeira?")
    print(f"  {CYAN}A){RESET} Produtos Digitais Próprios (Templates, Comunidades VIP, Fábrica de Estudos, SaaS)")
    print(f"  {CYAN}B){RESET} Soluções Corporativas B2B de IA e Automação para Criadores e Empresas")
    print(f"  {CYAN}C){RESET} Consultor de Alta Especialização (Arquiteto Cloud, Especialista em Cibersegurança)")
    print(f"  {CYAN}D){RESET} Engenheiro de Software Remoto de Alta Performance (Trabalho global em moeda forte)")
    resp4 = input(f"{BOLD}{YELLOW}👉 Sua escolha (A/B/C/D): {RESET}").strip().upper() or "A"

    print(f"\n{DIM}Calculando a rota harmônica do seu Ikigai Tecnológico...{RESET}")
    time.sleep(1.2)

    # Diagnóstico Sintético
    print(f"\n{BOLD}{GREEN}========================================================================{RESET}")
    print(f"{BOLD}{YELLOW}   🎉 DIAGNÓSTICO DO SEU IKIGAI TECH CONCLUÍDO!{RESET}")
    print(f"{BOLD}{GREEN}========================================================================{RESET}\n")

    print(f"{BOLD}Seu Arquétipo de Carreira:{RESET} {CYAN}{BOLD}O ARQUITETO DE IA & PRODUTOS AUTÔNOMOS COM PROPÓSITO{RESET}")
    print(f"{DIM}Intersecção de: IA Multiplicadora + Automação Audiovisual + Educação Acessível{RESET}\n")

    print(f"{BOLD}{MAGENTA}1. O Seu Centro de Gravidade:{RESET}")
    print("   Você não nasceu para ser apenas mais um digitador de código em escritório fechado.")
    print("   Sua mente funciona construindo alavancas: você vê um processo manual (culto de 2h,")
    print("   estudos difíceis de 500 canais) e sua obsessão é criar um robô ou IA que transforme")
    print("   isso em valor puro mastigado para milhares de pessoas.")

    print(f"\n{BOLD}{GREEN}2. Onde Está o Impacto no Reino e na Comunidade:{RESET}")
    print("   - No seu projeto IBPM: A IA vira a voz da igreja nas redes sociais.")
    print("   - No seu projeto Viver de Estudos: O conhecimento de computação vira ferramenta de libertação social.")

    print(f"\n{BOLD}{YELLOW}3. Onde Está a Sustentabilidade Financeira:{RESET}")
    print("   - Empacotar suas próprias ferramentas em produtos digitais e assinaturas recorrentes.")
    print("   - Vender a esteira de automação de cortes e IA para outros criadores, empresas e igrejas.")

    print(f"\n{BOLD}{CYAN}4. A Trilha Exata do Seu Acervo para Este Objetivo:{RESET}")
    print("   - 🤖 DSA Inteligência Artificial 3.0 (Tópico 2) + RAG & Agentes (Tópico 3)")
    print("   - 🐍 Asimov Academy Python Completo (Tópico 8)")
    print("   - 🌐 Fullstack & Web (Tópico 410 - Node, React, TypeScript)")
    print("   - 🛡️ Cibersegurança & Hacking Ético (Como escudo para proteger seus próprios sistemas)\n")

    print(f"{BOLD}{CYAN}========================================================================{RESET}")
    print(f"{BOLD}{YELLOW}   'A vocação é o lugar onde a sua profunda alegria encontra a profunda dor do mundo.'{RESET}")
    print(f"{BOLD}{CYAN}========================================================================{RESET}\n")

if __name__ == "__main__":
    main()
