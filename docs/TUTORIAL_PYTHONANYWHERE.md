# 🚀 Tutorial Completo: Subir a PythonAnywhere (GRATIS)

## Tu sistema estará en: `https://tu-usuario.pythonanywhere.com`

---

## 📋 PASO 1: Crear Cuenta (5 minutos)

1. Ve a: https://www.pythonanywhere.com
2. Clic en "Pricing & signup"
3. Elige "Create a Beginner account" (FREE - $0/mes)
4. Completa el registro:
   - Username: **upiiz-investigacion** (o el que prefieras)
   - Email: Tu email
   - Password: Contraseña segura
5. Confirma tu email

**Tu URL será:** `https://upiiz-investigacion.pythonanywhere.com`

---

## 📁 PASO 2: Subir Archivos (10 minutos)

### Opción A: Usando Git (Recomendado)

1. **En PythonAnywhere, ve a "Consoles"**
2. **Inicia una "Bash console"**
3. **Ejecuta estos comandos:**

```bash
# Opción 1: Si tienes los archivos en GitHub
git clone https://github.com/TU-USUARIO/DeptoInv.git
cd DeptoInv

# Opción 2: Si NO tienes GitHub, sube manualmente (ver Opción B)
```

### Opción B: Subir Manualmente

1. **Ve a la pestaña "Files"**
2. **Crea la carpeta `DeptoInv`**
3. **Sube cada archivo:**
   - `app.py`
   - `models.py`
   - `database.py`
   - `requirements.txt`
   - Carpeta `static/` completa (todos los archivos HTML, CSS, JS)
   - Archivo `investigacion_upiiz.db` (tu base de datos)

---

## 📦 PASO 3: Instalar Dependencias (5 minutos)

1. **En la consola Bash:**

```bash
cd DeptoInv

# Instalar todas las librerías
pip3.10 install --user flask flask-cors sqlalchemy pandas openpyxl
```

2. **Espera a que termine la instalación** (aparecerán mensajes de "Successfully installed...")

---

## 🌐 PASO 4: Crear Web App (5 minutos)

1. **Ve a la pestaña "Web"**
2. **Clic en "+ Add a new web app"**
3. **Sigue el wizard:**
   - Dominio: Deja el que te da (`tu-usuario.pythonanywhere.com`)
   - Framework: **"Manual configuration"**
   - Python version: **Python 3.10**
4. **Clic en "Next" hasta terminar**

---

## ⚙️ PASO 5: Configurar WSGI (Importante - 5 minutos)

1. **En la página de tu web app, busca la sección "Code"**
2. **Clic en el enlace azul que dice "/var/www/tu_usuario_pythonanywhere_com_wsgi.py"**
3. **BORRA TODO el contenido del archivo**
4. **Pega este código:**

```python
import sys
import os

# ========== IMPORTANTE: Cambia 'TU_USUARIO' por tu usuario real ==========
path = '/home/TU_USUARIO/DeptoInv'
if path not in sys.path:
    sys.path.insert(0, path)

# Configurar directorio de trabajo
os.chdir(path)

# Importar la aplicación Flask
from app import app as application

# Configuración adicional para producción
application.config['DEBUG'] = False
```

5. **⚠️ IMPORTANTE:** Cambia `TU_USUARIO` por tu username de PythonAnywhere
   - Si tu usuario es `upiiz-investigacion`, debe quedar:
   - `path = '/home/upiiz-investigacion/DeptoInv'`

6. **Guarda el archivo** (Clic en "Save" en la esquina superior)

---

## 🔄 PASO 6: Recargar y Probar (2 minutos)

1. **Regresa a la pestaña "Web"**
2. **Clic en el botón verde grande: "Reload tu-usuario.pythonanywhere.com"**
3. **Espera ~10 segundos**
4. **Clic en el link de tu sitio (arriba del todo)**

**¡Tu sistema ya está en línea!** 🎉

---

## 🧪 PASO 7: Verificar que Funciona

### Prueba estas URLs:

```
https://tu-usuario.pythonanywhere.com/
(Sistema principal - debe mostrar investigadores y proyectos)

https://tu-usuario.pythonanywhere.com/formulario
(Formulario para investigadores - ESTA es la URL que compartirás)

https://tu-usuario.pythonanywhere.com/panel-formularios
(Panel de administración - para ver formularios recibidos)
```

---

## 📧 PASO 8: Compartir con Investigadores

Envía este mensaje:

```
Estimado(a) investigador(a):

Favor de llenar el siguiente formulario de actualización de datos 
del Departamento de Investigación:

🔗 https://upiiz-investigacion.pythonanywhere.com/formulario

El formulario incluye información sobre proyectos vigentes, becas EDI, 
nombramiento SNII, ORCID y productividad académica 2025.

Fecha límite: [AGREGAR FECHA]

Gracias por su colaboración.

M. en C. Rafael Reveles Martínez
Jefe del Departamento de Investigación
UPIIZ - Campus Zacatecas
www.zacatecas.ipn.mx
```

