"""
=============================================================================
GERADOR OFICIAL DE DECKS DO ANKI (.APKG) — 700 MAPAS DA COMPUTAÇÃO
=============================================================================
Gera baralhos oficiais do Anki (.apkg) com estilização CSS Sketchnote,
Active Recall nos 8 blocos cognitivos de cada mapa e sub-baralhos por escola.
=============================================================================
"""

import os
import sys
import json
import genanki
import random

if sys.platform == "win32":
    try:
        sys.stdout.reconfigure(encoding='utf-8', line_buffering=True)
        sys.stderr.reconfigure(encoding='utf-8', line_buffering=True)
    except Exception:
        pass

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
PASTA_ANKI = os.path.join(BASE_DIR, "anki_decks")
os.makedirs(PASTA_ANKI, exist_ok=True)

from organizar_acervo import ESCOLAS_CONFIG

# Modelo CSS Sketchnote para o Anki
CSS_SKETCHNOTE = """
.card {
    font-family: 'Segoe UI', -apple-system, BlinkMacSystemFont, Roboto, sans-serif;
    font-size: 16px;
    text-align: left;
    color: #0f172a;
    background-color: #faf8f5;
    padding: 24px;
    max-width: 650px;
    margin: 0 auto;
    border: 2px solid #e2e8f0;
    border-radius: 16px;
    box-shadow: 0 4px 12px rgba(0,0,0,0.05);
}

.school-tag {
    display: inline-block;
    font-size: 11px;
    font-weight: 700;
    text-transform: uppercase;
    letter-spacing: 1px;
    color: #64748b;
    margin-bottom: 8px;
}

.card-ribbon {
    background: #facc15;
    color: #0f172a;
    font-weight: 800;
    font-size: 20px;
    padding: 8px 16px;
    border-radius: 8px;
    display: inline-block;
    margin-bottom: 16px;
    box-shadow: 2px 3px 0px rgba(0,0,0,0.15);
}

.block-badge {
    display: inline-block;
    font-weight: 700;
    font-size: 13px;
    padding: 4px 10px;
    border-radius: 6px;
    margin-bottom: 12px;
}

.badge-idea { background: #fef08a; color: #854d0e; }
.badge-alert { background: #fee2e2; color: #991b1b; }
.badge-code { background: #ccfbf1; color: #115e59; }
.badge-flow { background: #dbeafe; color: #1e40af; }
.badge-summary { background: #f3e8ff; color: #6b21a8; }

.question {
    font-size: 18px;
    font-weight: 600;
    line-height: 1.4;
    color: #1e293b;
    margin-bottom: 16px;
}

.divider {
    border: none;
    border-top: 2px dashed #cbd5e1;
    margin: 16px 0;
}

.definition-box {
    background: #ffffff;
    border-left: 4px solid #3b82f6;
    padding: 12px 16px;
    border-radius: 0 8px 8px 0;
    font-size: 15px;
    color: #334155;
    margin-bottom: 14px;
}

.bullet-item {
    margin: 8px 0;
    line-height: 1.5;
    position: relative;
    padding-left: 20px;
}

.bullet-item:before {
    content: "➔";
    position: absolute;
    left: 0;
    color: #eab308;
    font-weight: bold;
}

.tip-box {
    background: #f8fafc;
    border: 1px solid #e2e8f0;
    padding: 10px 14px;
    border-radius: 8px;
    font-size: 13px;
    color: #64748b;
    margin-top: 16px;
}
"""

# Modelo de Cartão Genanki
MODEL_ID = 1607392319
CARD_MODEL = genanki.Model(
    MODEL_ID,
    'DevSketch Sketchnote Card',
    fields=[
        {'name': 'Escola'},
        {'name': 'Tema'},
        {'name': 'Bloco'},
        {'name': 'BadgeClasse'},
        {'name': 'Pergunta'},
        {'name': 'Definicao'},
        {'name': 'RespostaHTML'},
        {'name': 'Dica'},
    ],
    templates=[
        {
            'name': 'Active Recall Card',
            'qfmt': """
<div class="card">
    <div class="school-tag">{{Escola}}</div><br/>
    <div class="card-ribbon">{{Tema}}</div>
    <div><span class="block-badge {{BadgeClasse}}">{{Bloco}}</span></div>
    <div class="question">{{Pergunta}}</div>
</div>
""",
            'afmt': """
<div class="card">
    <div class="school-tag">{{Escola}}</div><br/>
    <div class="card-ribbon">{{Tema}}</div>
    <div><span class="block-badge {{BadgeClasse}}">{{Bloco}}</span></div>
    <div class="question">{{Pergunta}}</div>
    
    <hr class="divider"/>
    
    <div class="definition-box">
        <strong>Conceito Chave:</strong> {{Definicao}}
    </div>
    
    <div class="answers">
        {{RespostaHTML}}
    </div>
    
    <div class="tip-box">
        💡 <strong>Metodologia Feynman:</strong> Se você não consegue explicar isso em 30 segundos com palavras simples, revise o mapa mental ilustrado!
    </div>
</div>
""",
        },
    ],
    css=CSS_SKETCHNOTE
)

