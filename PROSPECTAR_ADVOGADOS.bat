@echo off
chcp 65001 > nul
title ⚖️ PROSPECTOR DE ADVOGADOS — INTELIGÊNCIA PATRIMONIAL & OSINT
cd /d "c:\Users\mathe\Desktop\computacao"

echo ===========================================================================
echo   ⚖️ CENTRAL DE PROSPECÇÃO DE ADVOGADOS (CAMPO GRANDE / ZONA OESTE RJ)
echo ===========================================================================
echo.
echo Escolha a opção:
echo  [1] Listar Advogados Mapeados e Gerar Links de WhatsApp
echo  [2] Minerar Novos Escritórios na Região (Overpass / OpenStreetMap)
echo  [3] Abrir Pasta com o Dossiê Pericial Modelo e Cartas
echo  [4] Sair
echo.
set /p OPCAO="👉 Digite a opção (1-4) [Padrão: 1]: "
if "%OPCAO%"=="" set OPCAO=1

if "%OPCAO%"=="1" (
    echo.
    echo 📋 Listando escritórios e links de abordagem direta...
    echo.
    set PYTHONIOENCODING=utf-8
    C:\Python312\python.exe scripts\minerador_e_prospector_advogados.py --listar
)

if "%OPCAO%"=="2" (
    echo.
    echo 🔍 Minerando novos escritórios de advocacia na Zona Oeste...
    echo.
    set PYTHONIOENCODING=utf-8
    C:\Python312\python.exe scripts\minerador_e_prospector_advogados.py --minerar
)

if "%OPCAO%"=="3" (
    echo.
    echo 📂 Abrindo pasta de inteligência forense...
    start "" "c:\Users\mathe\Desktop\computacao\AGENCIA_INTELIGENCIA_FORENSE"
)

echo.
echo ===========================================================================
echo Processo Concluído!
echo ===========================================================================
pause
