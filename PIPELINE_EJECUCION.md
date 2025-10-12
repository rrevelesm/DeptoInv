# 🚀 Pipeline de Ejecución - Sistema de Padrón de Investigadores UPIIZ

## 📋 Para ejecutar en CUALQUIER computadora nueva

---

## 🔧 PRIMERA VEZ en una computadora nueva

### 1️⃣ **Prerrequisitos (instalar solo la primera vez)**

#### A) Instalar Python 3.8+
- Descargar desde: https://www.python.org/downloads/
- ⚠️ **IMPORTANTE:** Marcar "Add Python to PATH" durante instalación
- Verificar: `python --version`

#### B) Instalar Git
- Descargar desde: https://git-scm.com/downloads
- Verificar: `git --version`

#### C) Opcional: Instalar GitHub Desktop (interfaz gráfica)
- Descargar desde: https://desktop.github.com/

---

### 2️⃣ **Clonar el repositorio (solo primera vez)**

```bash
# Navegar a donde quieres el proyecto
cd D:\IDE_Cursor\

# Clonar el repositorio
git clone https://github.com/rrevelesm/DeptoInv.git

# Entrar al directorio
cd DeptoInv
```

---

### 3️⃣ **Instalar dependencias (solo primera vez)**

```bash
# Instalar todas las librerías necesarias
pip install -r requirements.txt
```

**Dependencias que se instalarán:**
- Flask==3.0.0
- flask-cors==4.0.0
- SQLAlchemy==2.0.23
- pandas>=2.0.0
- openpyxl>=3.0.0

---

### 4️⃣ **Configurar Git (solo primera vez)**

```bash
# Configurar tu identidad
git config --global user.name "Tu Nombre"
git config --global user.email "tu_email@ejemplo.com"

# Agregar directorio como seguro (si hay error de permisos)
git config --global --add safe.directory D:/IDE_Cursor/DeptoInv
```

---

## ⚡ EJECUCIÓN DIARIA (cada vez que trabajes)

### 1️⃣ **Actualizar código (traer cambios de GitHub)**

```bash
cd D:\IDE_Cursor\DeptoInv
git pull origin main
```

---

### 2️⃣ **Iniciar el servidor**

#### Opción A: Uso local (solo en esta computadora)
```bash
python app.py
```

#### Opción B: Acceso desde la red local (otras máquinas/celulares)
```bash
# Windows
batch\iniciar_sistema_red.bat

# O manualmente
python app.py
# (El servidor ya está configurado con host='0.0.0.0')
```

---

### 3️⃣ **Acceder al sistema**

#### En la misma computadora:
```
http://localhost:5000/formulario
http://localhost:5000/panel-formularios
http://localhost:5000/generar-qr
```

#### Desde otra computadora/celular en la red:
1. Obtén tu IP local: `ipconfig` en PowerShell
2. Busca "Dirección IPv4" (ej: 192.168.0.6)
3. Accede desde otros dispositivos: `http://192.168.0.6:5000/formulario`

---

## 📝 HACER CAMBIOS Y SUBIRLOS

### Flujo completo:

```bash
# 1. Ver qué archivos cambiaron
git status

# 2. Agregar cambios al staging
git add .
# O archivos específicos:
# git add static/formulario_investigador.html

# 3. Hacer commit
git commit -m "Descripción clara de tus cambios"

# 4. Subir a GitHub
git push origin main

# 🚀 TODO EN UNO (recomendado):
git add . ; git commit -m "Tu mensaje" ; git push origin main
```

---

## 🔄 SINCRONIZAR ENTRE COMPUTADORAS

### Computadora A (donde hiciste cambios):
```bash
git add .
git commit -m "Mis cambios"
git push origin main
```

### Computadora B (donde vas a trabajar ahora):
```bash
cd D:\IDE_Cursor\DeptoInv
git pull origin main
python app.py
```

---

## 🛠️ COMANDOS ÚTILES

### Ver historial de commits:
```bash
git log --oneline -n 10
```

### Descartar cambios locales (CUIDADO):
```bash
git restore nombre_archivo.html
```

