@echo off
chcp 65001 > nul
cls
echo ═══════════════════════════════════════════════════════════
echo   🌐 ABRIR PANEL WEB REMOTO - UPIIZ
echo ═══════════════════════════════════════════════════════════
echo.
echo Este script te ayudará a abrir el panel web del servidor
echo remoto donde están los 11 formularios.
echo.
echo ═══════════════════════════════════════════════════════════
echo.
set /p servidor="Ingresa usuario@servidor (ej: usuario@192.168.1.100): "
echo.
echo ═══════════════════════════════════════════════════════════
echo   📋 INSTRUCCIONES
echo ═══════════════════════════════════════════════════════════
echo.
echo Se abrirán 2 ventanas:
echo.
echo   1. TÚNEL SSH (NO CERRAR esta ventana)
echo      - Crea conexión segura al servidor
echo.
echo   2. SERVIDOR REMOTO
echo      - Ejecuta: cd ~/DeptoInv ^&^& python app.py
echo      - Espera que diga "Running on http://127.0.0.1:5000"
echo.
echo Luego tu navegador se abrirá automáticamente en:
echo   http://localhost:5000/admin-login
echo.
echo Token: bRIWynRiD-kz0KsyHtrgvuyEbQtBgNXBaGqWlOX1cIU
echo.
echo ═══════════════════════════════════════════════════════════
echo.
pause
echo.
echo 🔌 Creando túnel SSH...
echo.

REM Abrir túnel SSH en nueva ventana
start "🔌 TÚNEL SSH - NO CERRAR" cmd /k "echo ══════════════════════════════════════════════ & echo   🔌 TÚNEL SSH ACTIVO - NO CERRAR ESTA VENTANA & echo ══════════════════════════════════════════════ & echo. & echo Conectando a %servidor%... & echo. & ssh -L 5000:localhost:5000 %servidor%"

REM Esperar 3 segundos
timeout /t 3 /nobreak >nul

REM Abrir conexión SSH para iniciar servidor
start "🚀 Servidor Remoto" cmd /k "echo ══════════════════════════════════════════════ & echo   🚀 SERVIDOR FLASK REMOTO & echo ══════════════════════════════════════════════ & echo. & echo Conectando a %servidor%... & echo. & echo EJECUTA ESTE COMANDO: & echo    cd ~/DeptoInv ^&^& python app.py & echo. & echo ══════════════════════════════════════════════ & echo. & ssh %servidor%"

REM Esperar 5 segundos
timeout /t 5 /nobreak >nul

echo.
echo 🌐 Abriendo navegador...
start http://localhost:5000/admin-login

echo.
echo ═══════════════════════════════════════════════════════════
echo   ✅ TODO LISTO
echo ═══════════════════════════════════════════════════════════
echo.
echo 1. Túnel SSH: ACTIVO (ventana aparte)
echo 2. Servidor: Inicializando (ventana aparte)
echo 3. Navegador: ABIERTO
echo.
echo 🔑 Token para login:
echo    bRIWynRiD-kz0KsyHtrgvuyEbQtBgNXBaGqWlOX1cIU
echo.
echo ⚠️  IMPORTANTE:
echo    - NO cierres la ventana "TÚNEL SSH"
echo    - Espera a que el servidor diga "Running on..."
echo    - Luego ingresa el token en el navegador
echo.
echo ═══════════════════════════════════════════════════════════
echo.
pause

