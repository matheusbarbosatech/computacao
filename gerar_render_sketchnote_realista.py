"""
=============================================================================
RENDERIZADOR DE ALTA FIDELIDADE SKETCHNOTE (IDÊNTICO À REFERÊNCIA DO SITE)
=============================================================================
Gera arquivos HTML/SVG e renderiza em PNG Ultra-HD 1536 x 1024 (300 DPI)
com a estética artesanal idêntica a '150mapasdeprogramacao.netlify.app':
- 8 Cards orbitando em simetria perfeita (4 na esquerda, 4 na direita).
- Faixas de marcador/marca-texto com textura de pincel chanfrado Copic/Posca.
- Doodles vetoriais desenhados à mão com contornos orgânicos e cores vivas.
- Seleção contextual inteligente de ícones (Lâmpada, PC, Código, Alerta,
  Prancheta, Banco de Dados, Cadeado/Segurança, Nuvem/DevOps, Terminal, etc.)
- Nó central com raios de sol, acentos laterais e sublinhado duplo em marcador.
- 8 Setas curvas Bézier orgânicas nas cores dos respectivos cards.
- Fundo papel sketchbook off-white (#FAF8F5).
- Exportação em 1536 x 1024 (3:2) via Chrome/Edge headless para A4 Paisagem.
=============================================================================
"""

import os
import sys
import json
import subprocess
import tempfile
import re

