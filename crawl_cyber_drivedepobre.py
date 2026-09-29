import urllib.request
import re
import sys
import json
import time

sys.stdout.reconfigure(encoding='utf-8')

visited = set()
cyber_results = []
all_found_items = []

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8'
}

# Palavras-chave estritas de cibersegurança real
CYBER_KEYWORDS = [
    'hacker', 'hacking', 'cyber', 'ciber', 'segurança', 'security', 'pentest', 'pentesting',
    'red team', 'blue team', 'malware', 'forense', 'forensics', 'solyd', 'desec',
    'ethical', 'burp', 'kali', 'metasploit', 'wireshark', 'nmap', 'criptografia',
    'engenharia reversa', 'reversing', 'exploit', 'vulnerabilidade', 'owasp', 'soc',
    'firewall', 'threat', 'defesa cibernética', 'segurança da informação', 'cibersegurança',
    'infosec', 'cybersecurity', 'ransomware', 'osint', 'siem', 'cisco', 'redes'
]

# Palavras de exclusão (falsos positivos)
EXCLUDE_KEYWORDS = [
    'mente', 'cerebro', 'psicologia', 'concurso', 'vestibular', 'enem',
    'afiliado', 'tráfego', 'copy', 'vendas', 'emagrecer', 'militar', 'medicina',
    'relacionamento', 'sexualidade', 'sedução', 'instagram', 'tiktok', 'shopee',
    'dropshipping', 'direito', 'nutrição', 'fitness', 'culinária', 'bolo', 'maquiagem'
]

def crawl_url(url, depth=0, max_depth=3):
    if depth > max_depth or url in visited:
        return
    visited.add(url)
    
    print(f"[{depth}] Lendo: {url}", flush=True)
    try:
        req = urllib.request.Request(url, headers=headers)
        with urllib.request.urlopen(req, timeout=8) as response:
            html = response.read().decode('utf-8', errors='ignore')
    except Exception as e:
        print(f"    [-] Falha ao acessar {url}: {e}", flush=True)
        return

    # Procura todos os links na página
    links = re.findall(r'<a[^>]*href=["\']([^"\']+)["\'][^>]*>(.*?)</a>', html, re.DOTALL)
    
    subfolders_to_visit = []
    
    for href, inner in links:
        # Limpa HTML interno
        clean_text = ' '.join(re.sub(r'<[^>]+>', ' ', inner).split()).strip()
        # Remove tags de ícones comuns do site
        for junk in ['folder', 'trending_up', 'Em alta', 'description', 'menu', 'home', 'workspace_premium', 'help_outline']:
            clean_text = clean_text.replace(junk, '').strip()
            
        if not clean_text or len(clean_text) < 3:
            continue
            
        text_lower = clean_text.lower()
        full_href = 'https://drivedepobre.com' + href if href.startswith('/') else href
        
        # Registra item
        all_found_items.append({'title': clean_text, 'url': full_href, 'parent': url})
        
        # Filtro de Cibersegurança Real
        is_cyber = any(k in text_lower for k in CYBER_KEYWORDS)
        is_excluded = any(k in text_lower for k in EXCLUDE_KEYWORDS)
        
        if is_cyber and not is_excluded:
            if not any(r['title'].lower() == clean_text.lower() for r in cyber_results):
                print(f"    ⭐ [CYBER DETECTADO] {clean_text} ({full_href})", flush=True)
                cyber_results.append({
                    'title': clean_text,
                    'url': full_href,
                    'origem': url
                })
                
        # Se for link interno de categoria/pasta, agenda para aprofundar
        if href.startswith('/tecnologia-e-programacao/') or href.startswith('/outros-cursos/') or href.startswith('/livros/'):
            if full_href not in visited and depth < max_depth:
                subfolders_to_visit.append(full_href)
                
    for sub in subfolders_to_visit:
        crawl_url(sub, depth + 1, max_depth)
        time.sleep(0.2)

if __name__ == '__main__':
    start_urls = [
        'https://drivedepobre.com/tecnologia-e-programacao',
        'https://drivedepobre.com/tecnologia-e-programacao/0JyxZvXLRWZb', # Alura
        'https://drivedepobre.com/tecnologia-e-programacao/2JRykL_TNlsR', # Cursos
        'https://drivedepobre.com/tecnologia-e-programacao/EzK-lu1zqstf', # Udemy
        'https://drivedepobre.com/tecnologia-e-programacao/ESZy5yJP54Pg', # Casa do Código
        'https://drivedepobre.com/tecnologia-e-programacao/zauw4-PIMx2m', # DevSamurai
        'https://drivedepobre.com/livros',
        'https://drivedepobre.com/outros-cursos'
    ]
    
    for u in start_urls:
        crawl_url(u, depth=1, max_depth=3)
        
    print(f"\n==========================================")
    print(f"VARREDURA CONCLUÍDA! TOTAL DE CYBER: {len(cyber_results)}")
    print(f"Total de links gerais analisados: {len(all_found_items)}")
    print(f"==========================================")
    
    with open(r'C:\Users\matheus\Desktop\computacao\drivedepobre_cyber.json', 'w', encoding='utf-8') as f:
        json.dump(cyber_results, f, ensure_ascii=False, indent=2)
