@echo off
chcp 65001 > nul
title Estúdio de Mapas Mentais UNINTER — DevWorld AI
cd /d "%~dp0"

echo =====================================================================
echo   🚀 INICIANDO ESTÚDIO DE MAPAS MENTAIS (CIÊNCIA DA COMPUTAÇÃO)
echo   🎓 Matriz Curricular UNINTER (3.210h) & DevWorld AI
echo =====================================================================
echo.
echo Abrindo servidor local em http://localhost:8080 ...
echo Pressione Ctrl+C nesta janela quando desejar encerrar.
echo.

python servidor_studio.py

pause
