@echo off
chcp 65001 >nul
title GERADOR DE VÍDEOS VERTICAIS (VIDEOSCRIBE CLONE)
echo ======================================================================
echo 🎬 GERADOR DE VÍDEOS VERTICAIS WHITEBOARD (9:16 REELS / TIKTOK)
echo Motor: Python + OpenCV + Pillow + Edge-TTS + FFmpeg
echo ======================================================================
echo.
cd /d "%~dp0videoscribe_engine"
python -u videoscribe_engine.py
echo.
echo ======================================================================
echo ✅ Vídeo gerado com sucesso na pasta 'videoscribe_engine\output'!
echo ======================================================================
pause
