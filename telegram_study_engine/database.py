"""
=============================================================================
TELEGRAM STUDY ENGINE - DATABASE & STATE PERSISTENCE LAYER
=============================================================================
Gerencia o banco de dados SQLite local (courses_study_database.db)
Rastreia canais, cursos, aulas em streaming e artefatos gerados.
=============================================================================
"""

import sqlite3
import os
import json
from datetime import datetime

DB_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), "courses_study_database.db")

def get_connection():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    conn = get_connection()
    cursor = conn.cursor()

    # Tabela de Cursos / Canais
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS courses (
        chat_id INTEGER PRIMARY KEY,
        title TEXT NOT NULL,
        username TEXT,
        category TEXT DEFAULT 'Geral',
        total_lessons INTEGER DEFAULT 0,
        status TEXT DEFAULT 'DISCOVERED', -- DISCOVERED, INDEXED, STUDYING, COMPLETED
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
    """)

    # Tabela de Aulas (Streaming)
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS lessons (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        chat_id INTEGER NOT NULL,
        msg_id INTEGER NOT NULL,
        lesson_code TEXT, -- Ex: #Aula01, #F41
        title TEXT NOT NULL,
        duration_seconds INTEGER DEFAULT 0,
        file_size_mb REAL DEFAULT 0,
        media_type TEXT, -- VIDEO, AUDIO, DOCUMENT
        summary TEXT,
        status TEXT DEFAULT 'PENDING', -- PENDING, STREAMED, DISTILLED, FAILED
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY (chat_id) REFERENCES courses (chat_id),
        UNIQUE(chat_id, msg_id)
    )
    """)

    # Tabela de Ativos / Artefatos Gerados pelo Estudo
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS study_artifacts (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        lesson_id INTEGER NOT NULL,
        artifact_type TEXT NOT NULL, -- MIND_MAP, ANKI_CARDS, VIDEOSCRIBE_SCRIPT, DUOLINGO_QUIZ
        file_path TEXT,
        content_json TEXT,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY (lesson_id) REFERENCES lessons (id)
    )
    """)

    conn.commit()
    conn.close()

if __name__ == "__main__":
    init_db()
    print(f"✅ Banco de dados inicializado em: {DB_PATH}")
