#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Script para preparar archivos para despliegue en PythonAnywhere
Crea un archivo ZIP con todo lo necesario
"""

import os
import zipfile
import shutil
from pathlib import Path
from datetime import datetime

def crear_zip_pythonanywhere():
    """Crea un ZIP con todos los archivos necesarios para PythonAnywhere"""
    
    print("="*60)
    print("  PREPARAR PROYECTO PARA PYTHONANYWHERE".center(60))
    print("="*60)
    print()
    
    # Nombre del archivo ZIP
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    nombre_zip = f'DeptoInv_PythonAnywhere_{timestamp}.zip'
    
    # Archivos y carpetas a incluir
    archivos_incluir = [
        'app.py',
        'models.py',
        'security_utils.py',
        'config.py',
        'requirements.txt',
        'README.md'
    ]
    
    carpetas_incluir = [
        'static',
        'formularios',
        'scripts'
    ]
    
    print("📦 Creando archivo ZIP...")
    print(f"   Nombre: {nombre_zip}")
    print()
    
    try:
        with zipfile.ZipFile(nombre_zip, 'w', zipfile.ZIP_DEFLATED) as zipf:
            # Agregar archivos
            print("📄 Agregando archivos:")
            for archivo in archivos_incluir:
                if os.path.exists(archivo):
                    zipf.write(archivo, f'DeptoInv/{archivo}')
                    print(f"   ✅ {archivo}")
                else:
                    print(f"   ⚠️  {archivo} (no encontrado)")
            
            print()
            print("📁 Agregando carpetas:")
            
            # Agregar carpetas
            for carpeta in carpetas_incluir:
                if os.path.exists(carpeta):
                    count = 0
                    for root, dirs, files in os.walk(carpeta):
                        for file in files:
                            file_path = os.path.join(root, file)
                            arcname = os.path.join('DeptoInv', file_path)
                            zipf.write(file_path, arcname)
                            count += 1
                    print(f"   ✅ {carpeta}/ ({count} archivos)")
                else:
                    print(f"   ⚠️  {carpeta}/ (no encontrada)")
        
        print()
        print("="*60)
        print("✅ ARCHIVO ZIP CREADO EXITOSAMENTE")
        print("="*60)
        print()
        print(f"📦 Archivo: {nombre_zip}")
        print(f"📂 Ubicación: {os.path.abspath(nombre_zip)}")
        
        # Obtener tamaño del archivo
        size_mb = os.path.getsize(nombre_zip) / (1024 * 1024)
        print(f"💾 Tamaño: {size_mb:.2f} MB")
        
        print()
        print("="*60)
        print("  PRÓXIMOS PASOS")
        print("="*60)
        print()
        print("1. Ve a: https://www.pythonanywhere.com/")
        print("2. Crea una cuenta (o inicia sesión)")
        print("3. Ve a 'Files' en el menú")
        print("4. Sube este archivo ZIP:")
        print(f"   {nombre_zip}")
        print("5. Extrae el ZIP en PythonAnywhere")
        print("6. Sigue la guía: DESPLEGAR_PYTHONANYWHERE.md")
        print()
        print("="*60)
        
        return True
        
    except Exception as e:
        print(f"\n❌ Error al crear ZIP: {e}")
        return False

def verificar_archivos():
    """Verifica que existan los archivos necesarios"""
    
    print("🔍 Verificando archivos necesarios...")
    print()
    
    archivos_criticos = {
        'app.py': 'Servidor Flask principal',
        'models.py': 'Modelos de base de datos',
        'config.py': 'Configuración y credenciales',
        'requirements.txt': 'Dependencias Python',
        'static/panel_admin.html': 'Panel de administración',
        'static/admin_login.html': 'Página de login',
        'formularios/': 'Carpeta de formularios'
    }
    
    todos_ok = True
    
    for archivo, descripcion in archivos_criticos.items():
        existe = os.path.exists(archivo)
        simbolo = "✅" if existe else "❌"
        print(f"{simbolo} {archivo:<30} - {descripcion}")
        if not existe:
            todos_ok = False
    
    print()
    
    if not todos_ok:
        print("⚠️  ADVERTENCIA: Faltan archivos importantes")
        print("   El sistema podría no funcionar correctamente en PythonAnywhere")
        print()
        respuesta = input("¿Deseas continuar de todos modos? (s/n): ")
        return respuesta.lower() == 's'
    else:
        print("✅ Todos los archivos necesarios están presentes")
        print()
    
    return True

def contar_formularios():
    """Cuenta los formularios disponibles"""
    formularios_dir = Path('formularios')
    
    if not formularios_dir.exists():
        return 0
    
    archivos_json = list(formularios_dir.glob('*.json'))
    return len(archivos_json)

def mostrar_resumen():
    """Muestra un resumen del proyecto"""
    
    print()
    print("="*60)
    print("  RESUMEN DEL PROYECTO")
    print("="*60)
    print()
    
    # Contar formularios
    num_formularios = contar_formularios()
    print(f"📋 Formularios incluidos: {num_formularios}")
    
    # Verificar config
    if os.path.exists('config.py'):
        with open('config.py', 'r', encoding='utf-8') as f:
            contenido = f.read()
            if 'ADMIN_TOKEN' in contenido:
                print("🔑 Token de admin: ✅ Configurado")
            if 'SECRET_KEY' in contenido:
                print("🔐 Secret key: ✅ Configurado")
    
    # Verificar static
    static_files = ['panel_admin.html', 'admin_login.html', 'formulario_investigador.html']
    static_ok = all(os.path.exists(f'static/{f}') for f in static_files)
    print(f"🌐 Archivos estáticos: {'✅ Completos' if static_ok else '⚠️ Incompletos'}")
    
    print()

if __name__ == '__main__':
    import sys
    
    # Configurar encoding para Windows
    if sys.platform == 'win32':
        import io
        sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
    
    try:
        # Mostrar resumen
        mostrar_resumen()
        
        # Verificar archivos
        if not verificar_archivos():
            print("\n❌ Proceso cancelado")
            input("\nPresiona Enter para salir...")
            sys.exit(1)
        
        # Crear ZIP
        input("\n📦 Presiona Enter para crear el archivo ZIP...")
        print()
        
        if crear_zip_pythonanywhere():
            print("\n✅ ¡Todo listo para PythonAnywhere!")
        else:
            print("\n❌ Hubo un error al crear el ZIP")
        
        input("\nPresiona Enter para salir...")
        
    except KeyboardInterrupt:
        print("\n\n❌ Proceso cancelado por el usuario")
        input("\nPresiona Enter para salir...")
    except Exception as e:
        print(f"\n❌ Error inesperado: {e}")
        input("\nPresiona Enter para salir...")

