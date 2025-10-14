#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Script para crear ZIP sin confirmaciones"""

import os
import zipfile
from datetime import datetime
from pathlib import Path

print("="*60)
print("  CREANDO ZIP PARA PYTHONANYWHERE".center(60))
print("="*60)
print()

timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
nombre_zip = f'DeptoInv_PythonAnywhere_{timestamp}.zip'

archivos = [
    'app.py',
    'models.py',
    'security_utils.py',
    'config.py',
    'requirements.txt',
    'README.md'
]

carpetas = ['static', 'formularios', 'scripts']

print(f"Creando: {nombre_zip}")
print()

with zipfile.ZipFile(nombre_zip, 'w', zipfile.ZIP_DEFLATED) as zipf:
    for archivo in archivos:
        if os.path.exists(archivo):
            zipf.write(archivo, f'DeptoInv/{archivo}')
            print(f"   [OK] {archivo}")
    
    for carpeta in carpetas:
        if os.path.exists(carpeta):
            count = 0
            for root, dirs, files in os.walk(carpeta):
                for file in files:
                    file_path = os.path.join(root, file)
                    arcname = os.path.join('DeptoInv', file_path)
                    zipf.write(file_path, arcname)
                    count += 1
            print(f"   [OK] {carpeta}/ ({count} archivos)")

size_mb = os.path.getsize(nombre_zip) / (1024 * 1024)

print()
print("="*60)
print("ARCHIVO ZIP CREADO EXITOSAMENTE")
print("="*60)
print(f"Archivo: {nombre_zip}")
print(f"Tamano: {size_mb:.2f} MB")
print(f"Ruta completa: {os.path.abspath(nombre_zip)}")
print("="*60)

