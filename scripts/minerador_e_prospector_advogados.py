# -*- coding: utf-8 -*-
"""
🤖 MINERADOR & PROSPECTOR AUTÔNOMO DE ESCRITÓRIOS DE ADVOCACIA
=============================================================================
Este script automatiza a esteira de prospecção para serviços de
Inteligência Patrimonial & Perícia Forense Digital:
1. Minera escritórios de advocacia em Campo Grande e Zona Oeste (RJ).
2. Evita duplicidade e salva em LEADS_ADVOGADOS_CAMPO_GRANDE.json.
3. Gera links diretos de WhatsApp com mensagens altamente persuasivas.
4. Mantém controle de status de abordagem e follow-up.
=============================================================================
"""

import os
import sys
import json
import urllib.parse
import urllib.request
import argparse
from datetime import datetime

sys.stdout.reconfigure(encoding='utf-8')
sys.stderr.reconfigure(encoding='utf-8')

BASE_DIR = r"c:\Users\mathe\Desktop\computacao"
LEADS_FILE = os.path.join(BASE_DIR, "AGENCIA_INTELIGENCIA_FORENSE", "LEADS_ADVOGADOS_CAMPO_GRANDE.json")

def carregar_leads():
    if os.path.exists(LEADS_FILE):
        try:
            with open(LEADS_FILE, "r", encoding="utf-8") as f:
                return json.load(f)
        except Exception:
            pass
    return []

def salvar_leads(leads):
    os.makedirs(os.path.dirname(LEADS_FILE), exist_ok=True)
    with open(LEADS_FILE, "w", encoding="utf-8") as f:
        json.dump(leads, f, indent=2, ensure_ascii=False)

def gerar_mensagem_whatsapp(nome_escritorio, responsavel):
    tratamento = responsavel if responsavel and "Dr" in responsavel else f"Equipe da {nome_escritorio}"
    
    msg = (
        f"Olá, {tratamento}, tudo bem?\n\n"
        f"Meu nome é Matheus, atuo com Inteligência em Fontes Abertas (OSINT) e Investigação Patrimonial "
        f"aplicada ao suporte probatório para escritórios de advocacia aqui da Zona Oeste / RJ.\n\n"
        f"Acompanho a dificuldade recorrente nas ações de Execução e Família no TJ-RJ em localizar bens "
        f"de devedores que utilizam laranjas, empresas paralelas e ocultação patrimonial para frustrar a penhora.\n\n"
        f"Desenvolvemos uma metodologia pericial que cruza registros societários profundos, vínculos familiares, "
        f"rastreamento veicular e padrão de vida digital para fundamentar pedidos de penhora e desconsideração da personalidade jurídica.\n\n"
        f"Temos um modelo anonimizado de Dossiê Patrimonial de 3 páginas demonstrando a estrutura das provas que entregamos. "
        f"Posso te encaminhar o PDF de exemplo aqui pelo WhatsApp para o senhor(a) conhecer?"
    )
    return msg

def gerar_link_whatsapp(telefone_raw, mensagem):
    # Limpa apenas dígitos
    tel_limpo = "".join([c for c in str(telefone_raw) if c.isdigit()])
    if not tel_limpo:
        return ""
    if len(tel_limpo) in [10, 11] and not tel_limpo.startswith("55"):
        tel_limpo = "55" + tel_limpo
    
    texto_encoded = urllib.parse.quote(mensagem)
    return f"https://api.whatsapp.com/send?phone={tel_limpo}&text={texto_encoded}"

