@echo off
chcp 65001 > nul
title PROSPECTOR B2B — CLIENTES DE CIBERSEGURANCA & LGPD
echo ===============================================================
echo   💼 SISTEMA DE PROSPECÇÃO B2B PARA SERVIÇOS DE CYBER
echo ===============================================================
echo.
echo Escolha o nicho de empresas que deseja prospectar:
echo [1] Clínicas Médicas & Odontológicas
echo [2] Escritórios de Advocacia
echo [3] Escritórios de Contabilidade
echo [4] Imobiliárias
echo.
set /p opt="Escolha uma opção (1-4) [Padrão: 1]: "

if "%opt%"=="2" (
    set NICHO=advocacia
) else if "%opt%"=="3" (
    set NICHO=contabilidade
) else if "%opt%"=="4" (
    set NICHO=imobiliaria
) else (
    set NICHO=clinica
)

set /p CIDADE="Digite o nome da cidade [Padrão: Curitiba]: "
if "%CIDADE%"=="" set CIDADE=Curitiba

echo.
echo ===============================================================
echo 🚀 Buscando %NICHO% em %CIDADE% e gerando diagnósticos...
echo ===============================================================
echo.

python prospeccao_b2b_cyber\orquestrador_prospeccao.py %NICHO% %CIDADE% 4

echo.
echo Abrindo o painel de prospecção e scripts de WhatsApp...
start PAINEL_PROSPECCAO_B2B_CYBER.md
pause
