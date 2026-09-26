@echo off
chcp 65001 > nul
title 🛡️ CLONADOR DE ALTA PRIORIDADE - HACKONE & ACERVO CYBER

echo ======================================================================
echo   ☁️ CLONAGEM PRIORITÁRIA GOOGLE DRIVE: HACKONE & ACERVO CYBER
echo ======================================================================
echo.
echo [*] Pastas em clonagem:
echo     1. Hackone (Trilhas Ciberseguranca, Cloud, Mikrotik, Redes)
echo     2. Foco em SEC (4 Pilares de Cyber e Investigacao Digital)
echo     3. Pentest Web Profissional (Geraldo Alcantara)
echo.
echo [*] Destino: meudrive:MEU_ACERVO_CLONADO/
echo [*] Modo: Cloud-to-Cloud (Zero consumo de disco local)
echo.

python clonar_hackone_e_cyber.py

echo.
echo ======================================================================
echo   Processo finalizado! Pressione qualquer tecla para fechar.
echo ======================================================================
pause
