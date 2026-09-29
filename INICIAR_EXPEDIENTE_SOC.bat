@echo off
title CYBERDEFENSE CORP - MESA DE OPERACOES SOC N1
color 0a
echo ========================================================
echo   CYBERDEFENSE CORP - SOC N1 OPERATIONS CENTER
echo   SIMULADOR DE EXPEDIENTE CORPORATIVO (08:00 AS 17:00)
echo ========================================================
echo.
echo Iniciando estacao de trabalho e abrindo painel no navegador...
echo.
start "" "%~dp0simulador_empresa_soc\index.html"
echo Pronto! Painel aberto. Bom plantao, Analista!
timeout /t 3 >nul
exit
