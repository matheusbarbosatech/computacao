@echo off
chcp 65001 > nul
title Gerador em Lote de 200 Mapas Mentais — DevWorld AI
cd /d "%~dp0"

echo =====================================================================
echo   🚀 GERADOR AUTOMATIZADO DE 200 MAPAS MENTAIS (COMPUTAÇÃO UNINTER)
echo   ⚡ Motor: DevWorld AI (Claude Sonnet 5 / Fable)
echo =====================================================================
echo.
echo Processando fila de geração...
echo Os arquivos já existentes serão reaproveitados automaticamente!
echo.

python -u gerar_todos_em_lote.py

echo.
echo =====================================================================
echo   🏁 Concluído! Todos os mapas estão salvos em: output_mapas\
echo =====================================================================
pause
