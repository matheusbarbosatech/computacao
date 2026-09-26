#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
🛡️ SentinelSOC Live: Mini-SOC & Scanner de Segurança Cibernética em Tempo Real
Desenvolvido para Aprendizado Prático Baseado em Problemas (PBL)
100% Python Nativo (Sem dependências externas para execução instantânea)
"""

import http.server
import socketserver
import threading
import json
import urllib.parse
import socket
import ssl
import time
import re
import os
import sys
from datetime import datetime

PORT_DASHBOARD = 9090
PORT_HONEYPOT = 9091

# Estado global em memória do SOC
soc_state = {
    "total_requests": 0,
    "total_threats_blocked": 0,
    "blacklisted_ips": set(),
    "recent_events": [],
    "attack_stats": {
        "SQLi": 0,
        "XSS": 0,
        "Path Traversal (LFI)": 0,
        "Command Injection": 0,
        "Brute Force": 0,
        "Port Scan / Recon": 0,
        "Anomalous User-Agent": 0
    },
    "ip_request_history": {},  # {ip: [timestamps]}
    "missions_completed": {
        "mission_sqli": False,
        "mission_xss": False,
        "mission_bruteforce": False,
        "mission_lfi": False,
        "mission_scanner": False
    }
}

# Regras de Detecção de Ameaças (Inspiradas em WAF / Snort / OWASP CRS)
DETECTION_RULES = [
    {
        "name": "SQL Injection (SQLi)",
        "mitre_id": "T1190",
        "mitre_name": "Exploit Public-Facing Application",
        "severity": "CRITICAL",
        "regex": r"(?i)(\b(SELECT|UNION|INSERT|UPDATE|DELETE|DROP|ALTER|CREATE|TABLE|DATABASE|WHERE|OR|AND)\b.*\b(FROM|INTO|WHERE|TABLE|--|\#|\/\*))|(\b(OR|AND)\s+['\"]?1['\"]?\s*=\s*['\"]?1)|(';\s*--)|(--\s*$)|(\bUNION\s+ALL\s+SELECT\b)|(\bSLEEP\(\d+\))",
        "category": "SQLi"
    },
    {
        "name": "Cross-Site Scripting (XSS)",
        "mitre_id": "T1059.007",
        "mitre_name": "JavaScript Execution",
        "severity": "HIGH",
        "regex": r"(?i)(<script.*?>.*?</script>)|(<.*?on\w+\s*=\s*['\"].*?['\"])|\b(javascript:|vbscript:|data:text/html)|(<img\s+src=.*?onerror=)|(<svg.*?onload=)|(alert\(|prompt\(|confirm\()",
        "category": "XSS"
    },
    {
        "name": "Path Traversal & Local File Inclusion (LFI)",
        "mitre_id": "T1083",
        "mitre_name": "File and Directory Discovery",
        "severity": "HIGH",
        "regex": r"(\.\.[\/\\]|\/etc\/(passwd|shadow|hosts)|windows[\/\\]win\.ini|boot\.ini|\.\.%2f|\.\.%5c)",
        "category": "Path Traversal (LFI)"
    },
    {
        "name": "Command Injection (RCE)",
        "mitre_id": "T1059",
        "mitre_name": "Command and Scripting Interpreter",
        "severity": "CRITICAL",
        "regex": r"(?i)(;\s*(cat|ls|id|whoami|pwd|uname|dir|netstat|powershell|cmd\.exe|wget|curl|nc|bash|sh)\b)|(\|\s*(cat|ls|id|whoami|pwd|dir)\b)|(`.*?`)|(\$\(.*?\))",
        "category": "Command Injection"
    },
    {
        "name": "Scanner / Reconnaissance Tool",
        "mitre_id": "T1595",
        "mitre_name": "Active Scanning",
        "severity": "MEDIUM",
        "regex": r"(?i)(sqlmap|nikto|nmap|dirbuster|gobuster|ffuf|acunetix|wpscan|masscan|nuclei|nessus|openvas|hydra|burpcollaborator)",
        "category": "Port Scan / Recon"
    }
]

def analyze_payload(raw_data, user_agent="", path=""):
    """Motor de Inspeção Profunda de Pacotes (DPI / IDS)"""
    combined_target = f"{path} {raw_data} {user_agent}"
    detected_threats = []
    
    for rule in DETECTION_RULES:
        if re.search(rule["regex"], combined_target):
            detected_threats.append(rule)
            
    return detected_threats

def log_soc_event(event_type, source_ip, method, path, payload, threats, action_taken="BLOCKED"):
    """Registra evento com enriquecimento de dados MITRE ATT&CK"""
    soc_state["total_requests"] += 1
    
    severity = "INFO"
    mitre_info = "N/A"
    
    if threats:
        soc_state["total_threats_blocked"] += 1
        severities = [t["severity"] for t in threats]
        if "CRITICAL" in severities:
            severity = "CRITICAL"
        elif "HIGH" in severities:
            severity = "HIGH"
        else:
            severity = "MEDIUM"
            
        categories = [t["category"] for t in threats]
        for cat in categories:
            if cat in soc_state["attack_stats"]:
                soc_state["attack_stats"][cat] += 1
                
        mitre_info = ", ".join([f"{t['mitre_id']} ({t['name']})" for t in threats])
    else:
        if action_taken == "BLOCKED_IP":
            severity = "CRITICAL"
            mitre_info = "IP Quarantined (SOAR Auto-Response)"
            
    event = {
        "id": len(soc_state["recent_events"]) + 1,
        "timestamp": datetime.now().strftime("%H:%M:%S.%f")[:-3],
        "source_ip": source_ip,
        "method": method,
        "path": path,
        "payload": payload[:120] + ("..." if len(payload) > 120 else ""),
        "severity": severity,
        "threats": [t["name"] for t in threats] if threats else [],
        "mitre": mitre_info,
        "action": action_taken
    }
    
    soc_state["recent_events"].insert(0, event)
    if len(soc_state["recent_events"]) > 200:
        soc_state["recent_events"].pop()
        
    return event

# ==========================================
# 1. HONEYPOT SERVER (Porta 9091)
# Servidor isca realista que atrai e analisa invasores
# ==========================================
class HoneypotHTTPHandler(http.server.BaseHTTPRequestHandler):
    def log_message(self, format, *args):
        pass  # Silencia logs padrão no console para não poluir
        
    def check_rate_limit(self, client_ip):
        now = time.time()
        history = soc_state["ip_request_history"].get(client_ip, [])
        # Mantém apenas requisições dos últimos 5 segundos
        history = [t for t in history if now - t < 5.0]
        history.append(now)
        soc_state["ip_request_history"][client_ip] = history
        
        # Se mais de 8 requisições em 5 segundos -> Alerta de Força Bruta / Flood
        if len(history) > 8:
            return True
        return False

    def handle_request(self, method):
        client_ip = self.client_address[0]
        path = self.path
        user_agent = self.headers.get("User-Agent", "Unknown")
        
        # Leitura do Body se existir
        content_length = int(self.headers.get('Content-Length', 0))
        body = ""
        if content_length > 0:
            body = self.rfile.read(content_length).decode('utf-8', errors='ignore')
            
        full_query = urllib.parse.unquote(path)
        
        # Verifica se o IP está em quarentena (Blacklist)
        if client_ip in soc_state["blacklisted_ips"]:
            log_soc_event("CONNECTION_ATTEMPT", client_ip, method, path, body or full_query, [], "DROPPED (BLACKLISTED)")
            self.send_response(403)
            self.send_header("Content-Type", "application/json")
            self.end_headers()
            self.wfile.write(json.dumps({"status": "error", "message": "Access Denied: Your IP is quarantined by SentinelSOC."}).encode())
            return
            
        # 1. Verificação de Força Bruta / Rate Limit
        is_bruteforcing = self.check_rate_limit(client_ip)
        
        # 2. Análise de Ameaças em Tempo Real
        threats = analyze_payload(body + " " + full_query, user_agent, path)
        
        if is_bruteforcing:
            threats.append({
                "name": "High Rate / Brute Force Attempt",
                "mitre_id": "T1110",
                "mitre_name": "Brute Force",
                "severity": "HIGH",
                "category": "Brute Force"
            })
            soc_state["missions_completed"]["mission_bruteforce"] = True
            
        if any(t["category"] == "SQLi" for t in threats):
            soc_state["missions_completed"]["mission_sqli"] = True
        if any(t["category"] == "XSS" for t in threats):
            soc_state["missions_completed"]["mission_xss"] = True
        if any(t["category"] == "Path Traversal (LFI)" for t in threats):
            soc_state["missions_completed"]["mission_lfi"] = True
            
        action = "BLOCKED" if threats else "ALLOWED"
        log_soc_event("HTTP_REQUEST", client_ip, method, path, body or full_query, threats, action)
        
        # Resposta do Honeypot
        if threats:
            self.send_response(403)
            self.send_header("Content-Type", "application/json")
            self.send_header("X-Protected-By", "SentinelSOC-WAF-Active")
            self.end_headers()
            response_data = {
                "security_alert": "SentinelSOC WAF Triggered",
                "status": 403,
                "detected_threats": [t["name"] for t in threats],
                "mitre_technique": [t["mitre_id"] for t in threats],
                "source_ip": client_ip,
                "incident_logged": True
            }
            self.wfile.write(json.dumps(response_data, indent=2).encode())
        else:
            # Resposta simulada normal de um servidor corporativo vulnerável
            self.send_response(200)
            self.send_header("Content-Type", "application/json")
            self.send_header("Server", "Apache/2.4.41 (Ubuntu) Corporate Gateway")
            self.end_headers()
            
            # Resposta simulada baseada na rota
            if "/login" in path:
                resp = {"status": "success", "message": "Honeypot Login Endpoint Active. Awaiting credentials."}
            elif "/admin" in path:
                resp = {"status": "restricted", "message": "Admin area. Authentication required."}
            elif "/api/v1/users" in path:
                resp = {"status": "ok", "users": [{"id": 1, "username": "admin", "role": "SuperAdministrator"}, {"id": 2, "username": "guest", "role": "User"}]}
            else:
                resp = {"status": "online", "message": "Corporate Service v2.4 Active. Sentinel Honeypot listening.", "timestamp": time.time()}
            self.wfile.write(json.dumps(resp, indent=2).encode())

    def do_GET(self):
        self.handle_request("GET")
        
    def do_POST(self):
        self.handle_request("POST")

    def do_PUT(self):
        self.handle_request("PUT")
        
    def do_DELETE(self):
        self.handle_request("DELETE")


# ==========================================
# 2. MOTOR DE SCANNER DE REDE E VULNERABILIDADES (Mini-Nmap / Nikto)
# ==========================================
COMMON_PORTS = {
    21: "FTP (File Transfer Protocol)",
    22: "SSH (Secure Shell)",
    23: "Telnet (Insecure Cleartext)",
    25: "SMTP (Simple Mail Transfer)",
    53: "DNS (Domain Name System)",
    80: "HTTP (Web Server)",
    110: "POP3 (Mail Server)",
    143: "IMAP (Mail Server)",
    443: "HTTPS (Secure Web Server)",
    445: "SMB (Microsoft File Sharing)",
    1433: "MSSQL (Microsoft SQL Server)",
    1521: "Oracle Database",
    3306: "MySQL Database",
    3389: "RDP (Remote Desktop)",
    5432: "PostgreSQL Database",
    6379: "Redis (In-Memory Database)",
    8080: "HTTP-Proxy / Alternate Web",
    8443: "HTTPS Alternate",
    9090: "SentinelSOC Dashboard",
    9091: "SentinelSOC Honeypot",
    27017: "MongoDB Database"
}

def execute_port_scan(target_host, ports_to_scan):
    """Executa varredura de portas com sockets não bloqueantes e captura de banner"""
    results = []
    try:
        target_ip = socket.gethostbyname(target_host)
    except Exception as e:
        return {"error": f"Não foi possível resolver o host: {target_host} ({str(e)})"}
        
    for port in ports_to_scan:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(0.35)
        start_t = time.time()
        status = "CLOSED"
        banner = ""
        try:
            res = sock.connect_ex((target_ip, port))
            latency = round((time.time() - start_t) * 1000, 2)
            if res == 0:
                status = "OPEN"
                # Tenta capturar banner simples
                try:
                    sock.sendall(b"HEAD / HTTP/1.0\r\n\r\n")
                    banner_raw = sock.recv(256)
                    banner = banner_raw.decode('utf-8', errors='ignore').split('\r\n')[0]
                except:
                    banner = "Conexão aceita (Sem banner imediato)"
            results.append({
                "port": port,
                "service": COMMON_PORTS.get(port, "Custom / Unknown Service"),
                "status": status,
                "latency_ms": latency if status == "OPEN" else 0,
                "banner": banner
            })
        except:
            pass
        finally:
            sock.close()
            
    soc_state["missions_completed"]["mission_scanner"] = True
    return {
        "target_host": target_host,
        "target_ip": target_ip,
        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "open_ports_count": len([r for r in results if r["status"] == "OPEN"]),
        "ports": results
    }

def execute_web_audit(target_url):
    """Auditoria de Cabeçalhos de Segurança HTTP e Rotas Críticas"""
    if not target_url.startswith("http"):
        target_url = "http://" + target_url
        
    parsed = urllib.parse.urlparse(target_url)
    host = parsed.hostname
    port = parsed.port or (443 if parsed.scheme == "https" else 80)
    
    audit_results = {
        "url": target_url,
        "security_headers": {},
        "missing_headers": [],
        "risk_score": 0,
        "recommendations": []
    }
    
    # Lista de headers obrigatórios pela OWASP
    REQUIRED_SECURITY_HEADERS = {
        "Strict-Transport-Security": "Protege contra downgrade de HTTPS para HTTP e ataques MITM (HSTS).",
        "Content-Security-Policy": "Impede injeções de scripts maliciosos (XSS) e cliques forjados.",
        "X-Frame-Options": "Protege contra ataques de Clickjacking (carregamento em iframes invisíveis).",
        "X-Content-Type-Options": "Evita sniffing de tipos MIME pelo navegador (deve ser 'nosniff').",
        "Referrer-Policy": "Controla vazamento de URLs sensíveis em cabeçalhos Referer.",
        "Permissions-Policy": "Restringe acesso da página à câmera, microfone e geolocalização."
    }
    
    try:
        req = urllib.request.Request(
            target_url,
            headers={"User-Agent": "SentinelSOC-Auditor/1.0 (CyberSecurity Assessment)"}
        )
        ctx = ssl.create_default_context()
        ctx.check_hostname = False
        ctx.verify_mode = ssl.CERT_NONE
        
        with urllib.request.urlopen(req, timeout=3.0, context=ctx) as response:
            headers = dict(response.headers)
            
            for sec_header, description in REQUIRED_SECURITY_HEADERS.items():
                val = headers.get(sec_header) or headers.get(sec_header.lower())
                if val:
                    audit_results["security_headers"][sec_header] = {"value": val, "status": "SECURE"}
                else:
                    audit_results["missing_headers"].append({
                        "header": sec_header,
                        "risk": "HIGH" if sec_header in ["Content-Security-Policy", "X-Frame-Options", "Strict-Transport-Security"] else "MEDIUM",
                        "impact": description
                    })
                    audit_results["risk_score"] += 15
                    
            audit_results["server_banner"] = headers.get("Server", "Não revelado (Boa prática)")
            if headers.get("Server"):
                audit_results["recommendations"].append("Oculte o cabeçalho 'Server' para dificultar o reconhecimento de versões pelo invasor.")
                audit_results["risk_score"] += 10
                
    except Exception as e:
        audit_results["error"] = f"Falha ao conectar no alvo HTTP: {str(e)}"
        
    return audit_results


# ==========================================
# 3. DASHBOARD & API SERVER (Porta 9090)
# ==========================================
class DashboardHTTPHandler(http.server.SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        static_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "static")
        super().__init__(*args, directory=static_dir, **kwargs)

    def log_message(self, format, *args):
        pass  # Silencia logs padrão
        
    def do_GET(self):
        parsed = urllib.parse.urlparse(self.path)
        
        # API: Obter estado atual do SOC em tempo real
        if parsed.path == "/api/soc/state":
            self.send_response(200)
            self.send_header("Content-Type", "application/json")
            self.send_header("Access-Control-Allow-Origin", "*")
            self.end_headers()
            
            # Formata blacklist como lista
            payload = {
                "total_requests": soc_state["total_requests"],
                "total_threats_blocked": soc_state["total_threats_blocked"],
                "blacklisted_ips": list(soc_state["blacklisted_ips"]),
                "attack_stats": soc_state["attack_stats"],
                "recent_events": soc_state["recent_events"][:35],
                "missions": soc_state["missions_completed"]
            }
            self.wfile.write(json.dumps(payload).encode())
            return
            
        # Serve arquivos estáticos (HTML/CSS/JS)
        super().do_GET()
        
    def do_POST(self):
        parsed = urllib.parse.urlparse(self.path)
        content_length = int(self.headers.get('Content-Length', 0))
        body = self.rfile.read(content_length).decode('utf-8') if content_length > 0 else "{}"
        
        try:
            data = json.loads(body)
        except:
            data = {}
            
        # API: Executar Port Scan
        if parsed.path == "/api/tools/port-scan":
            target = data.get("target", "127.0.0.1")
            ports_mode = data.get("mode", "fast")
            
            if ports_mode == "fast":
                ports = [21, 22, 23, 80, 443, 445, 3306, 8080, 9090, 9091]
            elif ports_mode == "full":
                ports = list(COMMON_PORTS.keys())
            else:
                ports = [int(p.strip()) for p in str(data.get("custom_ports", "80,443,9090,9091")).split(",") if p.strip().isdigit()]
                
            res = execute_port_scan(target, ports)
            
            self.send_response(200)
            self.send_header("Content-Type", "application/json")
            self.end_headers()
            self.wfile.write(json.dumps(res).encode())
            return
            
        # API: Executar Auditoria Web
        if parsed.path == "/api/tools/web-audit":
            target = data.get("target", "http://127.0.0.1:9091")
            res = execute_web_audit(target)
            
            self.send_response(200)
            self.send_header("Content-Type", "application/json")
            self.end_headers()
            self.wfile.write(json.dumps(res).encode())
            return
            
        # API: Disparar Simulação de Ataque Red Team
        if parsed.path == "/api/tools/simulate-attack":
            attack_type = data.get("type", "SQLi")
            target_url = f"http://127.0.0.1:{PORT_HONEYPOT}"
            
            payload_map = {
                "SQLi": "/api/v1/users?id=1%20UNION%20SELECT%20username,password%20FROM%20admin_credentials%20--",
                "XSS": "/login?redirect=<script>alert('XSS_PAYLOAD_EXECUTED')</script>",
                "LFI": "/download?file=../../../../etc/passwd",
                "Command_Injection": "/ping?host=127.0.0.1;%20cat%20/etc/shadow",
                "Brute_Force": "/admin/login",
                "Scanner_Probe": "/wp-login.php?scanner=sqlmap/1.4.1"
            }
            
            endpoint = payload_map.get(attack_type, "/test")
            
            # Se for Brute Force, dispara 10 requisições rápidas para ativar o sensor
            if attack_type == "Brute_Force":
                for i in range(10):
                    try:
                        req = urllib.request.Request(
                            f"{target_url}{endpoint}",
                            data=json.dumps({"user": "admin", "pass": f"password_{i}"}).encode(),
                            headers={"Content-Type": "application/json", "User-Agent": "Hydra/9.2-BruteForcer"}
                        )
                        urllib.request.urlopen(req, timeout=1.0)
                    except:
                        pass
                sim_res = {"status": "success", "message": f"Simulação de 10 tentativas de Brute Force enviadas ao Honeypot."}
            else:
                try:
                    headers = {"User-Agent": "RedTeam-Simulation-Bot/3.0"}
                    if attack_type == "Scanner_Probe":
                        headers["User-Agent"] = "sqlmap/1.5.2#stable (http://sqlmap.org)"
                    req = urllib.request.Request(f"{target_url}{endpoint}", headers=headers)
                    with urllib.request.urlopen(req, timeout=1.5) as r:
                        response_text = r.read().decode()
                except urllib.error.HTTPError as e:
                    response_text = e.read().decode()
                except Exception as e:
                    response_text = str(e)
                sim_res = {"status": "success", "attack_type": attack_type, "endpoint_attacked": endpoint, "target": target_url}
                
            self.send_response(200)
            self.send_header("Content-Type", "application/json")
            self.end_headers()
            self.wfile.write(json.dumps(sim_res).encode())
            return
            
        # API: Adicionar/Remover IP da Blacklist (Ação SOAR)
        if parsed.path == "/api/soc/blacklist":
            ip = data.get("ip")
            action = data.get("action", "add")
            if ip:
                if action == "add":
                    soc_state["blacklisted_ips"].add(ip)
                    log_soc_event("SOAR_ACTION", ip, "SOAR", "/quarantine", f"IP {ip} adicionado à lista de quarentena pelo operador.", [], "BLACKLIST_APPLIED")
                elif action == "remove":
                    soc_state["blacklisted_ips"].discard(ip)
            self.send_response(200)
            self.send_header("Content-Type", "application/json")
            self.end_headers()
            self.wfile.write(json.dumps({"status": "success", "blacklisted_ips": list(soc_state["blacklisted_ips"])}).encode())
            return

        self.send_response(404)
        self.end_headers()


def start_honeypot_server():
    """Inicia o servidor Honeypot em thread separada"""
    server = socketserver.ThreadingTCPServer(("0.0.0.0", PORT_HONEYPOT), HoneypotHTTPHandler)
    server.allow_reuse_address = True
    print(f"[*] 🍯 Honeypot Ativo & Escutando na porta {PORT_HONEYPOT} (http://localhost:{PORT_HONEYPOT})")
    server.serve_forever()

def start_dashboard_server():
    """Inicia o servidor do Dashboard Web do SOC"""
    server = socketserver.ThreadingTCPServer(("0.0.0.0", PORT_DASHBOARD), DashboardHTTPHandler)
    server.allow_reuse_address = True
    print(f"[*] 🛡️ SentinelSOC Dashboard Ativo na porta {PORT_DASHBOARD} (http://localhost:{PORT_DASHBOARD})")
    print(f"[*] 🚀 Abra http://localhost:{PORT_DASHBOARD} no seu navegador para interagir!")
    server.serve_forever()

if __name__ == "__main__":
    print("=" * 70)
    print("🛡️  SENTINEL SOC & NETWORK DEFENSE LAB (PBL ENGINE) - INICIANDO")
    print("=" * 70)
    
    # Garante que a pasta static existe
    static_folder = os.path.join(os.path.dirname(os.path.abspath(__file__)), "static")
    os.makedirs(static_folder, exist_ok=True)
    
    # Inicia Honeypot em background
    t_honeypot = threading.Thread(target=start_honeypot_server, daemon=True)
    t_honeypot.start()
    
    # Inicia Dashboard principal
    start_dashboard_server()
