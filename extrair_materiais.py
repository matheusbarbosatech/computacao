# -*- coding: utf-8 -*-
import subprocess
import json
import sys
import os

sys.stdout.reconfigure(encoding='utf-8')

courses = [
    '04. 🌟 Marketing, Copy & Tráfego/Código do Produto Viral Workshop + Vitrine de Produtos Virais + IA DNA VIRAL',
    '04. 🌟 Marketing, Copy & Tráfego/Formação Copywriter de anúncios - Anthony Carreiro',
    '04. 🌟 Marketing, Copy & Tráfego/Venda Todo Santo Dia 2026 (Regravação)',
    '02. 💻 Programação & Desenvolvimento/Dev de Oferta | O Roadmap'
]

root_id = '1cBDvRvFL4B5TmD7oXYfcTYvlHl40GXGG'
found_files = {}

for c in courses:
    c_name = c.split('/')[-1]
    print(f"Varrendo curso: {c_name}...")
    cmd = ['rclone', 'lsf', '-R', f'meudrive,root_folder_id={root_id}:{c}']
    res = subprocess.run(cmd, capture_output=True, text=True, encoding='utf-8')
    lines = [l.strip() for l in res.stdout.splitlines() if l.strip() and not l.endswith('/')]
    txt_and_docs = [l for l in lines if any(l.lower().endswith(ext) for ext in ['.txt', '.pdf', '.doc', '.docx', '.json'])]
    found_files[c] = {
        'total_arquivos': len(lines),
        'documentos': txt_and_docs
    }
    print(f"  Total arquivos: {len(lines)} | Documentos/Textos: {len(txt_and_docs)}")

with open('materiais_marketing_encontrados.json', 'w', encoding='utf-8') as f:
    json.dump(found_files, f, ensure_ascii=False, indent=2)

print("Materiais mapeados com sucesso!")
