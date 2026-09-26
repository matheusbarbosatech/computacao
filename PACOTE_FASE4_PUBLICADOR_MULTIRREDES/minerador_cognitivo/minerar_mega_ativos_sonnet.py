#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
MINERADOR PATRIMONIAL DE ATIVOS — CLAUDE SONNET 5 (1M CONTEXTO)
IBPM CR Automation System — Extração em Lote dos 20 Ativos Teológicos

Processa o acervo de 460 transcrições neurais da IBPM e extrai via Sonnet 5:
1. 📖 Devocionais Diários ("365 Dias no Altar") com versículo, reflexão e oração.
2. 👥 Roteiros de Célula / Pequenos Grupos (Quebra-gelo, estudo, perguntas e desafio).
3. 🔥 Frases Proféticas categorizadas por sentimentos (Ansiedade, Luto, Vitória, Identidade).
4. 💡 Esboços Homiléticos e Comentários Bíblicos.

Persiste em:
- data/ativos_minerados/
- C:\\Users\\matheus\\Desktop\\SEEDS_APP_IBPMCR\\
"""

import os
import sys
import json
import time
import argparse
import urllib.request
from pathlib import Path

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
if hasattr(sys.stderr, "reconfigure"):
    sys.stderr.reconfigure(encoding="utf-8", errors="replace")

BASE_DIR = Path(__file__).resolve().parent.parent.parent
TRANSCRICOES_DIR = BASE_DIR / "data" / "fase1_mapeamento" / "transcriptions" / "json"
OUT_BASE = BASE_DIR / "data" / "ativos_minerados"
OUT_BASE.mkdir(parents=True, exist_ok=True)

DESKTOP_DIR = Path.home() / "Desktop" / "SEEDS_APP_IBPMCR"
DESKTOP_DIR.mkdir(parents=True, exist_ok=True)

DEVOCIONAIS_DIR = OUT_BASE / "devocionais"
CELULAS_DIR = OUT_BASE / "celulas"
FRASES_DIR = OUT_BASE / "frases_profeticas"

for d in [DEVOCIONAIS_DIR, CELULAS_DIR, FRASES_DIR]:
    d.mkdir(parents=True, exist_ok=True)

CHECKPOINT_FILE = OUT_BASE / "checkpoint_mineracao.json"

# API DevWorld Sonnet 5
API_URL = "https://chat.devwservices.shop/v1/chat/completions"
API_KEY = "dw_live_UgEYtrkRzOvCU-BV-IR8TvAzKBdsHoEnIROAq0OthLU"
MODEL = "claude-sonnet-5[1m]"


def carregar_checkpoint() -> set:
    if CHECKPOINT_FILE.exists():
        try:
            with open(CHECKPOINT_FILE, "r", encoding="utf-8") as f:
                return set(json.load(f))
        except Exception:
            return set()
    return set()


def salvar_checkpoint(processados: set):
    with open(CHECKPOINT_FILE, "w", encoding="utf-8") as f:
        json.dump(list(processados), f, indent=2)


def chamar_sonnet(prompt_sistema: str, prompt_usuario: str, max_tokens: int = 3500) -> str:
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {API_KEY}"
    }
    payload = {
        "model": MODEL,
        "temperature": 0.25,
        "max_tokens": max_tokens,
        "messages": [
            {"role": "system", "content": prompt_sistema},
            {"role": "user", "content": prompt_usuario}
        ]
    }
    req = urllib.request.Request(API_URL, data=json.dumps(payload).encode("utf-8"), headers=headers)
    for tentativa in range(4):
        try:
            with urllib.request.urlopen(req, timeout=120) as response:
                res_data = json.loads(response.read().decode("utf-8"))
                return res_data["choices"][0]["message"]["content"]
        except Exception as e:
            espera = 6 * (tentativa + 1)
            print(f"   ⚠️ Tentativa {tentativa+1}/4 falhou ({e}). Aguardando {espera}s...")
            time.sleep(espera)
    return None


PROMPT_SISTEMA = """Você é o Teólogo Assistente Sênior e Especialista em Conteúdo Editorial da Igreja Batista Palavra e Movimento (IBPM Campo Grande).
Sua missão é ler a transcrição completa de uma pregação e minerar com fidelidade espiritual e excelente português os seguintes 4 ativos estruturados no formato JSON estrito:

