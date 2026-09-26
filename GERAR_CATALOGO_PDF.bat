@echo off
chcp 65001 > nul
title GERADOR DO CATÁLOGO MESTRE EM PDF - GOOGLE DRIVE & TELEGRAM
echo ===============================================================
echo   📑 GERADOR DO CATÁLOGO MESTRE UNIFICADO EM PDF
echo   Google Drive (Cloud-to-Cloud) & Telegram (Streaming)
echo ===============================================================
echo.
cd /d "c:\Users\matheus\Desktop\computacao"
python gerar_pdf_catalogo_mestre.py
echo.
echo ===============================================================
echo   Documento atualizado com sucesso!
echo   Arquivo: CATALOGO_MESTRE_CURSOS_TELEGRAM_E_DRIVE.pdf
echo ===============================================================
pause
