@echo off
chcp 65001 > nul
cls
echo ═══════════════════════════════════════════════════════════
echo   📦 EXTRAER FORMULARIOS.TAR.GZ
echo ═══════════════════════════════════════════════════════════
echo.
echo Este script extrae el archivo formularios.tar.gz
echo que descargaste de PythonAnywhere.
echo.
echo ═══════════════════════════════════════════════════════════
echo.

REM Buscar archivo en Descargas
set "archivo_tar=%USERPROFILE%\Downloads\formularios.tar.gz"

if not exist "%archivo_tar%" (
    echo ERROR: No se encontro el archivo formularios.tar.gz
    echo.
    echo Buscado en: %archivo_tar%
    echo.
    echo Por favor:
    echo 1. Verifica que lo hayas descargado
    echo 2. Revisa tu carpeta de Descargas
    echo 3. Mueve el archivo a: %USERPROFILE%\Downloads\
    echo.
    pause
    exit /b 1
)

echo ✅ Archivo encontrado: %archivo_tar%
echo.
echo Extrayendo archivos...
echo.

REM Crear carpeta temporal
mkdir "%TEMP%\formularios_temp" 2>nul

REM Intentar extraer con tar (Windows 10+)
tar -xzf "%archivo_tar%" -C "%TEMP%\formularios_temp"

if %errorlevel% neq 0 (
    echo.
    echo ERROR al extraer. Intentando método alternativo...
    echo.
    echo Por favor instala 7-Zip desde: https://www.7-zip.org/
    pause
    exit /b 1
)

echo.
echo ✅ Archivos extraidos exitosamente
echo.

REM Copiar archivos JSON a la carpeta del proyecto
echo Copiando archivos a: %~dp0formularios\
xcopy /y "%TEMP%\formularios_temp\*.json" "%~dp0formularios\"

echo.
echo ═══════════════════════════════════════════════════════════
echo   ✅ PROCESO COMPLETADO
echo ═══════════════════════════════════════════════════════════
echo.
echo Los formularios han sido copiados a:
echo %~dp0formularios\
echo.
echo Ahora puedes verlos ejecutando:
echo.
echo   python resumen_formularios.py
echo.
echo O usando el panel local:
echo.
echo   INICIAR_PANEL_ADMIN.bat
echo.
echo ═══════════════════════════════════════════════════════════
echo.
pause

REM Limpiar archivos temporales
rmdir /s /q "%TEMP%\formularios_temp" 2>nul

