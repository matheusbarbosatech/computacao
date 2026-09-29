# -*- coding: utf-8 -*-
import os
import sys

# Forçar UTF-8 para evitar UnicodeEncodeError no Windows CP1252
sys.stdout.reconfigure(encoding='utf-8', errors='replace')
sys.stderr.reconfigure(encoding='utf-8', errors='replace')

LOG_FILE = r"c:\Users\mathe\Desktop\computacao\enviar_edital.log"

def log(msg):
    line = f"{msg}"
    print(line, flush=True)
    try:
        with open(LOG_FILE, "a", encoding="utf-8") as f:
            f.write(line + "\n")
    except Exception:
        pass

log("--- PONTO 1: Iniciando teste robusto ---")

try:
    import shutil
    import asyncio
    log("--- PONTO 2: asyncio importado com sucesso ---")
    
    from telethon import TelegramClient
    log("--- PONTO 3: Telethon importado com sucesso ---")
    
    SCRATCH_DIR = r"C:\Users\mathe\.gemini\antigravity-ide\scratch\telegram_downloader"
    API_ID = 26685077
    API_HASH = "8feff28fdf4808cff1ecf6050b18faae"
    
    SOURCE_SESSION = os.path.join(SCRATCH_DIR, "telegram_cleaner_session.session")
    TEMP_SESSION_BASE = os.path.join(SCRATCH_DIR, "telegram_edital_temp")
    TEMP_SESSION_FILE = TEMP_SESSION_BASE + ".session"
    DOC_PATH = r"c:\Users\mathe\Desktop\computacao\EDITAL_DE_CONTRATACAO_MERCADO_CYBER_2026.md"
    
    async def main():
        log("--- PONTO 4: Dentro da funcao main() ---")
        if not os.path.exists(DOC_PATH):
            log(f"[ERRO] Arquivo {DOC_PATH} nao existe!")
            return
            
        log("--- PONTO 5: Copiando sessao ---")
        if os.path.exists(SOURCE_SESSION):
            shutil.copy2(SOURCE_SESSION, TEMP_SESSION_FILE)
            log(f"Copiado de {SOURCE_SESSION}")
        elif os.path.exists(os.path.join(SCRATCH_DIR, "gamedev_search.session")):
            shutil.copy2(os.path.join(SCRATCH_DIR, "gamedev_search.session"), TEMP_SESSION_FILE)
            log("Copiado de gamedev_search.session")
        else:
            log("[ERRO] Nenhuma sessao encontrada!")
            return

        log("--- PONTO 6: Instanciando TelegramClient ---")
        client = TelegramClient(TEMP_SESSION_BASE, API_ID, API_HASH)
        
        log("--- PONTO 7: Conectando com timeout de 15s ---")
        await asyncio.wait_for(client.connect(), timeout=15)
        log("--- PONTO 8: Conectado! Verificando autorizacao ---")
        
        auth = await client.is_user_authorized()
        log(f"--- PONTO 9: Autorizado? {auth} ---")
        if not auth:
            log("[ERRO] Sessao nao autorizada!")
            await client.disconnect()
            return
            
        me = await client.get_me()
        log(f"[CONECTADO] {me.first_name} (@{me.username}) [ID: {me.id}]")
        
        caption = (
            "📄 **EDITAL OFICIAL DE CONTRATAÇÃO — CIBERSEGURANÇA & TECH 2026**\n\n"
            "🎯 **Guia Definitivo do Mercado:**\n"
            "• Cargos em Disputa (SOC Jr, Infra/Redes Jr, GRC Jr, Pentest Jr)\n"
            "• Faixas Salariais Reais (R$ 3.500 a R$ 7.500)\n"
            "• Critérios Eliminatórios dos robôs da Gupy (ATS)\n"
            "• Conteúdo Programático Verticalizado com os seus cursos\n"
            "• Projeto Prático Diferenciador (Home Lab Wazuh + Simulação de Expediente)\n"
            "• Cronograma Tático de 30 Dias para Contratação\n\n"
            "💾 *Salvo nas suas Mensagens Salvas para consulta rápida no celular e PC!*"
        )
        
        log(f"[ENVIANDO] {os.path.basename(DOC_PATH)} para Saved Messages...")
        sent_msg = await client.send_file('me', DOC_PATH, caption=caption)
        log(f"[SUCESSO] Mensagem enviada com ID: {sent_msg.id}")
        
        await client.disconnect()
        try:
            if os.path.exists(TEMP_SESSION_FILE):
                os.remove(TEMP_SESSION_FILE)
        except Exception:
            pass
        log("[FINALIZADO] Processo concluido com 100% de sucesso!")

    asyncio.run(main())

except Exception as ex:
    import traceback
    log(f"[ERRO CAPTURADO] {ex}\n{traceback.format_exc()}")
