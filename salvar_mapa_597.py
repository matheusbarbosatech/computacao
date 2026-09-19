"""
Script para salvar o mapa 597 completando exatamente os 700 mapas mentais do catálogo.
"""
import os
import json

dados_597 = {
  "id": 597,
  "title": "OS 4 TIPOS DE BANCOS NOSQL",
  "definition": "Bancos de dados não-relacionais modelados para formatos específicos de dados com alta performance e escalabilidade.",
  "topLeft": {
    "pill": "IDEIA CENTRAL",
    "icon": "💡",
    "bullets": [
      "Nem todo dado cabe numa planilha: o NoSQL traz formatos sob medida para velocidade e flexibilidade.",
      "Cada tipo resolve um problema de armazenamento diferente."
    ]
  },
  "topRight": {
    "pill": "OS 4 FORMATOS",
    "icon": "🗄️",
    "bullets": [
      "1. Documento (JSON flexível - MongoDB)",
      "2. Chave-Valor (Rápido em memória - Redis)",
      "3. Colunas (Big Data massivo - Cassandra)",
      "4. Grafos (Redes e conexões - Neo4j)"
    ]
  },
  "midRight": {
    "pill": "CÓDIGO OU REGRA",
    "icon": "{ }",
    "bullets": [
      "Exemplo em Banco de Documento (JSON):",
      "db.usuarios.insertOne({ nome: 'Ana', tags: ['dev', 'ia'] })"
    ]
  },
  "bottomRight": {
    "pill": "ONDE É USADO",
    "icon": "</>",
    "bullets": [
      "Redis: Sessões de login e carrinhos de compra.",
      "MongoDB: Catálogos de e-commerce e posts de blogs.",
      "Neo4j: Redes sociais e detecção de fraudes."
    ]
  },
  "bottomCenter": {
    "pill": "FLUXO DE ESCOLHA",
    "icon": "⚙️",
    "bullets": [
      "PASSO 1: Analise como o dado é estruturado e acessado",
      "PASSO 2: Avalie o volume de leitura vs escrita por segundo",
      "PASSO 3: Escolha o NoSQL especialista para essa função"
    ]
  },
  "bottomLeft": {
    "pill": "PEGADINHAS",
    "icon": "⚠️",
    "bullets": [
      "Achar que NoSQL substitui SQL em tudo (cada um tem seu propósito).",
      "Esquecer que bancos NoSQL priorizam velocidade sobre integridade ACID estrita."
    ]
  },
  "midLeft": {
    "pill": "RESUMO EXPRESSO",
    "icon": "💬",
    "bullets": [
      "JSON (Documento) ➔ Cache (Chave-Valor) ➔ Big Data (Colunas) ➔ Relações (Grafos)"
    ]
  },
  "exemploPratico": {
    "bullets": [
      "Documento: armazena objeto completo em JSON",
      "Chave-Valor: GET 'user:123' em milissegundos",
      "Grafo: conecta Usuário -> AmigoDe -> Usuário"
    ]
  },
  "_modelo_usado": "claude-sonnet-5[1m]",
  "modulo": "Banco de Dados e IA",
  "escola": "06_banco_dados_e_ia",
  "foco_pedagogico": "MongoDB, Redis, Cassandra e Neo4j explicados com clareza visual"
}

base_dir = os.path.dirname(os.path.abspath(__file__))
p1 = os.path.join(base_dir, "output_mapas", "mapa_597.json")
p2 = os.path.join(base_dir, "06_banco_dados_e_ia", "json", "mapa_597.json")

os.makedirs(os.path.dirname(p1), exist_ok=True)
os.makedirs(os.path.dirname(p2), exist_ok=True)

with open(p1, "w", encoding="utf-8") as f:
    json.dump(dados_597, f, indent=2, ensure_ascii=False)

with open(p2, "w", encoding="utf-8") as f:
    json.dump(dados_597, f, indent=2, ensure_ascii=False)

print("[OK] Mapa 597 salvo em ambos os locais!")
