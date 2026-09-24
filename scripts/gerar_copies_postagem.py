#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
GERADOR DE COPIES E METADADOS DE ALTA CONVERSÃO — CULTO 459 (20/09/2026)
IBPM CR Automation System — Fase 4

Gera o catálogo mestre de textos, títulos SEO, hashtags, CTAs e minutagem:
1. 📖 Tier 3: Pregação Completa com Capítulos/Timestamps clicáveis para o YouTube.
2. 🎬 Tier 2: 14 Cortes Médios com copies completas para YouTube 16:9, Instagram Reels e TikTok.
3. ⚡ Tier 1: Ganchos e copies ultra-rápidas para os Micro-Shorts de Ápice.

Saídas:
- C:\\Users\\matheus\\Desktop\\cortes_audio_culto_459_20_09_2026\\00_COPIES_E_METADADOS_POSTAGEM.txt
- C:\\Users\\matheus\\Desktop\\cortes_audio_culto_459_20_09_2026\\00_COPIES_E_METADADOS_POSTAGEM.json
"""

import sys
import json
from pathlib import Path
from typing import List, Dict, Any

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
if hasattr(sys.stderr, "reconfigure"):
    sys.stderr.reconfigure(encoding="utf-8", errors="replace")

DESKTOP_DIR = Path.home() / "Desktop" / "cortes_audio_culto_459_20_09_2026"
DESKTOP_DIR.mkdir(parents=True, exist_ok=True)

# Minutagem base da Pregação Completa (Tier 3)
T3_INICIO_SEC = 6050.0
T3_FIM_SEC = 8300.0
T3_DURACAO_SEC = T3_FIM_SEC - T3_INICIO_SEC

CORTES_MEDIOS = [
    {
        "id": "MEDIO_01",
        "nome_base": "MEDIO_01_TESTEMUNHO_MILAGRE_CECILIA",
        "titulo_base": "Testemunho do Milagre da Cecília (Alcançada pela Transmissão)",
        "titulo_youtube": "FUI ALCANÇADA PELA TRANSMISSÃO! Testemunho Forte de Milagre e Cura | IBPM",
        "titulo_reels": "O milagre aconteceu quando ela ligou a transmissão! 🔥😭",
        "titulo_tiktok": "Deus alcançou ela dentro de casa pela transmissão! Assista até o final",
        "tema": "Testemunho & Fé",
        "versiculo": "Lucas 1:37 — 'Porque para Deus nada é impossível.'",
        "st": 6059.5,
        "en": 6227.0,
        "palavras_enfase": ["MILAGRE", "TESTEMUNHO", "TELEVISÃO", "VITÓRIA", "SENHOR", "ORAÇÃO"]
    },
    {
        "id": "MEDIO_02",
        "nome_base": "MEDIO_02_GIDEAO_IDENTIDADE_GUERREIRO",
        "titulo_base": "Gideão e a Identidade de Homem Valente",
        "titulo_youtube": "VOCÊ NÃO É QUEM O CHÃO DISSE QUE VOCÊ É! A Mensagem de Gideão | IBPM",
        "titulo_reels": "Deus não te chamou pelo que você é no chão, mas pelo que Ele vai fazer! ⚔️🔥",
        "titulo_tiktok": "Você não é quem os outros disseram! Deus te chama de guerreiro valente",
        "tema": "Identidade & Propósito",
        "versiculo": "Juízes 6:12 — 'O Senhor é contigo, homem valoroso.'",
        "st": 6262.0,
        "en": 6455.0,
        "palavras_enfase": ["GIDEÃO", "GUERREIRO", "IDENTIDADE", "VALOROSO", "SENHOR"]
    },
    {
        "id": "MEDIO_04",
        "nome_base": "MEDIO_04_PROCESSO_SEMENTE_TEMPO_PLANTAR",
        "titulo_base": "Há Tempo de Plantar: O Processo da Semente no Escuro",
        "titulo_youtube": "RESPEITE O TEMPO DA SUA SEMENTE NO ESCURO | Palavra Poderosa | IBPM",
        "titulo_reels": "A semente não morreu no escuro da terra, ela está gerando vida! 🌱✨",
        "titulo_tiktok": "Antes de brotar, a semente fica no escuro. Aguente o processo!",
        "tema": "Paciência & Crescimento",
        "versiculo": "Eclesiastes 3:1-2 — 'Tudo tem o seu tempo determinado, e há tempo para todo o propósito debaixo do céu.'",
        "st": 6475.0,
        "en": 6657.0,
        "palavras_enfase": ["SEMENTE", "PLANTAR", "COLHEITA", "PROCESSO", "MILAGRE"]
    },
    {
        "id": "MEDIO_05",
        "nome_base": "MEDIO_05_TESTEMUNHO_LUTO_CONSOLO_ESPIRITO_SANTO",
        "titulo_base": "Testemunho no Luto: O Espírito Santo Quando o Chão Desaparece",
        "titulo_youtube": "QUANDO O CHÃO SUMIU, O ESPÍRITO SANTO ME SEGUROU PELA MÃO | Testemunho Real",
        "titulo_reels": "Quando o chão desaparece, o Espírito Santo segura na sua mão! 🕊️❤️",
        "titulo_tiktok": "Se você perdeu o chão, ouça isso hoje! O Consolador está aqui",
        "tema": "Consolo & Superação",
        "versiculo": "João 14:16 — 'E eu rogarei ao Pai, e ele vos dará outro Consolador, para que fique convosco para sempre.'",
        "st": 6658.0,
        "en": 6858.0,
        "palavras_enfase": ["ESPÍRITO SANTO", "CONSOLO", "LUTO", "DOR", "SENHOR", "VIDA"]
    },
    {
        "id": "MEDIO_06",
        "nome_base": "MEDIO_06_CAOS_IDENTIDADE_LEVANTE_PROFETIZE",
        "titulo_base": "O Caos Tentou Roubar Sua Identidade? Levante e Profetize!",
        "titulo_youtube": "O CAOS TENTOU ROUBAR A SUA IDENTIDADE? Levante e Profetize! | IBPM",
        "titulo_reels": "O inimigo tentou roubar sua identidade, mas Deus te devolve o cetro hoje! 👑⚡",
        "titulo_tiktok": "Não aceite perder quem você é em Deus! Levante e profetize",
        "tema": "Batalha Espiritual",
        "versiculo": "Romanos 8:37 — 'Mas em todas estas coisas somos mais do que vencedores, por aquele que nos amou.'",
        "st": 6860.0,
        "en": 7048.0,
        "palavras_enfase": ["IDENTIDADE", "PROFETIZE", "CAOS", "LEVANTE", "AUTORIDADE"]
    },
    {
        "id": "MEDIO_07",
        "nome_base": "MEDIO_07_EZEQUIEL_VALE_OSSOS_SECOS",
        "titulo_base": "Ezequiel no Vale de Ossos Secos: Onde Há Morte, Deus Vê Vida",
        "titulo_youtube": "EZEQUIEL NO VALE DE OSSOS SECOS: Onde Há Morte, Deus Vê Vida e Exército! | IBPM",
        "titulo_reels": "Onde o homem vê osso seco e fim, Deus vê um exército de pé! 💀➡️⚔️",
        "titulo_tiktok": "Deus te levou no vale não pra morrer, mas pra profetizar!",
        "tema": "Estudo Bíblico Profético",
        "versiculo": "Ezequiel 37:3 — 'Disse-me ele: Filho do homem, poderão viver estes ossos? E eu disse: Senhor Deus, tu o sabes.'",
        "st": 7050.0,
        "en": 7208.0,
        "palavras_enfase": ["VALE", "OSSOS", "EZEQUIEL", "VIDA", "PROFETA", "SENHOR"]
    },
    {
        "id": "MEDIO_08",
        "nome_base": "MEDIO_08_NO_VALE_OSSO_OU_PROFETA",
        "titulo_base": "No Vale: Ou Você é o Osso ou Você é o Profeta!",
        "titulo_youtube": "NO VALE: OU VOCÊ É O OSSO OU VOCÊ É O PROFETA! Palavra de Confronto | IBPM",
        "titulo_reels": "Decida hoje: ou você fica caído como o osso, ou fica de pé como o profeta! 🔥🗣️",
        "titulo_tiktok": "No vale não dá pra ficar em cima do muro: ou você é o osso ou é o profeta!",
        "tema": "Confronto & Avivamento",
        "versiculo": "Ezequiel 37:7 — 'Então profetizei como se me dera ordem; e ouve um ruído enquanto eu profetizava.'",
        "st": 7209.0,
        "en": 7392.0,
        "palavras_enfase": ["PROFETA", "OSSO", "VALE", "PÉ", "ORDEM", "AUTORIDADE"]
    },
    {
        "id": "MEDIO_09",
        "nome_base": "MEDIO_09_MAO_NA_CABECA_PROFETIZE_VIDA",
        "titulo_base": "Coloque a Mão na Cabeça e Profetize Vida em Cristo",
        "titulo_youtube": "COLOQUE A MÃO NA CABEÇA E PROFETIZE VIDA AGORA! Oração de Quebra de Prisão",
        "titulo_reels": "Coloque a mão na cabeça agora e receba essa oração de quebra de ansiedade! ✋🧠⚡",
        "titulo_tiktok": "Se a sua mente está cansada e em guerra, faça essa oração comigo agora!",
        "tema": "Saúde Mental & Cura Interior",
        "versiculo": "Filipenses 4:7 — 'E a paz de Deus, que excede todo o entendimento, guardará os vossos corações e os vossos pensamentos.'",
        "st": 7393.0,
        "en": 7558.0,
        "palavras_enfase": ["VIDA", "CRISTO", "CABEÇA", "PROFETIZE", "GUERRA"]
    },
    {
        "id": "MEDIO_03",
        "nome_base": "MEDIO_03_DEUS_DO_DE_REPENTE_PONTO_CRITICO",
        "titulo_base": "O Deus do De Repente: Ele Muda 20 Anos em 1 Segundo",
        "titulo_youtube": "O DEUS DO DE REPENTE: Ele Muda 20 Anos em 1 Segundo! Pregação Forte | IBPM",
        "titulo_reels": "O que demorou 20 anos pra travar, Deus destrava em 1 segundo! ⏱️⚡",
        "titulo_tiktok": "Deus não precisa de tempo pra agir. Quando Ele sopra, tudo muda de repente!",
        "tema": "Soberania & Milagres",
        "versiculo": "Atos 2:2 — 'E de repente veio do céu um som, como de um vento veemente e impetuoso.'",
        "st": 7560.0,
        "en": 7740.0,
        "palavras_enfase": ["DE REPENTE", "TEMPO", "SEGUNDO", "PONTO CRÍTICO", "MILAGRE"]
    },
    {
        "id": "MEDIO_10",
        "nome_base": "MEDIO_10_VOLTA_FILHO_PRODIGO_ANEL_AUTORIDADE",
        "titulo_base": "A Decisão do Filho Pródigo: O Anel de Autoridade e Sandálias",
        "titulo_youtube": "O PAI NÃO TE RECEBE COMO ESCRAVO, ELE TE DÁ O ANEL E A SANDÁLIA! | Filho Pródigo",
        "titulo_reels": "Você achou que voltaria como escravo, mas o Pai te coloca o anel de honra! 💍🕊️",
        "titulo_tiktok": "Deus não te trata como escravo. Você é filho e tem autoridade!",
        "tema": "Restauração de Filiação",
        "versiculo": "Lucas 15:22 — 'Mas o pai disse aos seus servos: Trazei depressa a melhor roupa; e vesti-lho, e ponhei-lhe um anel na mão, e alparcas nos pés.'",
        "st": 7740.0,
        "en": 7940.0,
        "palavras_enfase": ["FILHO", "PAI", "AUTORIDADE", "ANEL", "SANDÁLIAS", "PERDÃO"]
    },
    {
        "id": "MEDIO_11",
        "nome_base": "MEDIO_11_CAMINHANDO_DE_MAOS_DADAS_ESPIRITO_SANTO",
        "titulo_base": "Caminhando de Mãos Dadas com o Espírito Santo",
        "titulo_youtube": "APRENDA A CAMINHAR DE MÃOS DADAS COM O ESPÍRITO SANTO | Ministração Profunda",
        "titulo_reels": "Dê a mão para o Espírito Santo hoje e não caminhe mais sozinho! 🤝✨",
        "titulo_tiktok": "Quando você não tiver forças pra andar, segure na mão do Espírito Santo!",
        "tema": "Intimidade & Direção",
        "versiculo": "Gálatas 5:25 — 'Se vivemos no Espírito, andemos também no Espírito.'",
        "st": 7942.0,
        "en": 8118.0,
        "palavras_enfase": ["ESPÍRITO SANTO", "MÃOS DADAS", "CAMINHAR", "DIREÇÃO", "FORÇA"]
    },
    {
        "id": "MEDIO_12",
        "nome_base": "MEDIO_12_TIRE_VESTES_LUTO_RECEBA_VINHO_NOVO",
        "titulo_base": "Tire Hoje as Vestes de Luto e Vergonha e Receba o Vinho Novo",
        "titulo_youtube": "TIRE AS VESTES DE LUTO E VERGONHA E RECEBA O VINHO NOVO! | Palavra Profética",
        "titulo_reels": "Tire hoje a veste de vergonha e receba a unção de alegria e vinho novo! 🍷👗⚡",
        "titulo_tiktok": "Chega de carregar vestes de luto. Deus está trocando suas roupas agora!",
        "tema": "Libertação & Alegria",
        "versiculo": "Isaías 61:3 — 'A dar-lhes uma coroa em vez de cinzas, óleo de gozo em vez de luto, vestes de louvor em vez de espírito angustiado.'",
        "st": 8120.0,
        "en": 8300.0,
        "palavras_enfase": ["VINHO NOVO", "VESTES", "HONRA", "ALEGRIA", "UNÇÃO", "VERGONHA"]
    },
    {
        "id": "PASTOR_01",
        "nome_base": "PASTOR_01_VERDADEIRA_ADORACAO_EM_ESPIRITO",
        "titulo_base": "A Verdadeira Adoração Não é da Boca pra Fora (Pr. Presidente)",
        "titulo_youtube": "A VERDADEIRA ADORAÇÃO NÃO É DA BOCA PRA FORA! Pr. Presidente | IBPM",
        "titulo_reels": "Adoração que move o céu nasce na verdade do coração, não na aparência! 🙌🔥",
        "titulo_tiktok": "Deus não procura bajuladores, procura adoradores em espírito e em verdade!",
        "tema": "Alinhamento Pastoral",
        "versiculo": "João 4:24 — 'Deus é Espírito, e importa que os que o adoram o adorem em espírito e em verdade.'",
        "st": 4860.0,
        "en": 5042.0,
        "palavras_enfase": ["ADORAÇÃO", "ESPÍRITO", "VERDADE", "CORAÇÃO", "ENTREGA"]
    },
    {
        "id": "PASTOR_02",
        "nome_base": "PASTOR_02_ESTA_DOENDO_MAS_DOU_MEU_MELHOR",
        "titulo_base": "Está Doendo e Gemendo, mas Eu Dou Meu Melhor no Altar",
        "titulo_youtube": "ESTÁ DOENDO, MAS EU DOU MEU MELHOR NO ALTAR! Palavra Pastoral Forte | IBPM",
        "titulo_reels": "Mesmo doendo e gemendo, dê o seu melhor para Deus no altar! 😭💪",
        "titulo_tiktok": "O valor da sua entrega está no momento em que você dá o melhor na dor!",
        "tema": "Fidelidade na Dor",
        "versiculo": "2 Samuel 24:24 — 'Não oferecerei ao Senhor meu Deus holocaustos que não me custem nada.'",
        "st": 5050.0,
        "en": 5247.0,
        "palavras_enfase": ["ALTAR", "DOR", "MELHOR", "ENTREGA", "SACRIFÍCIO"]
    }
]

def format_timestamp(seconds: float) -> str:
    m = int(seconds // 60)
    s = int(seconds % 60)
    return f"{m:02d}:{s:02d}"

def gerar_catalogo_completo():
    print("=" * 80)
    print("🚀 GERANDO COPIES E METADADOS DE ALTA CONVERSÃO — CULTO 459")
    print("=" * 80)

    # 1. Montagem dos Capítulos do Tier 3 (Pregação da Pastora das 6050s às 8300s)
    # Ordena os cortes que pertencem à pregação pelo tempo de início
    cortes_pregacao = [c for c in CORTES_MEDIOS if c["st"] >= T3_INICIO_SEC and c["en"] <= T3_FIM_SEC]
    cortes_pregacao.sort(key=lambda x: x["st"])

    capitulos_youtube = ["00:00 - Abertura da Ministração"]
    for c in cortes_pregacao:
        rel_sec = max(0.0, c["st"] - T3_INICIO_SEC)
        capitulos_youtube.append(f"{format_timestamp(rel_sec)} - {c['titulo_base']}")

    capitulos_texto = "\n".join(capitulos_youtube)

    # 2. Estruturação do Pacote Completo (JSON e TXT)
    pacote_json = {
        "culto_id": 459,
        "data_culto": "2026-09-20",
        "tema_geral": "DOMINGO DE CELEBRAÇÃO: O DEUS DO DE REPENTE E A RESTAURAÇÃO DA IDENTIDADE",
        "tier3_pregacao_completa": {
            "titulo_youtube": "PREGAÇÃO COMPLETA: O Deus do De Repente e a Restauração da Identidade | IBPM (20/09/2026)",
            "duracao_estimada": f"{int(T3_DURACAO_SEC // 60)}m{int(T3_DURACAO_SEC % 60):02d}s",
            "capitulos": capitulos_youtube,
            "descricao_youtube": f"""🔥 Assista à ministração completa realizada no Domingo de Celebração da Igreja Batista Palavra e Movimento (20/09/2026).

