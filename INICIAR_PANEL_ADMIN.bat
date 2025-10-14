@echo off
chcp 65001 > nul
cls
echo ═══════════════════════════════════════════════════════════
echo   🎓 PANEL DE ADMINISTRACIÓN - INVESTIGADORES UPIIZ
echo ═══════════════════════════════════════════════════════════
echo.
echo 📋 Iniciando servidor Flask...
echo.

cd /d "%~dp0"

:: Verificar si Python está instalado
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo ❌ ERROR: Python no está instalado o no está en el PATH
    echo.
    echo 💡 Instala Python desde: https://www.python.org/downloads/
    pause
    exit /b 1
)

:: Verificar si app.py existe
if not exist "app.py" (
    echo ❌ ERROR: No se encuentra el archivo app.py
    echo.
    echo 📂 Directorio actual: %CD%
    pause
    exit /b 1
)

echo ✅ Python encontrado
echo ✅ Archivo app.py encontrado
echo.
echo ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
echo.
echo 🚀 SERVIDOR INICIADO
echo.
echo 📱 URLs Disponibles:
echo    ├─ 🔐 Login Admin:     http://localhost:5000/admin-login
echo    ├─ 📊 Panel Admin:     http://localhost:5000/panel-admin
echo    ├─ 📋 Formulario:      http://localhost:5000/formulario
echo    └─ 🏠 Inicio:          http://localhost:5000/
echo.
echo 🔑 TOKEN DE ADMIN:
echo    bRIWynRiD-kz0KsyHtrgvuyEbQtBgNXBaGqWlOX1cIU
echo.
echo ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
echo.
echo 💡 El servidor se abrirá automáticamente en tu navegador...
echo.
echo ⚠️  Presiona Ctrl+C para detener el servidor
echo.

:: Esperar 2 segundos y abrir el navegador
timeout /t 2 /nobreak >nul
start http://localhost:5000/admin-login

:: Iniciar el servidor Flask
python app.py

pause

