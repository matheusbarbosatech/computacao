# -*- coding: utf-8 -*-
import os
import sys
import psutil
import json
from datetime import datetime

if sys.platform == "win32":
    try:
        sys.stdout.reconfigure(encoding='utf-8')
        sys.stderr.reconfigure(encoding='utf-8')
    except Exception:
        pass

print("=" * 80)
print("🔍 1. PROCESSOS ATIVOS NO SISTEMA (PYTHON & RCLONE)")
print("=" * 80)

found_procs = []
for p in psutil.process_iter(['pid', 'name', 'cmdline', 'create_time', 'memory_info']):
    try:
        name = p.info['name'].lower()
        if 'python' in name or 'rclone' in name:
            cmd = " ".join(p.info['cmdline'] or [])
            ctime = datetime.fromtimestamp(p.info['create_time']).strftime('%Y-%m-%d %H:%M:%S')
            mem_mb = (p.info['memory_info'].rss / 1024 / 1024) if p.info['memory_info'] else 0
            found_procs.append({
                'pid': p.info['pid'],
                'name': p.info['name'],
                'cmd': cmd,
                'created': ctime,
                'mem_mb': mem_mb
            })
            print(f"[PID {p.info['pid']}] {p.info['name']} | Iniciado: {ctime} | RAM: {mem_mb:.1f} MB")
            print(f"   Comando: {cmd}\n")
    except Exception:
        pass

if not found_procs:
    print("Nenhum processo Python ou Rclone ativo no momento.\n")

print("=" * 80)
print("📁 2. LOGS & STATUS DO TELEGRAM DOWNLOADER / CLONER")
print("=" * 80)

td_dir = r"C:\Users\mathe\.gemini\antigravity-ide\scratch\telegram_downloader"

# Progresso audios pregadores
prog_file = os.path.join(td_dir, "progresso_audios_pregadores.json")
if os.path.exists(prog_file):
    try:
        with open(prog_file, "r", encoding="utf-8") as f:
            data = json.load(f)
            print(f"📊 progresso_audios_pregadores.json:\n{json.dumps(data, indent=2, ensure_ascii=False)}\n")
    except Exception as e:
        print("Erro ao ler progresso_audios_pregadores.json:", e)

# Current log
current_log = os.path.join(td_dir, "current_log.txt")
if os.path.exists(current_log):
    try:
        with open(current_log, "r", encoding="utf-8", errors="replace") as f:
            lines = f.readlines()
            print(f"📄 current_log.txt (últimas 10 linhas):")
            for l in lines[-10:]:
                print("   " + l.strip())
            print()
    except Exception as e:
        print("Erro ao ler current_log.txt:", e)

# Download log
dl_log = os.path.join(td_dir, "download_audios_pregadores.log")
if os.path.exists(dl_log):
    try:
        with open(dl_log, "r", encoding="utf-8", errors="replace") as f:
            lines = f.readlines()
            print(f"📄 download_audios_pregadores.log (últimas 10 linhas):")
            for l in lines[-10:]:
                print("   " + l.strip())
            print()
    except Exception as e:
        print("Erro ao ler download_audios_pregadores.log:", e)

# Download history count
hist_file = os.path.join(td_dir, "download_history.json")
if os.path.exists(hist_file):
    try:
        with open(hist_file, "r", encoding="utf-8") as f:
            hist_data = json.load(f)
            if isinstance(hist_data, list):
                print(f"📚 download_history.json: {len(hist_data)} itens registrados.")
            elif isinstance(hist_data, dict):
                print(f"📚 download_history.json: {len(hist_data)} chaves registradas.")
    except Exception as e:
        print("Erro ao ler download_history.json:", e)

print("\n" + "=" * 80)
print("☁️ 3. STATUS DO GOOGLE DRIVE & RCLONE / DRIVE DE POBRE")
print("=" * 80)

# Procurando referências a 'pobre', 'rclone', 'drive' em Desktop e projetos
desktop_path = r"C:\Users\mathe\Desktop"
for item in os.listdir(desktop_path):
    lower = item.lower()
    if any(k in lower for k in ["pobre", "drive", "clone", "acervo", "biblioteca"]):
        full_path = os.path.join(desktop_path, item)
        is_d = os.path.isdir(full_path)
        print(f"Desktop -> {'[DIR]' if is_d else '[ARQ]'} {item}")

# Procurando pasta ibpmcr-automation
ibpmcr_dir = r"C:\Users\mathe\Desktop\ibpmcr-automation"
if os.path.exists(ibpmcr_dir):
    print(f"\nDiretório ibpmcr-automation encontrado. Listando itens:")
    for f in os.listdir(ibpmcr_dir):
        print("   " + f)
