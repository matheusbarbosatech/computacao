import urllib.request
import re
import json
import sys

sys.stdout.reconfigure(encoding='utf-8')

def test_endpoints():
    base = 'https://drivedepobre.com'
    
    # 1. Busca na página /tecnologia-e-programacao
    req = urllib.request.Request(f'{base}/tecnologia-e-programacao', headers={'User-Agent': 'Mozilla/5.0'})
    try:
        html = urllib.request.urlopen(req).read().decode('utf-8', errors='ignore')
        print("Tecnologia page length:", len(html))
        # Extrai links de cursos de tecnologia
        tec_links = set(re.findall(r'href=["\'](/tecnologia-e-programacao/[^"\']+)["\']', html))
        print("Cursos encontrados em /tecnologia-e-programacao:", len(tec_links))
        for l in sorted(tec_links)[:30]:
            print("  ", l)
            
        # Extrai títulos de cards
        titles = re.findall(r'<h[2345][^>]*>([^<]+)</h[2345]>', html)
        print("\nTítulos na página:", len(titles))
        for t in titles[:30]:
            print("  -", t.strip())
            
    except Exception as e:
        print("Erro em tecnologia:", e)

    # 2. Testa busca por termos
    terms = ['hacker', 'cyber', 'pentest', 'segurança', 'security', 'red team', 'blue team', 'malware', 'forense', 'solyd', 'desec']
    for term in terms:
        search_urls = [
            f'{base}/api/search?q={urllib.parse.quote(term)}',
            f'{base}/busca?q={urllib.parse.quote(term)}',
            f'{base}/pesquisa?q={urllib.parse.quote(term)}',
            f'{base}/tecnologia-e-programacao?q={urllib.parse.quote(term)}'
        ]
        for s_url in search_urls:
            try:
                s_req = urllib.request.Request(s_url, headers={'User-Agent': 'Mozilla/5.0'})
                s_res = urllib.request.urlopen(s_req)
                s_data = s_res.read().decode('utf-8', errors='ignore')
                if len(s_data) > 200 and '404' not in s_data:
                    print(f"[FOUND] Endpoint {s_url} respondeu com {len(s_data)} bytes!")
                    break
            except Exception:
                pass

if __name__ == '__main__':
    test_endpoints()
