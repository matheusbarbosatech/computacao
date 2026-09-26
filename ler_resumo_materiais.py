# -*- coding: utf-8 -*-
import json
import sys

sys.stdout.reconfigure(encoding='utf-8')

with open('materiais_marketing_encontrados.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

for c, info in data.items():
    name = c.split('/')[-1]
    print(f"=== {name} ({len(info['documentos'])} docs) ===")
    for doc in info['documentos'][:12]:
        print(f"  * {doc}")
