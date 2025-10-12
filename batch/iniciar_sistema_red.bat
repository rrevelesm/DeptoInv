@echo off
chcp 65001 >nul
title Sistema UPIIZ - Modo Red Local
color 0A

echo ═══════════════════════════════════════════════════════════════
echo  🎓 SISTEMA DE GESTIÓN DE INVESTIGACIÓN - UPIIZ
echo  Instituto Politécnico Nacional
echo  M. en C. Rafael Reveles Martínez
echo ═══════════════════════════════════════════════════════════════
echo.

echo 🌐 Iniciando servidor en MODO RED LOCAL...
echo.
echo ⚠️  IMPORTANTE:
echo    - Tu computadora debe permanecer ENCENDIDA
echo    - Todos deben estar en la MISMA red WiFi/LAN
echo    - Windows puede pedir permiso de firewall (PERMITIR)
echo.

REM Mostrar IP local
echo 📍 Obteniendo tu dirección IP local...
for /f "tokens=2 delims=:" %%a in ('ipconfig ^| findstr /c:"IPv4"') do (
    set IP=%%a
    goto :found_ip
)
:found_ip
set IP=%IP: =%
echo.
echo ═══════════════════════════════════════════════════════════════
echo  ✅ Tu dirección IP: %IP%
echo ═══════════════════════════════════════════════════════════════
echo.
echo 📋 COMPARTIR FORMULARIO CON INVESTIGADORES:
echo.
echo    http://%IP%:5000/formulario
echo.
echo ═══════════════════════════════════════════════════════════════
echo  📊 PANEL DE ADMINISTRACIÓN (para ti):
echo.
echo    http://%IP%:5000/panel-formularios
echo.
echo ═══════════════════════════════════════════════════════════════
echo.
echo 🚀 Iniciando servidor Flask...
echo    Presiona Ctrl+C para detener el servidor
echo.

REM Agregar regla de firewall si no existe
netsh advfirewall firewall show rule name="Flask UPIIZ Puerto 5000" >nul 2>&1
if %errorlevel% neq 0 (
    echo 🔓 Configurando Firewall de Windows...
    netsh advfirewall firewall add rule name="Flask UPIIZ Puerto 5000" dir=in action=allow protocol=TCP localport=5000 profile=private,domain >nul 2>&1
    echo    ✅ Firewall configurado
    echo.
)

REM Iniciar servidor
python app.py

pause

