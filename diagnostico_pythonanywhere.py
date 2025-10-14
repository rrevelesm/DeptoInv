#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script de diagnóstico para PythonAnywhere
Ejecutar en la consola Bash de PythonAnywhere
"""

import os
import sys
from pathlib import Path

def print_header(text):
    print("\n" + "="*70)
    print(f"  {text}".center(70))
    print("="*70 + "\n")

def check_file(filepath, description):
    """Verifica si un archivo existe"""
    exists = os.path.exists(filepath)
    status = "[OK]" if exists else "[ERROR]"
    print(f"{status} {description}")
    if exists:
        size = os.path.getsize(filepath)
        print(f"      Tamaño: {size} bytes")
    else:
        print(f"      Archivo no encontrado: {filepath}")
    return exists

def check_directory():
    """Verifica estructura de directorios"""
    print_header("VERIFICACION DE ARCHIVOS")
    
    archivos_criticos = {
        'app.py': 'Servidor Flask principal',
        'models.py': 'Modelos de base de datos',
        'security_utils.py': 'Utilidades de seguridad',
        'config.py': 'Configuración y token',
        'requirements.txt': 'Dependencias',
        'static/admin_login.html': 'Página de login admin',
        'static/panel_admin.html': 'Panel de administración',
        'static/formulario_investigador.html': 'Formulario público',
        'static/index.html': 'Página principal'
    }
    
    todos_ok = True
    for archivo, desc in archivos_criticos.items():
        if not check_file(archivo, desc):
            todos_ok = False
    
    return todos_ok

def check_git():
    """Verifica estado de Git"""
    print_header("ESTADO DE GIT")
    
    print("Rama actual:")
    os.system("git branch")
    
    print("\nÚltimo commit:")
    os.system("git log -1 --oneline")
    
    print("\nEstado:")
    os.system("git status")

def check_imports():
    """Verifica que Flask pueda importar la app"""
    print_header("VERIFICACION DE IMPORTS")
    
    try:
        sys.path.insert(0, os.getcwd())
        from app import app
        print("[OK] Flask app importada correctamente")
        
        # Ver todas las rutas
        print("\nRutas disponibles:")
        for rule in app.url_map.iter_rules():
            print(f"  - {rule.rule} [{', '.join(rule.methods)}]")
        
        return True
    except Exception as e:
        print(f"[ERROR] No se pudo importar Flask app")
        print(f"Error: {e}")
        return False

def check_dependencies():
    """Verifica dependencias instaladas"""
    print_header("DEPENDENCIAS INSTALADAS")
    
    modulos = ['flask', 'flask_cors', 'sqlalchemy', 'pandas', 'openpyxl']
    
    for modulo in modulos:
        try:
            __import__(modulo)
            print(f"[OK] {modulo}")
        except ImportError:
            print(f"[ERROR] {modulo} - NO INSTALADO")
            print(f"        Instala con: pip3.10 install --user {modulo}")

def main():
    print("\n" + "="*70)
    print("  DIAGNOSTICO COMPLETO - PYTHONANYWHERE".center(70))
    print("="*70)
    
    print("\nDirectorio actual:", os.getcwd())
    print("Usuario:", os.environ.get('USER', 'unknown'))
    print()
    
    # Verificar ubicación
    if not os.path.exists('app.py'):
        print("\n[ERROR] No estás en el directorio correcto")
        print("Ejecuta: cd ~/DeptoInv")
        return
    
    # Ejecutar verificaciones
    check_directory()
    check_git()
    check_dependencies()
    check_imports()
    
    # Resumen final
    print_header("RESUMEN")
    
    print("Si todos los checks están [OK]:")
    print("  1. Ve a Web en PythonAnywhere")
    print("  2. Clic en 'Reload'")
    print("  3. Espera 15 segundos")
    print("  4. Accede a: https://upiizinvestigacion.pythonanywhere.com/admin-login")
    print()
    print("Si hay [ERROR]:")
    print("  - Ejecuta los comandos sugeridos")
    print("  - Vuelve a ejecutar este script")
    print("  - Haz Reload del sitio")
    print()

if __name__ == '__main__':
    main()

