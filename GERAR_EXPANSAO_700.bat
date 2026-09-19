@echo off
chcp 65001 > nul
title GERADOR DA EXPANSÃO - 700 MAPAS MENTAIS (DEVWORLD AI)
color 0b

echo ===========================================================================
echo   PRODUÇÃO EM LOTE DOS 500 MAPAS MENTAIS DA EXPANSÃO (DEVWORLD AI)
echo   Alvos: Python, DevOps/Linux, Ciberseguranca, UNINTER, Backend, etc.
echo ===========================================================================
echo.

cd /d "%~dp0"
python gerar_expansao_em_lote.py --workers 2

echo.
echo ===========================================================================
echo   ATUALIZANDO OS E-BOOKS EM A4 PAISAGEM PARA IMPRESSÃO...
echo ===========================================================================
python compilar_ebook_para_impressao.py

echo.
echo ===========================================================================
echo   TUDO PRONTO! Pressione qualquer tecla para encerrar.
echo ===========================================================================
pause
