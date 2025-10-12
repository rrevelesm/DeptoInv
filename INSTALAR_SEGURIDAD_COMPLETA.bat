@echo off
echo ============================================================
echo INSTALANDO PROTECCIONES DE SEGURIDAD COMPLETAS
echo ============================================================
echo.
echo Instalando Flask-Limiter (proteccion contra spam/DDoS)...
python -m pip install Flask-Limiter --upgrade
echo.
echo Instalando python-dotenv (variables de entorno seguras)...
python -m pip install python-dotenv --upgrade
echo.
echo ============================================================
echo INSTALACION COMPLETADA
echo ============================================================
echo.
echo Ahora REINICIA el servidor:
echo 1. Presiona Ctrl+C en la ventana donde corre Flask
echo 2. Ejecuta: python app.py
echo.
echo El rate limiting estara ACTIVO (5 formularios/hora)
echo ============================================================
pause

