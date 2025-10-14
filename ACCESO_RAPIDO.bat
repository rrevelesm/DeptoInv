@echo off
chcp 65001 > nul
cls
echo ═══════════════════════════════════════════════════════════
echo   🚀 ACCESOS RÁPIDOS - SISTEMA UPIIZ
echo ═══════════════════════════════════════════════════════════
echo.
echo Selecciona una opción:
echo.
echo   [1] 🖥️  Iniciar Servidor LOCAL y Panel Admin
echo   [2] 🌐  Abrir Panel WEB REMOTO (11 formularios)
echo   [3] 🚀  PREPARAR PARA PYTHONANYWHERE (Panel en Internet) ⭐
echo   [4] 📊  Ver Resumen de Formularios (sin servidor)
echo   [5] 📖  Abrir Guía de Acceso (HTML)
echo   [6] 🔑  Ver Credenciales
echo   [7] 📂  Abrir Carpeta de Formularios
echo   [8] 🌐  Abrir Panel en Navegador (servidor debe estar corriendo)
echo   [0] ❌  Salir
echo.
echo ═══════════════════════════════════════════════════════════
echo.
set /p opcion="Ingresa tu opción: "

if "%opcion%"=="1" (
    echo.
    echo 🚀 Iniciando servidor...
    start "" "%~dp0INICIAR_PANEL_ADMIN.bat"
    goto end
)

if "%opcion%"=="2" (
    echo.
    echo 🌐 Abriendo Panel Web Remoto...
    start "" "%~dp0ABRIR_PANEL_REMOTO.bat"
    goto end
)

if "%opcion%"=="3" (
    echo.
    echo 🚀 Preparando para PythonAnywhere...
    start "" "%~dp0PREPARAR_PYTHONANYWHERE.bat"
    start "" notepad "%~dp0GUIA_SIMPLE_PYTHONANYWHERE.txt"
    goto end
)

if "%opcion%"=="4" (
    echo.
    echo 📊 Mostrando resumen de formularios...
    python "%~dp0resumen_formularios.py"
    pause
    goto end
)

if "%opcion%"=="5" (
    echo.
    echo 📖 Abriendo guía de acceso...
    start "" "%~dp0GUIA_ACCESO_RAPIDO.html"
    goto end
)

if "%opcion%"=="6" (
    echo.
    echo 🔑 TOKEN DE ADMINISTRADOR:
    echo.
    echo    bRIWynRiD-kz0KsyHtrgvuyEbQtBgNXBaGqWlOX1cIU
    echo.
    echo ═══════════════════════════════════════════════════════════
    echo.
    pause
    goto end
)

if "%opcion%"=="7" (
    echo.
    echo 📂 Abriendo carpeta de formularios...
    start "" explorer "%~dp0formularios"
    goto end
)

if "%opcion%"=="8" (
    echo.
    echo 🌐 Abriendo panel en navegador...
    start http://localhost:5000/admin-login
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

