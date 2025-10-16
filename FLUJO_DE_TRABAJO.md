# 🔄 FLUJO DE TRABAJO ESTÁNDAR - DEPTOIV UPIIZ

## Proceso para Hacer Cambios al Sistema

Este es el proceso estándar que seguiremos cada vez que necesitemos hacer modificaciones al sistema.

---

## 📋 PROCESO COMPLETO (3 PASOS)

### ✅ **PASO 1: PRUEBA LOCAL** (En tu computadora)

#### 1.1 Hacer los cambios
Edita los archivos necesarios en:
```
C:\Users\rafae\OneDrive\Escritorio\Escritorio Otoño 2025\DeptoInv\
```

#### 1.2 Ejecutar servidor local
```bash
python app.py
```

El servidor se iniciará en: `http://localhost:5000`

#### 1.3 Probar los cambios
- Abre tu navegador en `http://localhost:5000`
- Prueba el formulario: `http://localhost:5000/formulario`
- Verifica que todo funcione correctamente
- ✅ Confirma que los cambios se ven y funcionan como esperas

#### 1.4 Detener servidor (cuando termines de probar)
```bash
Ctrl + C
```

---

### ✅ **PASO 2: SUBIR A GITHUB**

#### 2.1 Ir al repositorio clonado
```bash
cd "C:\Users\rafae\OneDrive\Escritorio\Escritorio Otoño 2025\DeptoInv_GitHub"
```

#### 2.2 Copiar archivos modificados desde tu carpeta de trabajo
```powershell
# Copiar archivos específicos que modificaste
Copy-Item "..\DeptoInv\ARCHIVO_MODIFICADO" "ARCHIVO_MODIFICADO" -Force

# Ejemplo si modificaste el formulario:
Copy-Item "..\DeptoInv\static\formulario_investigador.html" "static\formulario_investigador.html" -Force

# Ejemplo si modificaste app.py:
Copy-Item "..\DeptoInv\app.py" "app.py" -Force
```

#### 2.3 Ver qué archivos cambiaron
```bash
git status
```

#### 2.4 Agregar los archivos modificados
```bash
git add .
```

#### 2.5 Hacer commit con mensaje descriptivo
```bash
git commit -m "Descripción clara de los cambios realizados"
```

**Ejemplos de mensajes de commit:**
- `"Agregar validación de CURP al formulario"`
- `"Actualizar diseño de la sección de SNII"`
- `"Corregir error en validación de ORCID"`
- `"Agregar campo de fecha de nacimiento"`

#### 2.6 Subir a GitHub
```bash
git push origin main
```

✅ Confirma que se subió correctamente viendo el mensaje de éxito

---

### ✅ **PASO 3: ACTUALIZAR PYTHONANYWHERE**

#### 3.1 Acceder a PythonAnywhere
Ir a: https://www.pythonanywhere.com/

**Usuario:** `upiizinvestigacion`

#### 3.2 Abrir Consola Bash
- Menú: **Consoles** → **Bash**
- O usa una consola existente

#### 3.3 Actualizar desde GitHub
```bash
# Ir al directorio del proyecto
cd /home/upiizinvestigacion/DeptoInv

# Ver estado actual
git status

# Descartar cambios locales si los hay
git reset --hard

# Descargar últimos cambios de GitHub
git pull origin main
```

**Deberías ver algo como:**
```
Updating abc1234..def5678
Fast-forward
 static/formulario_investigador.html | 15 ++++++++++++---
 1 file changed, 12 insertions(+), 3 deletions(-)
```

#### 3.4 Recargar la aplicación web

**Opción A: Desde el Dashboard (Recomendado)**
1. Menú: **Web**
2. Busca: `upiizinvestigacion.pythonanywhere.com`
3. Clic en botón verde: **"Reload"**
4. Espera 10 segundos

**Opción B: Desde la Consola**
```bash
touch /var/www/upiizinvestigacion_pythonanywhere_com_wsgi.py
```

#### 3.5 Verificar que funcionó
Abre en tu navegador:
```
https://upiizinvestigacion.pythonanywhere.com/formulario
```

✅ Verifica que tus cambios estén visibles y funcionen correctamente

---

## 🎯 RESUMEN ULTRA RÁPIDO

```
LOCAL → GITHUB → PYTHONANYWHERE
  ↓         ↓           ↓
Pruebas  Push      Git Pull + Reload
```

### Comandos en orden:

**1️⃣ Local:**
```bash
python app.py
# Probar en http://localhost:5000
# Ctrl+C cuando termines
```

**2️⃣ GitHub:**
```bash
cd DeptoInv_GitHub
Copy-Item "..\DeptoInv\archivo_modificado" "archivo_modificado" -Force
git add .
git commit -m "Descripción del cambio"
git push origin main
```

**3️⃣ PythonAnywhere:**
```bash
cd /home/upiizinvestigacion/DeptoInv
git pull origin main
touch /var/www/upiizinvestigacion_pythonanywhere_com_wsgi.py
```

---

## 📁 ARCHIVOS QUE MODIFICARÁS CON FRECUENCIA

### Frontend (Interfaz):
- `static/formulario_investigador.html` - Formulario principal
- `static/panel_formularios.html` - Panel de administración
- `static/styles.css` - Estilos visuales
- `static/app.js` - Funcionalidad JavaScript

