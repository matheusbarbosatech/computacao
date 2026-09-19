"""
=============================================================================
TELEGRAM STUDY ENGINE - COURSE DISCOVERY & STREAMING INDEXER
=============================================================================
Descobre e cataloga automaticamente os cursos nos canais do usuário.
Mapeia a ementa de aulas (#Aula01, vídeos nativos, audios, títulos).
=============================================================================
"""

import asyncio
import os
import sys
import re
import configparser
from datetime import datetime
from pyrogram import Client, enums
from pyrogram.errors import FloodWait

try:
    from .database import get_connection, init_db
except ImportError:
    from database import get_connection, init_db

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
# Lê config do Telegram do diretório TelegramDownloader
TELEGRAM_DIR = r"C:\Users\matheus\Desktop\#COMPUTAÇÃO\TelegramDownloader"
config = configparser.ConfigParser()
config.read(os.path.join(TELEGRAM_DIR, "config.ini"))
api_id = config.get("pyrogram", "api_id")
api_hash = config.get("pyrogram", "api_hash")

class CourseDiscovery:
    def __init__(self, session_name="my_session"):
        self.session_name = session_name
        self.workdir = TELEGRAM_DIR
        init_db()

    async def get_client(self):
        return Client(
            self.session_name,
            api_id=api_id,
            api_hash=api_hash,
            workdir=self.workdir,
            no_updates=True
        )

    async def discover_all_joined_course_channels(self):
        """Descobre todos os canais e grupos de cursos que o usuário participa."""
        app = await self.get_client()
        await app.start()
        
        print("🔍 Analisando canais e grupos do seu Telegram...", flush=True)
        canais_cursos = []
        palavras_curso = [
            "curso", "cursos", "academy", "program", "dev", "tech", "code",
            "python", "java", "hacking", "cloud", "aws", "ia", "dados", "web",
            "fullstack", "frontend", "backend", "concurso", "streaming", "informática"
        ]

        async for dialog in app.get_dialogs():
            chat = dialog.chat
            title = chat.title or chat.first_name or ""
            t_low = title.lower()
            
            eh_curso = any(p in t_low for p in palavras_curso)
            if eh_curso and chat.type in [enums.ChatType.CHANNEL, enums.ChatType.SUPERGROUP]:
                canais_cursos.append({
                    "chat_id": chat.id,
                    "title": title,
                    "username": chat.username,
                    "type": str(chat.type)
                })

        await app.stop()
        return canais_cursos

    async def index_course_lessons(self, chat_id, limit_messages=300):
        """Indexa detalhadamente as aulas de um canal de curso em streaming."""
        app = await self.get_client()
        await app.start()

        chat = await app.get_chat(chat_id)
        chat_title = chat.title or "Curso Sem Título"
        print(f"\n📑 Indexando ementa de aulas: '{chat_title}' (ID: {chat_id})...", flush=True)

        conn = get_connection()
        cursor = conn.cursor()

        # Salva/Atualiza curso
        cursor.execute("""
        INSERT INTO courses (chat_id, title, username, status, updated_at)
        VALUES (?, ?, ?, 'INDEXING', CURRENT_TIMESTAMP)
        ON CONFLICT(chat_id) DO UPDATE SET
            title=excluded.title,
            username=excluded.username,
            updated_at=CURRENT_TIMESTAMP
        """, (chat_id, chat_title, chat.username))
        conn.commit()

        aulas_indexadas = 0
        ids_aulas = []

        async for msg in app.get_chat_history(chat_id, limit=limit_messages):
            if not msg:
                continue

            text = (msg.text or msg.caption or "").strip()
            video = msg.video
            audio = msg.audio
            doc = msg.document

            eh_aula_video = bool(video)
            eh_aula_audio = bool(audio)
            eh_doc_video = bool(doc and (doc.file_name or "").lower().endswith((".mp4", ".mkv", ".mov", ".avi")))

            if eh_aula_video or eh_aula_audio or eh_doc_video:
                # Extrai código da aula (Ex: #Aula01, #F41, Aula 02)
                match_codigo = re.search(r'(#(?:aula|f|m|mod|aula_)?\d+|aula\s*\d+|módulo\s*\d+)', text, re.IGNORECASE)
                codigo_aula = match_codigo.group(0).upper() if match_codigo else "AULA"

                # Extrai título da aula
                linhas = [l.strip() for l in text.split("\n") if l.strip()]
                if linhas:
                    tit_aula = linhas[0]
                elif video and video.file_name:
                    tit_aula = video.file_name
                elif doc and doc.file_name:
                    tit_aula = doc.file_name
                else:
                    tit_aula = f"Aula {msg.id}"

                # Duração e tamanho
                duracao = (video.duration if video else (audio.duration if audio else 0)) or 0
                tam_bytes = (video.file_size if video else (audio.file_size if audio else (doc.file_size if doc else 0))) or 0
                tam_mb = round(tam_bytes / (1024 * 1024), 2)
                tipo_midia = "VIDEO" if (video or eh_doc_video) else "AUDIO"

                cursor.execute("""
                INSERT INTO lessons (chat_id, msg_id, lesson_code, title, duration_seconds, file_size_mb, media_type, summary, status)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, 'PENDING')
                ON CONFLICT(chat_id, msg_id) DO UPDATE SET
                    lesson_code=excluded.lesson_code,
                    title=excluded.title,
                    duration_seconds=excluded.duration_seconds,
                    file_size_mb=excluded.file_size_mb,
                    media_type=excluded.media_type
                """, (chat_id, msg.id, codigo_aula, tit_aula[:120], duracao, tam_mb, tipo_midia, text[:300]))
                
                aulas_indexadas += 1
                ids_aulas.append(msg.id)

        # Atualiza contagem total do curso
        cursor.execute("UPDATE courses SET total_lessons = ?, status = 'INDEXED' WHERE chat_id = ?", (aulas_indexadas, chat_id))
        conn.commit()
        conn.close()

        print(f"✅ {aulas_indexadas} vídeo-aulas em streaming indexadas com sucesso!", flush=True)
        await app.stop()
        return aulas_indexadas

if __name__ == "__main__":
    disc = CourseDiscovery()
    asyncio.run(disc.index_course_lessons(-1001659890212)) # Teste na FOX