Uma palavra profética sobre restauração de identidade, o tempo de Deus, consolo no luto e o sopro do Espírito Santo que transforma vales de ossos secos em exércitos de pé!

⏱️ CAPÍTULOS DESTA MINISTRAÇÃO:
{capitulos_texto}

📖 VERSÍCULOS-CHAVE:
• Ezequiel 37 (O Vale de Ossos Secos)
• Juízes 6 (Gideão, Homem Valoroso)
• Lucas 15 (A Parábola do Filho Pródigo)

📍 Igreja Batista Palavra e Movimento — Campo Grande
🔔 Inscreva-se no canal, ative o sino e compartilhe essa bênção com quem você ama!

#IBPM #PregacaoCompleta #Avivamento #EspiritoSanto #PalavraDeDeus #CultoAoVivo #Fe""",
            "tags": [
                "ibpm", "pregação completa", "culto ao vivo", "deus do de repente",
                "ezequiel ossos secos", "gideao", "filho prodigo", "avivamento", "testemunho forte"
            ]
        },
        "cortes_medios_tier2": []
    }

    linhas_txt = [
        "=" * 80,
        "CATÁLOGO OFICIAL DE COPIES E METADADOS DE POSTAGEM — CULTO 459 (20/09/2026)",
        "IBPM Campo Grande — Esteira de Mídia de Alta Performance",
        "=" * 80,
        "",
        "################################################################################",
        "📖 [TIER 3] PREGAÇÃO COMPLETA — YOUTUBE (VÍDEO MESTRE)",
        "################################################################################",
        f"TÍTULO DO YOUTUBE:\n{pacote_json['tier3_pregacao_completa']['titulo_youtube']}\n",
        f"DURAÇÃO: {pacote_json['tier3_pregacao_completa']['duracao_estimada']}\n",
        f"DESCRIÇÃO COM CAPÍTULOS:\n{pacote_json['tier3_pregacao_completa']['descricao_youtube']}\n",
        f"TAGS SUGERIDAS:\n{', '.join(pacote_json['tier3_pregacao_completa']['tags'])}\n\n",
        "################################################################################",
        "🎬 [TIER 2] OS 14 CORTES MÉDIOS & [TIER 1] MICRO-SHORTS DE ÁPICE",
        "################################################################################\n"
    ]

    for idx, c in enumerate(CORTES_MEDIOS, 1):
        copy_corte = {
            "numero": idx,
            "id": c["id"],
            "tema": c["tema"],
            "versiculo": c["versiculo"],
            "youtube_16x9": {
                "titulo": c["titulo_youtube"],
                "descricao": f"""{c['titulo_youtube']}

📖 {c['versiculo']}

Trecho ministrado na Igreja Batista Palavra e Movimento (Culto de Celebração - 20/09/2026).
Se essa palavra tocou o seu coração, deixe seu like, inscreva-se no canal e envie para aquela pessoa que Deus colocou no seu coração agora!

👉 Assista à pregação completa no nosso canal!

#IBPM #{c['tema'].replace(' & ', '_').replace(' ', '_')} #PalavraDeDeus #Fe #Esperança #Jesus #Culto""",
                "tags": [c["id"].lower(), "ibpm", "corte", c["tema"].lower(), "palavra forte", "pregacao"]
            },
            "instagram_reels_9x16": {
                "headline_gancho": c["titulo_reels"],
                "copy_legenda": f"""{c['titulo_reels']}

Quantas vezes nós deixamos as circunstâncias definirem quem nós somos? Mas a Palavra do Senhor nos lembra:
📖 "{c['versiculo']}"

O tempo da vergonha acabou. Deus está soprando vida, restaurando identidades e levantando profetas de pé dentro das casas!

💬 Digite "AMÉM" se você recebe essa palavra no seu espírito hoje!
🚀 Envie esse vídeo no direct para quem precisa desse renovo agora.

.
.
.
#ibpm #palavradedeus #reelsfe #evangelho #fe #oracao #milagre #jesus #avivamento #palavraviva"""
            },
            "tiktok_9x16": {
                "titulo_gancho": c["titulo_tiktok"],
                "copy_tiktok": f"{c['titulo_tiktok']} 🙏🔥 Assista até o final e marque alguém! #ibpm #cristao #pregacao #fyp #foryou #fe #milagre"
            },
            "micro_short_tier1": {
                "duracao_alvo": "35s a 48s",
                "funil_cta": "Assista à mensagem completa no link do perfil / comentário fixado!"
            }
        }

        pacote_json["cortes_medios_tier2"].append(copy_corte)

        # Adiciona ao TXT de visualização amigável
        linhas_txt.extend([
            "=" * 80,
            f"[{idx:02d}/14] {c['id']} — {c['titulo_base'].upper()}",
            f"Tema: {c['tema']} | Versículo: {c['versiculo']}",
            "=" * 80,
            "📺 YOUTUBE 16:9:",
            f"TÍTULO: {copy_corte['youtube_16x9']['titulo']}",
            "DESCRIÇÃO:",
            copy_corte['youtube_16x9']['descricao'],
            "",
            "📱 INSTAGRAM REELS (9:16):",
            "LEGENDA / COPY:",
            copy_corte['instagram_reels_9x16']['copy_legenda'],
            "",
            "🎵 TIKTOK (9:16):",
            f"COPY: {copy_corte['tiktok_9x16']['copy_tiktok']}",
            "",
            "⚡ MICRO-SHORT ÁPICE (TIER 1 - 45s):",
            f"GANCHO: {c['titulo_reels']}",
            f"CTA FUNIL: {copy_corte['micro_short_tier1']['funil_cta']}",
            "\n"
        ])

    # Salva arquivos
    caminho_txt = DESKTOP_DIR / "00_COPIES_E_METADADOS_POSTAGEM.txt"
    caminho_json = DESKTOP_DIR / "00_COPIES_E_METADADOS_POSTAGEM.json"

    with open(caminho_txt, "w", encoding="utf-8") as f:
        f.write("\n".join(linhas_txt))

    with open(caminho_json, "w", encoding="utf-8") as f:
        json.dump(pacote_json, f, ensure_ascii=False, indent=2)

    print(f"✅ Catálogo de copies gerado com sucesso!")
    print(f"   📄 TXT:  {caminho_txt}")
    print(f"   📊 JSON: {caminho_json}")
    print("=" * 80)
    return caminho_txt, caminho_json

if __name__ == "__main__":
    gerar_catalogo_completo()
