@echo off
chcp 65001 > nul
title 🕵️ CYBER THREAT INTELLIGENCE (CTI) & INVESTIGADOR OSINT

echo ======================================================================
echo   🕵️ SUITE DE INTELIGÊNCIA DE AMEAÇAS & OSINT (CTI RECON)
echo ======================================================================
echo.
echo [*] Mapeando superfície de ataque via Certificate Transparency...
echo [*] Perfilando grupos APT e Ransomware (MITRE ATT&CK)...
echo [*] Consolidando Relatório Oficial de CTI em osint_threat_intelligence...
echo.

python osint_threat_intelligence\cti_investigator.py

echo.
echo ======================================================================
echo   Relatório gerado em osint_threat_intelligence\RELATORIO_INTELIGENCIA_CTI.md
echo ======================================================================
pause
