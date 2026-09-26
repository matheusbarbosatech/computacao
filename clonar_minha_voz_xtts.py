# -*- coding: utf-8 -*-
"""
=============================================================================
CLONADOR DE VOZ ZERO-SHOT (COQUI XTTS-v2) COM AUDIO DE REFERÊNCIA DO WHATSAPP
=============================================================================
Usa o áudio de WhatsApp do Matheus para clonar a voz real dele
usando a arquitetura XTTS-v2 sem fritar o computador local.
=============================================================================
"""
import os
import sys
import shutil
from gradio_client import Client, handle_file

sys.stdout.reconfigure(encoding='utf-8', errors='ignore')
sys.stderr.reconfigure(encoding='utf-8', errors='ignore')

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
REF_AUDIO_ORIGINAL = r"C:\Users\matheus\Desktop\WhatsApp Ptt 2026-09-23 at 11.39.54.ogg"
REF_AUDIO_WAV = os.path.join(BASE_DIR, "minha_voz_referencia.wav")
OUTPUT_DIR = os.path.join(BASE_DIR, "output_reels_demo")
os.makedirs(OUTPUT_DIR, exist_ok=True)
OUTPUT_TARGET = os.path.join(OUTPUT_DIR, "minha_voz_clonada_xtts.wav")

TEXTO_PARA_FALAR = (
    "Se você usa o WhatsApp todo dia, nunca responda uma mensagem que começar com essa frase: "
    "Oi mãe, troquei de número, salva aí. "
    "Criminosos colocam a foto do seu parente e pedem um Pix urgente! "
    "Presta muita atenção: número novo nunca ganha dinheiro. "
    "Manda esse vídeo no grupo da sua família para blindar quem você ama."
)

def garantir_audio_wav():
    if not os.path.exists(REF_AUDIO_WAV) and os.path.exists(REF_AUDIO_ORIGINAL):
        print("🔄 Convertendo áudio do WhatsApp para WAV 24kHz mono...")
        import subprocess
        cmd = ["ffmpeg", "-y", "-i", REF_AUDIO_ORIGINAL, "-ar", "24000", "-ac", "1", REF_AUDIO_WAV]
        subprocess.run(cmd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, check=True)
    print(f"✅ Áudio de referência pronto: {REF_AUDIO_WAV} ({os.path.getsize(REF_AUDIO_WAV)} bytes)")

def executar_clonagem():
    print("=" * 65)
    print("🚀 INICIANDO CLONAGEM DE VOZ (COQUI XTTS-v2)")
    print(f"👤 Fonte: Áudio do Matheus (WhatsApp Ptt 2026-09-23 at 11.39.54)")
    print("=" * 65)
    
    garantir_audio_wav()
    
    print("\n🌐 Conectando ao cluster XTTS-v2 com aceleração por GPU...")
    client = Client("tonyassi/voice-clone")
    
    print("🎙️ Enviando amostra de voz e gerando fala com suas características vocais...")
    result = client.predict(
        text=TEXTO_PARA_FALAR,
        audio=handle_file(REF_AUDIO_WAV),
        api_name="/clone"
    )
    
    print(f"📦 Arquivo gerado temporário: {result}")
    shutil.copyfile(result, OUTPUT_TARGET)
    
    tamanho_kb = os.path.getsize(OUTPUT_TARGET) / 1024
    print("=" * 65)
    print(f"🎉 SUA VOZ FOI CLONADA COM SUCESSO!")
    print(f"📍 Arquivo final: {OUTPUT_TARGET}")
    print(f"📦 Tamanho: {tamanho_kb:.1f} KB")
    print("=" * 65)

if __name__ == "__main__":
    executar_clonagem()
