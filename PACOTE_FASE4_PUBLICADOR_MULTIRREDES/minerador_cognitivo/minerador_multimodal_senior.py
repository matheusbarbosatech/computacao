#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
MINERADOR MULTIMODAL SÊNIOR (ÁUDIO REAL + VAD + QWEN 3.8 MAX)
IBPM CR Automation System - Fase 2 Multimodal

Arquitetura Multimodal Real:
1. Extração de energia acústica RMS (isola clímax e autoridade vocal).
2. Segmentação por respiração VAD (fronteiras naturais de silêncio > 0.45s).
3. Curadoria Semântica via Qwen 3.8 Max (DevWorld ilimitado/gratuito).
4. Timestamps 100% amarrados nos blocos físicos (Zero 0.0s, Zero sílabas cortadas).
"""

import os
import sys
import json
import time
import requests
import numpy as np
from pathlib import Path
from typing import List, Dict, Any, Optional
from dotenv import load_dotenv

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace", line_buffering=True)
if hasattr(sys.stderr, "reconfigure"):
    sys.stderr.reconfigure(encoding="utf-8", errors="replace", line_buffering=True)

BASE_DIR = Path(__file__).resolve().parent.parent.parent
sys.path.append(str(BASE_DIR))
load_dotenv(BASE_DIR / ".env")

from src.services.audio_energy_analyzer import AudioEnergyAnalyzer

# Configurações de API
DEVWORLD_KEY = os.getenv("DEVWORLD_API_KEY")
DEVWORLD_URL = f"{os.getenv('DEVWORLD_BASE_URL', 'https://chat.devwservices.shop/v1')}/chat/completions"
DEVWORLD_MODEL = os.getenv("DEVWORLD_MODEL", "devworld/qwen3.8-max-f")
DEVWORLD_FALLBACK = os.getenv("DEVWORLD_FALLBACK_MODEL", "devworld/kimi-k3-f")

AUDIOS_DIR = Path(r"Z:\data\fase1_mapeamento\audios")
TRANSCRICOES_DIR = BASE_DIR / "data" / "fase1_mapeamento" / "transcriptions" / "json"
OUTPUT_CORTES_DIR = BASE_DIR / "data" / "fase2_mineracao" / "cortes_por_culto"
OUTPUT_CORTES_DIR.mkdir(parents=True, exist_ok=True)


SYSTEM_PROMPT_MULTIMODAL = """Você é o Diretor Editorial e Editor Sênior de Redes Sociais da Igreja Batista Palavra e Movimento (IBPM).
Sua missão é extrair cortes virais de altíssimo impacto (TikTok, Instagram Reels, YouTube Shorts) e mensagens profundas (YouTube longo) a partir de blocos sintáticos de pregação pré-avaliados com ÁUDIO REAL e ENERGIA ACÚSTICA.

VOCÊ RECEBERÁ:
Uma lista numerada de blocos de fala de um culto, cada um com:
- bloco_id: número identificador
- duracao_sec: duração do bloco
- nivel_energia: 'CLIMAX_ALTA' (o pastor elevou a voz / ápice), 'MEDIA_CONSTANTE' ou 'BAIXA_CALMA'
- texto: o que o orador falou

SUAS REGRAS INEGOCIÁVEIS:
1. ESCOLHA APENAS BLOCOS COM ENERGIA E SENTIDO COMPLETO:
   - Priorize blocos com nivel_energia 'CLIMAX_ALTA' ou 'MEDIA_CONSTANTE'.
   - O corte DEVE conter um arco completo: Gancho forte nos primeiros 3s + Tese/Confronto/Ilustração + Punchline conclusiva.
2. LIMITES DE TEMPO RÍGIDOS:
   - TIER 1 (Shorts Verticais): Duração total entre 25 e 80 segundos (pode ser 1 bloco ou a união de 2 blocos consecutivos contíguos). NUNCA ultrapasse 85 segundos!
   - TIER 2 (Vídeos Médios): Duração entre 120 e 300 segundos (2 a 5 minutos) para parábolas inteiras, ministrações ou orações profundas.
   - TIER 3 (A Pregação Completa para YouTube): Duração contínua entre 1800 e 3600 segundos (30 a 60 minutos, ou todo o tempo da ministração da Palavra). Exatamente 1 por culto cobrindo o sermão na íntegra: começa quando o pregador assume o púlpito e abre a Bíblia, e termina na oração e apelo final.
