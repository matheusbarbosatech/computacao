@echo off
chcp 65001 > nul
title Compilador de PDFs A4 Paisagem para Impressão
cd /d "%~dp0"

echo =====================================================================
echo   🖨️ COMPILANDO E-BOOKS DAS ESCOLAS EM A4 PAISAGEM (PRINT-READY)
echo   🎓 Padrão Gráfica: Wire-o / Fichário / Livro
echo =====================================================================
echo.

python compilar_ebook_para_impressao.py

echo.
echo =====================================================================
echo   ✅ Concluído! Os PDFs estão salvos dentro da pasta 'pdf/' de cada escola!
echo =====================================================================
pause
