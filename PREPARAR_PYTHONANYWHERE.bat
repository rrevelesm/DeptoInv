@echo off
chcp 65001 > nul
cls
echo ═══════════════════════════════════════════════════════════
echo   📦 PREPARAR PROYECTO PARA PYTHONANYWHERE
echo ═══════════════════════════════════════════════════════════
echo.
echo Este script creará un archivo ZIP con todo lo necesario
echo para desplegar tu panel de administración en internet.
echo.
echo ═══════════════════════════════════════════════════════════
echo.
pause
echo.

python preparar_pythonanywhere.py

echo.
echo ═══════════════════════════════════════════════════════════
echo.
pause

