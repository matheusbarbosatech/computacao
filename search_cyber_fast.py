import urllib.request
import urllib.parse
import re
import json
import time

search_terms = [
    # General Hacker & Security
    'hacker', 'hacking', 'cyber', 'ciber', 'segurança', 'security', 'infosec', 'cibersegurança',
    # Offensive / Pentest / Red Team
    'pentest', 'pentesting', 'red team', 'ethical hacker', 'ethical hacking', 'invasão',
    'exploit', 'vulnerabilidade', 'owasp', 'burp', 'kali', 'metasploit', 'nmap', 'wireshark',
    'engenharia reversa', 'reversing', 'malware', 'shell script para hacker', 'pendrive hacker',
    # Defensive / Blue Team / SOC / Forense
    'blue team', 'soc', 'siem', 'forense', 'forensics', 'análise forense', 'incident response',
    'threat hunting', 'crowdstrike', 'snort', 'splunk', 'ransomware',
    # Networks & Infrastructure Security
    'firewall', 'pfsense', 'fortigate', 'checkpoint', 'analista de redes', 'redes', 'cisco',
    'wi-fi', 'wifi hacker', 'vpn', 'mikrotik', 'routeros',
    # Cloud & AppSec & Crypto
    'cloud security', 'segurança cloud', 'spring security', 'criptografia', 'osint',
    'solyd', 'desec', 'gustavo celani', 'guia anônima', 'hackersec'
]

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
}

# Termos que identificam falso positivo / conteúdo lixo que não é cibersegurança técnica
EXCLUDE_TERMS = [
    'mente', 'cerebro', 'cérebro', 'psicologia', 'concurso', 'vestibular', 'enem',
    'afiliado', 'tráfego', 'copy', 'vendas', 'emagrecer', 'militar', 'medicina',
    'relacionamento', 'sexualidade', 'sedução', 'instagram', 'tiktok', 'shopee',
    'dropshipping', 'direito', 'nutrição', 'fitness', 'culinária', 'bolo', 'maquiagem',
    'capcut', 'raiam santos', 'cintia chagas', 'elias maman', 'veo3'
]

all_cyber_items = {}

print("Iniciando busca profunda por Cibersegurança no Drive de Pobre...")

for term in search_terms:
    for search_type in ['all', 'folders']:
        url = f"https://drivedepobre.com/search?q={urllib.parse.quote(term)}&type={search_type}"
        try:
            req = urllib.request.Request(url, headers=headers)
            with urllib.request.urlopen(req, timeout=10) as resp:
                html = resp.read().decode('utf-8', errors='ignore')
        except Exception as e:
            # print(f"Erro buscando '{term}': {e}")
            continue

        # Extrair linhas da tabela de resultados
        rows = re.findall(r'<tr>\s*<td>(.*?)</td>\s*<td[^>]*>(.*?)</td>\s*<td[^>]*>(.*?)</td>\s*</tr>', html, re.DOTALL)
        for td_name, td_date, td_size in rows:
            # Link e Titulo
            link_match = re.search(r'href=["\']([^"\']+)["\'][^>]*>(.*?)</a>', td_name, re.DOTALL)
            if not link_match:
                continue
            href, inner = link_match.groups()
            clean_title = ' '.join(re.sub(r'<[^>]+>', ' ', inner).split()).strip()
            # Remove nomes de ícones
            for junk in ['folder', 'description', 'insert_drive_file', 'image', 'picture_as_pdf']:
                clean_title = clean_title.replace(junk, '').strip()
                
            clean_date = ' '.join(re.sub(r'<[^>]+>', ' ', td_date).split()).strip()
            clean_size = ' '.join(re.sub(r'<[^>]+>', ' ', td_size).split()).strip()

            if not clean_title or len(clean_title) < 3:
                continue

            clean_lower = clean_title.lower()

            # Checar se cai em falso positivo
            if any(ex in clean_lower for ex in EXCLUDE_TERMS):
                continue

            full_url = 'https://drivedepobre.com' + href if href.startswith('/') else href

            if full_url not in all_cyber_items:
                all_cyber_items[full_url] = {
                    'title': clean_title,
                    'url': full_url,
                    'size': clean_size,
                    'date': clean_date,
                    'matched_term': term
                }
                print(f"[+] [{clean_size}] {clean_title} -> {full_url}")
        
        time.sleep(0.15)

print(f"\n==========================================")
print(f"Total de itens autênticos de Cyber encontrados: {len(all_cyber_items)}")
print(f"==========================================")

with open(r'C:\Users\matheus\Desktop\computacao\drivedepobre_cyber_curated.json', 'w', encoding='utf-8') as f:
    json.dump(list(all_cyber_items.values()), f, ensure_ascii=False, indent=2)
