import urllib.request
import re
import json
import sys

sys.stdout.reconfigure(encoding='utf-8')

def extract_tec_page():
    url = "https://drivedepobre.com/tecnologia-e-programacao"
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
        'Accept-Language': 'pt-BR,pt;q=0.9,en-US;q=0.8,en;q=0.7'
    }
    req = urllib.request.Request(url, headers=headers)
    try:
        html = urllib.request.urlopen(req, timeout=15).read().decode('utf-8', errors='ignore')
        print(f"Total HTML: {len(html)} bytes")
        
        # Procura scripts com JSON ou dados embutidos
        json_matches = re.findall(r'<script[^>]*type=["\']application/json["\'][^>]*>(.*?)</script>', html, re.DOTALL)
        for j in json_matches:
            print(f"JSON script encontrado ({len(j)} bytes)")
            
        # Procura cards / links
        cards = re.findall(r'<a[^>]*href=["\'](/tecnologia-e-programacao/[^"\']+)["\'][^>]*>(.*?)</a>', html, re.DOTALL)
        print(f"Links em /tecnologia-e-programacao: {len(cards)}")
        for href, inner in cards:
            clean_text = re.sub(r'<[^>]+>', ' ', inner).strip()
            clean_text = ' '.join(clean_text.split())
            if clean_text:
                print(f"  [{href}] -> {clean_text}")
                
        # Se não achou links com /tecnologia-e-programacao/, procura todos os links internos
        all_links = re.findall(r'<a[^>]*href=["\']([^"\']+)["\'][^>]*>(.*?)</a>', html, re.DOTALL)
        print(f"\nTotal de todos os links na pagina: {len(all_links)}")
        for href, inner in all_links:
            clean_text = ' '.join(re.sub(r'<[^>]+>', ' ', inner).split()).strip()
            if any(k in clean_text.lower() or k in href.lower() for k in ['hack', 'sec', 'cyber', 'seguran', 'rede', 'linux', 'cloud', 'pentest']):
                print(f"  * CYBER MATCH: [{href}] -> {clean_text}")

    except Exception as e:
        print("Erro:", e)

if __name__ == '__main__':
    extract_tec_page()
