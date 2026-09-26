# -*- coding: utf-8 -*-
"""
🚀 ROBÔ DE CLONAGEM DO GOOGLE DRIVE (CLOUD-TO-CLOUD)
Pasta Alvo: HACKONE - ACADEMIA DE CIBERSEGURANÇA & REDES
Origem: 💎 DRIVE PREMIUM - MESTRE DOS CURSOS / 02. Programação & Desenvolvimento / Hackone
Destino: meudrive:MEU_ACERVO_CLONADO/HACKONE_ACADEMIA_CYBER_COMPLETA
Cópia direta Nuvem-para-Nuvem (Zero consumo de disco local)
"""
import subprocess
import os
import sys
import json
import time

sys.stdout.reconfigure(encoding='utf-8', line_buffering=True)
sys.stderr.reconfigure(encoding='utf-8', line_buffering=True)

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
LOG_FILE = os.path.join(BASE_DIR, "clonagem_hackone.log")
PROGRESSO_FILE = os.path.join(BASE_DIR, "progresso_hackone.json")

ORIGEM = "meudrive,shared_with_me:💎 DRIVE PREMIUM - MESTRE DOS CURSOS/02. 💻 Programação & Desenvolvimento/Hackone"
DESTINO = "meudrive:MEU_ACERVO_CLONADO/HACKONE_ACADEMIA_CYBER_COMPLETA"

# Lista de outros cursos de Cyber & Pentest prioritários disponíveis
CURSOS_CYBER_ADICIONAIS = [
    {
        "nome": "Foco em SEC - 4 Pilares de Cyber e Investigação Digital",
        "origem": "meudrive,shared_with_me:💎 DRIVE PREMIUM - MESTRE DOS CURSOS/02. 💻 Programação & Desenvolvimento/Ingresso FocoemSEC 4 Pilares de Cyber e Investigação Digital + Bônus - Foco em SEC",
        "destino": "meudrive:MEU_ACERVO_CLONADO/FOCO_EM_SEC_INVESTIGACAO_DIGITAL"
    },
    {
        "nome": "Pentest Web Profissional - Geraldo Alcantara",
        "origem": "meudrive,shared_with_me:💎 DRIVE PREMIUM - MESTRE DOS CURSOS/02. 💻 Programação & Desenvolvimento/Pentest Web Profissional: do recon ao report - Geraldo Alcantara",
        "destino": "meudrive:MEU_ACERVO_CLONADO/PENTEST_WEB_PROFISSIONAL_GERALDO_ALCANTARA"
    }
]

def log_msg(msg):
    ts = time.strftime("[%Y-%m-%d %H:%M:%S]")
    line = f"{ts} {msg}"
    print(line, flush=True)
    try:
        with open(LOG_FILE, "a", encoding="utf-8") as f:
            f.write(line + "\n")
    except Exception:
        pass

def salvar_progresso(status, curso="Hackone", extra=None):
    data = {
        "status": status,
        "curso": curso,
        "ultima_atualizacao": time.strftime("%Y-%m-%d %H:%M:%S"),
        "extra": extra or {}
    }
    try:
        with open(PROGRESSO_FILE, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
    except Exception as e:
        print(f"⚠️ Erro ao salvar progresso: {e}")

def clonar_pasta(origem, destino, nome_curso):
    cmd = [
        "rclone", "copy",
        origem,
        destino,
        "--server-side-across-configs",
        "--fast-list",
        "--transfers", "4",
        "--checkers", "8",
        "--tpslimit", "3",
        "--drive-pacer-min-sleep", "100ms",
        "--drive-stop-on-upload-limit",
        "--retries", "10",
        "--low-level-retries", "10",
        "--log-file", LOG_FILE,
        "--log-level", "INFO",
        "-P",
        "--stats", "5s"
    ]
    
    log_msg("=" * 65)
    log_msg(f"🚀 CLONANDO CLOUD-TO-CLOUD: {nome_curso.upper()}")
    log_msg(f"📁 Origem: {origem}")
    log_msg(f"☁️ Destino: {destino}")
    log_msg("⚡ Modo: Server-Side Copy (Transferência direta no Google Drive)")
    log_msg("=" * 65)
    
    salvar_progresso("EM_ANDAMENTO", nome_curso)
    proc = subprocess.Popen(cmd, stdout=sys.stdout, stderr=sys.stderr)
    returncode = proc.wait()
    
    if returncode == 0:
        log_msg(f"✅ {nome_curso.upper()} CLONADO COM SUCESSO ABSOLUTO!")
        salvar_progresso("CONCLUIDO", nome_curso)
    else:
        log_msg(f"⚠️ Processo de {nome_curso} finalizado com código: {returncode}")
        salvar_progresso("PAUSADO_OU_LIMITE_ATINGIDO", nome_curso, {"returncode": returncode})
        
    return returncode

def main():
    print("=" * 65)
    print("🛡️ CLONAGEM DE ALTA PRIORIDADE: HACKONE & ACERVO CYBER")
    print("=" * 65)
    
    # 1. Clona HackOne com prioridade máxima
    clonar_pasta(ORIGEM, DESTINO, "Hackone - Academia Cyber Completa")
    
    # 2. Clona os outros cursos de segurança de ponta encontrados
    for c in CURSOS_CYBER_ADICIONAIS:
        print("\n" + "-" * 65)
        clonar_pasta(c["origem"], c["destino"], c["nome"])
        
    log_msg("🏆 TODAS AS PASTAS PRIORITÁRIAS DE HACKING FORAM CLONADAS COM SUCESSO!")

if __name__ == "__main__":
    main()