### Ver diferencias:
```bash
git diff nombre_archivo.html
```

### Crear rama nueva:
```bash
git checkout -b nombre-rama
```

### Volver a la rama principal:
```bash
git checkout main
```

---

## 📱 COMPARTIR FORMULARIO CON INVESTIGADORES

### 1. Genera el código QR:
```
http://localhost:5000/generar-qr
```

### 2. Ingresa tu IP local (obtenerla con `ipconfig`)

### 3. Descarga o imprime el QR

### 4. Los investigadores escanean y acceden al formulario

---

## 🐛 SOLUCIÓN DE PROBLEMAS

### Error: "Python no se reconoce"
```bash
# Agregar Python al PATH manualmente
# Panel de Control > Sistema > Variables de entorno
# Agregar: C:\Users\TU_USUARIO\AppData\Local\Programs\Python\Python3X\
```

### Error: "git no se reconoce"
```bash
# En PowerShell (temporal):
$env:Path += ";C:\Program Files\Git\cmd"

# O agregar permanentemente en Variables de entorno
```

### Error: "Port 5000 already in use"
```bash
# Matar proceso en puerto 5000
netstat -ano | findstr :5000
taskkill /PID [número_de_PID] /F
```

### Error: "No module named 'flask'"
```bash
# Reinstalar dependencias
pip install -r requirements.txt
```

### Error: "Permission denied" en Git
```bash
git config --global --add safe.directory [RUTA_COMPLETA_PROYECTO]
```

---

## 📂 ESTRUCTURA DEL PROYECTO

```
DeptoInv/
├── app.py                          # Servidor Flask principal
├── models.py                       # Modelos de base de datos
├── requirements.txt                # Dependencias Python
├── depto_investigacion.db         # Base de datos SQLite
├── static/                         # Archivos estáticos
│   ├── formulario_investigador.html
│   ├── generar_qr.html
│   ├── panel_formularios.html
│   ├── styles.css
│   └── *.png, *.jpg               # Imágenes/logos
├── formularios/                    # Formularios guardados (JSON)
│   └── constancias_snii/          # Constancias SNII subidas
├── scripts/                        # Scripts auxiliares
│   ├── init_data.py
│   ├── importar_solo_aprobados.py
│   └── exportar_formularios_excel.py
└── batch/                          # Scripts de inicio
    ├── iniciar_sistema_red.bat
    └── iniciar_con_ngrok.bat
```

---

## 🎯 CHECKLIST RÁPIDO

### Primera vez en una PC nueva:
- [ ] Instalar Python 3.8+
- [ ] Instalar Git
- [ ] Clonar repositorio: `git clone https://github.com/rrevelesm/DeptoInv.git`
- [ ] Instalar dependencias: `pip install -r requirements.txt`
- [ ] Configurar Git: `git config --global user.name "Tu Nombre"`

### Cada día de trabajo:
- [ ] Actualizar código: `git pull origin main`
- [ ] Iniciar servidor: `python app.py`
- [ ] Hacer cambios
- [ ] Probar en navegador: `http://localhost:5000/formulario`
- [ ] Guardar cambios: `git add . ; git commit -m "mensaje" ; git push origin main`

---

## 📞 CONTACTO Y SOPORTE

**Jefe del Departamento de Investigación:**
- M. en C. Rafael Reveles Martínez
- 📧 investigacion_UPIIZ@ipn.mx
- 📱 492 250 4428
- Ext: 83530

**Repositorio GitHub:**
- https://github.com/rrevelesm/DeptoInv

---

## 🔐 IMPORTANTE - SEGURIDAD

⚠️ **NO subir a GitHub:**
- Archivos con contraseñas
- Tokens de API
- Datos personales sensibles
- Base de datos con información real

✅ **SÍ subir a GitHub:**
- Código fuente (.py, .html, .css, .js)
- Documentación (.md)
- Archivos de configuración (requirements.txt)
- Scripts auxiliares

---

**Última actualización:** 2025-10-12
**Versión:** 1.0
**Sistema:** Padrón de Investigadores UPIIZ - IPN

