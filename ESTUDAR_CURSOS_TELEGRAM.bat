@echo off
chcp 65001 > nul
title DevSketch - Telegram Course Study Engine
color 0a

echo ==============================================================================
echo 🤖 DEVSKETCH - TELEGRAM COURSE STUDY ENGINE (ZERO-DISK STREAMING)
echo ==============================================================================
echo Estuda cursos de streaming do Telegram e gera automaticamente:
echo   🗺️ 1. Mapas Mentais Sketchnote de alta densidade
echo   🧠 2. Flashcards Atômicos para o Anki (.apkg)
echo   🎬 3. Roteiros e Animações no VideoScribe (9:16 Vertical)
echo   ⚡ 4. Quizzes Interativos para o Duolingo da Computação
echo ==============================================================================
echo.

cd /d "C:\Users\matheus\Desktop\gerador-mapas-computacao\telegram_study_engine"
python -u telegram_study_cli.py

echo.
echo Pressione qualquer tecla para fechar...
pause > nul
