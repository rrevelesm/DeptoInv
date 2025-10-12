@echo off
chcp 65001 >nul
title Sistema Padrón de Investigadores UPIIZ
color 0A

echo ====================================
echo   SISTEMA PADRÓN DE INVESTIGADORES
echo   UPIIZ - IPN
echo ====================================
echo.

:: Navegar al directorio del proyecto
cd /d "%~dp0"

echo [1/3] Actualizando código desde GitHub...
git pull origin main
if %errorlevel% neq 0 (
    echo ⚠️  No se pudo actualizar desde GitHub
    echo Continuando con versión local...
    timeout /t 3 >nul
)
echo ✓ Código actualizado
echo.

echo [2/3] Verificando dependencias de Python...
pip install -q -r requirements.txt
if %errorlevel% neq 0 (
    echo ❌ Error instalando dependencias
    echo Ejecuta manualmente: pip install -r requirements.txt
    pause
    exit /b 1
)
echo ✓ Dependencias instaladas
echo.

echo [3/3] Iniciando servidor Flask...
echo.
echo ====================================
echo   SERVIDOR INICIADO
echo ====================================
echo.
echo 🌐 URLs disponibles:
echo.
echo    Local:     http://localhost:5000/formulario
echo    Panel:     http://localhost:5000/panel-formularios
echo    Gen. QR:   http://localhost:5000/generar-qr
echo.
echo 📱 Para acceso desde red local:
echo    1. Ejecuta: ipconfig
echo    2. Busca "Dirección IPv4"
echo    3. Usa: http://[TU_IP]:5000/formulario
echo.
echo ====================================
echo   Presiona CTRL+C para detener
echo ====================================
echo.

:: Iniciar servidor
python app.py

:: Si el servidor se detiene
echo.
echo ====================================
echo   SERVIDOR DETENIDO
echo ====================================
pause