{
  "devocional": {
    "titulo": "Título inspirador de até 8 palavras",
    "versiculo_chave": "Livro X:Y",
    "texto_versiculo": "Texto bíblico citado",
    "reflexao": "Texto devocional fluente e profundo de 200 a 250 palavras baseado nas falas do pastor.",
    "oracao_do_dia": "Oração dirigida de 3 a 4 linhas."
  },
  "roteiro_celula": {
    "tema": "Tema de estudo para o Pequeno Grupo",
    "versiculo_base": "Referência bíblica",
    "quebra_gelo": "Pergunta dinâmica para iniciar a conversa descontraída (1 a 2 linhas)",
    "estudo_topicos": [
      {"titulo": "Ponto 1", "explicacao": "Explicação teológica prática"},
      {"titulo": "Ponto 2", "explicacao": "Explicação teológica prática"},
      {"titulo": "Ponto 3", "explicacao": "Explicação teológica prática"}
    ],
    "perguntas_aplicacao": [
      "Pergunta 1 reflexiva para o dia a dia",
      "Pergunta 2 sobre vida prática e fé"
    ],
    "desafio_semana": "Ação prática individual para a semana"
  },
  "frases_profeticas": [
    {"frase": "Frase de impacto curta e declaratória dita pelo pastor", "sentimento": "Identidade / Guerra Espiritual"},
    {"frase": "Frase de impacto curta", "sentimento": "Consolo no Luto / Dor"},
    {"frase": "Frase de impacto curta", "sentimento": "Fé / Provisão"},
    {"frase": "Frase de impacto curta", "sentimento": "Esperança / Recomeço"}
  ]
}

