import re
import json

# Lendo os logs do task-348 e task-307
sources = [
    r'C:\Users\matheus\.gemini\antigravity-ide\brain\d0af5f42-0904-4bd1-813c-5e8765c22740\.system_generated\tasks\task-348.log',
    r'C:\Users\matheus\.gemini\antigravity-ide\brain\d0af5f42-0904-4bd1-813c-5e8765c22740\.system_generated\tasks\task-307.log',
]

EXCLUDE_PATTERNS = [
    'sociais', 'social', 'growth hacking', 'yield hacking', 'hackeando tudo',
    'memorization hack', 'cyber punk', 'cyberpunk', 'mente', 'cerebro', 'cérebro',
    'psicologia', 'concurso', 'vestibular', 'enem', 'afiliado', 'tráfego', 'trafego',
    'copy', 'vendas', 'emagrecer', 'militar', 'medicina', 'relacionamento',
    'sexualidade', 'sedução', 'seducao', 'instagram', 'tiktok', 'shopee',
    'dropshipping', 'direito', 'nutrição', 'nutricao', 'fitness', 'culinária',
    'culinaria', 'bolo', 'maquiagem', 'capcut', 'raiam santos', 'cintia chagas',
    'elias maman', 'veo3', 'edigas', 'designtex', 'stories', 'canva', 'flyers',
    'danilo', 'daniel den', 'trabalho - me passa', 'musica', 'música', 'qualitativa'
]

raw_items = {}

# Cursos essenciais mapeados manualmente da estrutura
manual_courses = [
    {"title": "Bootcamp Analista de Ataque Cibernético (Completo)", "size": "3.5 GB+", "url": "https://drivedepobre.com/tecnologia-e-programacao/arOKX82JnXjb", "cat": "Formações Completas & Bootcamps"},
    {"title": "Bootcamp Analista de Defesa Cibernética (Completo)", "size": "3.0 GB+", "url": "https://drivedepobre.com/tecnologia-e-programacao/rR0WgT9r6oKE", "cat": "Formações Completas & Bootcamps"},
    {"title": "Bootcamp Analista de Redes (Completo)", "size": "2.5 GB+", "url": "https://drivedepobre.com/tecnologia-e-programacao/V3i_3MeVohKJ", "cat": "Redes & Infraestrutura de Segurança"},
    {"title": "01 - Fundamentos em Segurança Cibernética Ofensiva", "size": "1.36 GB", "url": "https://drivedepobre.com/tecnologia-e-programacao/57KD42n4kbmh", "cat": "Ofensiva / Pentest / Red Team"},
    {"title": "03 - Ethical Hacker e Pentest", "size": "1.52 GB", "url": "https://drivedepobre.com/tecnologia-e-programacao/Xh0bnSuJ5UwH", "cat": "Ofensiva / Pentest / Red Team"},
    {"title": "04 - Análise Forense", "size": "850 MB+", "url": "https://drivedepobre.com/tecnologia-e-programacao/nFbJRz9y2B_Z", "cat": "Defensiva / Forense Digital & SOC"},
    {"title": "01 - Fundamentos em Segurança Cibernética Defensiva", "size": "788.18 MB", "url": "https://drivedepobre.com/tecnologia-e-programacao/iQ-EPbVa5Vnr", "cat": "Defensiva / Forense Digital & SOC"},
    {"title": "03 - Segurança de Infraestrutura Cloud", "size": "1.2 GB+", "url": "https://drivedepobre.com/tecnologia-e-programacao/qyEFF2XEH0w7", "cat": "Cloud, AppSec & Autenticação"},
    {"title": "04 - Segurança de Infraestrutura On-Premises", "size": "950 MB+", "url": "https://drivedepobre.com/tecnologia-e-programacao/7tA9jPvvQp16", "cat": "Redes & Infraestrutura de Segurança"},
]

for src in sources:
    try:
        with open(src, 'r', encoding='utf-8', errors='ignore') as f:
            for line in f:
                # [FOUND] [size] title -> url
                m = re.search(r'\[(?:FOUND|\+)\]\s*\[([^\]]+)\]\s*(.*?)\s*->\s*(https://drivedepobre.com/[^\s]+)', line)
                if m:
                    size, title, url = m.groups()
                    title = title.strip()
                    title_lower = title.lower()
                    if any(ex in title_lower for ex in EXCLUDE_PATTERNS):
                        continue
                    if 'enem-e-vestibulares' in url:
                        continue
                    raw_items[url] = {
                        'title': title,
                        'size': size.strip(),
                        'url': url.strip()
                    }
    except Exception as e:
        print("Erro lendo log:", e)

for item in manual_courses:
    raw_items[item['url']] = item

print(f"Total de itens filtrados sem ruído: {len(raw_items)}")

# Classificação por categoria
def categorize(item):
    if 'cat' in item:
        return item['cat']
    t = item['title'].lower()
    
    # Formações / Cursos Completos
    if any(k in t for k in ['formação hacker', 'profissao hacker', 'profissão hacker', 'hacker iniciante', 'solyd pentest profissional', 'novo pentest profissional', 'pack de segurança', 'especialista em segurança', 'curso de hackersec', 'hacker ético profissional com kali']):
        return "Formações Completas & Cursos Mestres"
    
    # Wi-Fi / Wireless / Mobile / Game Hacking
    if any(k in t for k in ['wifi', 'wi-fi', 'wireless', 'mobile', 'android', 'game hacking']):
        return "Wireless, Wi-Fi, Mobile & Game Hacking"
        
    # Pentest, Web Hacking & Exploração
    if any(k in t for k in ['pentest', 'pentesting', 'burp', 'metasploit', 'nmap', 'exploit', 'vulnerabilidade', 'web hacking', 'iniciando um contrato', 'ctf', 'black hat', 'ethical hack']):
        return "Ofensiva / Pentest / Red Team"
        
    # Forense, Defensiva & Malware
    if any(k in t for k in ['forense', 'forensics', 'malware', 'blue team', 'soc', 'siem', 'ciberseguranca', 'cibersegurança', 'segurança cibernética', 'threat', 'defesa cibernética']):
        return "Defensiva, Forense Digital, SOC & Análise de Malware"
        
    # Redes, Firewalls, Linux Security
    if any(k in t for k in ['firewall', 'pfsense', 'fortigate', 'snort', 'wireshark', 'redes', 'linux security', 'shell script para hacker', 'engenharia reversa']):
        return "Redes, Firewalls, Wireshark & Engenharia Reversa"
        
    # Cloud, AppSec, OWASP & Spring Security
    if any(k in t for k in ['owasp', 'spring security', 'cloud', 'segurança web', 'api', 'autenticacao', 'autenticação', 'ia aplicada a cibersegurança']):
        return "Cloud, AppSec, OWASP & Autenticação"
        
    return "Outros Recursos & Materiais Técnicos"

categorized = {}
for url, item in raw_items.items():
    cat = categorize(item)
    if cat not in categorized:
        categorized[cat] = []
    categorized[cat].append(item)

# Salva JSON estruturado
with open(r'C:\Users\matheus\Desktop\computacao\drivedepobre_cyber_organizado.json', 'w', encoding='utf-8') as f:
    json.dump(categorized, f, ensure_ascii=False, indent=2)

print("Categorias e contagens:")
for cat, items in categorized.items():
    print(f" - {cat}: {len(items)} itens")
