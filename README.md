# 🎓 Sistema de Gestión de Investigación - UPIIZ

Sistema web para la gestión integral de investigadores, proyectos, publicaciones y formularios de recolección de datos del Departamento de Investigación de la UPIIZ (Unidad Profesional Interdisciplinaria de Ingeniería Campus Zacatecas) del Instituto Politécnico Nacional.

## 🌐 Demo en Vivo

**URL del Sistema:** [https://upiiz-investigacion.pythonanywhere.com](https://upiiz-investigacion.pythonanywhere.com) *(cuando esté desplegado)*

**Formulario de Investigadores:** [https://upiiz-investigacion.pythonanywhere.com/formulario](https://upiiz-investigacion.pythonanywhere.com/formulario)

---

## ✨ Características Principales

### 📊 Gestión de Investigadores
- Registro completo de investigadores
- Información de contacto y categoría académica
- Seguimiento de becas EDI y nombramientos SNII
- Integración con ORCID

### 📚 Proyectos de Investigación
- Catálogo de proyectos SIP-IPN 2025
- Solo proyectos aprobados
- Clave SIP y responsable del proyecto
- Categorías: Iniciación, Colaborativos, Innovación, Estratégicos, Consorcios, Externos

### 📄 Publicaciones Científicas
- Registro de publicaciones académicas
- DOI, revista, factor de impacto
- Indexación y palabras clave

### 📋 Formulario de Recolección de Datos
Sistema completo para recolectar información actualizada de investigadores:

#### Datos Personales
- Nombre completo, género, CURP, fecha de nacimiento
- Clave de empleado y categoría
- Correo institucional
- Teléfono celular (opcional)

#### Proyectos Vigentes
- Permite múltiples proyectos de diferentes categorías
- Solo un proyecto por categoría
- Integración con SAPPI para consultar nombres

#### Distinciones Académicas
- **Beca EDI:** Niveles 1-8 y Permanente
- **SNII:** Nivel, vigencia, y carga de constancia (PDF)

#### Productividad Académica
- ORCID (con validación)
- 3-5 líneas de generación y aplicación del conocimiento
- DOIs de publicaciones 2025

### 📊 Panel de Administración
- Visualización de todos los formularios recibidos
- Estadísticas en tiempo real
- Búsqueda y filtrado de investigadores
- Exportación a Excel

---

## 🚀 Instalación y Configuración

### Requisitos Previos

- Python 3.8 o superior
- pip (gestor de paquetes de Python)
- Git

### Instalación Local

```bash
# 1. Clonar el repositorio
git clone https://github.com/rrevelesm/DeptoInv_UPIIZ.git
cd DeptoInv_UPIIZ

# 2. Crear entorno virtual (recomendado)
python -m venv venv

# Activar en Windows
venv\Scripts\activate

# Activar en Linux/Mac
source venv/bin/activate

# 3. Instalar dependencias
pip install -r requirements.txt

# 4. Inicializar la base de datos (si es necesario)
python database.py

# 5. Importar proyectos aprobados (opcional)
python importar_solo_aprobados.py

# 6. Ejecutar el servidor
python app.py
```

El sistema estará disponible en `http://localhost:5000`

---

## 🌐 Despliegue en Internet

### Opción 1: PythonAnywhere (Recomendado - Gratis)

Ver guía completa: [`TUTORIAL_PYTHONANYWHERE.md`](TUTORIAL_PYTHONANYWHERE.md)

**Pasos resumidos:**
1. Crear cuenta en [PythonAnywhere](https://www.pythonanywhere.com)
2. Subir archivos del proyecto
3. Configurar Web App (Python 3.10)
4. Configurar archivo WSGI
5. Instalar dependencias
6. Reload y ¡listo!

**URL final:** `https://tu-usuario.pythonanywhere.com`

### Opción 2: Red Local (UPIIZ)

Ver guía: [`COMPARTIR_FORMULARIO.md`](COMPARTIR_FORMULARIO.md)

```bash
# Ejecutar en modo red local
iniciar_sistema_red.bat
```

### Opción 3: Ngrok (Temporal desde casa)

Ver guía: [`USAR_NGROK.md`](USAR_NGROK.md)

```bash
# Iniciar con túnel ngrok
iniciar_con_ngrok.bat
```

---

## 📁 Estructura del Proyecto

```
DeptoInv_UPIIZ/
├── app.py                          # Aplicación Flask principal
├── models.py                       # Modelos de base de datos (SQLAlchemy)
├── database.py                     # Configuración de base de datos
├── requirements.txt                # Dependencias Python
├── investigacion_upiiz.db          # Base de datos SQLite (no en Git)
│
├── static/                         # Archivos estáticos
│   ├── index.html                  # Página principal del sistema
│   ├── formulario_investigador.html # Formulario de recolección
│   ├── panel_formularios.html      # Panel de administración
│   ├── generar_qr.html             # Generador de códigos QR
│   ├── styles.css                  # Estilos CSS
│   └── app.js                      # JavaScript del sistema
│
├── formularios/                    # Formularios recibidos (no en Git)
│   ├── *.json                      # Datos de formularios
│   └── constancias_snii/*.pdf      # PDFs de constancias SNII
│
├── scripts/
│   ├── importar_solo_aprobados.py  # Importar proyectos desde Excel
│   └── exportar_formularios_excel.py # Exportar formularios a Excel
│
├── docs/                           # Documentación
│   ├── TUTORIAL_PYTHONANYWHERE.md  # Guía de despliegue en nube
│   ├── COMPARTIR_FORMULARIO.md     # Guía red local
│   ├── USAR_NGROK.md               # Guía Ngrok
│   ├── GUIA_GESTION_FORMULARIOS.md # Gestión de formularios
│   └── FORMULARIO_INVESTIGADORES.md # Documentación del formulario
│
└── batch/                          # Scripts de inicio
    ├── iniciar_sistema_red.bat     # Iniciar en red local
    └── iniciar_con_ngrok.bat       # Iniciar con ngrok
```

---

## 🔧 Tecnologías Utilizadas

### Backend
- **Flask** - Framework web Python
- **SQLAlchemy** - ORM para base de datos
- **SQLite** - Base de datos
- **Pandas** - Procesamiento de datos
- **OpenPyXL** - Generación de Excel

### Frontend
- **HTML5, CSS3, JavaScript**
- **Vanilla JS** (sin frameworks)
- **Responsive Design**
- **QRCode.js** - Generación de códigos QR

---

## 📊 API REST

El sistema incluye una API REST completa:

### Investigadores
```
GET    /api/investigadores          # Listar todos
GET    /api/investigadores/<id>     # Obtener uno
POST   /api/investigadores          # Crear
PUT    /api/investigadores/<id>     # Actualizar
DELETE /api/investigadores/<id>     # Eliminar
```

### Proyectos
```
GET    /api/proyectos               # Listar todos
GET    /api/proyectos/<id>          # Obtener uno
POST   /api/proyectos               # Crear
PUT    /api/proyectos/<id>          # Actualizar
DELETE /api/proyectos/<id>          # Eliminar
```

### Publicaciones
```
GET    /api/publicaciones           # Listar todas
POST   /api/publicaciones           # Crear
PUT    /api/publicaciones/<id>     # Actualizar
DELETE /api/publicaciones/<id>     # Eliminar
```

### Formularios
```
POST   /api/formulario-investigador # Enviar formulario
GET    /api/formularios-lista       # Listar formularios
GET    /api/exportar-formularios-excel # Exportar a Excel
```

### Estadísticas
```
GET    /api/estadisticas            # Estadísticas generales
```

---

## 🔐 Seguridad y Privacidad

- ✅ HTTPS automático en PythonAnywhere
- ✅ Validación de datos en frontend y backend
- ✅ Archivos sensibles excluidos de Git (.gitignore)
- ✅ Formularios guardados en servidor seguro
- ✅ Constancias PDF almacenadas de forma segura

---

## 📥 Datos de Ejemplo

Para importar los proyectos aprobados 2025:

```bash
python importar_solo_aprobados.py
```

Esto cargará los proyectos desde `Proyectos 2025 Investigación.xlsx`

---

## 📧 Compartir Formulario con Investigadores

### Mensaje de Email Sugerido:

```
Estimado(a) investigador(a):

Favor de llenar el siguiente formulario de actualización de datos 
del Departamento de Investigación:

🔗 [URL DEL FORMULARIO]

El formulario incluye información sobre:
✓ Datos personales y de contacto
✓ Proyectos de investigación vigentes
✓ Becas EDI y nombramiento SNII
✓ ORCID y líneas de investigación
✓ Productividad académica 2025

Fecha límite: [FECHA]

Gracias por su colaboración.

M. en C. Rafael Reveles Martínez
Jefe del Departamento de Investigación
UPIIZ - Campus Zacatecas
www.zacatecas.ipn.mx
investigacion_UPIIZ@ipn.mx
Ext. 83530
```

---

## 🆘 Solución de Problemas

### Error: "No module named flask"
```bash
pip install -r requirements.txt
```

### Error: "Database is locked"
```bash
# Cerrar todas las conexiones y reiniciar
python app.py
```

### El formulario no guarda
- Verificar que existe la carpeta `formularios/`
- Verificar permisos de escritura

### No aparecen los proyectos
```bash
# Re-importar proyectos
python importar_solo_aprobados.py
```

---

## 📞 Contacto y Soporte

**UPIIZ - Departamento de Investigación**  
M. en C. Rafael Reveles Martínez  
Jefe del Departamento de Investigación

📧 investigacion_UPIIZ@ipn.mx  
☎️ Ext. 83530  
🌐 [www.zacatecas.ipn.mx](https://www.zacatecas.ipn.mx)

**Dirección:**  
Unidad Profesional Interdisciplinaria de Ingeniería  
Campus Zacatecas  
Instituto Politécnico Nacional

---

## 📝 Licencia

Este proyecto es de uso interno de la UPIIZ - IPN.

---

## 🙏 Créditos

Desarrollado para el Departamento de Investigación de la UPIIZ.

**Tecnologías utilizadas:**
- [Flask](https://flask.palletsprojects.com/)
- [SQLAlchemy](https://www.sqlalchemy.org/)
- [Pandas](https://pandas.pydata.org/)
- [QRCode.js](https://davidshimjs.github.io/qrcodejs/)

---

## 🎓 Instituto Politécnico Nacional

**La Técnica al Servicio de la Patria**

© 2025 UPIIZ - Campus Zacatecas
