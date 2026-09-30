import os
import shutil
import glob
import json

DESKTOP = r"C:\Users\matheus\Desktop"
SRC_DIR = r"C:\Users\matheus\Desktop\computacao\nutror_extractor\transcricoes_limpas"
DEST_TRANS = os.path.join(DESKTOP, "Clube_do_Consultor_Transcricoes")

os.makedirs(DEST_TRANS, exist_ok=True)

# 1. Copiar todas as 32 transcrições
src_files = sorted(glob.glob(os.path.join(SRC_DIR, "*.txt")))
print(f"Encontrados {len(src_files)} arquivos de transcrição.")

consolidated_text = []
lessons_data = []

for f in src_files:
    fname = os.path.basename(f)
    dest_path = os.path.join(DEST_TRANS, fname)
    shutil.copy2(f, dest_path)
    
    with open(f, "r", encoding="utf-8", errors="ignore") as fp:
        content = fp.read().strip()
        
    consolidated_text.append(f"================================================================================\n=== {fname.upper()} ===\n================================================================================\n\n{content}\n\n")
    
    # Extrair título ou primeiras linhas
    first_few = content[:300].replace('\n', ' ')
    lessons_data.append({
        "id": fname.replace(".txt", ""),
        "file": fname,
        "size": len(content),
        "preview": first_few,
        "content": content
    })

# Salvar arquivo consolidado no Desktop
consolidated_file = os.path.join(DEST_TRANS, "00_TODAS_AS_32_AULAS_CONSOLIDADAS.txt")
with open(consolidated_file, "w", encoding="utf-8") as fp:
    fp.write("".join(consolidated_text))
print(f"Salvo arquivo consolidado: {consolidated_file}")

# Salvar também uma cópia direta do consolidado no Desktop
shutil.copy2(consolidated_file, os.path.join(DESKTOP, "Clube_do_Consultor_32_Aulas_Consolidadas.txt"))

print("Todas as 32 transcrições copiadas com sucesso para o Desktop!")
