@echo off
chcp 65001 > nul
title 🕵️ INVESTIGAÇÃO DIGITAL & PERÍCIA FORENSE (DFIR)

echo ======================================================================
echo   🕵️ SUITE DE INVESTIGAÇÃO DIGITAL & TRIAGEM FORENSE
echo ======================================================================
echo.
echo [*] Coletando telemetria volátil e calculando hashes de integridade...
echo [*] Analisando evidências e gerando o Laudo Pericial Oficial...
echo.

python investigacao_digital\forensic_investigator.py

echo.
echo ======================================================================
echo   Laudo Pericial gerado em investigacao_digital\LAUDO_PERICIAL_FORENSE.md
echo ======================================================================
pause