if sys.platform == "win32":
    try:
        sys.stdout.reconfigure(encoding='utf-8', line_buffering=True)
        sys.stderr.reconfigure(encoding='utf-8', line_buffering=True)
    except Exception:
        pass

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# ACERVO DE DOODLES VETORIAIS SKETCH ART FEITOS À MÃO
DOODLES = {
    "lampada": """
    <svg viewBox="0 0 100 100" class="doodle-icon">
      <line x1="50" y1="8" x2="50" y2="1" stroke="#EAB308" stroke-width="3.5" stroke-linecap="round"/>
      <line x1="20" y1="18" x2="13" y2="11" stroke="#EAB308" stroke-width="3.5" stroke-linecap="round"/>
      <line x1="80" y1="18" x2="87" y2="11" stroke="#EAB308" stroke-width="3.5" stroke-linecap="round"/>
      <line x1="10" y1="42" x2="2" y2="42" stroke="#EAB308" stroke-width="3.5" stroke-linecap="round"/>
      <line x1="90" y1="42" x2="98" y2="42" stroke="#EAB308" stroke-width="3.5" stroke-linecap="round"/>
      <path d="M50,14 C33,14 24,26 24,42 C24,53 33,61 37,67 L37,73 C37,75 39,77 41,77 L59,77 C61,77 63,75 63,73 L63,67 C67,61 76,53 76,42 C76,26 67,14 50,14 Z" fill="#FACC15" stroke="#1E293B" stroke-width="3.5" stroke-linejoin="round"/>
      <path d="M41,47 Q45,35 50,47 Q55,35 59,47" fill="none" stroke="#1E293B" stroke-width="3" stroke-linecap="round"/>
      <path d="M39,77 L61,77 L59,85 L41,85 Z" fill="#E2E8F0" stroke="#1E293B" stroke-width="3"/>
      <path d="M43,85 Q50,91 57,85" fill="#94A3B8" stroke="#1E293B" stroke-width="2.5"/>
    </svg>
    """,
    "computador": """
    <svg viewBox="0 0 100 100" class="doodle-icon">
      <rect x="12" y="14" width="76" height="54" rx="12" fill="#F0FDF4" stroke="#15803D" stroke-width="3.5"/>
      <rect x="20" y="22" width="60" height="38" rx="8" fill="#DCFCE7" stroke="#15803D" stroke-width="2.5"/>
      <circle cx="40" cy="38" r="3.5" fill="#15803D"/>
      <circle cx="60" cy="38" r="3.5" fill="#15803D"/>
      <path d="M42,47 Q50,55 58,47" fill="none" stroke="#15803D" stroke-width="3" stroke-linecap="round"/>
      <rect x="44" y="68" width="12" height="10" fill="#E2E8F0" stroke="#15803D" stroke-width="3"/>
      <path d="M18,84 L82,84 L78,78 L22,78 Z" fill="#F0FDF4" stroke="#15803D" stroke-width="3" stroke-linejoin="round"/>
      <line x1="28" y1="81" x2="72" y2="81" stroke="#15803D" stroke-width="1.8"/>
    </svg>
    """,
    "codigo": """
    <svg viewBox="0 0 100 100" class="doodle-icon">
      <path d="M38,18 Q22,18 22,38 Q22,50 12,50 Q22,50 22,62 Q22,82 38,82" fill="none" stroke="#0D9488" stroke-width="4.5" stroke-linecap="round"/>
      <path d="M62,18 Q78,18 78,38 Q78,50 88,50 Q78,50 78,62 Q78,82 62,82" fill="none" stroke="#0D9488" stroke-width="4.5" stroke-linecap="round"/>
      <line x1="6" y1="36" x2="1" y2="34" stroke="#0D9488" stroke-width="2.5" stroke-linecap="round"/>
      <line x1="6" y1="64" x2="1" y2="66" stroke="#0D9488" stroke-width="2.5" stroke-linecap="round"/>
      <line x1="94" y1="36" x2="99" y2="34" stroke="#0D9488" stroke-width="2.5" stroke-linecap="round"/>
      <line x1="94" y1="64" x2="99" y2="66" stroke="#0D9488" stroke-width="2.5" stroke-linecap="round"/>
    </svg>
    """,
    "linguagens": """
    <svg viewBox="0 0 100 100" class="doodle-icon">
      <path d="M34,26 L14,50 L34,74" fill="none" stroke="#EA580C" stroke-width="5" stroke-linecap="round" stroke-linejoin="round"/>
      <path d="M44,78 L56,22" fill="none" stroke="#EA580C" stroke-width="4.5" stroke-linecap="round"/>
      <path d="M66,26 L86,50 L66,74" fill="none" stroke="#EA580C" stroke-width="5" stroke-linecap="round" stroke-linejoin="round"/>
    </svg>
    """,
    "fluxo": """
    <svg viewBox="0 0 100 100" class="doodle-icon">
      <circle cx="50" cy="50" r="21" fill="#EFF6FF" stroke="#2563EB" stroke-width="3.5"/>
      <circle cx="50" cy="50" r="7" fill="#FFFFFF" stroke="#2563EB" stroke-width="3"/>
      <rect x="46" y="19" width="8" height="8" rx="2" fill="#93C5FD" stroke="#2563EB" stroke-width="2"/>
      <rect x="46" y="73" width="8" height="8" rx="2" fill="#93C5FD" stroke="#2563EB" stroke-width="2"/>
      <rect x="19" y="46" width="8" height="8" rx="2" fill="#93C5FD" stroke="#2563EB" stroke-width="2"/>
      <rect x="73" y="46" width="8" height="8" rx="2" fill="#93C5FD" stroke="#2563EB" stroke-width="2"/>
      <rect x="28" y="28" width="8" height="8" rx="2" fill="#93C5FD" stroke="#2563EB" stroke-width="2" transform="rotate(45 32 32)"/>
      <rect x="64" y="64" width="8" height="8" rx="2" fill="#93C5FD" stroke="#2563EB" stroke-width="2" transform="rotate(45 68 68)"/>
      <rect x="64" y="28" width="8" height="8" rx="2" fill="#93C5FD" stroke="#2563EB" stroke-width="2" transform="rotate(45 68 32)"/>
      <rect x="28" y="64" width="8" height="8" rx="2" fill="#93C5FD" stroke="#2563EB" stroke-width="2" transform="rotate(45 32 68)"/>
      <path d="M18,50 A33,33 0 0,0 52,84" fill="none" stroke="#1D4ED8" stroke-width="3" stroke-linecap="round"/>
      <polygon points="58,83 48,78 51,88" fill="#1D4ED8"/>
    </svg>
    """,
    "pegadinhas": """
    <svg viewBox="0 0 100 100" class="doodle-icon">
      <polygon points="50,12 88,80 12,80" fill="#FEE2E2" stroke="#DC2626" stroke-width="4.5" stroke-linejoin="round"/>
      <polygon points="50,22 80,74 20,74" fill="#FFFFFF" stroke="#DC2626" stroke-width="2.5" stroke-linejoin="round"/>
      <line x1="50" y1="36" x2="50" y2="56" stroke="#DC2626" stroke-width="5.5" stroke-linecap="round"/>
      <circle cx="50" cy="65" r="4" fill="#DC2626"/>
      <line x1="10" y1="46" x2="2" y2="44" stroke="#DC2626" stroke-width="3" stroke-linecap="round"/>
      <line x1="90" y1="46" x2="98" y2="44" stroke="#DC2626" stroke-width="3" stroke-linecap="round"/>
      <line x1="50" y1="6" x2="50" y2="1" stroke="#DC2626" stroke-width="3" stroke-linecap="round"/>
    </svg>
    """,
    "exemplo": """
    <svg viewBox="0 0 100 100" class="doodle-icon">
      <rect x="20" y="16" width="60" height="76" rx="8" fill="#FFFBEB" stroke="#1E293B" stroke-width="3.5"/>
      <rect x="36" y="10" width="28" height="12" rx="4" fill="#E2E8F0" stroke="#1E293B" stroke-width="3"/>
      <circle cx="50" cy="16" r="2.5" fill="#1E293B"/>
      <text x="27" y="38" font-family="'Patrick Hand', cursive" font-size="16" font-weight="700" fill="#1E293B">1</text>
      <line x1="38" y1="35" x2="68" y2="35" stroke="#94A3B8" stroke-width="2.5" stroke-linecap="round"/>
      <text x="27" y="52" font-family="'Patrick Hand', cursive" font-size="16" font-weight="700" fill="#1E293B">2</text>
      <line x1="38" y1="49" x2="68" y2="49" stroke="#94A3B8" stroke-width="2.5" stroke-linecap="round"/>
      <circle cx="50" cy="74" r="14" fill="#FEF2F2" stroke="#16A34A" stroke-width="3"/>
      <path d="M43,74 L48,79 L58,68" fill="none" stroke="#16A34A" stroke-width="3.2" stroke-linecap="round" stroke-linejoin="round"/>
    </svg>
    """,
    "resumo": """
    <svg viewBox="0 0 100 100" class="doodle-icon">
      <path d="M22,24 Q50,14 78,24 Q90,48 78,66 Q50,76 34,68 L18,78 L24,62 Q10,44 22,24 Z" fill="#E0F2FE" stroke="#0284C7" stroke-width="3.5" stroke-linejoin="round"/>
      <circle cx="39" cy="45" r="4" fill="#0284C7"/>
      <circle cx="50" cy="45" r="4" fill="#0284C7"/>
      <circle cx="61" cy="45" r="4" fill="#0284C7"/>
    </svg>
    """,
    "banco_dados": """
    <svg viewBox="0 0 100 100" class="doodle-icon">
      <ellipse cx="50" cy="24" rx="34" ry="12" fill="#CFFAFE" stroke="#0891B2" stroke-width="3.5"/>
      <path d="M16,24 L16,50 C16,60 84,60 84,50 L84,24" fill="none" stroke="#0891B2" stroke-width="3.5"/>
      <path d="M16,50 L16,76 C16,86 84,86 84,76 L84,50" fill="none" stroke="#0891B2" stroke-width="3.5"/>
      <ellipse cx="50" cy="50" rx="34" ry="10" fill="none" stroke="#0891B2" stroke-width="2.5" stroke-dasharray="4,4"/>
      <ellipse cx="50" cy="76" rx="34" ry="10" fill="#E0F2FE" stroke="#0891B2" stroke-width="3.5"/>
      <circle cx="70" cy="38" r="3" fill="#0891B2"/>
      <circle cx="70" cy="64" r="3" fill="#0891B2"/>
    </svg>
    """,
    "cadeado": """
    <svg viewBox="0 0 100 100" class="doodle-icon">
      <path d="M30,44 L30,28 C30,16 70,16 70,28 L70,44" fill="none" stroke="#059669" stroke-width="5" stroke-linecap="round"/>
      <rect x="20" y="44" width="60" height="46" rx="10" fill="#D1FAE5" stroke="#059669" stroke-width="3.8"/>
      <circle cx="50" cy="64" r="5" fill="#059669"/>
      <line x1="50" y1="69" x2="50" y2="78" stroke="#059669" stroke-width="3.5" stroke-linecap="round"/>
    </svg>
    """,
    "nuvem": """
    <svg viewBox="0 0 100 100" class="doodle-icon">
      <path d="M26,68 C16,68 12,56 20,48 C18,34 32,26 44,32 C50,20 70,20 76,32 C86,32 92,42 86,52 C94,62 86,68 76,68 Z" fill="#E0F2FE" stroke="#0284C7" stroke-width="3.5" stroke-linejoin="round"/>
      <path d="M50,44 L50,60" stroke="#0284C7" stroke-width="3.5" stroke-linecap="round"/>
      <path d="M42,50 L50,42 L58,50" fill="none" stroke="#0284C7" stroke-width="3.5" stroke-linecap="round" stroke-linejoin="round"/>
    </svg>
    """,
    "terminal": """
    <svg viewBox="0 0 100 100" class="doodle-icon">
      <rect x="14" y="20" width="72" height="60" rx="8" fill="#1E293B" stroke="#475569" stroke-width="3.5"/>
      <circle cx="24" cy="28" r="2.5" fill="#EF4444"/>
      <circle cx="32" cy="28" r="2.5" fill="#F59E0B"/>
      <circle cx="40" cy="28" r="2.5" fill="#10B981"/>
      <line x1="14" y1="36" x2="86" y2="36" stroke="#475569" stroke-width="2"/>
      <text x="24" y="55" font-family="'Fira Code', monospace" font-size="16" font-weight="700" fill="#10B981">&gt;_</text>
      <rect x="48" y="44" width="8" height="13" fill="#10B981"/>
    </svg>
    """
}

