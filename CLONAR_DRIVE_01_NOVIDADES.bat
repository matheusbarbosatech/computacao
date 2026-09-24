@echo off
chcp 65001 > nul
title CLONADOR GOOGLE DRIVE - 01. NOVIDADES
echo ===============================================================
echo   ☁️ CLONAGEM DO GOOGLE DRIVE COM MONITOR DE COTA 750GB
echo ===============================================================
echo.
cd /d "C:\Users\matheus\Desktop\#COMPUTAÇÃO\TelegramDownloader"
python clonar_drive_com_monitor_cota.py
echo.
echo ===============================================================
echo   Processo finalizado!
echo ===============================================================
pause
