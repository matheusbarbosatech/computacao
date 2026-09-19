"""
=============================================================================
MOTOR DE IA DEVWORLD — GERAÇÃO AUTOMATIZADA DE MAPAS MENTAIS
=============================================================================
Conecta à API da DevWorld usando os modelos ilimitados (-f) para gerar
conteúdo pedagógico de altíssimo nível em formato JSON estruturado.
=============================================================================
"""

import os
import sys
import json
import re
import time
import requests
from typing import Dict, Any, Optional

if sys.platform == "win32":
    try:
        sys.stdout.reconfigure(encoding='utf-8')
        sys.stderr.reconfigure(encoding='utf-8')
    except Exception:
        pass

def carregar_env() -> Dict[str, str]:
    config = {
        "DEVWORLD_API_KEY": "dw_live_UgEYtrkRzOvCU-BV-IR8TvAzKBdsHoEnIROAq0OthLU",
        "DEVWORLD_BASE_URL": "https://chat.devwservices.shop/v1",
        "DEVWORLD_MODEL": "devworld/gemini-3.7-flash-f",
        "GEMINI_API_KEY": ""
    }
    
    # Procura .env local
    env_path = os.path.join(os.path.dirname(__file__), ".env")
    if os.path.exists(env_path):
        with open(env_path, "r", encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                if line and not line.startswith("#") and "=" in line:
                    k, v = line.split("=", 1)
                    config[k.strip()] = v.strip().strip('"').strip("'")
                    
    # Procura chave do Gemini como fallback de alta velocidade se houver
    ibpm_env = r"C:\Users\matheus\Desktop\ibpmcr-automation\.env"
    if os.path.exists(ibpm_env):
        try:
            with open(ibpm_env, "r", encoding="utf-8") as f:
                for line in f:
                    if line.startswith("GEMINI_API_KEY="):
                        config["GEMINI_API_KEY"] = line.split("=", 1)[1].strip().strip('"').strip("'")
        except Exception:
            pass

    return config

ENV_CONFIG = carregar_env()

# Modelos Ilimitados / Gratuitos da DevWorld (terminados em -f)
MODELOS_ILIMITADOS = [
    "devworld/gemini-3.7-flash-f",
    "devworld/deepseek-v4-pro-0813-f",
    "devworld/gpt-5.6-sol-f",
    "devworld/claude-opus-5-f",
    "devworld/qwen3.8-max-f",
    "devworld/kimi-k3-f"
]

SYSTEM_PROMPT_PEDAGOGICO = """Você é um Especialista em Ensino de Ciência da Computação para Iniciantes Absolutos e Designer de Infográficos Sketchnote.

Sua tarefa é criar o conteúdo completo de um MAPA MENTAL no formato SKETCHNOTE (visual, direto, com linguagem simples e analogias do dia a dia).

REGRAS OBRIGATÓRIAS:
1. Responda ESTRITAMENTE com um objeto JSON válido (sem markdown, sem ```json, apenas as chaves JSON).
2. O conteúdo deve ser compreensível para alguém que NUNCA programou na vida.
3. Use frases curtas, objetivas e de alto impacto (máximo 12 a 18 palavras por ponto).
4. O JSON deve ter EXATAMENTE a seguinte estrutura:

{
  "id": 1,
  "title": "TÍTULO DO TEMA EM MAIÚSCULAS",
  "definition": "Definição central em 1 frase simples e clara.",
  "topLeft": {
    "pill": "IDEIA CENTRAL",
    "icon": "💡",
    "bullets": ["Frase resumindo o que é esse conceito sem jargões."]
  },
  "topRight": {
    "pill": "NOME DO CONCEITO 1",
    "icon": "🖥️",
    "bullets": ["Como o computador ou o sistema lida com isso.", "Ponto prático 2."]
  },
  "midRight": {
    "pill": "CÓDIGO OU REGRA",
    "icon": "{ }",
    "bullets": ["Explicação simples da sintaxe.", "exemplo(codigo)"]
  },
  "bottomRight": {
    "pill": "ONDE É USADO",
    "icon": "</>",
    "bullets": ["Aplicação no dia a dia do programador.", "Exemplos de linguagens ou ferramentas."]
  },
  "bottomCenter": {
    "pill": "FLUXO OU PASSO A PASSO",
    "icon": "⚙️",
    "bullets": [
      "PASSO 1: O que acontece primeiro",
      "PASSO 2: O processamento ou decisão",
      "PASSO 3: O resultado final"
    ]
  },
  "bottomLeft": {
    "pill": "PEGADINHAS COMUNS",
    "icon": "⚠️",
    "bullets": ["Erro clássico que iniciantes cometem.", "Dica de ouro para não travar."]
  },
  "midLeft": {
    "pill": "RESUMO EXPRESSO",
    "icon": "💬",
    "bullets": ["Conceito A ➔ Ação B ➔ Resultado C"]
  }
}
"""

def limpar_resposta_json(texto: str) -> str:
    """Extrai JSON válido mesmo que a IA inclua marcações."""
    texto = texto.strip()
    match = re.search(r'\{.*\}', texto, re.DOTALL)
    if match:
        return match.group(0)
    return texto

def gerar_mapa_devworld(
    topico: str,
    id_mapa: int = 1,
    foco: str = "",
    modelo: Optional[str] = None
) -> Dict[str, Any]:
    api_key = ENV_CONFIG.get("DEVWORLD_API_KEY")
    base_url = ENV_CONFIG.get("DEVWORLD_BASE_URL", "https://chat.devwservices.shop/v1").rstrip("/")
    endpoint = f"{base_url}/chat/completions"
    
    modelos_para_tentar = [modelo] if modelo else [
        ENV_CONFIG.get("DEVWORLD_MODEL", "claude-sonnet-5[1m]"),
        "claude-fable-5-1[1m]",
        "devworld/gemini-3.7-flash-f",
        "devworld/deepseek-v4-pro-0813-f"
    ]

    user_prompt = f"Gere o mapa mental #{id_mapa} sobre o tema: '{topico}'."
    if foco:
        user_prompt += f" Foco pedagógico especial: {foco}."

    ultimo_erro = None

    for mod in modelos_para_tentar:
        if not mod:
            continue
        try:
            payload = {
                "model": mod,
                "messages": [
                    {"role": "system", "content": SYSTEM_PROMPT_PEDAGOGICO},
                    {"role": "user", "content": user_prompt}
                ],
                "temperature": 0.2,
                "max_tokens": 1400
            }
            headers = {
                "Content-Type": "application/json",
                "Authorization": f"Bearer {api_key}",
                "User-Agent": "GeradorMapasMentais/1.0"
            }

            resp = requests.post(endpoint, json=payload, headers=headers, timeout=90)
            if resp.status_code == 200:
                data = resp.json()
                conteudo = data["choices"][0]["message"]["content"]
                conteudo_limpo = limpar_resposta_json(conteudo)
                dados_mapa = json.loads(conteudo_limpo)
                dados_mapa["id"] = id_mapa
                dados_mapa["_modelo_usado"] = mod
                return dados_mapa
            else:
                ultimo_erro = f"HTTP {resp.status_code}: {resp.text[:100]}"
                time.sleep(1)
        except Exception as e:
            ultimo_erro = str(e)
            time.sleep(1)
            continue

    raise RuntimeError(f"Falha na DevWorld ({ultimo_erro})")

if __name__ == "__main__":
    t0 = time.time()
    print("Testando gerador DevWorld...")
    res = gerar_mapa_devworld("O que é Programação?", 1)
    print(f"Sucesso em {time.time()-t0:.1f}s!")
    print("Titulo:", res.get("title"))
    print("Modelo:", res.get("_modelo_usado"))