3. QUANTIDADE POR CULTO:
   - De 3 a 5 Shorts Tier 1 de altíssimo impacto.
   - De 1 a 2 Vídeos Médios Tier 2.
   - Exatamente 1 Pregação Completa Tier 3.
4. NUNCA INVENTE TIMESTAMPS:
   - Você DEVE referenciar os blocos exatos pelos seus campos 'bloco_inicio_id' e 'bloco_fim_id' (se for 1 bloco só, ambos são iguais).

RESPONDA EXCLUSIVAMENTE UM OBJETO JSON VÁLIDO no seguinte formato:
{
  "culto_id": 439,
  "tema_geral_sermão": "Título temático do sermão",
  "cortes_tier1_shorts": [
    {
      "bloco_inicio_id": 153,
      "bloco_fim_id": 153,
      "titulo_viral": "TÍTULO VIRAL EM MAIÚSCULAS (SEM EMOJI)",
      "arquetipo": "Confronto Profético | Quebra de Padrão | Quebrantamento | Revelação Teológica",
      "gancho_primeiros_3s": "Descrição do que prende o espectador nos primeiros 3 segundos",
      "punchline_final": "A frase exata de encerramento do corte",
      "nota_viral": 95,
      "motivo_escolha": "Por que este trecho acústico é magnético"
    }
  ],
  "cortes_tier2_medios": [
    {
      "bloco_inicio_id": 140,
      "bloco_fim_id": 143,
      "titulo_devocional": "TÍTULO DO ESTUDO OU HISTÓRIA COMPLETA",
      "tema": "Tema central abordado",
      "resumo_narrativa": "Resumo em 2 linhas da reflexão",
      "punchline_final": "Frase de impacto final"
    }
  ],
  "corte_tier3_tematico": {
    "bloco_inicio_id": 40,
    "bloco_fim_id": 65,
    "titulo_estudo_youtube": "TÍTULO FORTE PARA BUSCA NO YOUTUBE",
    "tema_central": "Tese teológica e aplicação prática da mensagem",
    "nome_playlist_sugerida": "Série: Nome da Playlist Temática Recomendada",
    "resumo_estudo": "Sinopse completa de 3 a 5 linhas para a descrição do YouTube",
    "tags_youtube": ["pregação ibpm", "tema central", "estudo bíblico", "palavra de deus", "fé"]
  }
}
"""


GROQ_KEY = os.getenv("GROQ_API_KEY")


def chamar_llm_devworld(prompt_usuario: str, model_name: str = DEVWORLD_MODEL) -> dict:
    """Faz chamada na API da DevWorld com retries e fallback automático (incluindo Groq Qwen 3.8)."""
    candidatos_devworld = ["devworld/qwen3.8-max-f", "devworld/gemini-3.7-flash-f", "devworld/kimi-k3-f"]
    if model_name in candidatos_devworld:
        candidatos_devworld.remove(model_name)
        candidatos_devworld.insert(0, model_name)

    headers_devworld = {
        "Authorization": f"Bearer {DEVWORLD_KEY}",
        "Content-Type": "application/json"
    }

    # 1. Tenta provedor primário DevWorld com timeout ágil de 8s para não reter a esteira
    for modelo in candidatos_devworld[:2]:
        payload = {
            "model": modelo,
            "messages": [
                {"role": "system", "content": SYSTEM_PROMPT_MULTIMODAL},
                {"role": "user", "content": prompt_usuario}
            ],
            "temperature": 0.2,
            "max_tokens": 3000
        }

        try:
            print(f"   [API DevWorld] Chamando {modelo} (timeout 8s)...")
            r = requests.post(DEVWORLD_URL, headers=headers_devworld, json=payload, timeout=8)
            if r.status_code == 200:
                resp_json = r.json()
                msg = resp_json["choices"][0]["message"]
                raw_text = (msg.get("content") or "").strip()
                
                if not raw_text:
                    print(f"⚠️ {modelo} retornou conteúdo vazio, tentando próximo...")
                    continue

                clean_text = raw_text
                if "```" in clean_text:
                    parts = clean_text.split("```")
                    for part in parts:
                        p = part.strip()
                        if p.startswith("json"):
                            p = p[4:].strip()
                        if p.startswith("{") and p.endswith("}"):
                            clean_text = p
                            break
                if "{" in clean_text and "}" in clean_text:
                    ini = clean_text.find("{")
                    fim = clean_text.rfind("}") + 1
                    clean_text = clean_text[ini:fim]

                dados = json.loads(clean_text)
                print(f"   --> Sucesso com {modelo}!")
                return dados
            else:
                print(f"⚠️ Aviso {modelo} (Status {r.status_code}): {r.text[:80]}")
        except Exception as e:
            print(f"⚠️ Aviso com {modelo}: {e}")

    # 2. Fallback de Alta Resiliência: Groq (Qwen 3.8 / GPT-OSS 120B) (Zero Custo, Instantâneo)
    if GROQ_KEY:
        print("⚡ [FALLBACK RESILIENTE] Ativando IA via Groq (Custo R$ 0, Resposta Instantânea)...")
        headers_groq = {
            "Authorization": f"Bearer {GROQ_KEY}",
            "Content-Type": "application/json"
        }
        modelos_groq = ["qwen/qwen3.8-27b", "openai/gpt-oss-120b"]
        for m_groq in modelos_groq:
            payload_groq = {
                "model": m_groq,
                "messages": [
                    {"role": "system", "content": SYSTEM_PROMPT_MULTIMODAL},
                    {"role": "user", "content": prompt_usuario}
                ],
                "response_format": {"type": "json_object"},
                "max_tokens": 3000,
                "temperature": 0.2
            }
            for tent_groq in range(2):
                try:
                    r_groq = requests.post("https://api.groq.com/openai/v1/chat/completions", headers=headers_groq, json=payload_groq, timeout=30)
                    if r_groq.status_code == 200:
                        raw = r_groq.json()["choices"][0]["message"]["content"].strip()
                        clean = raw
                        if "```" in clean:
                            parts = clean.split("```")
                            for part in parts:
                                p = part.strip()
                                if p.startswith("json"):
                                    p = p[4:].strip()
                                if p.startswith("{") and p.endswith("}"):
                                    clean = p
                                    break
                        if "{" in clean and "}" in clean:
                            ini = clean.find("{")
                            fim = clean.rfind("}") + 1
                            clean = clean[ini:fim]
                        dados = json.loads(clean)
                        print(f"   --> Sucesso com {m_groq} via Groq!")
                        return dados
                    else:
                        print(f"⚠️ Aviso Groq {m_groq} (Status {r_groq.status_code}): {r_groq.text[:80]}")
                        time.sleep(1)
                except Exception as e:
                    print(f"⚠️ Erro Groq {m_groq} tentativa {tent_groq+1}: {e}")
                    time.sleep(1)

    raise RuntimeError("Nenhum modelo (DevWorld ou Groq) conseguiu responder a requisição.")



def carregar_palavras_deepgram(json_path: Path) -> List[Dict[str, Any]]:
    """Carrega palavras desduplicadas da transcrição Deepgram."""
    with open(json_path, "r", encoding="utf-8") as f:
        data = json.load(f)

    segs = data.get("segments", [])
    unique_segs = {}
    for s in segs:
        key = (round(float(s.get("start", 0)), 2), round(float(s.get("end", 0)), 2))
        unique_segs[key] = s

    sorted_segs = sorted(unique_segs.values(), key=lambda x: float(x.get("start", 0)))
    words = []
    seen = set()
    for s in sorted_segs:
        for w in s.get("words", []):
            if w.get("word"):
                st = float(w.get("start", 0.0))
                en = float(w.get("end", 0.0))
                key = (w["word"].strip().lower(), round(st, 2))
                if key not in seen:
                    seen.add(key)
                    words.append({
                        "word": w["word"].strip(),
                        "start": st,
                        "end": en
                    })
    return sorted(words, key=lambda x: x["start"])


def minerar_culto_multimodal(culto_id: int, audio_file: Optional[Path] = None) -> Path:
    """Executa o pipeline completo de mineração multimodal em 1 culto."""
    print("\n" + "=" * 75)
    print(f"🚀 INICIANDO MINERAÇÃO MULTIMODAL SÊNIOR — CULTO {culto_id}")
    print(f"🧠 Modelo Ativo: {DEVWORLD_MODEL} (Gratuito e Ilimitado)")
    print("=" * 75)

    # 1. Localiza áudio (com fallback direto para vídeo se necessário)
    pad_id = f"{culto_id:03d}_"
    if not audio_file:
        matches = list(AUDIOS_DIR.glob(f"*{pad_id}*.mp3")) + list(AUDIOS_DIR.glob(f"{culto_id}_*.mp3"))
        if matches:
            audio_file = matches[0]
        else:
            from scripts.fase3_render.renderizar_aprovados_multimodal import localizar_video_culto
            try:
                audio_file = localizar_video_culto(culto_id)
                print(f"⚡ [ÁUDIO FALLBACK] Usando mídia de vídeo para análise acústica: {audio_file.name}")
            except Exception as e:
                raise FileNotFoundError(f"Áudio ou vídeo do culto {culto_id} não encontrado: {e}")

    # 2. Localiza transcrição
    transcricoes = list(TRANSCRICOES_DIR.glob(f"*{pad_id}*.json")) + list(TRANSCRICOES_DIR.glob(f"{culto_id}_*.json"))
    if not transcricoes:
        raise FileNotFoundError(f"Transcrição do culto {culto_id} não encontrada em {TRANSCRICOES_DIR}")
    transcricao_path = transcricoes[0]

    # 3. Análise Acústica (RMS + VAD com Cache)
    t0 = time.time()
    analyzer = AudioEnergyAnalyzer(sample_rate=16000, window_sec=1.0)
    cache_energy = BASE_DIR / "scratch" / f"energy_profile_{culto_id}.npy"

    if cache_energy.exists():
        print(f"⚡ [CACHE] Carregando perfil de energia acústica de: {cache_energy.name}...")
        energy_profile = np.load(cache_energy)
    else:
        print(f"🎙️ [1/4] Extraindo perfil acústico RMS de: {audio_file.name}...")
        energy_profile = analyzer.extract_rms_profile(audio_file)
        np.save(cache_energy, energy_profile)
        print(f"   --> Perfil de energia acústica gerado e salvo em cache ({len(energy_profile)} segundos mapeados)")

    # 4. Fatiamento por Respiração
    print("✂️ [2/4] Fatiando transcrição por pausas naturais de respiração (VAD)...")
    words = carregar_palavras_deepgram(transcricao_path)
    raw_blocks = analyzer.segmentar_transcricao_por_respiracao(words, min_block_sec=25.0, max_block_sec=75.0, min_silence_gap=0.45)
    enriched_blocks = analyzer.enriquecer_blocos_com_energia(raw_blocks, energy_profile)
    print(f"   --> {len(enriched_blocks)} blocos sintáticos naturais criados e enriquecidos com energia.")

    # Mapeia blocos por ID para consulta instantânea
    blocos_map = {b["bloco_id"]: b for b in enriched_blocks}

    # 5. FILTRAGEM MULTIMODAL PRÉ-LLM:
    # O grande diferencial do OpusClip/Klap: descarta blocos frios/silenciosos ANTES de chamar a IA!
    # Seleciona os blocos de maior impacto acústico (Top 25) e reordena cronologicamente
    candidatos_quentes = [
        b for b in enriched_blocks 
        if b["nivel_energia"] in ("CLIMAX_ALTA", "MEDIA_CONSTANTE") and b["n_words"] >= 18
    ]
    # Ordena por energia decrescente para selecionar a elite acústica da pregação
    candidatos_quentes.sort(key=lambda x: x["energia_media"], reverse=True)
    top_candidatos = candidatos_quentes[:25]
    # Reordena por bloco_id para manter a progressão narrativa do culto
    top_candidatos.sort(key=lambda x: x["bloco_id"])

    blocos_cards = []
    for b in top_candidatos:
        txt_curto = b['texto'][:160] + ("..." if len(b['texto']) > 160 else "")
        blocos_cards.append(
            f"[BLOCO {b['bloco_id']} | DURAÇÃO: {b['duracao_sec']:.0f}s | ENERGIA: {b['nivel_energia']}]\n"
            f"\"{txt_curto}\""
        )

    # Cria uma linha do tempo macro enxuta para ancoragem do Tier 3
    timeline_macro = []
    passo_macro = max(1, len(enriched_blocks) // 40)
    for b in enriched_blocks[::passo_macro]:
        st_m = b["start_sec"] / 60.0
        words_snippet = " ".join(b["texto"].split()[:6])
        timeline_macro.append(f"Bloco {b['bloco_id']:03d} ({st_m:4.1f}m): \"{words_snippet}...\"")

    print(f"🔥 [MULTIMODAL] Top {len(top_candidatos)} blocos acústicos de elite selecionados (descartados {len(enriched_blocks) - len(top_candidatos)} blocos mornos/frios)")

    # 6. Chamada aos Modelos Gratuitos da DevWorld / Groq
    print(f"🧠 [3/4] Enviando {len(top_candidatos)} blocos quentes e linha do tempo macro para curadoria...")
    prompt_usuario = (
        f"Analise a estrutura do CULTO {culto_id} e os blocos de maior autoridade vocal abaixo.\n"
        f"EXTRAIA:\n"
        f"1. De 3 a 5 Shorts Tier 1 (25s a 80s) com alto clímax acústico.\n"
        f"2. De 1 a 2 Vídeos Médios Tier 2 (120s a 300s) para reflexões/orações.\n"
        f"3. Exatamente 1 Pregação Completa Tier 3 (30 a 60 minutos contínuos) cobrindo a mensagem bíblica na íntegra, desde a leitura inicial até o apelo/oração final (eliminando louvor e avisos).\n"
        f"Use EXCLUSIVAMENTE os IDs dos blocos fornecidos (bloco_inicio_id e bloco_fim_id).\n\n"
        f"--- LINHA DO TEMPO MACRO DO CULTO (Use para ancorar o início e fim do Tier 3) ---\n"
        + "\n".join(timeline_macro) + "\n\n"
        f"--- BLOCOS DE ELITE ACÚSTICA (Use para os Tiers 1 e 2) ---\n"
        + "\n\n".join(blocos_cards)
    )

    t_llm = time.time()
    resposta_ia = chamar_llm_devworld(prompt_usuario)
    print(f"   --> Resposta do LLM obtida em {time.time()-t_llm:.1f}s com sucesso!")

    # 7. Amarração Blindada dos Timestamps (Herdados dos Blocos Físicos)
    print("🔒 [4/4] Amarrando timestamps físicos diretamente dos blocos de respiração...")
    cortes_tier1_finais = []
    for idx, c in enumerate(resposta_ia.get("cortes_tier1_shorts", [])):
        b_ini_id = c.get("bloco_inicio_id")
        b_fim_id = c.get("bloco_fim_id", b_ini_id)

        if b_ini_id in blocos_map and b_fim_id in blocos_map:
            b_ini = blocos_map[b_ini_id]
            b_fim = blocos_map[b_fim_id]

            st_sec = b_ini["start_sec"]
            en_sec = b_fim["end_sec"]
            dur_real = round(en_sec - st_sec, 2)

            # Junta texto dos blocos
            textos = [blocos_map[i]["texto"] for i in range(b_ini_id, b_fim_id + 1) if i in blocos_map]
            texto_completo = " ".join(textos)

            cortes_tier1_finais.append({
                "corte_id": f"{culto_id}_multimodal_t1_{idx+1:02d}",
                "tipo": "TIER1_SHORTS",
                "titulo_viral": c.get("titulo_viral", "").upper(),
                "arquetipo": c.get("arquetipo", "Confronto Profético"),
                "nota_viral": c.get("nota_viral", 95),
                "gancho_primeiros_3s": c.get("gancho_primeiros_3s", ""),
                "punchline_final": c.get("punchline_final", ""),
                "start_sec": st_sec,
                "end_sec": en_sec,
                "duracao_sec": dur_real,
                "nivel_energia": b_ini.get("nivel_energia", "CLIMAX_ALTA"),
                "texto_completo": texto_completo
            })

    cortes_tier2_finais = []
    for idx, c in enumerate(resposta_ia.get("cortes_tier2_medios", [])):
        b_ini_id = c.get("bloco_inicio_id")
        b_fim_id = c.get("bloco_fim_id", b_ini_id)

        if b_ini_id in blocos_map and b_fim_id in blocos_map:
            b_ini = blocos_map[b_ini_id]
            b_fim = blocos_map[b_fim_id]

            st_sec = b_ini["start_sec"]
            en_sec = b_fim["end_sec"]
            dur_real = round(en_sec - st_sec, 2)

            textos = [blocos_map[i]["texto"] for i in range(b_ini_id, b_fim_id + 1) if i in blocos_map]

            cortes_tier2_finais.append({
                "corte_id": f"{culto_id}_multimodal_t2_{idx+1:02d}",
                "tipo": "TIER2_MEDIO",
                "titulo_devocional": c.get("titulo_devocional", "").upper(),
                "tema": c.get("tema", ""),
                "resumo_narrativa": c.get("resumo_narrativa", ""),
                "punchline_final": c.get("punchline_final", ""),
                "start_sec": st_sec,
                "end_sec": en_sec,
                "duracao_sec": dur_real,
                "texto_completo": " ".join(textos)
            })

    corte_tier3_final = None
    t3 = resposta_ia.get("corte_tier3_tematico")
    if t3 and isinstance(t3, dict) and t3.get("bloco_inicio_id"):
        b_ini_id = t3.get("bloco_inicio_id")
        b_fim_id = t3.get("bloco_fim_id", b_ini_id)

        if b_ini_id in blocos_map and b_fim_id in blocos_map:
            b_ini = blocos_map[b_ini_id]
            b_fim = blocos_map[b_fim_id]

            st_sec = b_ini["start_sec"]
            en_sec = b_fim["end_sec"]
            dur_real = round(en_sec - st_sec, 2)

            corte_tier3_final = {
                "corte_id": f"{culto_id}_multimodal_t3_01",
                "tipo": "TIER3_TEMATICO",
                "titulo_estudo_youtube": t3.get("titulo_estudo_youtube", "").upper(),
                "tema_central": t3.get("tema_central", ""),
                "nome_playlist_sugerida": t3.get("nome_playlist_sugerida", "Série: Estudos Bíblicos IBPM"),
                "resumo_estudo": t3.get("resumo_estudo", ""),
                "tags_youtube": t3.get("tags_youtube", ["ibpm", "pregação", "estudo bíblico"]),
                "start_sec": st_sec,
                "end_sec": en_sec,
                "duracao_sec": dur_real,
                "bloco_inicio_id": b_ini_id,
                "bloco_fim_id": b_fim_id
            }

    resultado_final = {
        "culto_id": culto_id,
        "titulo_culto": resposta_ia.get("tema_geral_sermão", f"Culto {culto_id}"),
        "modelo_utilizado": DEVWORLD_MODEL,
        "timestamp_mineracao": time.strftime("%Y-%m-%d %H:%M:%S"),
        "total_shorts_tier1": len(cortes_tier1_finais),
        "total_medios_tier2": len(cortes_tier2_finais),
        "possui_tier3_tematico": corte_tier3_final is not None,
        "cortes_tier1_shorts": cortes_tier1_finais,
        "cortes_tier2_medios": cortes_tier2_finais,
        "corte_tier3_tematico": corte_tier3_final
    }

    out_json = OUTPUT_CORTES_DIR / f"culto_{culto_id}_cortes_multimodal.json"
    with open(out_json, "w", encoding="utf-8") as f:
        json.dump(resultado_final, f, ensure_ascii=False, indent=2)

    print(f"\n✅ MINERAÇÃO CONCLUÍDA COM SUCESSO! Salvo em: {out_json.name}")
    print(f"   Shorts Tier 1: {len(cortes_tier1_finais)} | Médios Tier 2: {len(cortes_tier2_finais)} | Tier 3 Temático: {'SIM' if corte_tier3_final else 'NÃO'}")
    if corte_tier3_final:
        print(f"   📖 [TIER 3] {corte_tier3_final['duracao_sec']/60:.1f} min: \"{corte_tier3_final['titulo_estudo_youtube']}\" (Playlist: {corte_tier3_final['nome_playlist_sugerida']})")
    for s in cortes_tier1_finais:
        print(f"   • [{s['corte_id']}] {s['duracao_sec']}s ({s['nivel_energia']}): \"{s['titulo_viral']}\"")

    return out_json


if __name__ == "__main__":
    cid = 439
    if len(sys.argv) > 1:
        try: cid = int(sys.argv[1])
        except ValueError: pass
    minerar_culto_multimodal(cid)