### Backend (Servidor):
- `app.py` - Rutas y API
- `models.py` - Modelos de base de datos
- `database.py` - Configuración de BD

### Documentación:
- `README.md` - Documentación principal
- `*.md` - Otros documentos

---

## ⚠️ IMPORTANTE: NO MODIFICAR EN PYTHONANYWHERE

**NUNCA edites archivos directamente en PythonAnywhere.**

Siempre sigue el flujo:
```
Local → GitHub → PythonAnywhere
```

**¿Por qué?**
- Git pull sobrescribirá cambios manuales
- Perderás control de versiones
- No tendrás respaldo de cambios

---

## 🔍 VERIFICACIÓN ANTES DE SUBIR A PRODUCCIÓN

Antes de hacer `git push`, verifica:

- [ ] Los cambios funcionan correctamente en local
- [ ] No hay errores en la consola del navegador (F12)
- [ ] El formulario se puede enviar sin problemas
- [ ] La página se ve bien en móvil y desktop
- [ ] No rompiste funcionalidades existentes

---

## 🚨 SI ALGO SALE MAL EN PYTHONANYWHERE

### Ver errores:
```bash
# En consola de PythonAnywhere
tail -50 /var/log/upiizinvestigacion.pythonanywhere.com.error.log
```

### Volver a versión anterior:
```bash
cd /home/upiizinvestigacion/DeptoInv

# Ver últimos commits
git log --oneline -5

# Volver al commit anterior
git reset --hard <commit-hash>

# Recargar
touch /var/www/upiizinvestigacion_pythonanywhere_com_wsgi.py
```

### Reinstalar dependencias:
```bash
pip3.10 install --user flask flask-cors sqlalchemy pandas openpyxl werkzeug
```

---

## 📝 PLANTILLA DE COMMIT MESSAGES

Usa mensajes claros y descriptivos:

### Buenos ejemplos:
✅ `"Agregar validación de email institucional"`
✅ `"Actualizar diseño de sección de proyectos"`
✅ `"Corregir error en guardado de constancia SNII"`
✅ `"Agregar campo de CVU al formulario"`

### Malos ejemplos:
❌ `"cambios"`
❌ `"fix"`
❌ `"actualización"`
❌ `"asdf"`

---

## 🎨 TIPS PARA DESARROLLO LOCAL

### Reinicio automático de Flask:
Flask en modo debug (`debug=True`) recarga automáticamente cuando guardas cambios.

### Ver cambios en tiempo real:
1. Deja el servidor corriendo (`python app.py`)
2. Edita archivos
3. Guarda (Ctrl+S)
4. Recarga navegador (F5)

### Probar en móvil (misma red WiFi):
```
http://TU-IP-LOCAL:5000/formulario
```

Para saber tu IP:
```bash
ipconfig
# Busca "Dirección IPv4"
```

---

## 📊 ESTRUCTURA DE CARPETAS

```
DeptoInv/                           # Tu carpeta de trabajo
├── static/
│   ├── formulario_investigador.html
│   ├── panel_formularios.html
│   ├── styles.css
│   └── app.js
├── app.py
├── models.py
├── database.py
└── ...

DeptoInv_GitHub/                    # Clon del repositorio
├── static/
│   └── ...
├── app.py
└── ...
```

**Trabajas en:** `DeptoInv/`  
**Subes desde:** `DeptoInv_GitHub/`  
**Actualizas en:** PythonAnywhere

---

## 🔄 ACTUALIZACIÓN TÍPICA (Ejemplo Real)

### Escenario: Agregar campo de teléfono de oficina

#### 1️⃣ Local:
```bash
# Editar: static/formulario_investigador.html
# Agregar campo de teléfono de oficina

python app.py
# Probar en http://localhost:5000/formulario
# Ctrl+C
```

#### 2️⃣ GitHub:
```bash
cd DeptoInv_GitHub
Copy-Item "..\DeptoInv\static\formulario_investigador.html" "static\formulario_investigador.html" -Force
git add static/formulario_investigador.html
git commit -m "Agregar campo de teléfono de oficina al formulario"
git push origin main
```

#### 3️⃣ PythonAnywhere:
```bash
cd /home/upiizinvestigacion/DeptoInv
git pull origin main
# Web → Reload
```

✅ Verificar en: https://upiizinvestigacion.pythonanywhere.com/formulario

---

## 📞 INFORMACIÓN DE CONTACTO

**Repositorio GitHub:**  
https://github.com/rrevelesm/DeptoInv

**Sitio en Producción:**  
https://upiizinvestigacion.pythonanywhere.com/

**Formulario:**  
https://upiizinvestigacion.pythonanywhere.com/formulario

**Panel:**  
https://upiizinvestigacion.pythonanywhere.com/panel

---

## 🎓 Instituto Politécnico Nacional

**La Técnica al Servicio de la Patria**

UPIIZ - Campus Zacatecas  
Departamento de Investigación  
© 2025

---

**Este flujo de trabajo garantiza:**
- ✅ Cambios probados antes de producción
- ✅ Control de versiones completo
- ✅ Respaldos en GitHub
- ✅ Rollback fácil si algo falla
- ✅ Trabajo organizado y profesional

