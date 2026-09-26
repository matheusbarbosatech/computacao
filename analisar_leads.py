# -*- coding: utf-8 -*-
import json
import sys

sys.stdout.reconfigure(encoding='utf-8')

with open('comercios_campo_grande.json', 'r', encoding='utf-8') as f:
    items = json.load(f)

print(f"Total itens mapeados: {len(items)}")

non_schools = [it for it in items if it['categoria'] != 'school']
print(f"Comércios e serviços privados: {len(non_schools)}")

for it in non_schools:
    print(f"- [{it['categoria']}] {it['nome']} | End: {it['endereco']} | Tel: {it['telefone']} | Site: {it['website']}")
