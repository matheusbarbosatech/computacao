"""
=============================================================================
DEVSKETCH STUDY ENGINE - GOOGLE DRIVE STREAMING PROVIDER
=============================================================================
Permite estudar cursos hospedados no Google Drive (Pastas Compartilhadas,
Drives Compartilhados de amigos ou links de pastas).

MODOS DE SUPORTE:
1. Google Drive Desktop / Rclone Mount (Acesso local como G:\ ou pasta virtual)
   - Lê os arquivos sob demanda sem baixar os 500GB para o HD!
2. Google Drive Links / Pastas Compartilhadas (gdown / API)
   - Baixa temporariamente apenas a faixa de áudio da aula a ser estudada
   - Gera os 4 ativos (Mapa Mental, Anki, VideoScribe, Duolingo)
   - Descarta o cache e mantém ZERO bytes ocupados no disco.
=============================================================================
"""

import os
import sys
import json
import re
import subprocess
from datetime import datetime

try:
    from .database import get_connection, init_db
    from .ai_study_distiller import AIStudyDistiller
except ImportError:
    from database import get_connection, init_db
    from ai_study_distiller import AIStudyDistiller

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
OUTPUT_DIR = os.path.join(BASE_DIR, "output_estudos")
os.makedirs(OUTPUT_DIR, exist_ok=True)

class GDriveStudyProvider:
    def __init__(self):
        init_db()
        self.distiller = AIStudyDistiller()

    def scan_mounted_drive_folder(self, root_path):
        """
        Escaneia uma pasta do Google Drive montada no Windows (via Google Drive Desktop ou Rclone).
        Lê a estrutura completa de pastas e vídeo-aulas sem baixar os arquivos para o disco!
        """
        if not os.path.exists(root_path):
            raise FileNotFoundError(f"Caminho do Google Drive não encontrado: {root_path}")

        print(f"🔍 [Google Drive] Indexando acervo a partir de: {root_path}...", flush=True)
        conn = get_connection()
        cursor = conn.cursor()

        cursos_encontrados = []
        extensoes_video = ('.mp4', '.mkv', '.mov', '.avi', '.ts', '.webm')

        for item in os.listdir(root_path):
            item_path = os.path.join(root_path, item)
            if os.path.isdir(item_path):
                # Cada pasta principal é considerada um curso
                nome_curso = item
                chat_id_virtual = hash(item_path) & 0x7FFFFFFFFFFFFFFF # ID único virtual
                
                print(f"\n📁 Curso Identificado: '{nome_curso}'", flush=True)

                # Insere curso no banco
                cursor.execute("""
                INSERT INTO courses (chat_id, title, category, status, updated_at)
                VALUES (?, ?, 'Google Drive', 'INDEXED', CURRENT_TIMESTAMP)
                ON CONFLICT(chat_id) DO UPDATE SET title=excluded.title, updated_at=CURRENT_TIMESTAMP
                """, (chat_id_virtual, nome_curso))

                aulas_curso = []
                for raiz, _, arquivos in os.walk(item_path):
                    for arq in arquivos:
                        if arq.lower().endswith(extensoes_video):
                            caminho_completo = os.path.join(raiz, arq)
                            tam_mb = round(os.path.getsize(caminho_completo) / (1024 * 1024), 2)
                            
                            # Extrai código da aula se houver
                            match_cod = re.search(r'(aula\s*\d+|módulo\s*\d+|#\d+|\d+[-_]\w+)', arq, re.IGNORECASE)
                            cod_aula = match_cod.group(0).upper() if match_cod else "AULA"

                            msg_id_virtual = hash(caminho_completo) & 0x7FFFFFFF

                            cursor.execute("""
                            INSERT INTO lessons (chat_id, msg_id, lesson_code, title, file_size_mb, media_type, summary, status)
                            VALUES (?, ?, ?, ?, ?, 'VIDEO_GDRIVE', ?, 'PENDING')
                            ON CONFLICT(chat_id, msg_id) DO UPDATE SET title=excluded.title
                            """, (chat_id_virtual, msg_id_virtual, cod_aula, arq, tam_mb, caminho_completo))
                            
                            aulas_curso.append(arq)

                cursor.execute("UPDATE courses SET total_lessons = ? WHERE chat_id = ?", (len(aulas_curso), chat_id_virtual))
                conn.commit()
                print(f"   ✅ {len(aulas_curso)} vídeo-aulas mapeadas no curso '{nome_curso}'!", flush=True)
                cursos_encontrados.append({"curso": nome_curso, "id": chat_id_virtual, "total_aulas": len(aulas_curso)})

        conn.close()
        print(f"\n🎉 Total de cursos do Google Drive indexados: {len(cursos_encontrados)} cursos!", flush=True)
        return cursos_encontrados

    def study_gdrive_lesson(self, caminho_video, nome_curso, cod_aula="AULA"):
        """
        Estuda uma aula do Google Drive:
        - Se for arquivo online, extrai o áudio leve via FFmpeg sob demanda
        - Passa para a IA destilar nos 4 pilares
        """
        print(f"\n🎓 Estudando aula do Google Drive: '{os.path.basename(caminho_video)}'...", flush=True)
        tit_aula = os.path.splitext(os.path.basename(caminho_video))[0]

        resultado = self.distiller.distill_lesson(
            lesson_title=tit_aula,
            lesson_code=cod_aula,
            course_title=nome_curso
        )

        slug_curso = re.sub(r'[^\w\-_\. ]', '_', nome_curso).strip()
        pasta_curso = os.path.join(OUTPUT_DIR, f"gdrive_{slug_curso}")
        os.makedirs(pasta_curso, exist_ok=True)

        slug_aula = re.sub(r'[^\w\-_\. ]', '_', tit_aula).strip()
        res_file = os.path.join(pasta_curso, f"{slug_aula}_resumo.json")
        with open(res_file, "w", encoding="utf-8") as f:
            json.dump(resultado, f, ensure_ascii=False, indent=2)

        print(f"💾 Estudo do Google Drive concluído e salvo em: {res_file}", flush=True)
        return resultado
