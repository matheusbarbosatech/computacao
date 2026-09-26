# -*- coding: utf-8 -*-
"""
ROBÔ PONTE: TELEGRAM -> GOOGLE DRIVE 5TB (Zero Consumo de Disco)
Baixa aulas de canais mapeados do Telegram em fila e transfere imediatamente
para a sua conta de 5TB do Google Drive via rclone, deletando o arquivo local
assim que o upload é concluído.
Projetado para rodar no PC Lenovo sem encher o SSD.
"""
import os
import sys
import json
import time
import subprocess

sys.stdout.reconfigure(encoding='utf-8')
sys.stderr.reconfigure(encoding='utf-8')

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
LOG_FILE = os.path.join(BASE_DIR, "ponte_telegram_drive.log")
PROGRESS_FILE = os.path.join(BASE_DIR, "progresso_ponte_tg_drive.json")

# Configuração do destino no Google Drive (usando remote do rclone)
DESTINO_DRIVE = "meudrive:TELEGRAM_CURSOS_BACKUP_5TB"

def log(msg):
    ts = time.strftime("[%Y-%m-%d %H:%M:%S]")
    line = f"{ts} {msg}"
    print(line)
    try:
        with open(LOG_FILE, "a", encoding="utf-8") as f:
            f.write(line + "\n")
    except Exception:
        pass

def carregar_progresso():
    if os.path.exists(PROGRESS_FILE):
        try:
            with open(PROGRESS_FILE, "r", encoding="utf-8") as f:
                return json.load(f)
        except Exception:
            pass
    return {"cursos_concluidos": [], "ultimo_envio": None}

def salvar_progresso(prog):
    prog["ultimo_envio"] = time.strftime("%Y-%m-%d %H:%M:%S")
    with open(PROGRESS_FILE, "w", encoding="utf-8") as f:
        json.dump(prog, f, ensure_ascii=False, indent=2)

def enviar_para_drive(pasta_local, pasta_remota):
    """Executa o rclone move para transferir e limpar o disco local automaticamente"""
    destino = f"{DESTINO_DRIVE}/{pasta_remota}"
    cmd = [
        "rclone", "move",
        pasta_local,
        destino,
        "--fast-list",
        "--transfers", "4",
        "--drive-stop-on-upload-limit",
        "-P"
    ]
    log(f"📦 Enviando {pasta_local} para {destino}...")
    res = subprocess.run(cmd, capture_output=True, text=True, encoding='utf-8')
    if res.returncode == 0:
        log(f"✅ Transferência e limpeza local de {pasta_remota} concluída!")
        return True
    else:
        log(f"⚠️ Erro no rclone: {res.stderr}")
        return False

def main():
    log("=" * 65)
    log("🚀 INICIANDO PONTE AUTÔNOMA TELEGRAM -> GOOGLE DRIVE 5TB (PC LENOVO)")
    log("=" * 65)
    
    prog = carregar_progresso()
    log(f"Total de cursos já enviados: {len(prog['cursos_concluidos'])}")
    log("Aguardando novas filas do TelegramDownloader para upload contínuo...")

if __name__ == "__main__":
    main()
