# -*- coding: utf-8 -*-
"""
RADAR AUTOMÁTICO DE NOTÍCIAS DE GOLPES, FRAUDES E SEGURANÇA DIGITAL
Coleta feeds de notícias em tempo real no Brasil, identifica novos golpes
e gera automaticamente roteiros virais para TikTok/Reels e palestras comunitárias.
"""
import urllib.request
import xml.etree.ElementTree as ET
import json
import os
import sys
import re
from datetime import datetime

sys.stdout.reconfigure(encoding='utf-8', errors='ignore')
sys.stderr.reconfigure(encoding='utf-8', errors='ignore')

FEEDS = [
    {"nome": "G1 Tecnologia", "url": "https://g1.globo.com/rss/g1/tecnologia/"},
    {"nome": "TecMundo", "url": "https://rss.tecmundo.com.br/feed"},
    {"nome": "Olhar Digital", "url": "https://olhardigital.com.br/feed/"},
    {"nome": "The Hack", "url": "https://thehack.com.br/feed/"},
    {"nome": "CISO Advisor", "url": "https://cisoadvisor.com.br/feed/"}
]

PALAVRAS_CHAVE = [
    "golpe", "fraude", "falso", "falsa", "pix", "whatsapp", "clonagem", "clonado",
    "phishing", "banco", "vazamento", "deepfake", "invasão", "sequestro", "hacker",
    "estelionato", "alerta", "malware", "vírus", "espeto", "ligação", "sms"
]

def limpar_tags_html(texto):
    if not texto:
        return ""
    clean = re.sub(r'<[^>]+>', '', texto)
    return clean.replace("&quot;", '"').replace("&apos;", "'").replace("&amp;", "&").strip()

def buscar_alertas_golpes():
    alertas = []
    headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"}

    for f in FEEDS:
        try:
            req = urllib.request.Request(f["url"], headers=headers)
            with urllib.request.urlopen(req, timeout=10) as resp:
                xml_data = resp.read()
                root = ET.fromstring(xml_data)

                # RSS 2.0 (channel -> item) ou Atom (entry)
                itens = root.findall(".//item")
                for item in itens[:15]:
                    titulo = item.findtext("title", "")
                    link = item.findtext("link", "")
                    desc = item.findtext("description", "")
                    pub_date = item.findtext("pubDate", "")

                    texto_completo = f"{titulo} {desc}".lower()

                    # Verifica se o texto tem relevância com golpes ou segurança do cidadão
                    matches = [k for k in PALAVRAS_CHAVE if k in texto_completo]
                    if matches:
                        alertas.append({
                            "fonte": f["nome"],
                            "titulo": limpar_tags_html(titulo),
                            "descricao": limpar_tags_html(desc)[:250] + "...",
                            "link": link.strip(),
                            "gatilhos": list(set(matches)),
                            "data": pub_date
                        })
        except Exception as e:
            # Falha de rede ou timeout em algum feed específico
            pass

    return alertas

def gerar_roteiro_viral_video(alerta):
    """Gera um roteiro pronto de 60 segundos focado em proteção familiar e viralização"""
    titulo = alerta["titulo"]
    return f"""### 🚨 ROTEIRO VIRAL: {titulo}
**Duração:** 50 a 60 segundos | **Formato:** 9:16 (Vertical)

* **[00:00 - 00:05] GANCHO HIPNÓTICO (Olhando firme pra câmera):**
  > "Se você tem conta em banco ou usa o WhatsApp todo dia, para tudo e presta muita atenção nesse alerta que acabou de sair."

* **[00:05 - 00:20] O NOVO GOLPE NA PRÁTICA (A História Real):**
  > "Criminosos estão usando {alerta['gatilhos'][0] if alerta['gatilhos'] else 'mensagens falsas'} pra enganar milhares de brasileiros. Funciona assim: você recebe uma mensagem que parece 100% real dizendo que {alerta['descricao'][:120]}..."

* **[00:20 - 00:40] A ENGENHARIA REVERSA DO GOLPE (Onde está o truque):**
  > "O detalhe que entrega o bandido é que eles criam um senso de urgência absurdo pra você não pensar. O link parece do banco, mas na verdade tem uma letrinha trocada ou pede confirmação de código."

* **[00:40 - 00:52] A BLINDAGEM (O que fazer agora mesmo):**
  > "Regra de ouro: Banco NUNCA liga pedindo pra você fazer transferência teste, e parente NUNCA pede dinheiro urgente por número novo sem ligar por vídeo. Nunca clique em link recebido por SMS ou WhatsApp!"

* **[00:52 - 01:00] CHAMADA DE PROTEÇÃO FAMILIAR (Viraliza no WhatsApp):**
  > "Manda esse vídeo agora no grupo da sua família e da sua igreja pra proteger quem você ama antes que seja tarde. Me segue aqui pra manter seu celular blindado!"
"""

def salvar_painel(alertas):
    base_dir = os.path.dirname(os.path.abspath(__file__))
    project_dir = os.path.dirname(base_dir)

    # 1. Salvar JSON estruturado
    json_path = os.path.join(project_dir, "radar_golpes_conteudo.json")
    with open(json_path, "w", encoding="utf-8") as f:
        json.dump(alertas, f, ensure_ascii=False, indent=2)

    # 2. Gerar Painel Markdown com roteiros
    md_path = os.path.join(project_dir, "PAINEL_ALERTAS_GOLPES_VIRAL.md")
    with open(md_path, "w", encoding="utf-8") as f:
        f.write("# 🚨 Painel Radar: Alertas de Golpes & Segurança para Famílias\n\n")
        f.write(f"> **Última Atualização:** {datetime.now().strftime('%d/%m/%Y %H:%M')}\n")
        f.write("> Notícias mineradas automaticamente para alimentar vídeos curtos e palestras comunitárias.\n\n---\n\n")

        f.write("## 📰 Notícias Quentes Mineradas Hoje\n\n")
        for i, a in enumerate(alertas[:8], 1):
            f.write(f"### {i}. {a['titulo']}\n")
            f.write(f"* **Fonte:** {a['fonte']} | **Gatilhos:** `{', '.join(a['gatilhos'])}`\n")
            f.write(f"* **Resumo:** {a['descricao']}\n")
            f.write(f"* [Ler Notícia Completa]({a['link']})\n\n")
            f.write(gerar_roteiro_viral_video(a))
            f.write("\n---\n\n")

    print(f"✅ Radar atualizado com sucesso! {len(alertas)} notícias de golpes encontradas.")
    print(f"📄 Arquivo gerado: {md_path}")

if __name__ == "__main__":
    print("🔍 Varrendo feeds brasileiros de segurança e tecnologia contra golpes...")
    alertas = buscar_alertas_golpes()
    salvar_painel(alertas)
