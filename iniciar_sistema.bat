@echo off
echo ========================================
echo   Sistema de Gestion de Investigacion
echo ========================================
echo.

REM Verificar si Python esta instalado
python --version >nul 2>&1
if errorlevel 1 (
    echo [ERROR] Python no esta instalado o no esta en el PATH
    echo Por favor instala Python desde https://python.org
    pause
    exit /b 1
)

echo [1/3] Verificando dependencias...
pip show flask >nul 2>&1
if errorlevel 1 (
    echo Instalando dependencias...
    pip install -r requirements.txt
    if errorlevel 1 (
        echo [ERROR] No se pudieron instalar las dependencias
        pause
        exit /b 1
    )
) else (
    echo Dependencias ya instaladas
)

echo.
echo [2/3] Verificando base de datos...
if not exist depto_investigacion.db (
    echo Base de datos no encontrada. Creando con datos de ejemplo...
    python init_data.py
    if errorlevel 1 (
        echo [ERROR] No se pudo inicializar la base de datos
        pause
        exit /b 1
    )
) else (
    echo Base de datos encontrada
)

echo.
echo [3/3] Iniciando servidor...
echo.
echo ============================================
echo   Sistema iniciado correctamente!
echo   Abre tu navegador en: http://localhost:5000
echo ============================================
echo.
echo Presiona Ctrl+C para detener el servidor
echo.

python app.py


