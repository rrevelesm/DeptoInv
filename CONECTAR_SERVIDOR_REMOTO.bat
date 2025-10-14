@echo off
chcp 65001 > nul
cls
echo ═══════════════════════════════════════════════════════════
echo   🌐 CONECTAR AL SERVIDOR REMOTO - UPIIZ
echo ═══════════════════════════════════════════════════════════
echo.
echo 📊 Servidor Remoto:
echo    - Ubicación: ~/DeptoInv
echo    - Formularios: 11 investigadores
echo    - Estado: Operativo
echo.
echo ═══════════════════════════════════════════════════════════
echo.
echo Selecciona una opción:
echo.
echo   [1] 🔌 Conectar al servidor por SSH
echo   [2] 📊 Ver resumen de formularios remotos
echo   [3] 🚀 Iniciar servidor remoto y crear túnel
echo   [4] 📥 Descargar formularios del servidor a este PC
echo   [5] 💡 Ver instrucciones completas
echo   [0] ❌ Salir
echo.
echo ═══════════════════════════════════════════════════════════
echo.
set /p opcion="Ingresa tu opción: "

if "%opcion%"=="1" (
    echo.
    echo 🔌 Conectando al servidor...
    echo.
    echo 💡 Ingresa los datos de tu servidor cuando lo solicite
    echo.
    set /p servidor="Ingresa usuario@servidor (ej: usuario@192.168.1.100): "
    echo.
    echo Conectando a %servidor%...
    ssh %servidor%
    goto end
)

if "%opcion%"=="2" (
    echo.
    echo 📊 Ver resumen de formularios remotos...
    echo.
    set /p servidor="Ingresa usuario@servidor: "
    echo.
    echo Ejecutando resumen en el servidor...
    ssh %servidor% "cd ~/DeptoInv && python resumen_formularios.py"
    pause
    goto end
)

if "%opcion%"=="3" (
    echo.
    echo 🚀 Iniciando servidor remoto con túnel SSH...
    echo.
    set /p servidor="Ingresa usuario@servidor: "
    echo.
    echo ═══════════════════════════════════════════════════════════
    echo   INSTRUCCIONES:
    echo ═══════════════════════════════════════════════════════════
    echo.
    echo 1. Se abrirá una ventana SSH
    echo 2. En el servidor ejecuta: cd ~/DeptoInv ^&^& python app.py
    echo 3. Desde tu navegador ve a: http://localhost:5000/admin-login
    echo 4. Token: bRIWynRiD-kz0KsyHtrgvuyEbQtBgNXBaGqWlOX1cIU
    echo.
    echo ═══════════════════════════════════════════════════════════
    echo.
    pause
    echo.
    echo Creando túnel SSH...
    ssh -L 5000:localhost:5000 %servidor%
    goto end
)

if "%opcion%"=="4" (
    echo.
    echo 📥 Descargar formularios del servidor...
    echo.
    set /p servidor="Ingresa usuario@servidor: "
    echo.
    echo Descargando formularios...
    scp -r %servidor%:~/DeptoInv/formularios/* "%~dp0formularios\"
    echo.
    echo ✅ Formularios descargados!
    echo.
    echo Ahora puedes verlos localmente ejecutando:
    echo    python resumen_formularios.py
    echo.
    pause
    goto end
)

if "%opcion%"=="5" (
    echo.
    echo 💡 Abriendo instrucciones completas...
    start "" "%~dp0ACCEDER_SERVIDOR_REMOTO.md"
    goto end
)

if "%opcion%"=="0" (
    echo.
    echo 👋 ¡Hasta luego!
    timeout /t 1 /nobreak >nul
    exit
)

echo.
echo ❌ Opción no válida
pause

:end

