# 🌐 DESPLEGAR PANEL ADMIN EN PYTHONANYWHERE

## 🎯 OBJETIVO

Tener el panel de administración disponible en internet:
```
https://tu-usuario.pythonanywhere.com/admin-login
```

Para poder ver los 11 formularios desde cualquier lugar.

---

## ✅ VENTAJAS DE PYTHONANYWHERE

- ✅ **GRATIS** (plan gratuito disponible)
- ✅ **HTTPS automático** (seguro)
- ✅ **Acceso desde cualquier lugar**
- ✅ **No necesitas servidor propio**
- ✅ **URL pública profesional**
- ✅ **Fácil de configurar** (15 minutos)

---

## 🚀 PASO 1: CREAR CUENTA EN PYTHONANYWHERE

### 1.1 Ir a PythonAnywhere

Abre tu navegador y ve a:
```
https://www.pythonanywhere.com/registration/register/beginner/
```

### 1.2 Crear cuenta GRATIS

- **Username**: Elige tu nombre de usuario (ej: `upiizinvestigacion`)
- **Email**: Tu correo institucional
- **Password**: Crea una contraseña segura

✅ Confirma tu email

---

## 📂 PASO 2: SUBIR TU PROYECTO

### 2.1 Abrir Consola Bash

Una vez dentro de PythonAnywhere:

1. Clic en **"Consoles"** en el menú superior
2. Clic en **"Bash"** para abrir una terminal

### 2.2 Clonar tu repositorio

En la consola Bash de PythonAnywhere, ejecuta:

```bash
# Opción A: Si está en GitHub
git clone https://github.com/rrevelesm/DeptoInv.git
cd DeptoInv

# Opción B: Si NO está en GitHub, subir archivos manualmente
# (Ver sección 2.3)
```

### 2.3 Subir archivos manualmente (si no usas GitHub)

Si prefieres subir archivos directamente:

1. Clic en **"Files"** en el menú
2. Navega a `/home/tu-usuario/`
3. Crea carpeta `DeptoInv`
4. Sube estos archivos:
   - `app.py`
   - `models.py`
   - `security_utils.py`
   - `config.py`
   - `requirements.txt`
   - Carpeta `static/` completa
   - Carpeta `formularios/` con los JSON

---

## 🔧 PASO 3: INSTALAR DEPENDENCIAS

En la consola Bash de PythonAnywhere:

```bash
cd ~/DeptoInv

# Instalar dependencias
pip3.10 install --user flask flask-cors sqlalchemy pandas openpyxl flask-limiter
```

---

## 🌐 PASO 4: CONFIGURAR WEB APP

### 4.1 Crear Web App

1. Clic en **"Web"** en el menú superior
2. Clic en **"Add a new web app"**
3. Selecciona **"Manual configuration"**
4. Selecciona **"Python 3.10"**
5. Clic en **"Next"**

### 4.2 Configurar WSGI

1. En la página de configuración de Web, busca **"Code:"**
2. Clic en el link del archivo WSGI (algo como `/var/www/tu-usuario_pythonanywhere_com_wsgi.py`)
3. **BORRA TODO** el contenido del archivo
4. **PEGA ESTE CÓDIGO**:

```python
import sys
import os

# Agregar tu proyecto al path
project_home = '/home/tu-usuario/DeptoInv'
if project_home not in sys.path:
    sys.path.insert(0, project_home)

# Configurar variable de entorno
os.environ['FLASK_APP'] = 'app.py'

# Importar la aplicación Flask
from app import app as application
```

⚠️ **IMPORTANTE**: Reemplaza `tu-usuario` con tu nombre de usuario de PythonAnywhere

5. Clic en **"Save"** (arriba a la derecha)

### 4.3 Configurar Static Files

En la misma página de configuración Web, en la sección **"Static files"**:

1. Clic en **"Enter URL"** → Escribe: `/static/`
2. Clic en **"Enter path"** → Escribe: `/home/tu-usuario/DeptoInv/static/`
3. Clic en el ✅ verde para guardar

### 4.4 Configurar Variables de Entorno (Opcional)

Si quieres, en la sección **"Environment variables"**:

```
DEBUG=False
SECRET_KEY=(tu secret key)
```

---

## 📋 PASO 5: COPIAR FORMULARIOS DEL SERVIDOR

Necesitas copiar los 11 formularios del servidor remoto a PythonAnywhere.

### Opción A: Desde tu PC

```bash
# 1. Descargar formularios del servidor a tu PC
scp -r usuario@servidor:~/DeptoInv/formularios D:\temp\

# 2. Subir a PythonAnywhere (desde el navegador)
# Files → DeptoInv → Upload → Seleccionar carpeta formularios
```

### Opción B: Directamente desde servidor a PythonAnywhere

En la consola Bash de PythonAnywhere:

```bash
cd ~/DeptoInv

# Crear carpeta
mkdir -p formularios/constancias_snii

# Copiar desde tu servidor remoto
scp -r usuario@tu-servidor:~/DeptoInv/formularios/*.json formularios/
```

---

## 🚀 PASO 6: INICIAR EL SITIO

1. Ve a la pestaña **"Web"**
2. Clic en el botón verde **"Reload"**
3. Espera 10-15 segundos

✅ **¡Tu sitio ya está en línea!**

---

## 🌐 PASO 7: ACCEDER AL PANEL

### Tu URL será:

```
https://tu-usuario.pythonanywhere.com/admin-login
```

Ejemplo:
```
https://upiizinvestigacion.pythonanywhere.com/admin-login
```

### Ingresar token:

```
bRIWynRiD-kz0KsyHtrgvuyEbQtBgNXBaGqWlOX1cIU
```

### ¡Listo! Verás el panel con los 11 formularios

---

## 📥 DESCARGAR EXCEL

Una vez dentro del panel:

1. Clic en botón **"📥 Descargar Excel"**
2. El archivo se descargará automáticamente
3. Contiene todos los datos de los 11 formularios

---

## 🔧 SOLUCIÓN DE PROBLEMAS

### Error: "Something went wrong"

Revisa los logs de error:

1. En PythonAnywhere, ve a **"Web"**
2. Busca **"Log files"**
3. Abre **"Error log"**
4. Busca el error específico

### Error: "ModuleNotFoundError"

Instala la dependencia faltante:

```bash
pip3.10 install --user nombre-del-modulo
```

Luego **Reload** la web app.

### No aparecen los formularios

Verifica que los archivos JSON estén en:
```bash
cd ~/DeptoInv/formularios
ls -la
```

### Token no funciona

Verifica que `config.py` esté en el servidor:
```bash
cd ~/DeptoInv
cat config.py
```

---

## 📊 URLS DISPONIBLES

Una vez desplegado, tendrás:

| URL | Descripción |
|-----|-------------|
| `https://tu-usuario.pythonanywhere.com/` | Página principal |
| `https://tu-usuario.pythonanywhere.com/admin-login` | **Login admin** ⭐ |
| `https://tu-usuario.pythonanywhere.com/panel-admin` | Panel de administración |
| `https://tu-usuario.pythonanywhere.com/formulario` | Formulario público |

---

## 🔄 ACTUALIZAR EL SITIO

Cuando hagas cambios:

### Si usas GitHub:

```bash
cd ~/DeptoInv
git pull origin main
```

### Si subes archivos manualmente:

1. Ve a **"Files"**
2. Sube los archivos modificados

### Siempre después de cambios:

1. Ve a **"Web"**
2. Clic en **"Reload"**

---

## 🔒 SEGURIDAD EN PYTHONANYWHERE

✅ **Ya incluido:**
- HTTPS automático (SSL gratis)
- Autenticación con token
- Rate limiting activo
- Validaciones de datos

⚠️ **Recomendaciones:**
- NO compartas tu URL públicamente sin protección
- Cambia el token regularmente
- Mantén los logs monitoreados

---

## 💰 PLAN GRATUITO - LIMITACIONES

| Característica | Plan Gratuito |
|----------------|---------------|
| CPU | 100 segundos/día |
| Espacio | 512 MB |
| Tráfico | Ilimitado* |
| HTTPS | ✅ Incluido |
| Dominio | usuario.pythonanywhere.com |

*Para un sistema como este, es más que suficiente.

---

## 🎯 RESUMEN VISUAL

```
1. Crear cuenta en PythonAnywhere
   ↓
2. Subir archivos del proyecto
   ↓
3. Instalar dependencias (pip install)
   ↓
4. Configurar Web App + WSGI
   ↓
5. Copiar los 11 formularios
   ↓
6. Reload del sitio
   ↓
7. Acceder a: https://tu-usuario.pythonanywhere.com/admin-login
   ↓
8. Ingresar token
   ↓
9. ✅ Ver 11 formularios + Descargar Excel
```

---

## 📞 CONTACTO PYTHONANYWHERE

Si tienes problemas:
- **Help**: https://help.pythonanywhere.com/
- **Forum**: https://www.pythonanywhere.com/forums/

---

## 🎉 RESULTADO FINAL

Tendrás:

✅ Panel admin accesible desde internet  
✅ HTTPS seguro automático  
✅ Ver los 11 formularios desde cualquier lugar  
✅ Descargar Excel con un clic  
✅ Sin necesidad de configurar servidores  
✅ Sin costo (plan gratuito)  

**URL final:**  
`https://tu-usuario.pythonanywhere.com/admin-login`

---

**Tiempo estimado de configuración:** 15-20 minutos  
**Nivel de dificultad:** ⭐⭐☆☆☆ (Fácil)  
**Costo:** GRATIS