def gerar_cartoes_do_mapa(dados: dict, nome_escola: str):
    """Gera de 2 a 4 cartões de alto valor cognitivo para cada mapa mental."""
    cartoes = []
    tema = dados.get("title", "Tópico de Computação").upper()
    definicao = dados.get("definition", "")

    # Cartão 1: Conceito Central & Onde é Usado
    tl = dados.get("topLeft", {})
    br = dados.get("bottomRight", {})
    bullets_tl = "".join([f'<div class="bullet-item">{b}</div>' for b in tl.get("bullets", [])])
    bullets_br = "".join([f'<div class="bullet-item">{b}</div>' for b in br.get("bullets", [])])
    
    html_resp1 = f"""
    <strong>{tl.get('pill', 'IDEIA CENTRAL')}:</strong>
    {bullets_tl}
    <br/>
    <strong>{br.get('pill', 'ONDE É USADO / APLICAÇÃO')}:</strong>
    {bullets_br}
    """
    cartoes.append(genanki.Note(
        model=CARD_MODEL,
        fields=[
            nome_escola,
            tema,
            "💡 IDEIA CENTRAL & APLICAÇÃO",
            "badge-idea",
            f"Qual a essência de <strong>{tema}</strong> e onde isso é aplicado na prática?",
            definicao,
            html_resp1,
            ""
        ]
    ))

    # Cartão 2: Pegadinhas Comuns & Armadilhas de Código (Vital para Entrevistas / Concursos)
    bl = dados.get("bottomLeft", {})
    bullets_bl = "".join([f'<div class="bullet-item">{b}</div>' for b in bl.get("bullets", [])])
    if bullets_bl:
        cartoes.append(genanki.Note(
            model=CARD_MODEL,
            fields=[
                nome_escola,
                tema,
                "⚠️ PEGADINHA / ERRO CLÁSSICO",
                "badge-alert",
                f"Quais são as principais <strong>pegadinhas e erros clássicos</strong> que muitos cometem ao lidar com <strong>{tema}</strong>?",
                definicao,
                bullets_bl,
                ""
            ]
        ))

    # Cartão 3: Regra Prática ou Fluxo de Execução
    mr = dados.get("midRight", {})
    bc = dados.get("bottomCenter", {})
    bullets_pratica = "".join([f'<div class="bullet-item">{b}</div>' for b in mr.get("bullets", []) + bc.get("bullets", [])])
    if bullets_pratica:
        cartoes.append(genanki.Note(
            model=CARD_MODEL,
            fields=[
                nome_escola,
                tema,
                "⚙️ FLUXO & REGRA PRÁTICA",
                "badge-flow",
                f"Qual é o <strong>fluxo passo a passo</strong> ou a regra de código para implementar <strong>{tema}</strong>?",
                definicao,
                bullets_pratica,
                ""
            ]
        ))

    return cartoes

def gerar_todos_os_decks():
    print("=" * 70, flush=True)
    print("🚀 GERANDO BARALHOS OFICIAIS DO ANKI (.APKG) PARA AS 8 ESCOLAS", flush=True)
    print("=" * 70, flush=True)

    # Deck Master com todas as 700 matérias
    deck_master_id = 2026091701
    deck_master = genanki.Deck(deck_master_id, "DevSketch :: 700 Mapas Mentais da Computação (Master)")

    total_cartoes_geral = 0
    decks_individuais = []

    for idx, esc in enumerate(ESCOLAS_CONFIG, 1):
        pasta = esc["pasta"]
        nome = esc["nome"]
        deck_id = 2026091700 + idx
        deck_escola = genanki.Deck(deck_id, f"DevSketch :: {nome}")

        pasta_json = os.path.join(BASE_DIR, pasta, "json")
        if not os.path.exists(pasta_json):
            continue

        arquivos_json = sorted([f for f in os.listdir(pasta_json) if f.endswith(".json")])
        cartoes_escola = 0

        for arq in arquivos_json:
            caminho_arq = os.path.join(pasta_json, arq)
            with open(caminho_arq, "r", encoding="utf-8") as f:
                dados = json.load(f)
            
            notas = gerar_cartoes_do_mapa(dados, nome)
            for nota in notas:
                deck_escola.add_note(nota)
                deck_master.add_note(nota)
                cartoes_escola += 1

        total_cartoes_geral += cartoes_escola
        saida_apkg = os.path.join(PASTA_ANKI, f"{pasta}.apkg")
        genanki.Package(deck_escola).write_to_file(saida_apkg)
        tam_kb = os.path.getsize(saida_apkg) / 1024
        print(f"[{idx}/8] ✅ {nome[:38]:<40} -> {cartoes_escola} cartões | {tam_kb:.1f} KB (.apkg)", flush=True)

    # Salva o Master Deck Geral
    master_apkg = os.path.join(PASTA_ANKI, "DevSketch_700_Mapas_Mentais_COMPLETO.apkg")
    genanki.Package(deck_master).write_to_file(master_apkg)
    tam_master_mb = os.path.getsize(master_apkg) / (1024 * 1024)

    print("\n" + "=" * 70, flush=True)
    print(f"🏆 TODOS OS DECKS DO ANKI FORAM GERADOS COM SUCESSO!", flush=True)
    print(f"📊 Total de Flashcards Atômicos Criados: {total_cartoes_geral} cartões!", flush=True)
    print(f"📦 Master Deck Unificado: {master_apkg} ({tam_master_mb:.2f} MB)", flush=True)
    print("=" * 70, flush=True)

if __name__ == "__main__":
    gerar_todos_os_decks()