def escolher_doodle(titulo: str, texto_contexto: str, padrao: str) -> str:
    """Seleciona o ícone vetorial mais adequado com base em palavras-chave."""
    combinado = f"{titulo} {texto_contexto}".upper()
    if any(k in combinado for k in ["SQL", "BANCO", "DADOS", "TABELA", "RELACIONAL", "QUERY", "INDEX"]):
        return DOODLES["banco_dados"]
    if any(k in combinado for k in ["SEGURANÇA", "CRIPTO", "SENHA", "CADEADO", "HASH", "TOKEN", "AUTENTICAÇÃO", "OWASP", "VULNERABILIDADE"]):
        return DOODLES["cadeado"]
    if any(k in combinado for k in ["DOCKER", "CONTAINER", "NUVEM", "CLOUD", "DEPLOY", "KUBERNETES", "AWS", "CI/CD"]):
        return DOODLES["nuvem"]
    if any(k in combinado for k in ["LINUX", "TERMINAL", "BASH", "SHELL", "COMANDO", "CLI", "SSH"]):
        return DOODLES["terminal"]
    if any(k in combinado for k in ["FLUXO", "PROCESSO", "PASSO", "CICLO", "ORDEM", "ENGRENAGEM"]):
        return DOODLES["fluxo"]
    if any(k in combinado for k in ["PEGADINHA", "ALERTA", "CUIDADO", "ERRO", "ATENÇÃO", "BUG"]):
        return DOODLES["pegadinhas"]
    if any(k in combinado for k in ["CÓDIGO", "SINTAXE", "FUNÇÃO", "SCRIPT", "CHAVES"]):
        return DOODLES["codigo"]
    if any(k in combinado for k in ["TAG", "WEB", "FRONT", "HTML", "CSS", "LINGUAGEM"]):
        return DOODLES["linguagens"]
    if any(k in combinado for k in ["RESUMO", "SÍNTESE", "EXPRESSO", "CONCEITO RÁPIDO"]):
        return DOODLES["resumo"]
    if any(k in combinado for k in ["EXEMPLO", "PRÁTICO", "CASO", "TESTE", "NA PRÁTICA"]):
        return DOODLES["exemplo"]
    
    return DOODLES.get(padrao, DOODLES["lampada"])

