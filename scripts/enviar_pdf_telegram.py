# -*- coding: utf-8 -*-
"""
Script dedicado e robusto para envio do PDF às Mensagens Salvas ('me') no Telegram via Telethon.
Usa as credenciais e sessão comprovadas em telegram_downloader/.env
"""

import os
import sys
import asyncio
from pathlib import Path

if sys.platform == "win32":
    try:
        sys.stdout.reconfigure(encoding='utf-8')
        sys.stderr.reconfigure(encoding='utf-8')
    except Exception:
        pass

from telethon import TelegramClient

BASE_DIR = Path(r"C:\Users\mathe\.gemini\antigravity-ide\scratch\telegram_downloader")
SESSION_FILE = BASE_DIR / "telegram_downloader_session"
PDF_PATH = Path(r"C:\Users\mathe\Desktop\CATALOGO_DEEP_RESEARCH_CURSOS_PERICIA_E_INVESTIGACAO.pdf")

API_ID = 25851137
API_HASH = "4efdcd76e8de2b06763f8dee8668b130"

async def main():
    print(f"[1/4] Verificando existência do PDF em: {PDF_PATH}")
    if not PDF_PATH.exists():
        print(f"❌ Erro: Arquivo {PDF_PATH} não encontrado!")
        return

    size_bytes = PDF_PATH.stat().st_size
    print(f"📄 Arquivo confirmado! Tamanho: {size_bytes:,} bytes ({size_bytes/1024:.1f} KB)")

    print(f"[2/4] Conectando ao Telegram usando sessão: {SESSION_FILE}.session...")
    client = TelegramClient(str(SESSION_FILE), API_ID, API_HASH)
    client.session.set_dc(1, "149.154.175.55", 443)

    await client.connect()

    if not await client.is_user_authorized():
        print("❌ Sessão do Telegram não está autorizada!")
        await client.disconnect()
        return

    me = await client.get_me()
    print(f"👤 [3/4] Autenticado com sucesso como: {me.first_name} {me.last_name or ''} (@{me.username or 'sem_username'}) - ID: {me.id}")

    caption = (
        "📚 **CATÁLOGO MASTER DE INTELIGÊNCIA FORENSE, OSINT & SUPORTE A ADVOGADOS (2026)**\n\n"
        "🎯 **Deep Research Exaustiva Concluída:**\n"
        "• Mapeamento de Cursos de Investigação Patrimonial (Execução & Penhora de Bens)\n"
        "• WB Educação (Pós OSINT & Perícia), Academia Forense Digital (AFD) e Montax (Briefing SPQR)\n"
        "• Trabalho Notável ('Execução Sem Trégua' - Prof. Fabiano Coelho) e Lexverse Academy\n"
        "• Assinaturas Econômicas Mensais (JusClass da Juspodivm & Sindplay da AFD)\n"
        "• Computação Forense, ISO 27037 (Hash SHA-256) & Blockchain Forensics (USDT/Bitcoin)\n"
        "• Cursos Gratuitos Oficiais com Certificado (EV.G / Enap / SENASP - Ministério da Justiça)\n\n"
        "💾 *Arquivo PDF salvo diretamente na sua Área de Trabalho (Desktop) e aqui nas suas Mensagens Salvas!*"
    )

    print(f"[4/4] Enviando documento '{PDF_PATH.name}' para Mensagens Salvas ('me')...")
    msg = await client.send_file(
        entity='me',
        file=str(PDF_PATH),
        caption=caption,
        force_document=True
    )

    print(f"🎉 SUCESSO ABSOLUTO! Mensagem enviada para 'me'! Mensagem ID: {msg.id}")
    await client.disconnect()

if __name__ == "__main__":
    asyncio.run(main())
