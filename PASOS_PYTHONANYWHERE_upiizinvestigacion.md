# 🚀 Tutorial PythonAnywhere - Usuario: upiizinvestigacion

## Tu URL final: https://upiizinvestigacion.pythonanywhere.com

---

## ✅ PASO 1: Ya Creaste la Cuenta

- Username: **upiizinvestigacion** ✅
- URL: **https://upiizinvestigacion.pythonanywhere.com**

**Confirma tu email** (revisa bandeja de entrada)

---

## 📦 PASO 2: Clonar Repositorio desde GitHub

### 2.1 Abrir Consola Bash

1. **Menú superior:** Clic en **"Consoles"**
2. **Clic en:** "Bash" (ícono de terminal negro)
3. Se abrirá una terminal

### 2.2 Ejecutar Comandos

**Copia y pega estos comandos UNO POR UNO:**

```bash
# Clonar tu repositorio
git clone https://github.com/rrevelesm/DeptoInv.git
```

**Presiona Enter. Verás:**
```
Cloning into 'DeptoInv'...
remote: Enumerating objects...
Unpacking objects: 100% (...), done.
```

```bash
# Entrar al directorio
cd DeptoInv
```

```bash
# Ver archivos
ls -la
```

**Deberías ver:** `app.py`, `models.py`, `README.md`, `static/`, etc.

---

## 📚 PASO 3: Instalar Dependencias

**En la misma consola, ejecuta:**

```bash
pip3.10 install --user flask flask-cors sqlalchemy pandas openpyxl werkzeug
```

**Espera 1-2 minutos.** Verás mensajes como:
```
Successfully installed flask-3.0.0 ...
```

**Verificar instalación:**
```bash
pip3.10 list | grep -i flask
```

Debería mostrar Flask y otras librerías.

---

## 🌐 PASO 4: Crear Web App

### 4.1 Ir a Web

1. **Menú superior:** Clic en **"Web"**
2. **Clic en:** "+ Add a new web app"

### 4.2 Wizard de Configuración

**Pantalla 1:**
- Tu dominio: `upiizinvestigacion.pythonanywhere.com` ✅
- **Clic:** "Next"

**Pantalla 2:**
- Select a Python Web framework: **"Manual configuration"** ⚠️ IMPORTANTE
- **Clic:** "Next"

**Pantalla 3:**
- Select a Python version: **"Python 3.10"** ⚠️ IMPORTANTE
- **Clic:** "Next"

**Pantalla 4:**
- Quickstart new Flask project: **SKIP (Next)**

**¡Listo!** Verás tu configuración de Web App.

---

## ⚙️ PASO 5: Configurar WSGI (MUY IMPORTANTE)

### 5.1 Editar Archivo WSGI

1. **En la página Web, busca sección "Code"**
2. **Clic en el link azul:**
   ```
   /var/www/upiizinvestigacion_pythonanywhere_com_wsgi.py
   ```
3. Se abrirá el editor

### 5.2 BORRAR TODO y Pegar Esto

**BORRA TODO el contenido** y pega este código:

```python
import sys
import os

# Configurar path del proyecto
path = '/home/upiizinvestigacion/DeptoInv'
if path not in sys.path:
    sys.path.insert(0, path)

# Configurar directorio de trabajo
os.chdir(path)

# Importar la aplicación Flask
from app import app as application

# Configuración para producción
application.config['DEBUG'] = False
```

### 5.3 Guardar

**Clic en:** "Save" (botón verde arriba a la izquierda)

---

## 📁 PASO 6: Configurar Archivos Estáticos

### 6.1 En la página Web, busca "Static files"

### 6.2 Agregar Ruta para /static/

**Clic en los campos vacíos:**

- **URL:** `/static/`
- **Directory:** `/home/upiizinvestigacion/DeptoInv/static/`

**Clic en el ✓ verde** para guardar

---

## 🔄 PASO 7: Reload y Probar

