import urllib.request
import urllib.parse
import re
import json
from concurrent.futures import ThreadPoolExecutor, as_completed

CYBER_SEARCH_TERMS = [
    # Ethical Hacking / Pentest / Red Team
    'pentest', 'pentesting', 'ethical hacker', 'ethical hacking', 'hacker', 'hacking',
    'kali linux', 'metasploit', 'wireshark', 'nmap', 'burp suite', 'owasp',
    'engenharia reversa', 'reversing', 'malware', 'exploit', 'vulnerabilidade',
    'web hacking', 'wireless hacking', 'wifi hacking', 'game hacking', 'osint',
    'solyd', 'desec', 'hackersec', 'guia anonima', 'gustavo celani',
    
    # Defensive / Blue Team / Forense / SOC
    'blue team', 'red team', 'defesa cibernetica', 'ataque cibernetico',
    'analise forense', 'computacao forense', 'forense digital', 'pericia digital',
    'soc', 'siem', 'incident response', 'threat hunting', 'crowdstrike', 'snort',
    'ransomware', 'ciberseguranca', 'seguranca ofensiva', 'seguranca defensiva',
    
    # Redes, Firewalls & Infraestrutura de Segurança
    'firewall', 'pfsense', 'fortigate', 'checkpoint', 'snort',
    'analista de redes', 'seguranca de redes', 'seguranca em redes',
    'spring security', 'cloud security', 'seguranca cloud'
]

HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
}

# Falsos positivos estritos
EXCLUDE = [
    'growth hacking', 'yield hacking', 'hackeando tudo', 'memorization hack',
    'cyber punk', 'cyberpunk', 'mente', 'cerebro', 'cérebro', 'psicologia',
    'concurso', 'vestibular', 'enem', 'afiliado', 'tráfego', 'trafego',
    'copy', 'vendas', 'emagrecer', 'militar', 'medicina', 'relacionamento',
    'sexualidade', 'sedução', 'seducao', 'instagram', 'tiktok', 'shopee',
    'dropshipping', 'direito', 'nutrição', 'nutricao', 'fitness', 'culinária',
    'culinaria', 'bolo', 'maquiagem', 'capcut', 'raiam santos', 'cintia chagas',
    'elias maman', 'veo3', 'social'
]

def search_term(term, search_type):
    results = []
    url = f"https://drivedepobre.com/search?q={urllib.parse.quote(term)}&type={search_type}"
    try:
        req = urllib.request.Request(url, headers=HEADERS)
        with urllib.request.urlopen(req, timeout=8) as resp:
            html = resp.read().decode('utf-8', errors='ignore')
            
        rows = re.findall(r'<tr>\s*<td>(.*?)</td>\s*<td[^>]*>(.*?)</td>\s*<td[^>]*>(.*?)</td>\s*</tr>', html, re.DOTALL)
        for td_name, td_date, td_size in rows:
            link_match = re.search(r'href=["\']([^"\']+)["\'][^>]*>(.*?)</a>', td_name, re.DOTALL)
            if not link_match:
                continue
            href, inner = link_match.groups()
            clean_title = ' '.join(re.sub(r'<[^>]+>', ' ', inner).split()).strip()
            for junk in ['folder', 'description', 'insert_drive_file', 'image', 'picture_as_pdf']:
                clean_title = clean_title.replace(junk, '').strip()
                
            clean_date = ' '.join(re.sub(r'<[^>]+>', ' ', td_date).split()).strip()
            clean_size = ' '.join(re.sub(r'<[^>]+>', ' ', td_size).split()).strip()

            if not clean_title or len(clean_title) < 3:
                continue

            clean_lower = clean_title.lower()
            if any(ex in clean_lower for ex in EXCLUDE):
                continue

            full_url = 'https://drivedepobre.com' + href if href.startswith('/') else href
            results.append({
                'title': clean_title,
                'url': full_url,
                'size': clean_size,
                'date': clean_date,
                'term': term
            })
    except Exception as e:
        pass
    return results

if __name__ == '__main__':
    all_items = {}
    tasks = []
    with ThreadPoolExecutor(max_workers=8) as executor:
        for t in CYBER_SEARCH_TERMS:
            for st in ['all', 'folders']:
                tasks.append(executor.submit(search_term, t, st))
                
        for future in as_completed(tasks):
            res_list = future.result()
            for item in res_list:
                url = item['url']
                if url not in all_items:
                    all_items[url] = item
                    print(f"[FOUND] [{item['size']}] {item['title']} -> {url}", flush=True)

    print(f"\nTOTAL ENCONTRADO: {len(all_items)} itens.", flush=True)
    with open(r'C:\Users\matheus\Desktop\computacao\drivedepobre_cyber_final.json', 'w', encoding='utf-8') as f:
        json.dump(list(all_items.values()), f, ensure_ascii=False, indent=2)
