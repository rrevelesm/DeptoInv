@echo off
chcp 65001 >nul
title Subir Proyecto a GitHub - UPIIZ
color 0B

echo ═══════════════════════════════════════════════════════════════
echo  📤 SUBIR PROYECTO A GITHUB
echo  DeptoInv_UPIIZ
echo ═══════════════════════════════════════════════════════════════
echo.

REM Verificar si Git está instalado
git --version >nul 2>&1
if %errorlevel% neq 0 (
    echo ❌ ERROR: Git no está instalado
    echo.
    echo 📥 Por favor instala Git:
    echo    1. Ve a: https://git-scm.com/download/win
    echo    2. Descarga e instala Git
    echo    3. Reinicia esta ventana
    echo    4. Vuelve a ejecutar este script
    echo.
    pause
    exit /b 1
)

echo ✅ Git detectado
echo.

REM Verificar si ya hay un repositorio Git
if exist ".git" (
    echo 📁 Repositorio Git ya existe
    echo.
) else (
    echo 🔧 Inicializando repositorio Git...
    git init
    echo ✅ Repositorio inicializado
    echo.
)

echo 📊 Estado actual del repositorio:
echo ════════════════════════════════════════════════════════════════
git status
echo ════════════════════════════════════════════════════════════════
echo.

echo 📦 Agregando archivos...
git add .
echo ✅ Archivos agregados
echo.

echo 💬 Creando commit...
git commit -m "🎓 Sistema de Gestión de Investigación UPIIZ - Actualización completa"
if %errorlevel% equ 0 (
    echo ✅ Commit creado
) else (
    echo ⚠️  No hay cambios para commitear o ya está commiteado
)
echo.

echo 🔗 Configurando repositorio remoto...
git remote remove origin >nul 2>&1
git remote add origin https://github.com/rrevelesm/DeptoInv_UPIIZ.git
echo ✅ Remote configurado: https://github.com/rrevelesm/DeptoInv_UPIIZ.git
echo.

echo 🌿 Configurando rama principal...
git branch -M main
echo ✅ Rama 'main' configurada
echo.

echo ═══════════════════════════════════════════════════════════════
echo  🚀 SUBIENDO A GITHUB...
echo ═══════════════════════════════════════════════════════════════
echo.
echo ⚠️  IMPORTANTE: GitHub te pedirá autenticación
echo.
echo    Usuario: rrevelesm
echo    Contraseña: Tu Personal Access Token (NO tu contraseña normal)
echo.
echo    Si no tienes token, créalo en:
echo    https://github.com/settings/tokens
echo.

git push -u origin main

if %errorlevel% equ 0 (
    echo.
    echo ═══════════════════════════════════════════════════════════════
    echo  ✅ ¡PROYECTO SUBIDO EXITOSAMENTE!
    echo ═══════════════════════════════════════════════════════════════
    echo.
    echo  🌐 Ver tu proyecto en:
    echo     https://github.com/rrevelesm/DeptoInv_UPIIZ
    echo.
    echo  📚 README.md se mostrará automáticamente en GitHub
    echo.
) else (
    echo.
    echo ═══════════════════════════════════════════════════════════════
    echo  ❌ ERROR AL SUBIR
    echo ═══════════════════════════════════════════════════════════════
    echo.
    echo  Posibles soluciones:
    echo.
    echo  1. Crear Personal Access Token:
    echo     https://github.com/settings/tokens
    echo     - Selecciona: Generate new token (classic)
    echo     - Marca: repo (acceso completo)
    echo     - Usa ese token como contraseña
    echo.
    echo  2. Verificar credenciales de GitHub
    echo.
    echo  3. Ver guía completa: SUBIR_A_GITHUB.md
    echo.
)

pause