Responda APENAS o JSON puro, sem blocos de código markdown, sem texto antes ou depois."""


def extrair_texto_transcricao(json_path: Path) -> str:
    with open(json_path, "r", encoding="utf-8") as f:
        data = json.load(f)

    # Suporte tanto a formato Deepgram segments quanto words ou full_transcript
    if "segments" in data:
        textos = [s.get("text", "") for s in data["segments"]]
        return " ".join(textos)
    elif "results" in data and "channels" in data["results"]:
        ch = data["results"]["channels"][0]
        return ch["alternatives"][0].get("transcript", "")
    elif "text" in data:
        return data["text"]
    return ""


def processar_culto(json_path: Path):
    culto_id = json_path.stem
    print(f"\n⚡ Processando Culto: {culto_id}...")

    texto = extrair_texto_transcricao(json_path)
    if len(texto) < 500:
        print(f"   ⚠️ Transcrição muito curta ou vazia ({len(texto)} caracteres). Pulando.")
        return None

    # Reduz para os 25.000 caracteres mais densos da pregação para agilizar a API
    trecho_analise = texto[:28000]

    t0 = time.time()
    prompt_usuario = f"Pregação do Culto IBPM: {culto_id}\n\nTranscrição:\n{trecho_analise}"
    resposta_ia = chamar_sonnet(PROMPT_SISTEMA, prompt_usuario)

    if not resposta_ia:
        print(f"   ❌ Falha ao obter resposta do Sonnet 5.")
        return None

    dados_minerados = reparar_e_carregar_json(resposta_ia)

    # Salva arquivos individuais
    arquivo_devocional = DEVOCIONAIS_DIR / f"{culto_id}_devocional.json"
    with open(arquivo_devocional, "w", encoding="utf-8") as f:
        json.dump(dados_minerados.get("devocional", {}), f, indent=2, ensure_ascii=False)

    arquivo_celula = CELULAS_DIR / f"{culto_id}_celula.json"
    with open(arquivo_celula, "w", encoding="utf-8") as f:
        json.dump(dados_minerados.get("roteiro_celula", {}), f, indent=2, ensure_ascii=False)

    arquivo_frases = FRASES_DIR / f"{culto_id}_frases.json"
    with open(arquivo_frases, "w", encoding="utf-8") as f:
        json.dump(dados_minerados.get("frases_profeticas", []), f, indent=2, ensure_ascii=False)

    print(f"   ✅ [OK em {time.time()-t0:.1f}s] Devocional, Roteiro de Célula e Frases minerados com sucesso!")
    return dados_minerados


def reparar_e_carregar_json(raw_text: str) -> dict:
    import re
    s = raw_text.strip()
    if s.startswith("```json"):
        s = s[7:]
    if s.startswith("```"):
        s = s[3:]
    if s.endswith("```"):
        s = s[:-3]
    s = s.strip()

    start = s.find('{')
    end = s.rfind('}')
    if start != -1 and end != -1:
        s = s[start:end+1]

    try:
        return json.loads(s)
    except Exception:
        pass

    # Limpeza de vírgulas trailing
    s_fixed = re.sub(r',\s*([}\]])', r'\1', s)
    try:
        return json.loads(s_fixed)
    except Exception:
        pass

    # Extração de emergência por regex dos blocos principais
    res = {"devocional": {}, "roteiro_celula": {}, "frases_profeticas": []}
    m_dev = re.search(r'"devocional"\s*:\s*(\{.*?\})\s*,\s*"roteiro_celula"', s, re.DOTALL)
    if m_dev:
        try:
            res["devocional"] = json.loads(re.sub(r',\s*([}\]])', r'\1', m_dev.group(1)))
        except Exception:
            pass

    m_cel = re.search(r'"roteiro_celula"\s*:\s*(\{.*?\})\s*,\s*"frases_profeticas"', s, re.DOTALL)
    if m_cel:
        try:
            res["roteiro_celula"] = json.loads(re.sub(r',\s*([}\]])', r'\1', m_cel.group(1)))
        except Exception:
            pass

    m_fra = re.search(r'"frases_profeticas"\s*:\s*(\[.*?\])\s*\}', s, re.DOTALL)
    if m_fra:
        try:
            res["frases_profeticas"] = json.loads(re.sub(r',\s*([}\]])', r'\1', m_fra.group(1)))
        except Exception:
            pass

    if not res["devocional"] and not res["roteiro_celula"]:
        return {"raw_response": raw_text}
    return res


def compilar_seeds_master():
    """
    Agrupa todos os devocionais, células e frases minerados em arquivos master para o app e banco de dados.
    """
    print("\n📦 Compilando Seeds Master para o Super-App IBPM CR...")
    
    todos_devocionais = []
    todos_roteiros = []
    todas_frases = []
    
    # 1. Devocionais
    for f in sorted(list(DEVOCIONAIS_DIR.glob("*.json"))):
        try:
            with open(f, "r", encoding="utf-8") as dev_f:
                c = json.load(dev_f)
                if c and isinstance(c, dict) and "titulo" in c:
                    c["culto_origem"] = f.stem.replace("_devocional", "")
                    todos_devocionais.append(c)
        except Exception:
            pass

    # 2. Células
    for f in sorted(list(CELULAS_DIR.glob("*.json"))):
        try:
            with open(f, "r", encoding="utf-8") as cel_f:
                c = json.load(cel_f)
                if c and isinstance(c, dict) and "tema" in c:
                    c["culto_origem"] = f.stem.replace("_celula", "")
                    todos_roteiros.append(c)
        except Exception:
            pass

    # 3. Frases Proféticas
    for f in sorted(list(FRASES_DIR.glob("*.json"))):
        try:
            with open(f, "r", encoding="utf-8") as fra_f:
                c = json.load(fra_f)
                if c and isinstance(c, list):
                    for item in c:
                        item["culto_origem"] = f.stem.replace("_frases", "")
                        todas_frases.append(item)
        except Exception:
            pass

    # Salva master no Desktop
    seed_dev = DESKTOP_DIR / "DEVOCIONAIS_365_MASTER.json"
    with open(seed_dev, "w", encoding="utf-8") as f:
        json.dump(todos_devocionais, f, indent=2, ensure_ascii=False)

    seed_cel = DESKTOP_DIR / "ROTEIROS_CELULA_MASTER.json"
    with open(seed_cel, "w", encoding="utf-8") as f:
        json.dump(todos_roteiros, f, indent=2, ensure_ascii=False)

    seed_fra = DESKTOP_DIR / "FRASES_PROFETICAS_MASTER.json"
    with open(seed_fra, "w", encoding="utf-8") as f:
        json.dump(todas_frases, f, indent=2, ensure_ascii=False)

    print(f"   📖 Devocionais compilados: {len(todos_devocionais)} -> {seed_dev.name}")
    print(f"   👥 Roteiros de Célula compilados: {len(todos_roteiros)} -> {seed_cel.name}")
    print(f"   🔥 Frases Proféticas compiladas: {len(todas_frases)} -> {seed_fra.name}")


def main():
    parser = argparse.ArgumentParser(description="Minerador de Ativos Teológicos via Claude Sonnet 5")
    parser.add_argument("--limite", type=int, default=5, help="Quantidade máxima de cultos a minerar nesta rodada (padrão: 5)")
    parser.add_argument("--todos", action="store_true", help="Processa todos os cultos pendentes sem limite")
    parser.add_argument("--apenas-culto", type=str, default=None, help="Processa apenas um culto específico (ex: 459)")
    parser.add_argument("--compilar", action="store_true", help="Apenas compila os seeds existentes")
    args = parser.parse_args()

    if args.compilar:
        compilar_seeds_master()
        return

    arquivos = sorted(list(TRANSCRICOES_DIR.glob("*.json")))
    print("=" * 80)
    print("💎 MINERADOR PATRIMONIAL DE ATIVOS — CLAUDE SONNET 5 (1M CONTEXTO)")
    print(f"   Total de Transcrições Disponíveis no SSD: {len(arquivos)} cultos")
    print(f"   Modelo IA: {MODEL}")
    print("=" * 80)

    checkpoint = carregar_checkpoint()
    print(f"ℹ️ Cultos já processados em rodadas anteriores: {len(checkpoint)}")

    if args.apenas_culto:
        arquivos_para_rodar = [f for f in arquivos if args.apenas_culto in f.name]
    else:
        # Prioriza os cultos mais recentes (2026/2025) que ainda não estão no checkpoint
        arquivos_pendentes = [f for f in arquivos if f.stem not in checkpoint]
        arquivos_pendentes.sort(key=lambda x: x.name, reverse=True)
        arquivos_para_rodar = arquivos_pendentes if args.todos else arquivos_pendentes[:args.limite]

    print(f"🚀 Cultos a processar nesta rodada: {len(arquivos_para_rodar)}")

    processados_agora = 0
    for i, arq in enumerate(arquivos_para_rodar):
        print(f"\n[{i+1}/{len(arquivos_para_rodar)}] Processando arquivo: {arq.name}...")
        res = processar_culto(arq)
        if res:
            checkpoint.add(arq.stem)
            salvar_checkpoint(checkpoint)
            processados_agora += 1
            # A cada 10 cultos minerados, atualiza automaticamente os Masters no Desktop
            if processados_agora % 10 == 0:
                print(f"\n🔄 Checkpoint automático ({processados_agora} novos cultos): Atualizando Masters no Desktop...")
                compilar_seeds_master()
            # Pausa de 8s para respeitar a taxa da API Sonnet 5
            time.sleep(8)

    compilar_seeds_master()
    print(f"\n🎉 Rodada concluída com sucesso! {processados_agora} novos cultos minerados.")


if __name__ == "__main__":
    main()
