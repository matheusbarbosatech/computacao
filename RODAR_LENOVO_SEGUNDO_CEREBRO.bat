@echo off
chcp 65001 > nul
title CENTRAL SEGUNDO CEREBRO OBSIDIAN - PC LENOVO
color 0A

echo ===============================================================================
echo        🧠 CENTRAL SEGUNDO CÉREBRO TECH & OBSIDIAN (PC LENOVO)
echo ===============================================================================
echo.
echo   [1] 🚀 Executar Robô Minerador do Segundo Cérebro (Atualizar Vault)
echo   [2] 📁 Abrir a Pasta do Vault no Windows Explorer (Para abrir no Obsidian)
echo   [3] ☁️ Iniciar Ponte Telegram -> Google Drive 5TB
echo   [4] 🌐 Abrir Painel Visual HTML de Cursos
echo   [5] ❌ Sair
echo.
echo ===============================================================================
set /p OPCAO="Digite a sua opção e aperte [ENTER]: "

if "%OPCAO%"=="1" (
    echo.
    echo Iniciando Robô Minerador...
    python scripts\minerador_segundo_cerebro_obsidian.py
    echo.
    echo Processo finalizado! Pressione qualquer tecla para voltar ao menu...
    pause > nul
    goto MENU
)

if "%OPCAO%"=="2" (
    echo.
    echo Abrindo a pasta do Vault...
    start "" "SEGUNDO_CEREBRO_VAULT"
    goto MENU
)

if "%OPCAO%"=="3" (
    echo.
    echo Disparando ponte Telegram para Drive...
    python scripts\ponte_telegram_para_drive.py
    pause > nul
    goto MENU
)

if "%OPCAO%"=="4" (
    echo.
    echo Abrindo Painel de Cursos...
    start "" "PAINEL_CRIACAO_DE_PRODUTO.html"
    goto MENU
)

if "%OPCAO%"=="5" (
    exit
)

:MENU
cls
goto MENU
