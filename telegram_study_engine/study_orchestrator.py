"""
=============================================================================
TELEGRAM STUDY ENGINE - MASTER STUDY ORCHESTRATOR
=============================================================================
Coordena o fluxo completo de estudo de um curso hospedado no Telegram:
1. Conecta ao canal e obtém dados da aula
2. Extrai áudio streaming leve (Zero-Disk) se necessário
3. Destila o conhecimento com a IA nos 4 pilares
4. Persiste o progresso no SQLite
5. Gera os arquivos finais de estudo
=============================================================================
"""

import asyncio
import os
import sys
import json
import re

try:
    from .database import get_connection, init_db
    from .course_discovery import CourseDiscovery
    from .audio_stream_extractor import AudioStreamExtractor
    from .ai_study_distiller import AIStudyDistiller
except ImportError:
    from database import get_connection, init_db
    from course_discovery import CourseDiscovery
    from audio_stream_extractor import AudioStreamExtractor
    from ai_study_distiller import AIStudyDistiller

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
OUTPUT_DIR = os.path.join(BASE_DIR, "output_estudos")
os.makedirs(OUTPUT_DIR, exist_ok=True)

class StudyOrchestrator:
    def __init__(self):
        init_db()
        self.discovery = CourseDiscovery()
        self.audio_extractor = AudioStreamExtractor()
        self.distiller = AIStudyDistiller()

    async def study_single_lesson(self, chat_id, msg_id, extract_audio=False):
        """Estuda uma aula específica de um canal de streaming do Telegram."""
        conn = get_connection()
        cursor = conn.cursor()

        # Verifica se já está indexada
        cursor.execute("SELECT * FROM lessons WHERE chat_id = ? AND msg_id = ?", (chat_id, msg_id))
        row = cursor.fetchone()

        # Se não estiver no banco, busca na hora
        if not row:
            app = await self.discovery.get_client()
            await app.start()
            chat = await app.get_chat(chat_id)
            msg = await app.get_messages(chat_id, msg_id)
            await app.stop()

            text = msg.text or msg.caption or "Aula Sem Título"
            tit = text.split("\n")[0][:100]
            duracao = (msg.video.duration if msg.video else (msg.audio.duration if msg.audio else 0)) or 0
            tam_mb = round((msg.video.file_size if msg.video else 0) / (1024 * 1024), 2)
            c_title = chat.title or "Curso Telegram"
            code = f"#Aula_{msg.id}"
        else:
            tit = row["title"]
            duracao = row["duration_seconds"]
            tam_mb = row["file_size_mb"]
            code = row["lesson_code"]
            cursor.execute("SELECT title FROM courses WHERE chat_id = ?", (chat_id,))
            c_row = cursor.fetchone()
            c_title = c_row["title"] if c_row else "Curso Telegram"

        print(f"\n🎓 ========================================================")
        print(f"📚 ESTUDANDO AULA: {tit}")
        print(f"🏛️ CURSO: {c_title} | CÓDIGO: {code}")
        print(f"🎓 ========================================================", flush=True)

        audio_path = None
        if extract_audio:
            try:
                audio_path = await self.audio_extractor.extract_audio_from_lesson(chat_id, msg_id)
            except Exception as e:
                print(f"⚠️ Nota de áudio: {e}")

        # Destila o conhecimento com a IA
        resultado = self.distiller.distill_lesson(
            lesson_title=tit,
            lesson_code=code,
            course_title=c_title
        )

        # Salva pasta específica do curso
        slug_curso = re.sub(r'[^\w\-_\. ]', '_', c_title).strip()
        pasta_curso = os.path.join(OUTPUT_DIR, slug_curso)
        os.makedirs(pasta_curso, exist_ok=True)

        slug_aula = re.sub(r'[^\w\-_\. ]', '_', code).strip()
        res_file = os.path.join(pasta_curso, f"{slug_aula}_resumo_completo.json")
        with open(res_file, "w", encoding="utf-8") as f:
            json.dump(resultado, f, ensure_ascii=False, indent=2)

        print(f"💾 Pacote de estudo completo gerado em: {res_file}", flush=True)
        print(f"   🗺️ Mapa Mental: '{resultado['mapa_mental']['titulo_central']}'")
        print(f"   🧠 Anki: {len(resultado['anki_cards'])} Flashcards Atômicos")
        print(f"   🎬 VideoScribe: Roteiro 9:16 '{resultado['videoscribe_script']['titulo']}'")
        print(f"   ⚡ Duolingo: {len(resultado['duolingo_quiz'])} Questões Interativas")

        # Limpeza do áudio se foi extraído
        if audio_path:
            self.audio_extractor.cleanup_audio(audio_path)

        # Atualiza status no banco
        cursor.execute("""
        UPDATE lessons SET status = 'DISTILLED' WHERE chat_id = ? AND msg_id = ?
        """, (chat_id, msg_id))
        conn.commit()
        conn.close()

        return resultado

    async def study_entire_course(self, chat_id, max_lessons=15):
        """Estuda em lote as aulas de um canal em streaming."""
        # 1. Indexa se necessário
        await self.discovery.index_course_lessons(chat_id)

        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM lessons WHERE chat_id = ? AND status = 'PENDING' ORDER BY msg_id ASC LIMIT ?", (chat_id, max_lessons))
        aulas = cursor.fetchall()
        conn.close()

        print(f"\n🚀 Iniciando estudo em lote de {len(aulas)} aulas...", flush=True)
        estudadas = 0
        for row in aulas:
            await self.study_single_lesson(row["chat_id"], row["msg_id"])
            estudadas += 1
            await asyncio.sleep(0.5)

        print(f"\n🏆 Curso concluído! {estudadas} aulas estudadas e transformadas em ativos educacionais!", flush=True)
        return estudadas
