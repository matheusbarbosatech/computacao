@echo off
title CYBERDEFENSE 3D - SIMULADOR CORPORATIVO POV
color 0b
echo ========================================================
echo   CYBERDEFENSE 3D - FIRST PERSON WORK SIMULATOR (POV)
echo   EXPEDIENTE CORPORATIVO 08:00 AS 17:00 (SOC N1)
echo ========================================================
echo.
echo Abrindo escritorio 3D interativo no seu navegador...
echo.
start "" "%~dp0simulador_empresa_3d\index.html"
echo Pronto! Aproveite a imersao em primeira pessoa. Bom plantao!
timeout /t 3 >nul
exit