# GERADOR DO MARCADOR DE TEXTO / RIBBON SVG COM LARGURA DINÂMICA
def gerar_svg_marker_ribbon(texto: str, cor: str) -> str:
    """Gera o badge com estilo realista de pincel chanfrado Copic Marker sem cortar texto."""
    texto_limpo = texto.strip().upper()
    simplificacoes = {
        "PEGADINHAS COMUNS": "PEGADINHAS",
        "COMO A MÁQUINA PENSA": "COMPUTADOR",
        "CÓDIGO OU REGRA": "CÓDIGO",
        "ONDE É USADO": "LINGUAGENS",
        "FLUXO OU PASSO A PASSO": "FLUXO BÁSICO"
    }
    texto_exibicao = simplificacoes.get(texto_limpo, texto_limpo)
    
    # Se ainda for longo demais (>22 caracteres), encurta elegantemente
    if len(texto_exibicao) > 22:
        if "(" in texto_exibicao:
            partes = texto_exibicao.split("(")
            if len(partes[0].strip()) >= 3:
                texto_exibicao = partes[0].strip()
            else:
                texto_exibicao = partes[1].replace(")", "").strip()
        else:
            palavras = texto_exibicao.split()
            if len(palavras) > 2:
                texto_exibicao = f"{palavras[0]} {palavras[1]}"

    tamanho = len(texto_exibicao)
    font_size = 21 if tamanho <= 14 else (18 if tamanho <= 20 else 15)
    char_w = 14 if font_size == 21 else (11.5 if font_size == 18 else 9.5)
    largura = max(160, int(tamanho * char_w + 44))
    filtro_id = abs(hash(cor + texto_exibicao)) % 10000

    return f"""
    <svg class="marker-ribbon" width="{largura}" height="46" viewBox="0 0 {largura} 46" style="overflow: visible;">
      <defs>
        <filter id="brush-shadow-{filtro_id}" x="-5%" y="-5%" width="115%" height="120%">
          <feDropShadow dx="2" dy="3" stdDeviation="1.5" flood-color="rgba(0,0,0,0.14)"/>
        </filter>
      </defs>
      <path d="M 12 7 C {largura*0.4} 4, {largura*0.8} 3, {largura-10} 7 C {largura+2} 9, {largura+3} 37, {largura-12} 40 C {largura*0.6} 43, {largura*0.2} 44, 10 40 C -1 37, -1 9, 12 7 Z"
            fill="{cor}" filter="url(#brush-shadow-{filtro_id})"/>
      <path d="M 18 13 C {largura*0.5} 10, {largura*0.8} 11, {largura-20} 14"
            stroke="rgba(255,255,255,0.30)" stroke-width="3.5" stroke-linecap="round" fill="none"/>
      <path d="M 15 35 C {largura*0.4} 37, {largura*0.75} 36, {largura-18} 33"
            stroke="rgba(0,0,0,0.12)" stroke-width="2.5" stroke-linecap="round" fill="none"/>
      <text x="{largura/2}" y="29" fill="#FFFFFF"
            font-family="'Patrick Hand', 'Kalam', cursive"
            font-size="{font_size}" font-weight="700"
            letter-spacing="1.2px"
            text-anchor="middle">{texto_exibicao}</text>
    </svg>
    """