---

## 🔍 SOLUCIÓN DE PROBLEMAS

### Problema: "Error running WSGI application"

**Causa:** Error en la configuración WSGI

**Solución:**
1. Ve a "Web" → "Log files" → "Error log"
2. Lee el error (generalmente indica qué falta)
3. Común: Olvidaste cambiar `TU_USUARIO` en el WSGI

### Problema: "ImportError: No module named flask"

**Causa:** No se instalaron las dependencias

**Solución:**
```bash
cd DeptoInv
pip3.10 install --user flask flask-cors sqlalchemy pandas openpyxl
```

Luego "Reload" en la web app.

### Problema: "Not Found - The requested URL was not found"

**Causa:** Ruta incorrecta en WSGI

**Solución:**
Verifica que en el archivo WSGI:
- El path sea correcto: `/home/TU_USUARIO/DeptoInv`
- Los archivos estén en esa ubicación

### Problema: Base de datos vacía

**Causa:** No se subió el archivo `investigacion_upiiz.db`

**Solución:**
1. Ve a "Files"
2. Navega a `/home/TU_USUARIO/DeptoInv/`
3. Sube tu archivo `investigacion_upiiz.db`
4. "Reload" la web app

---

## 🔄 ACTUALIZAR EL SISTEMA (Futuro)

Cuando hagas cambios en tu código:

### Si usas Git:

```bash
cd DeptoInv
git pull
```

### Si subes manualmente:

1. Ve a "Files"
2. Navega al archivo que quieres cambiar
3. Edítalo o súbelo de nuevo

**Siempre después de cambios:**
1. Ve a "Web"
2. Clic en "Reload"

---

## 💾 RESPALDO DE DATOS

Para descargar los formularios recibidos:

### Desde el Panel Web:
```
https://tu-usuario.pythonanywhere.com/panel-formularios
→ Botón "Exportar a Excel"
```

### Desde Files:
1. Ve a "Files"
2. Navega a `DeptoInv/formularios/`
3. Descarga cada JSON
4. Para constancias PDF: `DeptoInv/formularios/constancias_snii/`

---

## 💰 LÍMITES DEL PLAN GRATUITO

| Recurso | Límite | Suficiente para |
|---------|--------|-----------------|
| Tráfico diario | 100,000 hits | ✅ 500+ investigadores/día |
| Almacenamiento | 512 MB | ✅ Miles de formularios |
| CPU | Compartida | ✅ Uso normal |
| Bases de datos | SQLite | ✅ Tu sistema actual |
| Uptime | 100% | ✅ Siempre disponible |

**Para UPIIZ:** El plan gratuito es MÁS que suficiente

---

## 🆙 UPGRADE A PLAN DE PAGO (Opcional)

### Plan Hacker ($5/mes):

✅ Dominio personalizado: `investigacion.upiiz.ipn.mx`
✅ 2 web apps
✅ Sin anuncios de PythonAnywhere
✅ Mayor CPU

**¿Vale la pena?** Solo si quieres dominio personalizado

---

## 📊 MONITOREO

### Ver estadísticas de uso:

1. Ve a "Web"
2. Sección "Statistics"
3. Verás:
   - Visitas al sitio
   - Uso de CPU
   - Errores recientes

---

## 🎓 URL FINAL

Tu sistema estará disponible en:

```
🌐 https://upiiz-investigacion.pythonanywhere.com
```

**Características:**
- ✅ Disponible 24/7
- ✅ URL permanente (no cambia)
- ✅ No necesitas tu PC encendida
- ✅ Acceso desde cualquier dispositivo
- ✅ HTTPS (seguro)
- ✅ Gratis para siempre

---

## 📞 SOPORTE

**PythonAnywhere:**
- Foros: https://www.pythonanywhere.com/forums/
- Email: support@pythonanywhere.com
- Documentación: https://help.pythonanywhere.com/

**UPIIZ:**
- investigacion_UPIIZ@ipn.mx
- Ext. 83530

---

## ✅ CHECKLIST FINAL

- [ ] Cuenta creada en PythonAnywhere
- [ ] Archivos subidos a `/home/TU_USUARIO/DeptoInv/`
- [ ] Dependencias instaladas (`pip install`)
- [ ] Web app creada (Python 3.10)
- [ ] Archivo WSGI configurado (cambiar TU_USUARIO)
- [ ] Web app "Reload" ejecutado
- [ ] Sitio funcionando (probar las 3 URLs)
- [ ] URL compartida con investigadores

---

© 2025 UPIIZ - Instituto Politécnico Nacional
La Técnica al Servicio de la Patria

