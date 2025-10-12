# 📊 Guía de Importación de Datos desde Excel

## Sistema de Gestión de Investigación - IPN

Esta guía explica cómo importar datos desde archivos Excel al sistema.

---

## ✅ Importación Completada

Se han importado exitosamente **37 proyectos** del archivo `Proyectos 2025 Investigación.xlsx` al sistema.

### Datos Importados:
- **37 Proyectos de Investigación SIP 2025**
- Claves SIP
- Títulos completos
- Investigadores responsables y participantes
- Tipos de investigación
- Información de alumnos participantes

---

## 🔧 Cómo Importar Más Datos

### Requisitos
```bash
pip install pandas openpyxl
```

### Para Importar Proyectos

El archivo debe tener las siguientes columnas:
- `Clave SIP`: Número de proyecto
- `Título`: Título del proyecto
- `Investigador`: Nombre del investigador responsable
- `Proyecto`: Tipo de proyecto
- `Corto plazo`: Objetivos a corto plazo
- `Mediano plazo`: Objetivos a mediano plazo
- `Tipo de investigación`: Clasificación
- `Investigadores participantes`: Lista de investigadores
- `Alumnos participantes`: Lista de alumnos

**Comando:**
```bash
python importar_proyectos_final.py
```

---

## 📝 Crear Scripts de Importación Personalizados

### Ejemplo: Importar Investigadores

```python
import pandas as pd
from models import get_session, Investigador

def importar_investigadores(archivo):
    df = pd.read_excel(archivo)
    session = get_session()
    
    for _, row in df.iterrows():
        investigador = Investigador(
            nombre=row['Nombre'],
            apellido_paterno=row['Apellido Paterno'],
            apellido_materno=row['Apellido Materno'],
            email=row['Email'],
            especialidad=row['Especialidad'],
            grado_academico=row['Grado'],
            estatus="Activo"
        )
        session.add(investigador)
    
    session.commit()
    session.close()
```

### Ejemplo: Importar Publicaciones

```python
import pandas as pd
from models import get_session, Publicacion

def importar_publicaciones(archivo):
    df = pd.read_excel(archivo)
    session = get_session()
    
    for _, row in df.iterrows():
        publicacion = Publicacion(
            titulo=row['Título'],
            tipo=row['Tipo'],
            revista_editorial=row['Revista'],
            anio=row['Año'],
            doi=row['DOI'],
            issn_isbn=row['ISSN/ISBN']
        )
        session.add(publicacion)
    
    session.commit()
    session.close()
```

---

## 🗄️ Formato de Archivos Excel Recomendado

### Investigadores
| Nombre | Apellido Paterno | Apellido Materno | Email | Especialidad | Grado |
|--------|------------------|------------------|-------|--------------|-------|
| Juan | Pérez | López | juan.perez@ipn.mx | IA | Doctorado |

### Proyectos
| Título | Descripción | Tipo | Financiamiento | Monto | Fecha Inicio | Fecha Fin |
|--------|-------------|------|----------------|-------|--------------|-----------|
| Proyecto 1 | Desc... | Investigación | CONACYT | 1000000 | 2025-01-01 | 2025-12-31 |

### Publicaciones
| Título | Tipo | Revista | Año | DOI | ISSN |
|--------|------|---------|-----|-----|------|
| Artículo 1 | Artículo | Nature | 2025 | 10.xxx | 1234-5678 |

### SNII
| Investigador ID | Nivel | Fecha Ingreso | Fecha Vigencia | Estatus |
|-----------------|-------|---------------|----------------|---------|
| 1 | Nivel II | 2020-01-01 | 2026-12-31 | Vigente |

---

## 🔍 Verificación de Datos

Después de importar, verifica los datos en el sistema web:

1. Abre http://localhost:5000
2. Navega a la pestaña correspondiente (Investigadores, Proyectos, etc.)
3. Usa la función de búsqueda para encontrar registros específicos
4. Verifica que todos los datos se hayan importado correctamente

---

## ⚠️ Consideraciones Importantes

1. **Duplicados**: El script verifica títulos duplicados en proyectos
2. **Investigadores**: Si no existe, se crea automáticamente
3. **Encoding**: Los archivos se procesan con UTF-8
4. **Errores**: Se muestran en consola con número de fila
5. **Backup**: Respalda la base de datos antes de importaciones grandes

---

## 🆘 Solución de Problemas

### Error: "No se puede leer el archivo"
```bash
# Verifica que el archivo existe
dir "Proyectos 2025 Investigación.xlsx"

# Verifica que pandas esté instalado
pip install pandas openpyxl
```

### Error: "Columna no encontrada"
- Verifica que los nombres de las columnas coincidan exactamente
- Revisa mayúsculas, minúsculas y acentos
- Asegúrate de que no haya espacios extras

### Error: "Clave foránea no válida"
- Asegúrate de que los investigadores existan antes de importar proyectos
- Verifica los IDs de las relaciones

---

## 📞 Soporte

Para más información sobre el sistema, consulta el archivo `README.md`.

---

**Instituto Politécnico Nacional**  
*La Técnica al Servicio de la Patria*

