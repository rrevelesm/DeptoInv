# ===============================================================================
# ARCHIVO WSGI PARA PYTHONANYWHERE
# Sistema de Gestión de Investigadores - UPIIZ
# ===============================================================================
#
# INSTRUCCIONES:
# 1. Ve a la configuración de tu Web App en PythonAnywhere
# 2. Clic en el link del archivo WSGI
# 3. BORRA TODO el contenido existente
# 4. COPIA Y PEGA TODO este archivo
# 5. REEMPLAZA "tu-usuario" con tu nombre de usuario de PythonAnywhere
# 6. Guarda y Reload
#
# ===============================================================================

import sys
import os

# ⚠️ IMPORTANTE: Reemplaza "tu-usuario" con tu nombre de usuario de PythonAnywhere
# Ejemplo: Si tu usuario es "upiizinvestigacion", la ruta sería:
# /home/upiizinvestigacion/DeptoInv

project_home = '/home/tu-usuario/DeptoInv'

# Agregar el directorio del proyecto al path de Python
if project_home not in sys.path:
    sys.path.insert(0, project_home)

# Configurar variables de entorno
os.environ['FLASK_APP'] = 'app.py'
os.environ['DEBUG'] = 'False'  # SIEMPRE False en producción

# Importar la aplicación Flask
from app import app as application

# ===============================================================================
# NO MODIFICAR NADA DEBAJO DE ESTA LÍNEA
# ===============================================================================

# Esta es la aplicación WSGI que PythonAnywhere usará
# La variable 'application' es lo que PythonAnywhere espera encontrar

