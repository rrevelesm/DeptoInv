@echo off
chcp 65001 > nul
cls
echo ═══════════════════════════════════════════════════════════
echo   📥 DESCARGAR FORMULARIOS DEL SERVIDOR
echo ═══════════════════════════════════════════════════════════
echo.
echo Este script descargará los 11 formularios del servidor
echo a tu PC para analizarlos localmente.
echo.
echo ═══════════════════════════════════════════════════════════
echo.
set /p servidor="Ingresa usuario@servidor: "
echo.
echo Descargando formularios desde %servidor%...
echo.

REM Crear carpeta de respaldo si existe
if exist formularios_respaldo rmdir /s /q formularios_respaldo
mkdir formularios_respaldo

REM Copiar formularios locales actuales al respaldo
if exist formularios xcopy /s /y formularios formularios_respaldo\

REM Descargar formularios del servidor
scp -r %servidor%:~/DeptoInv/formularios/* formularios\

echo.
echo ═══════════════════════════════════════════════════════════
echo   ✅ DESCARGA COMPLETADA
echo ═══════════════════════════════════════════════════════════
echo.
echo Ahora puedes ver los formularios ejecutando:
echo    python resumen_formularios.py
echo.
echo O usar el panel local:
echo    INICIAR_PANEL_ADMIN.bat
echo.
pause

