# 📊 Guía de Gestión de Formularios - UPIIZ

## Sistema de Recolección de Información de Investigadores

**UPIIZ - Departamento de Investigación**  
Jefe de Departamento: M. en C. Rafael Reveles Martínez

---

## 🌐 URLs del Sistema

### Formulario de Captura (Para Investigadores):
```
http://localhost:5000/formulario
```

### Panel de Gestión (Para Administradores):
```
http://localhost:5000/panel-formularios
```

### Sistema Principal:
```
http://localhost:5000
```

---

## 📋 1. Panel Web de Formularios

### Acceso al Panel

**Opción 1:** Desde el sistema principal
- Abre `http://localhost:5000`
- Clic en el botón dorado **"📋 Ver Formularios Recibidos"**

**Opción 2:** Acceso directo
- Abre `http://localhost:5000/panel-formularios`

### Funcionalidades del Panel

✅ **Estadísticas en Tiempo Real:**
- Total de formularios recibidos
- Cantidad con SNII
- Cantidad con Beca EDI
- Cantidad con proyectos vigentes

✅ **Visualización de Formularios:**
- Todos los formularios en tarjetas
- Información completa de cada investigador
- Ordenados por fecha (más recientes primero)

✅ **Búsqueda Rápida:**
- Buscar por nombre
- Buscar por clave de empleado
- Buscar por correo
- Buscar por CURP

✅ **Exportación a Excel:**
- Botón "📥 Exportar a Excel"
- Descarga inmediata
- Archivo con timestamp

---

## 📥 2. Exportación a Excel

### Desde el Panel Web (Recomendado)

1. Abre el panel: `http://localhost:5000/panel-formularios`
2. Clic en **"📥 Exportar a Excel"**
3. El archivo se descarga automáticamente
4. Nombre: `Formularios_UPIIZ_[FECHA]_[HORA].xlsx`

### Desde Línea de Comandos

```bash
python exportar_formularios_excel.py
```

**Resultado:**
- Archivo Excel generado en la carpeta del proyecto
- Nombre: `Formularios_Investigadores_UPIIZ_[TIMESTAMP].xlsx`

---

## 📊 3. Estructura del Archivo Excel

### Columnas Incluidas:

**Datos Personales:**
1. Nombre Completo
2. CURP
3. Fecha Nacimiento
4. Género
5. Clave Empleado
6. Categoría
7. Correo Institucional
8. Teléfono

**Proyectos:**
9. Tiene Proyecto (Sí/No)
10. Proyectos (Categoría: Nombre)

**Distinciones:**
11. Beca EDI (Nivel o No)
12. SNII (Nivel o No)
13. SNII Vigencia (Fechas)

**Identificadores:**
14. ORCID

**Investigación:**
15. Líneas Investigación
16. Publicaciones 2025 (DOIs)

**Metadata:**
17. Fecha Registro

---

## 💾 4. Ubicación de Archivos

### Datos JSON (Backend)
```
DeptoInv/
└── formularios/
    ├── investigador_12345_20251012_081229.json
    ├── investigador_67890_20251012_083045.json
    └── constancias_snii/
        ├── snii_12345_20251012_081229.pdf
        └── snii_67890_20251012_083045.pdf
```

### Archivos Excel Generados
```
DeptoInv/
├── Formularios_UPIIZ_20251012_143020.xlsx
├── Formularios_UPIIZ_20251012_150530.xlsx
└── ...
```

---

## 🔍 5. Consultar Datos Específicos

### Ver un Formulario Específico (JSON)

```bash
# Listar formularios
dir formularios

# Ver contenido de un formulario
type formularios\investigador_12345_20251012_081229.json
```

### Ver una Constancia SNII

```bash
# Listar constancias
dir formularios\constancias_snii

# Abrir un PDF
start formularios\constancias_snii\snii_12345_20251012_081229.pdf
```

---

## 📈 6. Análisis de Datos en Excel

### Filtros Útiles

**Por Beca EDI:**
- Filtrar columna "Beca EDI" ≠ "No"
- Ver todos los investigadores con EDI

**Por SNII:**
- Filtrar columna "SNII" ≠ "No"
- Ver niveles y vigencias

**Por Proyectos:**
- Filtrar "Tiene Proyecto" = "Sí"
- Ver categorías en columna "Proyectos"

### Tablas Dinámicas Recomendadas

**Contar por Categoría:**
- Filas: Categoría
- Valores: Contar de Nombre Completo

**Distribución de Niveles EDI:**
- Filas: Beca EDI
- Valores: Contar

**Distribución de Niveles SNII:**
- Filas: SNII
- Valores: Contar

---

## 🔄 7. Flujo de Trabajo Recomendado

### Paso 1: Recolección
1. Compartir el formulario: `http://localhost:5000/formulario`
2. Investigadores llenan el formulario
3. Datos se guardan automáticamente

### Paso 2: Monitoreo
1. Revisar panel: `http://localhost:5000/panel-formularios`
2. Ver estadísticas en tiempo real
3. Buscar investigadores específicos

### Paso 3: Exportación
1. Cuando termina el período de recolección
2. Clic en "Exportar a Excel"
3. Analizar datos en Excel

### Paso 4: Respaldo
1. Copiar carpeta `formularios/` completa
2. Incluye JSONs y PDFs
3. Guardar en ubicación segura

---

## 🆘 8. Solución de Problemas

### No aparecen formularios en el panel

**Verificar:**
```bash
# ¿Existe la carpeta?
dir formularios

# ¿Hay archivos JSON?
dir formularios\*.json
```

**Solución:**
- Asegúrate de que al menos un investigador haya enviado el formulario

### Error al exportar a Excel

**Requisito:**
```bash
pip install openpyxl
```

### El panel muestra "Error al cargar"

**Solución:**
- Verifica que el servidor esté corriendo
- Revisa la consola del navegador (F12)
- Verifica permisos de lectura en carpeta `formularios/`

---

## 📞 9. Contacto y Soporte

**Departamento de Investigación - UPIIZ**  
Jefe: M. en C. Rafael Reveles Martínez  
Correo: investigacion_UPIIZ@ipn.mx  
Extensión: 83530

**Sitio Web:** [https://www.zacatecas.ipn.mx/](https://www.zacatecas.ipn.mx/)

---

## 📝 10. Resumen de Comandos

```bash
# Iniciar sistema
python app.py

# Exportar a Excel (línea de comandos)
python exportar_formularios_excel.py

# Ver formularios (JSON)
dir formularios\*.json

# Ver constancias (PDF)
dir formularios\constancias_snii\*.pdf
```

---

## 🎓 UPIIZ - Instituto Politécnico Nacional

**Unidad Profesional Interdisciplinaria de Ingeniería**  
**Campus Zacatecas**

Sistema de Gestión de Investigación  
Panel de Formularios de Investigadores

**La Técnica al Servicio de la Patria**

© 2025

