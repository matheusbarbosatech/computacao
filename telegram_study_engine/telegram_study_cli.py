"""
=============================================================================
DEVSKETCH MULTI-CLOUD STUDY ENGINE - CLI INTERATIVO & LINHA DE COMANDO
=============================================================================
Suporta:
1. 📱 Telegram Streaming (Cursos em canais/grupos sem ocupar espaço no HD)
2. ☁️ Google Drive (Pastas compartilhadas, Shared Drives, Rclone Mount)
=============================================================================
"""

import asyncio
import os
import sys
import argparse

sys.stdout.reconfigure(encoding="utf-8", errors="replace")

try:
    from database import init_db, get_connection
    from course_discovery import CourseDiscovery
    from study_orchestrator import StudyOrchestrator
    from gdrive_study_provider import GDriveStudyProvider
except ImportError:
    from telegram_study_engine.database import init_db, get_connection
    from telegram_study_engine.course_discovery import CourseDiscovery
    from telegram_study_engine.study_orchestrator import StudyOrchestrator
    from telegram_study_engine.gdrive_study_provider import GDriveStudyProvider

async def listar_canais():
    disc = CourseDiscovery()
    canais = await disc.discover_all_joined_course_channels()
    print(f"\n📋 Canais de Cursos Encontrados no seu Telegram ({len(canais)}):")
    print("-" * 75)
    for idx, c in enumerate(canais, 1):
        user = f"@{c['username']}" if c['username'] else "privado"
        print(f"[{idx}] {c['title']} | ID: {c['chat_id']} ({user})")
    print("-" * 75)

async def indexar_canal(chat_id):
    disc = CourseDiscovery()
    await disc.index_course_lessons(chat_id)

async def estudar_aula(chat_id, msg_id):
    orc = StudyOrchestrator()
    await orc.study_single_lesson(chat_id, msg_id)

async def estudar_curso(chat_id, limite=10):
    orc = StudyOrchestrator()
    await orc.study_entire_course(chat_id, max_lessons=limite)

def indexar_gdrive(caminho):
    gdrive = GDriveStudyProvider()
    gdrive.scan_mounted_drive_folder(caminho)

def mostrar_estatisticas():
    init_db()
    conn = get_connection()
    c = conn.cursor()
    c.execute("SELECT COUNT(*) FROM courses")
    total_cursos = c.fetchone()[0]
    c.execute("SELECT COUNT(*) FROM lessons")
    total_aulas = c.fetchone()[0]
    c.execute("SELECT COUNT(*) FROM lessons WHERE status = 'DISTILLED'")
    total_estudadas = c.fetchone()[0]
    conn.close()

    print("\n📊 ESTATÍSTICAS DO MULTI-CLOUD STUDY ENGINE:")
    print("-" * 55)
    print(f"🏛️ Cursos Indexados (Telegram + GDrive): {total_cursos}")
    print(f"📺 Aulas em Streaming Mapeadas: {total_aulas}")
    print(f"🧠 Aulas Estudadas & Destiladas pela IA: {total_estudadas}")
    print("-" * 55)

def main():
    parser = argparse.ArgumentParser(description="Multi-Cloud Course Study Engine")
    parser.add_argument("--list-channels", action="store_true", help="Listar canais de cursos do Telegram")
    parser.add_argument("--index", type=int, help="Indexar aulas de um canal pelo Chat ID")
    parser.add_argument("--index-gdrive", type=str, help="Indexar pasta de cursos do Google Drive")
    parser.add_argument("--study-course", type=int, help="Estudar curso completo pelo Chat ID")
    parser.add_argument("--study-lesson", nargs=2, type=int, metavar=("CHAT_ID", "MSG_ID"), help="Estudar uma aula específica")
    parser.add_argument("--stats", action="store_true", help="Mostrar estatísticas do banco de dados")
    parser.add_argument("--limit", type=int, default=10, help="Limite de aulas para estudo em lote (padrão: 10)")

    args = parser.parse_args()

    if args.list_channels:
        asyncio.run(listar_canais())
    elif args.index:
        asyncio.run(indexar_canal(args.index))
    elif args.index_gdrive:
        indexar_gdrive(args.index_gdrive)
    elif args.study_course:
        asyncio.run(estudar_curso(args.study_course, args.limit))
    elif args.study_lesson:
        asyncio.run(estudar_aula(args.study_lesson[0], args.study_lesson[1]))
    elif args.stats:
        mostrar_estatisticas()
    else:
        # Modo Interativo
        print("=" * 70)
        print("🤖 DEVSKETCH - MULTI-CLOUD STUDY ENGINE")
        print("📱 Telegram Streaming + ☁️ Google Drive")
        print("=" * 70)
        print("1. [Telegram] Listar canais de cursos que participo")
        print("2. [Telegram] Indexar ementa de um canal de curso")
        print("3. [Telegram] Estudar um curso completo com a IA (Zero-Disk)")
        print("4. [Google Drive] Indexar pasta de cursos (Local ou Rclone Mount)")
        print("5. Ver estatísticas do acervo")
        print("6. Sair")
        print("=" * 70)
        opcao = input("Escolha uma opção (1-6): ").strip()

        if opcao == "1":
            asyncio.run(listar_canais())
        elif opcao == "2":
            cid = int(input("Digite o Chat ID do canal: ").strip())
            asyncio.run(indexar_canal(cid))
        elif opcao == "3":
            cid = int(input("Digite o Chat ID do canal: ").strip())
            lim = input("Quantas aulas deseja estudar neste lote? (padrão 10): ").strip()
            limite = int(lim) if lim.isdigit() else 10
            asyncio.run(estudar_curso(cid, limite))
        elif opcao == "4":
            caminho = input("Digite o caminho da pasta do Google Drive: ").strip()
            indexar_gdrive(caminho)
        elif opcao == "5":
            mostrar_estatisticas()
        else:
            print("Saindo...")

if __name__ == "__main__":
    main()
