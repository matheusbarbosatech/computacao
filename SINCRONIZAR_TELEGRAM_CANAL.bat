@echo off
chcp 65001 >nul
title SINCRONIZADOR TELEGRAM - CANAL COMPUTAÇÃO
echo ======================================================================
echo 🚀 SINCRONIZANDO MATERIAIS PARA O SEU CANAL PRIVADO DO TELEGRAM
echo Destino: Canal COMPUTAÇÃO (https://t.me/+Dqtyyae4LSQyOTUx)
echo ======================================================================
echo.
cd /d "C:\Users\matheus\Desktop\#COMPUTAÇÃO\TelegramDownloader"
python clonar_materiais_para_canal.py
echo.
echo ======================================================================
echo ✅ Processo finalizado! Abra o Telegram para conferir os arquivos.
echo ======================================================================
pause