HTML_TEMPLATE_HQ = """<!DOCTYPE html>
<html lang="pt-BR">
<head>
  <meta charset="UTF-8">
  <title>Sketchnote #{id} - {title}</title>
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link href="https://fonts.googleapis.com/css2?family=Patrick+Hand&family=Kalam:wght@400;700&family=Caveat:wght@700&family=Fira+Code:wght@500;600&display=swap" rel="stylesheet">
  <style>
    * {{ box-sizing: border-box; margin: 0; padding: 0; }}
    
    body {{
      width: 1536px;
      height: 1024px;
      background-color: #FAF8F5;
      font-family: 'Kalam', cursive;
      color: #1E293B;
      position: relative;
      overflow: hidden;
      -webkit-font-smoothing: antialiased;
    }}

    /* CAMADA DE SETAS BÉZIER ORGÂNICAS */
    .arrows-layer {{
      position: absolute;
      top: 0; left: 0;
      width: 1536px;
      height: 1024px;
      pointer-events: none;
      z-index: 2;
    }}
    .sketch-arrow {{
      fill: none;
      stroke-width: 3.5;
      stroke-linecap: round;
    }}

    /* NÓ CENTRAL COM ESTÉTICA SKETCHNOTE */
    .center-container {{
      position: absolute;
      left: 768px;
      top: 485px;
      transform: translate(-50%, -50%);
      width: 480px;
      text-align: center;
      z-index: 10;
    }}
    .center-rays {{
      font-size: 2.3rem;
      color: #EAB308;
      line-height: 1;
      letter-spacing: 10px;
      margin-bottom: 2px;
      font-weight: 700;
    }}
    .title-wrapper {{
      position: relative;
      display: inline-flex;
      align-items: center;
      justify-content: center;
      gap: 14px;
    }}
    .center-title {{
      font-family: 'Patrick Hand', cursive;
      font-size: 3.8rem;
      font-weight: 700;
      line-height: 0.95;
      text-transform: uppercase;
      color: #0F172A;
      letter-spacing: 1px;
    }}
    .title-dashes {{
      font-size: 2.6rem;
      color: #8B5CF6;
      font-weight: 700;
      letter-spacing: -2px;
      user-select: none;
    }}
    .center-underline {{
      margin: 4px auto 14px auto;
      display: block;
    }}
    .center-definition {{
      background: #FFFFFF;
      border: 3.2px solid #8B5CF6;
      border-radius: 255px 22px 225px 22px/22px 225px 22px 255px;
      padding: 12px 24px;
      font-size: 1.32rem;
      color: #1E293B;
      line-height: 1.3;
      box-shadow: 2px 4px 0px rgba(0,0,0,0.06);
    }}

    /* CARDS DO SKETCHNOTE COM BORDAS ORGÂNICAS */
    .sketch-card {{
      position: absolute;
      background: #FFFFFF;
      border: 3.5px solid;
      border-radius: 255px 20px 225px 20px/20px 225px 20px 255px;
      box-shadow: 3px 4px 0px rgba(0,0,0,0.06);
      padding: 18px 22px;
      display: flex;
      flex-direction: column;
      z-index: 5;
    }}

    .marker-ribbon {{
      position: absolute;
      top: -24px;
      left: 18px;
      transform: rotate(-1.2deg);
    }}

    .card-body {{
      margin-top: 10px;
      display: flex;
      gap: 16px;
      align-items: center;
      height: 100%;
    }}

    .card-text {{
      flex: 1;
      font-size: 1.22rem;
      line-height: 1.35;
      color: #1E293B;
    }}
    .card-text ul {{ list-style: none; }}
    .card-text li {{
      position: relative;
      padding-left: 20px;
      margin-bottom: 6px;
    }}
    .card-text li::before {{
      content: "•";
      position: absolute;
      left: 0;
      font-size: 1.8rem;
      line-height: 0.9;
      color: var(--accent-color);
    }}

    .code-box {{
      font-family: 'Fira Code', monospace;
      background: #F8FAFC;
      border: 2px dashed #94A3B8;
      border-radius: 8px;
      padding: 4px 10px;
      font-size: 1.05rem;
      color: #0F172A;
      display: inline-block;
      margin-top: 6px;
    }}

    .doodle-icon {{
      width: 74px;
      height: 74px;
      flex-shrink: 0;
      filter: drop-shadow(1px 2px 1px rgba(0,0,0,0.08));
    }}

    /* COORDENADAS E CORES DOS 8 CARDS ORBITANDO EM CURVA ORGÂNICA */
    .c-top-left {{
      top: 35px; left: 40px; width: 440px; min-height: 175px;
      border-color: #8B5CF6; --accent-color: #8B5CF6;
    }}
    .c-mid-left-upper {{
      top: 260px; left: 35px; width: 380px; min-height: 165px;
      border-color: #0284C7; --accent-color: #0284C7;
    }}
    .c-mid-left-lower {{
      top: 480px; left: 35px; width: 380px; min-height: 180px;
      border-color: #DC2626; --accent-color: #DC2626;
    }}
    .c-bottom-left {{
      top: 710px; left: 40px; width: 440px; min-height: 185px;
      border-color: #EA580C; --accent-color: #EA580C;
    }}

    .c-top-right {{
      top: 35px; right: 40px; width: 480px; min-height: 175px;
      border-color: #16A34A; --accent-color: #16A34A;
    }}
    .c-mid-right-upper {{
      top: 260px; right: 35px; width: 390px; min-height: 165px;
      border-color: #0D9488; --accent-color: #0D9488;
    }}
    .c-mid-right-lower {{
      top: 480px; right: 35px; width: 390px; min-height: 180px;
      border-color: #F97316; --accent-color: #F97316;
    }}
    .c-bottom-right {{
      top: 710px; right: 40px; width: 460px; min-height: 185px;
      border-color: #2563EB; --accent-color: #2563EB;
    }}
  </style>
</head>
<body>

  <!-- CAMADA DE SETAS BÉZIER ORGÂNICAS EM SVG -->
  <svg class="arrows-layer" viewBox="0 0 1536 1024">
    <defs>
      <marker id="arrow-purple" markerWidth="10" markerHeight="10" refX="6" refY="3" orient="auto">
        <path d="M0,0 L0,6 L9,3 z" fill="#8B5CF6" />
      </marker>
      <marker id="arrow-sky" markerWidth="10" markerHeight="10" refX="6" refY="3" orient="auto">
        <path d="M0,0 L0,6 L9,3 z" fill="#0284C7" />
      </marker>
      <marker id="arrow-red" markerWidth="10" markerHeight="10" refX="6" refY="3" orient="auto">
        <path d="M0,0 L0,6 L9,3 z" fill="#DC2626" />
      </marker>
      <marker id="arrow-orange" markerWidth="10" markerHeight="10" refX="6" refY="3" orient="auto">
        <path d="M0,0 L0,6 L9,3 z" fill="#EA580C" />
      </marker>
      <marker id="arrow-green" markerWidth="10" markerHeight="10" refX="6" refY="3" orient="auto">
        <path d="M0,0 L0,6 L9,3 z" fill="#16A34A" />
      </marker>
      <marker id="arrow-teal" markerWidth="10" markerHeight="10" refX="6" refY="3" orient="auto">
        <path d="M0,0 L0,6 L9,3 z" fill="#0D9488" />
      </marker>
      <marker id="arrow-coral" markerWidth="10" markerHeight="10" refX="6" refY="3" orient="auto">
        <path d="M0,0 L0,6 L9,3 z" fill="#F97316" />
      </marker>
      <marker id="arrow-blue" markerWidth="10" markerHeight="10" refX="6" refY="3" orient="auto">
        <path d="M0,0 L0,6 L9,3 z" fill="#2563EB" />
      </marker>
    </defs>

    <!-- Setas curvas partindo do centro para os 8 cards -->
    <path d="M 670, 420 C 580, 310 520, 240 485, 190" class="sketch-arrow" stroke="#8B5CF6" marker-end="url(#arrow-purple)"/>
    <path d="M 580, 465 C 520, 430 470, 390 420, 345" class="sketch-arrow" stroke="#0284C7" marker-end="url(#arrow-sky)"/>
    <path d="M 580, 535 C 520, 550 470, 560 420, 565" class="sketch-arrow" stroke="#DC2626" marker-end="url(#arrow-red)"/>
    <path d="M 670, 580 C 580, 680 520, 750 485, 790" class="sketch-arrow" stroke="#EA580C" marker-end="url(#arrow-orange)"/>

    <path d="M 865, 420 C 955, 310 1015, 240 1050, 190" class="sketch-arrow" stroke="#16A34A" marker-end="url(#arrow-green)"/>
    <path d="M 955, 465 C 1015, 430 1065, 390 1110, 345" class="sketch-arrow" stroke="#0D9488" marker-end="url(#arrow-teal)"/>
    <path d="M 955, 535 C 1015, 550 1065, 560 1110, 565" class="sketch-arrow" stroke="#F97316" marker-end="url(#arrow-coral)"/>
    <path d="M 865, 580 C 955, 680 1015, 750 1070, 790" class="sketch-arrow" stroke="#2563EB" marker-end="url(#arrow-blue)"/>
  </svg>

  <!-- NÓ CENTRAL COM RAIO DE SOL, ACENTOS E SUBLINHADO DUPLO -->
  <div class="center-container">
    <div class="center-rays">\\ | /</div>
    <div class="title-wrapper">
      <div class="title-dashes">=</div>
      <div class="center-title">{id}. {title}</div>
      <div class="title-dashes">=</div>
    </div>
    
    <svg class="center-underline" width="300" height="24" viewBox="0 0 300 24">
      <path d="M 10 7 Q 150 17 290 7" stroke="#8B5CF6" stroke-width="5" stroke-linecap="round" fill="none"/>
      <path d="M 35 17 Q 150 24 265 16" stroke="#8B5CF6" stroke-width="3" stroke-linecap="round" fill="none"/>
    </svg>

    <div class="center-definition">
      {definition}
    </div>
  </div>

  <!-- COLUNA ESQUERDA: 4 CARDS -->
  <div class="sketch-card c-top-left">
    {ribbon_top_left}
    <div class="card-body">
      {doodle_top_left}
      <div class="card-text">
        <ul>{bullets_top_left}</ul>
      </div>
    </div>
  </div>

  <div class="sketch-card c-mid-left-upper">
    {ribbon_mid_left_upper}
    <div class="card-body">
      {doodle_mid_left_upper}
      <div class="card-text">
        <ul>{bullets_mid_left_upper}</ul>
      </div>
    </div>
  </div>

  <div class="sketch-card c-mid-left-lower">
    {ribbon_mid_left_lower}
    <div class="card-body">
      {doodle_mid_left_lower}
      <div class="card-text">
        <ul>{bullets_mid_left_lower}</ul>
      </div>
    </div>
  </div>

  <div class="sketch-card c-bottom-left">
    {ribbon_bottom_left}
    <div class="card-body">
      <div class="card-text">
        <ul>{bullets_bottom_left}</ul>
      </div>
      {doodle_bottom_left}
    </div>
  </div>

  <!-- COLUNA DIREITA: 4 CARDS -->
  <div class="sketch-card c-top-right">
    {ribbon_top_right}
    <div class="card-body">
      <div class="card-text">
        <ul>{bullets_top_right}</ul>
      </div>
      {doodle_top_right}
    </div>
  </div>

  <div class="sketch-card c-mid-right-upper">
    {ribbon_mid_right_upper}
    <div class="card-body">
      <div class="card-text">
        {bullets_mid_right_upper}
      </div>
      {doodle_mid_right_upper}
    </div>
  </div>

  <div class="sketch-card c-mid-right-lower">
    {ribbon_mid_right_lower}
    <div class="card-body">
      <div class="card-text">
        <ul>{bullets_mid_right_lower}</ul>
      </div>
      {doodle_mid_right_lower}
    </div>
  </div>

  <div class="sketch-card c-bottom-right">
    {ribbon_bottom_right}
    <div class="card-body">
      <div class="card-text">
        <ul>{bullets_bottom_right}</ul>
      </div>
      {doodle_bottom_right}
    </div>
  </div>

</body>
</html>
"""