### 7.1 Reload

1. **En la parte superior de la página Web:**
2. **Clic en el botón verde grande:**
   ```
   Reload upiizinvestigacion.pythonanywhere.com
   ```
3. **Espera ~10 segundos**

### 7.2 Verificar

**Clic en el link** (arriba del todo):
```
https://upiizinvestigacion.pythonanywhere.com
```

---

## ✅ PASO 8: Probar las URLs

**Abre estas URLs en tu navegador:**

```
1. Sistema Principal:
   https://upiizinvestigacion.pythonanywhere.com/

2. Formulario (para investigadores):
   https://upiizinvestigacion.pythonanywhere.com/formulario

3. Panel de Administración:
   https://upiizinvestigacion.pythonanywhere.com/panel-formularios
```

---

## 🎉 ¡LISTO! SISTEMA EN LÍNEA

**URL para compartir con investigadores:**
```
https://upiizinvestigacion.pythonanywhere.com/formulario
```

---

## 🔍 SI HAY ERRORES

### Ver el Error Log

1. **Pestaña "Web"**
2. **Sección "Log files"**
3. **Clic en:** "Error log" (link rojo)
4. **Copia el error** y dímelo

### Errores Comunes

**Error: "ImportError: No module named flask"**
```bash
cd DeptoInv
pip3.10 install --user flask flask-cors sqlalchemy pandas openpyxl werkzeug
```
Luego Reload.

**Error: "No such file or directory: DeptoInv"**
- Verifica que clonaste el repo: `ls -la` debe mostrar `DeptoInv/`
- El path en WSGI debe ser: `/home/upiizinvestigacion/DeptoInv`

**Error: "Database is locked"**
- Necesitas inicializar la base de datos:
```bash
cd DeptoInv
python3.10 database.py
python3.10 scripts/importar_solo_aprobados.py
```

---

## 📊 INICIALIZAR BASE DE DATOS (Si es necesario)

Si el sistema carga pero no muestra proyectos:

```bash
# En consola Bash de PythonAnywhere
cd DeptoInv

# Inicializar base de datos
python3.10 database.py

# Importar proyectos aprobados
python3.10 scripts/importar_solo_aprobados.py
```

Luego **Reload** la web app.

---

## 📧 MENSAJE PARA INVESTIGADORES

```
Estimado(a) investigador(a):

Favor de llenar el siguiente formulario de actualización de datos:

🔗 https://upiizinvestigacion.pythonanywhere.com/formulario

El formulario incluye información sobre proyectos vigentes, becas EDI, 
nombramiento SNII, ORCID y productividad académica 2025.

Fecha límite: [AGREGAR FECHA]

Gracias por su colaboración.

M. en C. Rafael Reveles Martínez
Jefe del Departamento de Investigación
UPIIZ - Campus Zacatecas
www.zacatecas.ipn.mx
investigacion_UPIIZ@ipn.mx
```

---

## 🔄 ACTUALIZAR EN EL FUTURO

Cuando hagas cambios en tu código local y los subas a GitHub:

```bash
# En consola Bash de PythonAnywhere
cd DeptoInv
git pull
```

Luego **Reload** en la pestaña Web.

---

## ✅ CHECKLIST

- [ ] Cuenta creada (upiizinvestigacion)
- [ ] Email confirmado
- [ ] Consola Bash abierta
- [ ] Repositorio clonado (`git clone`)
- [ ] Dependencias instaladas (`pip3.10 install`)
- [ ] Web App creada (Python 3.10, Manual)
- [ ] WSGI configurado (path correcto)
- [ ] Static files configurado (/static/)
- [ ] Reload ejecutado
- [ ] URLs funcionando

---

## 📞 SOPORTE

**PythonAnywhere:** https://help.pythonanywhere.com/
**UPIIZ:** investigacion_UPIIZ@ipn.mx

© 2025 UPIIZ - IPN

