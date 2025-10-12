# 📋 Formulario de Registro de Investigadores - UPIIZ

## 🎯 Descripción

Formulario web completo para recolectar información detallada de investigadores de la Unidad Profesional Interdisciplinaria de Ingeniería, Campus Zacatecas - UPIIZ, del Instituto Politécnico Nacional.

**Jefe del Departamento de Investigación:**  
M. en C. Rafael Reveles Martínez

**Sitio Web:** [https://www.zacatecas.ipn.mx/](https://www.zacatecas.ipn.mx/)

## 🌐 Acceso al Formulario

### URL del Formulario:
```
http://localhost:5000/formulario
```

**También puedes acceder desde:**
- Navegador web: `http://127.0.0.1:5000/formulario`
- Dispositivos móviles en la misma red: `http://[IP-DE-TU-PC]:5000/formulario`

---

## 📊 Campos del Formulario

### 1. 👤 Datos Personales
- **Nombre Completo** (obligatorio)
- **CURP** (obligatorio)
  - Clave Única de Registro de Población
  - 18 caracteres
  - Validación de formato automática
- **Fecha de Nacimiento** (obligatorio)
  - Selector de fecha
- **Género** (obligatorio)
  - Femenino
  - Masculino
  - Otro
  - Prefiero no decirlo
- **Clave de Empleado** (obligatorio)
- **Categoría** (obligatorio)
  - Profesor Titular (A, B, C)
  - Profesor Asociado (A, B, C)
  - Profesor Asistente (A, B, C)
  - Técnico Académico Titular (A, B, C)
  - Otro
- **Correo Electrónico Institucional** (obligatorio)
  - Validación de formato email
  - Ejemplo: ejemplo@ipn.mx
- **¿Acepta ser contactado por teléfono celular?** (obligatorio)
  - Sí / No
- **Número de Teléfono Celular** (si acepta - obligatorio)
  - 10 dígitos
  - Validación automática de formato

### 2. 📊 Proyectos de Investigación Vigentes
- **¿Cuenta con proyecto(s) vigente(s)?** (obligatorio)
  - Sí / No
- **Agregar Proyectos** (si tiene - dinámico)
  - Puede agregar **múltiples proyectos de DIFERENTES categorías**
  - **Solo UN proyecto por categoría** (validación automática)
  - Ejemplo válido: 1 Iniciación + 1 Innovación ✅
  - Ejemplo inválido: 2 Iniciación ❌

**Por cada proyecto:**
- **Categoría** (obligatorio)
  - Iniciación en la investigación
  - Grupos colaborativos
  - Innovación y maduración tecnológica
  - Proyectos estratégicos
  - Consorcios
  - Externos al IPN
- **Tipo** (obligatorio - dinámico según categoría)
  - Basado en convocatorias oficiales IPN
  - Incluye **SECIHTI** (antes CONACyT) para externos
- **Nombre del Proyecto** (obligatorio)
  - Nombre completo del proyecto
  - Consultar en [SAPPI](https://sappi.ipn.mx/) si no recuerda

### 3. 💰 Beca EDI (Estímulo al Desempeño de los Investigadores)
- **¿Cuenta con Beca EDI?** (obligatorio)
  - Sí / No
- **Nivel EDI** (si aplica)
  - Nivel I, II, III, IV

### 4. 🏆 Sistema Nacional de Investigadores (SNII)
- **¿Cuenta con nombramiento SNII?** (obligatorio)
  - Sí / No
- **Nivel SNII** (si aplica)
  - Candidato
  - Nivel I, II, III
  - Emérito
- **Fecha de Inicio** (si aplica)
- **Fecha de Término** (si aplica)
- **Constancia/Comprobante SNII** (si aplica - obligatorio)
  - **Formato preferente: PDF**
  - Máximo 5 MB
  - Se guarda en carpeta `formularios/constancias_snii/`
  - Nombre de archivo: `snii_[CLAVE]_[FECHA]_[HORA].pdf`

### 5. 🔗 Identificador ORCID
- **ORCID** (opcional)
  - Formato: 0000-0000-0000-0000
  - Si no tiene, puede obtenerlo en [orcid.org](https://orcid.org/)

### 6. 🔬 Líneas de Generación y Aplicación del Conocimiento
- **Mínimo 3 líneas** (obligatorio)
- **Máximo 5 líneas**
- Deben ser líneas en las que haya trabajado en los últimos 3 años

### 7. 📄 Productividad Académica 2025
- **DOIs de publicaciones 2025** (opcional)
- Tipos de publicación:
  - Artículo
  - Revista
  - Proceedings
  - Capítulo de libro
  - Libro
  - Conferencia
- Puede agregar hasta 10 publicaciones
- Formato DOI: 10.1234/ejemplo.2025.001

---

## ✨ Características del Formulario

### ✅ Validación Automática
- Campos obligatorios marcados con asterisco rojo (*)
- Validación de formato ORCID
- Validación de fechas
- Mínimo 3 líneas de investigación

### 🎨 Diseño Responsivo
- Funciona en computadoras, tablets y móviles
- Diseño moderno con colores institucionales del IPN
- Interfaz intuitiva y fácil de usar

### 💾 Guardado de Datos
Los datos se guardan de **DOS formas**:

1. **En el servidor** (carpeta `formularios/`)
   - Archivo JSON con timestamp
   - Formato: `investigador_[CLAVE]_[FECHA]_[HORA].json`

2. **Descarga automática en el navegador**
   - Se descarga un archivo JSON con los datos
   - Respaldo local inmediato

### 🔄 Campos Condicionales
- Los campos de EDI solo aparecen si selecciona "Sí tiene EDI"
- Los campos de SNII solo aparecen si selecciona "Sí tiene SNII"
- Optimiza la experiencia del usuario

### ➕ Líneas Dinámicas
- Comienza con 3 campos para líneas de investigación
- Botón "Agregar otra línea" para añadir hasta 5
- Botón de eliminar en líneas adicionales

---

## 📁 Ubicación de Datos Guardados

### Servidor (Backend)
```
DeptoInv/
└── formularios/
    ├── investigador_12345_20251012_143020.json
    ├── investigador_67890_20251012_143521.json
    ├── ...
    └── constancias_snii/
        ├── snii_12345_20251012_143020.pdf
        ├── snii_67890_20251012_143521.pdf
        └── ...
```

### Cliente (Descarga)
Los archivos se descargan en la carpeta de Descargas del usuario:
```
investigador_[CLAVE]_[TIMESTAMP].json
```

---

## 📋 Ejemplo de Datos Guardados

```json
{
  "nombreCompleto": "María Elena García López",
  "curp": "GALM850615MDFRRR01",
  "fechaNacimiento": "1985-06-15",
  "genero": "Femenino",
  "claveEmpleado": "12345",
  "categoria": "Profesor Titular A",
  "correoInstitucional": "maria.garcia@ipn.mx",
  "aceptaContacto": "Si",
  "telefonoCelular": "5512345678",
  "tieneProyectoVigente": "Si",
  "proyectosVigentes": [
    {
      "categoria": "Iniciación",
      "tipo": "Iniciación",
      "nombre": "Desarrollo de algoritmos de IA para diagnóstico médico"
    },
    {
      "categoria": "Innovación",
      "tipo": "Innovación - Profesores",
      "nombre": "Sistema de monitoreo inteligente con IoT"
    }
  ],
  "cuentaBecaEDI": "Si",
  "nivelEDI": "Nivel 2",
  "cuentaSNII": "Si",
  "nivelSNII": "Nivel I",
  "sniiInicio": "2022-01-01",
  "sniiFinal": "2026-12-31",
  "orcid": "0000-0001-2345-6789",
  "lineasInvestigacion": [
    "Inteligencia Artificial aplicada a la medicina",
    "Machine Learning para diagnóstico médico",
    "Procesamiento de imágenes médicas con Deep Learning"
  ],
  "publicaciones2025": [
    {
      "tipo": "Artículo",
      "doi": "10.1234/nature.2025.001"
    },
    {
      "tipo": "Proceedings",
      "doi": "10.5678/ieee.conf.2025.456"
    }
  ],
  "timestamp": "2025-10-12T14:30:20.123Z"
}
```

---

## 🚀 Cómo Usar el Formulario

### Paso 1: Iniciar el Sistema
```bash
python app.py
```

### Paso 2: Abrir el Formulario
1. Abre tu navegador web
2. Ve a: `http://localhost:5000/formulario`

### Paso 3: Llenar el Formulario
1. Completa todos los campos obligatorios (*)
2. Los campos condicionales aparecerán según tus respuestas
3. Agrega al menos 3 líneas de investigación

### Paso 4: Enviar
1. Clic en "✓ Enviar Formulario"
2. Espera el mensaje de confirmación verde
3. Se descargará automáticamente un archivo JSON

---

## 🔍 Consultar Datos Enviados

### Desde el Servidor
Los formularios guardados están en la carpeta `formularios/`:

```bash
# Listar todos los formularios
ls formularios/

# Ver contenido de un formulario
cat formularios/investigador_12345_20251012_143020.json
```

### Desde Python
```python
import json
import os

# Listar todos los formularios
formularios = os.listdir('formularios')
print(f"Total de formularios: {len(formularios)}")

# Leer un formulario
with open('formularios/investigador_12345_20251012_143020.json', 'r') as f:
    datos = json.load(f)
    print(f"Investigador: {datos['nombreCompleto']}")
```

---

## 📊 Exportar Datos a Excel

Puedes crear un script para exportar todos los formularios a Excel:

```python
import json
import pandas as pd
import os

# Leer todos los formularios
formularios = []
for archivo in os.listdir('formularios'):
    if archivo.endswith('.json'):
        with open(f'formularios/{archivo}', 'r') as f:
            formularios.append(json.load(f))

# Convertir a DataFrame
df = pd.DataFrame(formularios)

# Guardar en Excel
df.to_excel('formularios_investigadores.xlsx', index=False)
print("Datos exportados a formularios_investigadores.xlsx")
```

---

## 🎨 Personalización

### Cambiar Colores
Edita el archivo `static/formulario_investigador.html`:

```css
/* Color principal (Guinda IPN) */
background: linear-gradient(135deg, #6B1F3D 0%, #8B2F4D 100%);

/* Color secundario (Dorado) */
border-bottom: 3px solid #D4AF37;
```

### Agregar Más Campos
1. Abre `static/formulario_investigador.html`
2. Agrega el HTML del nuevo campo en la sección correspondiente
3. El formulario capturará automáticamente el valor

### Modificar Validaciones
En el JavaScript del formulario, puedes agregar validaciones personalizadas:

```javascript
// Ejemplo: Validar que la clave tenga 5 dígitos
const clave = data.claveEmpleado;
if (!/^\d{5}$/.test(clave)) {
    alert('La clave debe tener exactamente 5 dígitos');
    return;
}
```

---

## 🔐 Seguridad y Privacidad

### Recomendaciones:
1. **Uso Local**: Este formulario está diseñado para uso en red local del IPN
2. **No exponer a Internet**: Sin autenticación, no debe estar público
3. **Respaldo**: Los datos se guardan localmente, hacer respaldos periódicos
4. **Datos Sensibles**: Considerar cifrado para información confidencial

---

## 🆘 Solución de Problemas

### El formulario no carga
```bash
# Verificar que el servidor esté corriendo
python app.py

# Verificar en el navegador
http://localhost:5000/formulario
```

### No se guardan los datos
```bash
# Verificar permisos de escritura
# La carpeta 'formularios' se crea automáticamente

# Ver logs del servidor
# Los mensajes aparecen en la consola donde ejecutaste python app.py
```

### Error al descargar JSON
- Verifica que tu navegador permita descargas
- Revisa la configuración de seguridad del navegador

---

## 📞 Contacto y Soporte

Para dudas o soporte sobre el formulario, contacte al:

**Departamento de Investigación - UPIIZ**  
Jefe de Departamento: M. en C. Rafael Reveles Martínez  
Unidad Profesional Interdisciplinaria de Ingeniería  
Campus Zacatecas  
Instituto Politécnico Nacional

**📧 Correo:** investigacion_UPIIZ@ipn.mx  
**📞 Extensión:** 83530  
**🌐 Sitio Web:** [https://www.zacatecas.ipn.mx/](https://www.zacatecas.ipn.mx/)

---

## 📝 Licencia

Sistema desarrollado para el Instituto Politécnico Nacional

**La Técnica al Servicio de la Patria**

---

## 🎓 UPIIZ - Instituto Politécnico Nacional

**Unidad Profesional Interdisciplinaria de Ingeniería**  
**Campus Zacatecas - UPIIZ**  
Instituto Politécnico Nacional

Sistema de Gestión de Investigación  
Formulario de Registro de Investigadores  

**Jefe del Departamento de Investigación:**  
M. en C. Rafael Reveles Martínez

**La Técnica al Servicio de la Patria**

© 2025

