# -*- coding: utf-8 -*-
"""
Teste dos dois repositórios solicitados pelo Matheus:
1. Kokoro-82M (hexgrad/kokoro - Top 1 Tendências GitHub)
2. F5-TTS (SWivid/F5-TTS - Flow-Matching)
"""
import os
import sys
import shutil
from gradio_client import Client, handle_file

sys.stdout.reconfigure(encoding='utf-8', errors='ignore')
sys.stderr.reconfigure(encoding='utf-8', errors='ignore')

BASE_DIR = r"c:\Users\matheus\Desktop\computacao"
OUTPUT_DIR = os.path.join(BASE_DIR, "output_reels_demo")
os.makedirs(OUTPUT_DIR, exist_ok=True)

TEXTO = (
    "Se você usa o WhatsApp todo dia, nunca responda uma mensagem que começar com essa frase: "
    "Oi mãe, troquei de número, salva aí. Isso é golpe de engenharia social! "
    "Manda esse vídeo no grupo da sua família para blindar quem você ama."
)

def testar_kokoro():
    print("=" * 65)
    print("🚀 [1/2] TESTANDO KOKORO-82M (hexgrad/kokoro)")
    print("=" * 65)
    try:
        c = Client("Pendrokar/Kokoro-TTS")
        
        # Teste 1: am_adam (Masculino profissional)
        print("🎙️ Gerando Kokoro (am_adam, pt)...")
        res1 = c.predict(
            text=TEXTO,
            voice="am_adam",
            speed=1.0,
            use_gpu=True,
            lang="pt",
            api_name="/generate_all"
        )
        dest1 = os.path.join(OUTPUT_DIR, "teste_kokoro_adam.wav")
        shutil.copyfile(res1, dest1)
        print(f"✅ Salvo: {dest1} ({os.path.getsize(dest1)} bytes)")
        
        # Teste 2: bm_george (Masculino documental britânico adaptado)
        print("🎙️ Gerando Kokoro (bm_george, pt)...")
        res2 = c.predict(
            text=TEXTO,
            voice="bm_george",
            speed=1.0,
            use_gpu=True,
            lang="pt",
            api_name="/generate_all"
        )
        dest2 = os.path.join(OUTPUT_DIR, "teste_kokoro_george.wav")
        shutil.copyfile(res2, dest2)
        print(f"✅ Salvo: {dest2} ({os.path.getsize(dest2)} bytes)")
        
    except Exception as e:
        print(f"❌ Erro no Kokoro: {e}")

def testar_f5_tts():
    print("\n" + "=" * 65)
    print("🚀 [2/2] TESTANDO F5-TTS (SWivid/F5-TTS - Flow Matching)")
    print("=" * 65)
    try:
        # F5-TTS usa zero-shot flow matching com uma referência limpa de voz narrativa
        c = Client("mrfakename/E2-F5-TTS")
        
        # Usamos uma referência em áudio de alta clareza
        ref_audio = os.path.join(BASE_DIR, "minha_voz_referencia.wav")
        ref_text = "oi, tudo bem? estou mandando esse áudio aqui pra você testar."
        
        print("🎙️ Enviando para síntese F5-TTS...")
        res = c.predict(
            ref_audio=handle_file(ref_audio),
            ref_text=ref_text,
            gen_text=TEXTO,
            remove_silence=True,
            api_name="/predict"
        )
        dest = os.path.join(OUTPUT_DIR, "teste_f5_tts_flow.wav")
        shutil.copyfile(res, dest)
        print(f"✅ Salvo: {dest} ({os.path.getsize(dest)} bytes)")
    except Exception as e:
        print(f"❌ Erro no F5-TTS: {e}")

if __name__ == "__main__":
    testar_kokoro()
    testar_f5_tts()
