@echo off
chcp 65001 >nul
title 🛡️ SentinelSOC Live - Mini-SOC & Laboratório Prático de Cibersegurança

echo ======================================================================
echo 🛡️  SENTINELSOC LIVE - LABORATÓRIO PRÁTICO DE CIBERSEGURANÇA (PBL)
echo ======================================================================
echo.
echo [*] Iniciando o Servidor SentinelSOC (Dashboard + Honeypot + IDS/WAF)...
echo [*] Abrindo seu navegador em http://localhost:9090 ...
echo.

start http://localhost:9090
python projeto_pratico_hoje_sentinel_soc\sentinel_server.py

pause