def minerar_osm_campo_grande():
    """
    Minera escritórios de advocacia em Campo Grande RJ usando a API pública do Overpass / OpenStreetMap
    """
    print("🔍 [MINERADOR] Consultando OpenStreetMap para escritórios de advocacia em Campo Grande (RJ)...")
    
    # Bounding Box de Campo Grande RJ aprox: -22.95 a -22.85 (lat) e -43.62 a -43.52 (lon)
    overpass_query = """
    [out:json][timeout:25];
    (
      node["office"="lawyer"](-22.95, -43.65, -22.85, -43.50);
      way["office"="lawyer"](-22.95, -43.65, -22.85, -43.50);
    );
    out body;
    >;
    out skel qt;
    """
    url = "https://overpass-api.de/api/interpreter"
    data = urllib.parse.urlencode({'data': overpass_query}).encode('utf-8')
    
    try:
        req = urllib.request.Request(url, data=data, headers={'User-Agent': 'AgenciaInteligenciaBot/1.0'})
        with urllib.request.urlopen(req, timeout=30) as response:
            res_json = json.loads(response.read().decode('utf-8'))
            elementos = res_json.get("elements", [])
            print(f"📦 Elementos brutos encontrados: {len(elementos)}")
            
            leads_existentes = carregar_leads()
            nomes_existentes = {l.get("nome_escritorio", "").lower().strip() for l in leads_existentes}
            
            novos = 0
            for el in elementos:
                tags = el.get("tags", {})
                nome = tags.get("name")
                if not nome:
                    continue
                if nome.lower().strip() in nomes_existentes:
                    continue
                
                rua = tags.get("addr:street", "")
                num = tags.get("addr:housenumber", "")
                bairro = tags.get("addr:suburb", "Campo Grande")
                endereco = f"{rua}, {num} - {bairro}".strip(", -")
                tel = tags.get("phone") or tags.get("contact:phone") or tags.get("contact:whatsapp") or ""
                
                novo_lead = {
                    "id": f"lead_osm_{len(leads_existentes) + 1:03d}",
                    "nome_escritorio": nome,
                    "responsavel": f"Dr(a). Responsável ({nome})",
                    "endereco": endereco if endereco else "Campo Grande, RJ",
                    "telefone": tel,
                    "whatsapp": "".join([c for c in tel if c.isdigit()]),
                    "areas_atuacao": ["Direito Civil", "Execução", "Família"],
                    "status": "Pronto para Abordagem",
                    "gatilho_dor": "Cobrança de dívidas e localização de patrimônio",
                    "data_adicionado": datetime.now().strftime("%Y-%m-%d")
                }
                leads_existentes.append(novo_lead)
                nomes_existentes.add(nome.lower().strip())
                novos += 1
                
            salvar_leads(leads_existentes)
            print(f"🎉 Novos escritórios adicionados à base: {novos}")
    except Exception as e:
        print(f"⚠️ Erro ao consultar base pública: {e}")

def listar_esteira():
    leads = carregar_leads()
    print("=" * 80)
    print(f"📋 ESTEIRA DE PROSPECÇÃO DE ADVOGADOS — TOTAL: {len(leads)} ESCRITÓRIOS")
    print("=" * 80)
    
    prontos = [l for l in leads if l.get("status") == "Pronto para Abordagem"]
    print(f"🎯 Prontos para contato hoje: {len(prontos)}\n")
    
    for idx, lead in enumerate(leads, 1):
        nome = lead.get("nome_escritorio")
        resp = lead.get("responsavel")
        tel = lead.get("whatsapp") or lead.get("telefone") or "Não informado"
        end = lead.get("endereco")
        status = lead.get("status")
        
        msg = gerar_mensagem_whatsapp(nome, resp)
        link = gerar_link_whatsapp(tel, msg) if tel != "Não informado" else "Sem WhatsApp direto cadastrado"
        
        print(f"[{idx:02d}] 🏛️ {nome}")
        print(f"     👤 Contato: {resp} | 📞 Tel: {tel}")
        print(f"     📍 Endereço: {end}")
        print(f"     📊 Status: {status}")
        if link.startswith("http"):
            print(f"     👉 Link de Envio Rápido: {link[:75]}...")
        print("-" * 80)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Prospector de Advogados para Inteligência Patrimonial")
    parser.add_argument("--minerar", action="store_true", help="Minera novos escritórios na região")
    parser.add_argument("--listar", action="store_true", help="Lista todos os leads e gera links de WhatsApp")
    args = parser.parse_args()

    if args.minerar:
        minerar_osm_campo_grande()
    elif args.listar:
        listar_esteira()
    else:
        # Padrão: lista
        listar_esteira()