def extrair_bullets(obj) -> list:
    """Extrai lista limpa de bullets independente do formato (lista, string ou dicionario)."""
    if not obj:
        return []
    if isinstance(obj, list):
        return [str(x) for x in obj if x]
    if isinstance(obj, str):
        return [obj]
    if isinstance(obj, dict):
        if "bullets" in obj:
            return extrair_bullets(obj["bullets"])
        if "itens" in obj:
            return extrair_bullets(obj["itens"])
    return []

def renderizar_mapa_html(dados: dict, caminho_html: str):
    """Monta o HTML estilizado em altíssima fidelidade com os dados do mapa."""
    
    mid = dados.get("id", 1)
    title = dados.get("title", "CONCEITO").strip()
    definition = dados.get("definition", "").strip()
    if not definition:
        definition = f"Conceito fundamental e prático sobre {title}."

    tl = dados.get("topLeft", dados.get("top_left", {}))
    tr = dados.get("topRight", dados.get("top_right", {}))
    mr = dados.get("midRight", dados.get("mid_right", {}))
    br = dados.get("bottomRight", dados.get("bottom_right", {}))
    bc = dados.get("bottomCenter", dados.get("bottom_center", {}))
    bl = dados.get("bottomLeft", dados.get("bottom_left", {}))
    ml = dados.get("midLeft", dados.get("mid_left", {}))

    def formata_bullets(b_list):
        items = extrair_bullets(b_list)
        if not items:
            return "<li>Instrução essencial para o funcionamento do sistema.</li>"
        return "\n".join([f"<li>{it}</li>" for it in items])

    def formata_codigo(b_list):
        items = extrair_bullets(b_list)
        if not items:
            return "<p>Instrução direta e regra aplicada pelo sistema.</p>"
        html_items = []
        for it in items:
            if any(s in it for s in ["(", ")", "=", "{", "}", "print", "console", "def ", "class ", "SELECT", "import"]):
                html_items.append(f'<div class="code-box">{it}</div>')
            else:
                html_items.append(f"<p>{it}</p>")
        return "\n".join(html_items)

    # Obtenção inteligente do 8º card (Exemplo Prático)
    ex_obj = dados.get("exemploPratico", dados.get("exemplo_pratico", {}))
    ex_bullets = extrair_bullets(ex_obj.get("bullets", ex_obj))
    if not ex_bullets:
        # Extrai código de midRight ou constrói caso prático padrão
        mr_bullets = extrair_bullets(mr.get("bullets", []))
        codigo_cand = [b for b in mr_bullets if any(s in b for s in ["(", ")", "=", "{", "}", "print", "console", "def ", "class ", "SELECT"])]
        if codigo_cand:
            ex_bullets = [
                "Aplicação prática:",
                f"Código: {codigo_cand[0][:45]}",
                "Resultado imediato no terminal"
            ]
        else:
            ex_bullets = [
                "Entrada: dados ou solicitação",
                "Regra: processamento lógico",
                "Saída: solução esperada"
            ]

    # Ícones consistentes e temáticos:
    # A coluna esquerda mantém a identidade visual dos 4 pilares Sketchnote:
    doodle_tl = DOODLES["lampada"]        # 1. Ideia Central -> Sempre a Lâmpada
    doodle_ml = DOODLES["resumo"]         # 2. Resumo Expresso -> Sempre Balão de Fala
    doodle_bl = DOODLES["pegadinhas"]     # 3. Pegadinhas -> Sempre Triângulo de Alerta
    doodle_ex = DOODLES["exemplo"]        # 4. Exemplo Prático -> Sempre Prancheta com Checklist

    # A coluna direita varia contextualmente de acordo com o tema:
    doodle_tr = escolher_doodle(tr.get("pill", "MECANICA"), str(tr.get("bullets", "")), "computador")
    doodle_mr = escolher_doodle(mr.get("pill", "CODIGO"), str(mr.get("bullets", "")), "codigo")
    doodle_br = escolher_doodle(br.get("pill", "LINGUAGENS"), str(br.get("bullets", "")), "linguagens")
    doodle_bc = escolher_doodle(bc.get("pill", "FLUXO"), str(bc.get("bullets", "")), "fluxo")

    html_final = HTML_TEMPLATE_HQ.format(
        id=mid,
        title=title,
        definition=definition,
        
        # Coluna Esquerda (4 cards)
        ribbon_top_left=gerar_svg_marker_ribbon(tl.get("pill", "IDEIA CENTRAL"), "#8B5CF6"),
        doodle_top_left=doodle_tl,
        bullets_top_left=formata_bullets(tl.get("bullets", [])),

        ribbon_mid_left_upper=gerar_svg_marker_ribbon(ml.get("pill", "RESUMO EXPRESSO"), "#0284C7"),
        doodle_mid_left_upper=doodle_ml,
        bullets_mid_left_upper=formata_bullets(ml.get("bullets", [])),

        ribbon_mid_left_lower=gerar_svg_marker_ribbon(bl.get("pill", "PEGADINHAS"), "#DC2626"),
        doodle_mid_left_lower=doodle_bl,
        bullets_mid_left_lower=formata_bullets(bl.get("bullets", [])),

        ribbon_bottom_left=gerar_svg_marker_ribbon("EXEMPLO PRÁTICO", "#EA580C"),
        doodle_bottom_left=doodle_ex,
        bullets_bottom_left=formata_bullets(ex_bullets),

        # Coluna Direita (4 cards)
        ribbon_top_right=gerar_svg_marker_ribbon(tr.get("pill", "MECÂNICA"), "#16A34A"),
        doodle_top_right=doodle_tr,
        bullets_top_right=formata_bullets(tr.get("bullets", [])),

        ribbon_mid_right_upper=gerar_svg_marker_ribbon(mr.get("pill", "CÓDIGO OU REGRA"), "#0D9488"),
        doodle_mid_right_upper=doodle_mr,
        bullets_mid_right_upper=formata_codigo(mr.get("bullets", [])),

        ribbon_mid_right_lower=gerar_svg_marker_ribbon(br.get("pill", "ONDE É USADO"), "#F97316"),
        doodle_mid_right_lower=doodle_br,
        bullets_mid_right_lower=formata_bullets(br.get("bullets", [])),

        ribbon_bottom_right=gerar_svg_marker_ribbon(bc.get("pill", "FLUXO BÁSICO"), "#2563EB"),
        doodle_bottom_right=doodle_bc,
        bullets_bottom_right=formata_bullets(bc.get("bullets", []))
    )

    with open(caminho_html, "w", encoding="utf-8") as f:
        f.write(html_final)

