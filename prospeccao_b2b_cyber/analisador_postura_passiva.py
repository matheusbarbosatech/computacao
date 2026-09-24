# -*- coding: utf-8 -*-
"""
ANALISADOR DE POSTURA PASSIVA DE SEGURANÇA WEB (100% ÉTICO & LEGAL)
Realiza apenas requisições HTTP GET/HEAD públicas (como um navegador comum)
e avalia a presença de cabeçalhos essenciais de proteção e conformidade LGPD.
"""
import urllib.request
import urllib.parse
import ssl
import sys

def analisar_site(url):
    if not url.startswith("http://") and not url.startswith("https://"):
        url = "https://" + url

    resultado = {
        "url": url,
        "https_ativo": False,
        "hsts": False,
        "clickjacking_protegido": False,
        "x_content_type": False,
        "csp": False,
        "waf_detectado": False,
        "servidor_exposto": None,
        "tecnologia_exposta": None,
        "score": 0,
        "nota": "F",
        "pontos_criticos": [],
        "pontos_positivos": []
    }

    try:
        # Contexto SSL seguro
        ctx = ssl.create_default_context()
        ctx.check_hostname = True
        ctx.verify_mode = ssl.CERT_REQUIRED

        req = urllib.request.Request(
            url,
            headers={
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
            },
            method="GET"
        )

        with urllib.request.urlopen(req, timeout=12, context=ctx) as response:
            headers = {k.lower(): v for k, v in response.headers.items()}
            final_url = response.geturl()

            if final_url.startswith("https://"):
                resultado["https_ativo"] = True
                resultado["score"] += 30
                resultado["pontos_positivos"].append("Certificado SSL/HTTPS Ativo (Tráfego Criptografado)")
            else:
                resultado["pontos_criticos"].append("Site sem criptografia HTTPS ativa (Dados em texto puro)")

            # 1. HSTS (Strict-Transport-Security)
            if "strict-transport-security" in headers:
                resultado["hsts"] = True
                resultado["score"] += 15
                resultado["pontos_positivos"].append("Proteção HSTS configurada contra downgrade de conexão")
            else:
                resultado["pontos_criticos"].append("Falta de cabeçalho HSTS (Permite interceptação em redes Wi-Fi)")

            # 2. X-Frame-Options (Proteção contra Clickjacking e Clonagem)
            x_frame = headers.get("x-frame-options", "").lower()
            csp = headers.get("content-security-policy", "").lower()
            if x_frame in ["deny", "sameorigin"] or "frame-ancestors" in csp:
                resultado["clickjacking_protegido"] = True
                resultado["score"] += 20
                resultado["pontos_positivos"].append("Proteção contra clonagem e incorporação por terceiros (Clickjacking)")
            else:
                resultado["pontos_criticos"].append("Site vulnerável a clonagem de página e iframe oculto (Clickjacking)")

            # 3. X-Content-Type-Options
            if headers.get("x-content-type-options") == "nosniff":
                resultado["x_content_type"] = True
                resultado["score"] += 15
                resultado["pontos_positivos"].append("Proteção ativa contra ataques de tipo MIME (nosniff)")
            else:
                resultado["pontos_criticos"].append("Sem cabeçalho nosniff para impedir execução de scripts mascarados")

            # 4. Content-Security-Policy (CSP)
            if csp:
                resultado["csp"] = True
                resultado["score"] += 20
                resultado["pontos_positivos"].append("Política de Segurança de Conteúdo (CSP) implementada")
            else:
                resultado["pontos_criticos"].append("Ausência de CSP (Aumenta risco de injeção de scripts maliciosos)")

            # 5. Detecção de WAF / Proteção de Borda
            server_header = headers.get("server", "").lower()
            if "cloudflare" in server_header or "cf-ray" in headers:
                resultado["waf_detectado"] = True
                resultado["pontos_positivos"].append("Proteção de Borda Cloudflare ativa")

            # 6. Vazamento de Versões de Servidor
            if "server" in headers and any(c.isdigit() for c in headers["server"]):
                resultado["servidor_exposto"] = headers["server"]
                resultado["pontos_criticos"].append(f"Servidor expondo versão exata publicamente ({headers['server']})")

            if "x-powered-by" in headers:
                resultado["tecnologia_exposta"] = headers["x-powered-by"]
                resultado["pontos_criticos"].append(f"Linguagem/Framework exposto no cabeçalho ({headers['x-powered-by']})")

    except Exception as e:
        resultado["pontos_criticos"].append(f"Erro ao conectar ao domínio: {str(e)[:100]}")

    # Cálculo da Nota
    score = resultado["score"]
    if score >= 90:
        resultado["nota"] = "A (Excelente)"
    elif score >= 75:
        resultado["nota"] = "B (Bom)"
    elif score >= 50:
        resultado["nota"] = "C (Regular / Atenção)"
    elif score >= 30:
        resultado["nota"] = "D (Vulnerável)"
    else:
        resultado["nota"] = "F (Crítico)"

    return resultado

if __name__ == "__main__":
    url_teste = sys.argv[1] if len(sys.argv) > 1 else "google.com"
    print(f"🔍 Analisando postura de: {url_teste}")
    res = analisar_site(url_teste)
    import json
    print(json.dumps(res, indent=2, ensure_ascii=False))
