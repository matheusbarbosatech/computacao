@echo off
chcp 65001 > nul
title RADAR ANTI-GOLPES & ALERTAS FAMILIARES
echo ===============================================================
echo   🚨 VARRENDO NOTÍCIAS DE GOLPES, FRAUDES & SEGURANÇA DIGITAL
echo ===============================================================
echo.
python scripts/radar_anti_golpe_noticias.py
echo.
echo ===============================================================
echo   Painel atualizado em: PAINEL_ALERTAS_GOLPES_VIRAL.md
echo ===============================================================
pause
