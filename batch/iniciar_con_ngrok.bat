@echo off
chcp 65001 >nul
title Sistema UPIIZ - Acceso desde Internet (Ngrok)
color 0A

echo ═══════════════════════════════════════════════════════════════
echo  🌐 SISTEMA DE GESTIÓN DE INVESTIGACIÓN - UPIIZ
echo  Modo: Acceso desde Internet con Ngrok
echo  M. en C. Rafael Reveles Martínez
echo ═══════════════════════════════════════════════════════════════
echo.

REM Verificar si existe ngrok
if not exist ngrok.exe (
    echo ❌ ERROR: No se encontró ngrok.exe
    echo.
    echo 📥 Por favor descarga ngrok:
    echo    1. Ve a: https://ngrok.com/download
    echo    2. Descarga la versión para Windows
    echo    3. Descomprime ngrok.exe en esta carpeta
    echo.
    pause
    exit /b 1
)

echo ✅ Ngrok encontrado
echo.
echo 📋 INSTRUCCIONES:
echo.
echo    1. Se abrirán DOS ventanas:
echo       - Ventana 1: Servidor Flask
echo       - Ventana 2: Ngrok
echo.
echo    2. En la ventana de Ngrok verás una URL como:
echo       https://abc123.ngrok.io
echo.
echo    3. Comparte con investigadores:
echo       https://abc123.ngrok.io/formulario
echo.
echo    4. Para detener: Cierra ambas ventanas
echo.
echo ⚠️  IMPORTANTE:
echo    - Tu computadora debe permanecer ENCENDIDA
echo    - La URL cambia cada vez que reinicias
echo    - Sesión gratuita: 2 horas
echo.

pause
echo.
echo 🚀 Iniciando servidor Flask...
start "Flask Server - UPIIZ" /MIN python app.py

echo ⏳ Esperando 5 segundos para que Flask inicie...
timeout /t 5 /nobreak >nul

echo 🌐 Iniciando túnel Ngrok...
start "Ngrok Tunnel - UPIIZ" ngrok http 5000

echo.
echo ═══════════════════════════════════════════════════════════════
echo  ✅ SISTEMA INICIADO
echo.
echo  📝 PASOS FINALES:
echo.
echo  1. Ve a la ventana de "Ngrok Tunnel - UPIIZ"
echo  2. Busca la línea que dice "Forwarding"
echo  3. Copia la URL HTTPS (ejemplo: https://abc123.ngrok.io)
echo  4. Comparte: https://TU-URL-NGROK.ngrok.io/formulario
echo.
echo  📊 Para ver formularios recibidos:
echo     https://TU-URL-NGROK.ngrok.io/panel-formularios
echo.
echo ═══════════════════════════════════════════════════════════════
echo.
echo Presiona cualquier tecla para salir de esta ventana
echo (Las ventanas de Flask y Ngrok seguirán abiertas)
pause >nul

