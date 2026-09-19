"""
=============================================================================
ESTÚDIO VISUAL DE MAPAS MENTAIS — SERVIDOR LOCAL INTEGRADO (DEVWORLD AI)
=============================================================================
Inicia um servidor web local super leve (sem dependências pesadas) que conecta
a interface visual Sketchnote à API da DevWorld e à Matriz UNINTER.
=============================================================================
"""

import http.server
import socketserver
import json
import os
import sys
import webbrowser
from urllib.parse import urlparse

if sys.platform == "win32":
    try:
        sys.stdout.reconfigure(encoding='utf-8')
        sys.stderr.reconfigure(encoding='utf-8')
    except Exception:
        pass

from matriz_uninter import TODOS_OS_200_MAPAS
from matriz_expansao_700 import obter_todos_os_mapas_expansao
from devworld_engine import gerar_mapa_devworld, MODELOS_ILIMITADOS, ENV_CONFIG

TODOS_OS_700_MAPAS = TODOS_OS_200_MAPAS + obter_todos_os_mapas_expansao()

PORT = 8080
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
WEB_DIR = os.path.join(BASE_DIR, "web_studio")

class StudioHandler(http.server.SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=WEB_DIR, **kwargs)

    def do_GET(self):
        parsed = urlparse(self.path)
        
        # Endpoint: Retorna a Trilha UNINTER completa
        if parsed.path == "/api/trilha":
            self.send_response(200)
            self.send_header("Content-Type", "application/json; charset=utf-8")
            self.end_headers()
            
            # Verifica quais mapas já estão gerados no disco
            mapas_gerados = set()
            output_dir = os.path.join(BASE_DIR, "output_mapas")
            if os.path.exists(output_dir):
                for f in os.listdir(output_dir):
                    if f.startswith("mapa_") and f.endswith(".json"):
                        try:
                            num = int(f.split("_")[1].split(".")[0])
                            mapas_gerados.add(num)
                        except Exception:
                            pass

            from catalogo_escolas import ESCOLAS_METADATA
            payload = {
                "trilha_iniciante": TODOS_OS_700_MAPAS,
                "escolas": ESCOLAS_METADATA,
                "mapas_gerados": list(mapas_gerados),
                "modelos_ilimitados": MODELOS_ILIMITADOS,
                "modelo_padrao": ENV_CONFIG.get("DEVWORLD_MODEL")
            }
            self.wfile.write(json.dumps(payload, ensure_ascii=False).encode("utf-8"))
            return

        # Endpoint: Carrega mapa específico do disco
        if parsed.path.startswith("/api/mapa/"):
            try:
                map_id = int(parsed.path.split("/")[-1])
                arquivo_json = os.path.join(BASE_DIR, "output_mapas", f"mapa_{map_id:03d}.json")
                if os.path.exists(arquivo_json):
                    with open(arquivo_json, "r", encoding="utf-8") as f:
                        conteudo = f.read()
                    self.send_response(200)
                    self.send_header("Content-Type", "application/json; charset=utf-8")
                    self.end_headers()
                    self.wfile.write(conteudo.encode("utf-8"))
                    return
                else:
                    self.send_response(404)
                    self.end_headers()
                    return
            except Exception:
                self.send_response(400)
                self.end_headers()
                return

        # Serve arquivos estáticos normalmente da pasta web_studio
        return super().do_GET()

    def do_POST(self):
        parsed = urlparse(self.path)

        # Endpoint: Gerar Mapa Mental com a DevWorld AI
        if parsed.path == "/api/gerar":
            content_length = int(self.headers.get('Content-Length', 0))
            body = self.rfile.read(content_length).decode('utf-8')
            
            try:
                data = json.loads(body)
                topico = data.get("topico", "O que é Programação?")
                id_mapa = int(data.get("id", 1))
                foco = data.get("foco", "")
                modelo = data.get("modelo", None)

                print(f"🧠 [DevWorld AI] Gerando mapa #{id_mapa}: '{topico}' (Modelo: {modelo or 'Padrão'})...")
                resultado = gerar_mapa_devworld(topico, id_mapa=id_mapa, foco=foco, modelo=modelo)
                
                # Salva automaticamente na pasta de saída
                arquivo_json = os.path.join(BASE_DIR, "output_mapas", f"mapa_{id_mapa:03d}.json")
                with open(arquivo_json, "w", encoding="utf-8") as f:
                    json.dump(resultado, f, indent=2, ensure_ascii=False)
                    
                print(f"✅ [DevWorld AI] Mapa #{id_mapa} gerado e salvo em disco com sucesso!")

                self.send_response(200)
                self.send_header("Content-Type", "application/json; charset=utf-8")
                self.end_headers()
                self.wfile.write(json.dumps(resultado, ensure_ascii=False).encode("utf-8"))
            except Exception as e:
                print(f"❌ [DevWorld AI] Erro ao gerar: {e}")
                self.send_response(500)
                self.send_header("Content-Type", "application/json; charset=utf-8")
                self.end_headers()
                self.wfile.write(json.dumps({"error": str(e)}, ensure_ascii=False).encode("utf-8"))
            return

        self.send_response(404)
        self.end_headers()

def iniciar_servidor():
    os.makedirs(WEB_DIR, exist_ok=True)
    os.makedirs(os.path.join(BASE_DIR, "output_mapas"), exist_ok=True)

    socketserver.TCPServer.allow_reuse_address = True
    with socketserver.TCPServer(("", PORT), StudioHandler) as httpd:
        url = f"http://localhost:{PORT}"
        print("=" * 70)
        print("🚀 ESTÚDIO DE MAPAS MENTAIS UNINTER (DEVWORLD AI) INICIADO!")
        print(f"🌐 Acesse no seu navegador: {url}")
        print("=" * 70)
        
        # Abre o navegador automaticamente
        try:
            webbrowser.open(url)
        except Exception:
            pass

        try:
            httpd.serve_forever()
        except KeyboardInterrupt:
            print("\n🛑 Servidor encerrado.")
            httpd.server_close()

if __name__ == "__main__":
    iniciar_servidor()
