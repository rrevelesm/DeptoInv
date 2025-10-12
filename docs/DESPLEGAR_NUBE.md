# ☁️ Desplegar el Sistema en la Nube (PythonAnywhere)

## ¿Por qué PythonAnywhere?

✅ **Gratis** para uso básico
✅ URL **permanente** (no cambia)
✅ **No necesitas** tener tu PC encendida
✅ Acceso desde **cualquier lugar del mundo**
✅ **Fácil** de configurar
✅ Soporte para **Flask** y **SQLite**

---

## 🚀 Guía Paso a Paso

### Paso 1: Crear Cuenta

1. Ve a: https://www.pythonanywhere.com
2. Clic en "Start running Python online in less than a minute!"
3. Crea cuenta gratuita (Beginner account)
4. Confirma tu email

---

### Paso 2: Subir Archivos

**Opción A: Desde la Web**

1. En PythonAnywhere, ve a "Files"
2. Crea carpeta: `DeptoInv`
3. Sube todos tus archivos:
   - `app.py`
   - `models.py`
   - `database.py`
   - `requirements.txt`
   - Carpeta `static/` completa

**Opción B: Desde GitHub (Recomendado)**

```bash
# En la consola de PythonAnywhere
cd ~
git clone https://github.com/TU-USUARIO/DeptoInv.git
```

---

### Paso 3: Instalar Dependencias

En la consola de PythonAnywhere:

```bash
cd DeptoInv
pip3.10 install --user -r requirements.txt
```

---

### Paso 4: Crear Web App

1. Ve a la pestaña "Web"
2. Clic en "Add a new web app"
3. Elige "Manual configuration"
4. Selecciona "Python 3.10"

---

### Paso 5: Configurar WSGI

1. En la página de tu web app, busca "WSGI configuration file"
2. Clic para editar
3. Reemplaza TODO el contenido con:

```python
import sys
import os

# Agregar directorio del proyecto
path = '/home/TU_USUARIO/DeptoInv'
if path not in sys.path:
    sys.path.append(path)

# Importar la app Flask
from app import app as application
```

4. Guarda el archivo

---

### Paso 6: Configurar Virtualenv (Opcional)

Si creaste un virtualenv:

1. En la sección "Virtualenv" de la web app
2. Ingresa: `/home/TU_USUARIO/DeptoInv/venv`

---

### Paso 7: Recargar y Probar

1. Clic en el botón verde "Reload" en la página de tu web app
2. Tu URL será: `https://TU_USUARIO.pythonanywhere.com`
3. Prueba: `https://TU_USUARIO.pythonanywhere.com/formulario`

---

## 🔧 Ajustes Necesarios en el Código

### Modificar `app.py`

Cambia la última línea de:

```python
if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True, port=5000)
```

A:

```python
if __name__ == '__main__':
    # En producción, no usar debug=True
    app.run(host='0.0.0.0', debug=False, port=5000)
```

---

## 📋 Tu URL Permanente

Una vez configurado, tu URL será:

```
https://TU_USUARIO.pythonanywhere.com/formulario
```

**Ejemplo:**
```
https://upiiz-investigacion.pythonanywhere.com/formulario
```

Esta URL:
- ✅ **NO cambia nunca**
- ✅ **Siempre disponible** (24/7)
- ✅ **No necesitas** tener tu PC encendida
- ✅ Funciona desde **cualquier lugar**

---

## 📧 Mensaje para Investigadores

```
Estimado(a) investigador(a):

Favor de llenar el siguiente formulario de actualización de datos:

🔗 https://upiiz-investigacion.pythonanywhere.com/formulario

Este formulario estará disponible hasta [FECHA]

Departamento de Investigación - UPIIZ
M. en C. Rafael Reveles Martínez
investigacion_UPIIZ@ipn.mx
```

---

## 💾 Respaldo de Datos

Para descargar los formularios recibidos:

1. Ve a "Files" en PythonAnywhere
2. Navega a `DeptoInv/formularios/`
3. Descarga cada archivo JSON
4. O usa la función "Exportar a Excel" desde el panel web

---

## 🆓 Límites de la Cuenta Gratuita

| Recurso | Límite |
|---------|--------|
| Tráfico | 100,000 hits/día |
| Almacenamiento | 512 MB |
| Consolas | 2 simultáneas |
| Web apps | 1 |
| Velocidad | Compartida |

**Para UPIIZ:** Más que suficiente para 50-100 investigadores

---

## 🔒 Seguridad

PythonAnywhere incluye:
- ✅ HTTPS automático
- ✅ Backups diarios
- ✅ Protección DDoS
- ✅ Aislamiento de aplicaciones

---

## 🆙 Actualizar el Sistema

Cuando hagas cambios:

1. Sube los archivos actualizados
2. Ve a la pestaña "Web"
3. Clic en "Reload"

O si usas Git:

```bash
cd DeptoInv
git pull
# Luego Reload en la web app
```

---

## 💰 Upgrade (Opcional)

Si necesitas más recursos:

| Plan | Precio | Beneficios |
|------|--------|------------|
| Hacker | $5/mes | 2 web apps, sin ads |
| Student | $7/mes | Más almacenamiento |
| Web Developer | $12/mes | Dominio personalizado |

---

## 🔗 Dominio Personalizado

Con plan de pago puedes usar:
```
https://investigacion.upiiz.ipn.mx
```

En lugar de:
```
https://upiiz-investigacion.pythonanywhere.com
```

---

## 🛠️ Solución de Problemas

### "Import Error: No module named flask"

```bash
pip3.10 install --user flask flask-cors sqlalchemy pandas openpyxl
```

### "Database is locked"

PythonAnywhere tiene límites en SQLite concurrente. Considera usar MySQL (gratuito en su plan).

### "502 Bad Gateway"

Verifica el log de errores en la pestaña "Web" → "Error log"

---

## 📞 Soporte

**PythonAnywhere:**
- Foros: https://www.pythonanywhere.com/forums/
- Email: support@pythonanywhere.com

**UPIIZ:**
- investigacion_UPIIZ@ipn.mx
- Ext. 83530

---

© 2025 UPIIZ - Instituto Politécnico Nacional