def obter_navegador_headless():
    """Descobre o executável do Chrome ou Edge instalado na máquina."""
    candidatos = [
        r"C:\Program Files\Google\Chrome\Application\chrome.exe",
        r"C:\Program Files (x86)\Google\Chrome\Application\chrome.exe",
        r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe",
        r"C:\Program Files\Microsoft\Edge\Application\msedge.exe"
    ]
    for c in candidatos:
        if os.path.exists(c):
            return c
    raise RuntimeError("Nenhum navegador Chrome ou Edge encontrado para renderização!")

def exportar_png_headless(caminho_html: str, caminho_png: str, navegador: str = None):
    """Renderiza a página HTML em um PNG de 1536x1024 com 300 DPI sem concorrência de perfil."""
    import shutil
    if not navegador:
        navegador = obter_navegador_headless()

    caminho_abs = os.path.abspath(caminho_html).replace('\\', '/')
    url_arquivo = f"file:///{caminho_abs}"
    temp_user_data = tempfile.mkdtemp(prefix="chrome_hq_")

    cmd = [
        navegador,
        "--headless=new",
        "--disable-gpu",
        "--no-first-run",
        "--no-default-browser-check",
        "--hide-scrollbars",
        "--no-sandbox",
        "--disable-dev-shm-usage",
        f"--user-data-dir={temp_user_data}",
        "--force-device-scale-factor=1",
        "--window-size=1536,1024",
        f"--screenshot={os.path.abspath(caminho_png)}",
        url_arquivo
    ]

    try:
        subprocess.run(cmd, check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    finally:
        shutil.rmtree(temp_user_data, ignore_errors=True)

def renderizar_mapa_direto(dados: dict, caminho_png: str, navegador: str = None):
    """Recebe o dicionário com os dados do mapa e grava o PNG de alta fidelidade."""
    pasta_destino = os.path.dirname(caminho_png)
    if pasta_destino and not os.path.exists(pasta_destino):
        os.makedirs(pasta_destino, exist_ok=True)

    # Cria arquivo HTML temporário
    with tempfile.NamedTemporaryFile(suffix=".html", delete=False, mode="w", encoding="utf-8") as tmp:
        caminho_tmp_html = tmp.name

    try:
        renderizar_mapa_html(dados, caminho_tmp_html)
        exportar_png_headless(caminho_tmp_html, caminho_png, navegador=navegador)
    finally:
        if os.path.exists(caminho_tmp_html):
            try:
                os.remove(caminho_tmp_html)
            except Exception:
                pass

def renderizar_lote_escola(pasta_escola: str, limite: int = None, workers: int = 3):
    """Renderiza todas as imagens PNG de uma escola em paralelo com Chrome Headless."""
    from concurrent.futures import ThreadPoolExecutor, as_completed

    caminho_escola = os.path.join(BASE_DIR, pasta_escola)
    pasta_json = os.path.join(caminho_escola, "json")
    pasta_img = os.path.join(caminho_escola, "imagens")
    os.makedirs(pasta_img, exist_ok=True)

    if not os.path.exists(pasta_json):
        print(f"Pasta json não encontrada: {pasta_json}")
        return 0

    arquivos = sorted([f for f in os.listdir(pasta_json) if f.endswith(".json")])
    if limite:
        arquivos = arquivos[:limite]

    nav = obter_navegador_headless()
    tarefas_pendentes = []

    for arq in arquivos:
        nome_base = os.path.splitext(arq)[0]
        caminho_png = os.path.join(pasta_img, f"{nome_base}.png")
        caminho_json = os.path.join(pasta_json, arq)

        # Só adiciona na fila se ainda não foi gerado ou se for muito pequeno
        if not os.path.exists(caminho_png) or os.path.getsize(caminho_png) < 10000:
            tarefas_pendentes.append((caminho_json, caminho_png, nome_base))

    total = len(arquivos)
    pendentes = len(tarefas_pendentes)
    ja_existiam = total - pendentes

    print(f"🎨 [{pasta_escola}] Total: {total} mapas ({ja_existiam} já existiam, {pendentes} para renderizar com {workers} workers)...", flush=True)

    if not tarefas_pendentes:
        print(f"✅ {pasta_escola}: 100% das imagens já estão prontas!", flush=True)
        return total

    def _render_worker(item):
        c_json, c_png, n_base = item
        try:
            with open(c_json, "r", encoding="utf-8") as f:
                dados = json.load(f)
            renderizar_mapa_direto(dados, c_png, navegador=nav)
            return True, n_base, None
        except Exception as e:
            return False, n_base, str(e)

    gerados = 0
    with ThreadPoolExecutor(max_workers=workers) as executor:
        futuros = {executor.submit(_render_worker, item): item for item in tarefas_pendentes}
        for fut in as_completed(futuros):
            sucesso, n_base, erro = fut.result()
            if sucesso:
                gerados += 1
                if gerados % 5 == 0 or gerados == pendentes:
                    print(f"  [{ja_existiam + gerados}/{total}] {n_base}.png gerado!", flush=True)
            else:
                print(f"  [ERRO] {n_base}: {erro}", flush=True)

    print(f"✅ {pasta_escola}: {gerados} novas artes Sketchnote concluídas com sucesso.", flush=True)
    return ja_existiam + gerados

if __name__ == "__main__":
    if len(sys.argv) > 1:
        alvo = sys.argv[1]
        if alvo.endswith(".json"):
            with open(alvo, "r", encoding="utf-8") as f:
                d = json.load(f)
            saida = alvo.replace(".json", ".png")
            renderizar_mapa_direto(d, saida)
            print(f"Gerado: {saida}")
        else:
            renderizar_lote_escola(alvo)
    else:
        # Teste padrão mapa 1
        caminho_json = os.path.join(BASE_DIR, "output_mapas", "mapa_001.json")
        with open(caminho_json, "r", encoding="utf-8") as f:
            dados = json.load(f)
        png_teste = os.path.join(BASE_DIR, "teste_mapa_001_hq.png")
        renderizar_mapa_direto(dados, png_teste)
        print(f"Teste gerado: {png_teste}")
