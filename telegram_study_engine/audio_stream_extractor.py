"""
=============================================================================
TELEGRAM STUDY ENGINE - ZERO-DISK STREAMING AUDIO EXTRACTOR
=============================================================================
Baixa de forma sob demanda apenas o áudio da aula em streaming.
Converte para áudio ultra-leve (16kHz mono MP3) com FFmpeg e descarta
imediatamente o arquivo bruto de vídeo para manter ZERO de uso no disco.
=============================================================================
"""

import asyncio
import os
import sys
import subprocess
import configparser
import shutil
from pyrogram import Client

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
CACHE_DIR = os.path.join(BASE_DIR, "temp_stream_cache")
os.makedirs(CACHE_DIR, exist_ok=True)

TELEGRAM_DIR = r"C:\Users\matheus\Desktop\#COMPUTAÇÃO\TelegramDownloader"
config = configparser.ConfigParser()
config.read(os.path.join(TELEGRAM_DIR, "config.ini"))
api_id = config.get("pyrogram", "api_id")
api_hash = config.get("pyrogram", "api_hash")

class AudioStreamExtractor:
    def __init__(self, session_name="my_session"):
        self.session_name = session_name
        self.workdir = TELEGRAM_DIR

    async def extract_audio_from_lesson(self, chat_id, msg_id):
        """
        Baixa o vídeo temporário, extrai áudio MP3 de alta qualidade e
        remove o vídeo bruto imediatamente para economizar 100% de espaço.
        """
        app = Client(self.session_name, api_id=api_id, api_hash=api_hash, workdir=self.workdir, no_updates=True)
        await app.start()

        msg = await app.get_messages(chat_id, msg_id)
        if not msg or not (msg.video or msg.audio or msg.document):
            await app.stop()
            raise ValueError(f"Mensagem {msg_id} não possui mídia de vídeo ou áudio.")

        print(f"📥 Baixando streaming temporário da aula (Chat: {chat_id}, Msg: {msg_id})...", flush=True)

        temp_video_path = await app.download_media(
            message=msg,
            file_name=os.path.join(CACHE_DIR, f"lesson_{chat_id}_{msg_id}.tmp")
        )

        await app.stop()

        output_audio_path = os.path.join(CACHE_DIR, f"audio_{chat_id}_{msg_id}.mp3")

        print("🎵 Extraindo faixa de áudio compacta via FFmpeg...", flush=True)
        # Converte para MP3 16kHz mono de voz (tamanho médio de ~5MB a 15MB)
        cmd = [
            "ffmpeg", "-y",
            "-i", temp_video_path,
            "-vn",
            "-acodec", "libmp3lame",
            "-ar", "16000",
            "-ac", "1",
            "-b:a", "32k",
            output_audio_path
        ]

        try:
            subprocess.run(cmd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, check=True)
        finally:
            # Apaga o vídeo bruto imediatamente!
            if os.path.exists(temp_video_path):
                try:
                    os.remove(temp_video_path)
                    print("🧹 Vídeo bruto descartado da memória com sucesso.", flush=True)
                except Exception:
                    pass

        audio_size_mb = round(os.path.getsize(output_audio_path) / (1024 * 1024), 2)
        print(f"✅ Áudio pronto para estudo: {output_audio_path} ({audio_size_mb} MB)", flush=True)

        return output_audio_path

    def cleanup_audio(self, audio_path):
        """Remove o arquivo de áudio após o estudo estar concluído."""
        if os.path.exists(audio_path):
            try:
                os.remove(audio_path)
                print(f"🧹 Áudio temporário {os.path.basename(audio_path)} removido.", flush=True)
            except Exception:
                pass
