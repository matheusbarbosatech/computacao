import os
import zipfile
import re
import json

base_dir = r"C:\Users\matheus\Desktop\Ingresso FocoemSEC 4 Pilares de Cyber e Investigação Digital + Bônus - Foco em SEC"

url_pattern = re.compile(r'https?://[^\s<>"\'\)]+|www\.[^\s<>"\'\)]+')

results = {}

for root, dirs, files in os.walk(base_dir):
    for f in files:
        full_path = os.path.join(root, f)
        rel_path = os.path.relpath(full_path, base_dir)
        links = set()
        
        if f.endswith('.docx'):
            try:
                with zipfile.ZipFile(full_path, 'r') as z:
                    for name in z.namelist():
                        if name.endswith('.rels'):
                            content = z.read(name).decode('utf-8', errors='ignore')
                            for m in re.finditer(r'Target="(https?://[^"]+)"', content):
                                links.add(m.group(1))
                        if name.endswith('.xml'):
                            content = z.read(name).decode('utf-8', errors='ignore')
                            for m in url_pattern.finditer(content):
                                clean = m.group(0).rstrip('.,;:"\'()[]{}<>')
                                links.add(clean)
            except Exception as e:
                print(f"Error reading docx {rel_path}: {e}")
        
        elif f.endswith('.pdf'):
            try:
                with open(full_path, 'rb') as pdf_file:
                    raw = pdf_file.read().decode('latin-1', errors='ignore')
                    # Look for /URI in PDF objects
                    for m in re.finditer(r'/URI\s*\((https?://[^)]+)\)', raw):
                        links.add(m.group(1))
                    for m in url_pattern.finditer(raw):
                        clean = m.group(0).rstrip('.,;:"\'()[]{}<>\\/')
                        links.add(clean)
            except Exception as e:
                print(f"Error reading pdf {rel_path}: {e}")

        elif not f.endswith('.mp4'):
            try:
                with open(full_path, 'r', encoding='utf-8', errors='ignore') as txt_file:
                    content = txt_file.read()
                    for m in url_pattern.finditer(content):
                        clean = m.group(0).rstrip('.,;:"\'()[]{}<>')
                        links.add(clean)
            except Exception as e:
                pass
                
        if links:
            # Filter out schema xml namespaces like w3.org or microsoft schemas
            filtered = []
            for lk in links:
                if any(x in lk for x in ['schemas.openxmlformats.org', 'schemas.microsoft.com', 'w3.org/2001', 'purl.org', 'xml.org']):
                    continue
                filtered.append(lk)
            if filtered:
                results[rel_path] = sorted(list(set(filtered)))

output_file = r"c:\Users\matheus\Desktop\computacao\links_focoemsec.json"
with open(output_file, 'w', encoding='utf-8') as out:
    json.dump(results, out, ensure_ascii=False, indent=2)

print(f"Extracted links from {len(results)} files to {output_file}")
total_links = sum(len(l) for l in results.values())
print(f"Total links found: {total_links}")
for path, lks in results.items():
    print(f"\n[{path}] ({len(lks)} links):")
    for lk in lks[:10]:
        print(f"  - {lk}")
    if len(lks) > 10:
        print(f"  ... e mais {len(lks)-10} links")
