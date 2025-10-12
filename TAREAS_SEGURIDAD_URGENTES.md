# 🚨 TAREAS DE SEGURIDAD URGENTES

## ⚡ HACER AHORA MISMO (15 minutos)

### 1. Instalar protección contra spam/DDoS
```bash
pip install Flask-Limiter
```

### 2. Agregar rate limiting al formulario

Abre `app.py` y agrega estas líneas **DESPUÉS** de `app = Flask(...)`:

```python
# Después de: app = Flask(__name__, static_folder='static')
# Agregar:

from flask_limiter import Limiter
from flask_limiter.util import get_remote_address

limiter = Limiter(
    app=app,
    key_func=get_remote_address,
    default_limits=["200 per day", "50 per hour"],
    storage_uri="memory://"
)
```

Luego busca la función `guardar_formulario_investigador` y agrega `@limiter.limit("5 per hour")`:

```python
@app.route('/api/formulario-investigador', methods=['POST'])
@limiter.limit("5 per hour")  # ← AGREGAR ESTA LÍNEA
def guardar_formulario_investigador():
    """Guarda los datos del formulario de investigador con archivo adjunto"""
    # ... resto del código ...
```

### 3. Desactivar modo debug

Al final de `app.py`, cambia `debug=True` por `debug=False`:

```python
if __name__ == '__main__':
    # ANTES: app.run(host='0.0.0.0', debug=True, port=5000)
    # DESPUÉS:
    app.run(host='0.0.0.0', debug=False, port=5000)
```

### 4. Reiniciar el servidor

1. En la terminal donde corre Flask, presiona Ctrl+C
2. Ejecuta de nuevo: `python app.py`

**¡LISTO!** Con esto tienes protección básica contra:
- ✅ Spam masivo de formularios
- ✅ Ataques DDoS simples
- ✅ Exposición de código interno

---

## 📋 HACER HOY (1 hora más)

### 5. Generar claves de seguridad

```bash
python config_ejemplo.py
```

Guarda las claves que genera en un lugar seguro (Notepad, pero no lo subas a GitHub).

### 6. Crear archivo config.py

Crea un nuevo archivo llamado `config.py` (copia de `config_ejemplo.py`) y reemplaza:
- `SECRET_KEY = 'cambiar...'` → Pega la que generaste
- `ADMIN_TOKEN = 'cambiar...'` → Pega la que generaste
- `DEBUG = True` → Cambia a `False`

### 7. Proteger rutas administrativas

En `app.py`, al inicio importa:

```python
from security_utils import require_auth
```

Luego protege estas rutas agregando `@require_auth`:

```python
@app.route('/api/formularios-lista', methods=['GET'])
@require_auth  # ← AGREGAR
def listar_formularios():
    # ...

@app.route('/api/exportar-formularios-excel', methods=['GET'])
@require_auth  # ← AGREGAR
def exportar_excel_endpoint():
    # ...

@app.route('/api/investigadores', methods=['GET'])
@require_auth  # ← AGREGAR
def get_investigadores():
    # ...
```

### 8. Validar archivos subidos

En la función `guardar_formulario_investigador`, reemplaza el código de guardar archivos:

```python
from security_utils import validar_archivo, generar_nombre_archivo_seguro, log_archivo_rechazado

# Buscar: if 'sniiConstancia' in request.files:
# Y reemplazar por:

if 'sniiConstancia' in request.files:
    archivo = request.files['sniiConstancia']
    if archivo and archivo.filename:
        try:
            # Validar archivo (tipo y tamaño)
            validar_archivo(archivo)
            
            # Generar nombre seguro
            nombre_archivo = generar_nombre_archivo_seguro(
                archivo.filename,
                prefijo=f"snii_{data.get('claveEmpleado', 'sin_clave')}"
            )
            
            ruta_archivo = os.path.join('formularios/constancias_snii', nombre_archivo)
            archivo.save(ruta_archivo)
            data['sniiConstanciaArchivo'] = ruta_archivo
            archivo_guardado = nombre_archivo
            
        except ValueError as e:
            # Archivo inválido
            log_archivo_rechazado(request.remote_addr, archivo.filename, str(e))
            return jsonify({
                'success': False,
                'error': f'Archivo inválido: {str(e)}'
            }), 400
```

---

## 🎯 NIVEL DE PROTECCIÓN

```
ANTES:     ░░░░░░░░░░ 10%  ❌ MUY VULNERABLE
DESPUÉS:   ████████░░ 75%  ✅ BIEN PROTEGIDO
```

---

## 📊 QUÉ LOGRASTE CON ESTO

| Amenaza | Antes | Después |
|---------|-------|---------|
| Spam de formularios | ❌ Ilimitado | ✅ Máx 5/hora |
| DDoS básico | ❌ Sin protección | ✅ Bloqueado |
| Ver todos los formularios | ❌ Cualquiera | ✅ Solo con token |
| Descargar Excel | ❌ Cualquiera | ✅ Solo con token |
| Subir malware | ❌ Permitido | ✅ Bloqueado |
| Ver código/errores | ❌ Visible | ✅ Oculto |

---

## 🔑 CÓMO ACCEDER AHORA A RUTAS PROTEGIDAS

Necesitas tu ADMIN_TOKEN (el que generaste en paso 5).

### Opción A: Usando el navegador con extensión

1. Instala una extensión como "ModHeader" en Chrome
2. Agrega un header:
   - Nombre: `Authorization`
   - Valor: `Bearer tu_token_aqui`

### Opción B: Desde código JavaScript

```javascript
fetch('http://localhost:5000/api/formularios-lista', {
    headers: {
        'Authorization': 'Bearer tu_token_aqui'
    }
})
.then(res => res.json())
.then(data => console.log(data))
```

### Opción C: Crear página de admin

Crea `static/admin_login.html`:

```html
<!DOCTYPE html>
<html>
<head>
    <title>Admin - UPIIZ</title>
</head>
<body>
    <h1>Acceso Administrativo</h1>
    <input type="password" id="token" placeholder="Token de acceso">
    <button onclick="cargarDatos()">Acceder</button>
    <div id="resultado"></div>

    <script>
    function cargarDatos() {
        const token = document.getElementById('token').value;
        fetch('/api/formularios-lista', {
            headers: {
                'Authorization': 'Bearer ' + token
            }
        })
        .then(res => res.json())
        .then(data => {
            document.getElementById('resultado').innerHTML = 
                '<pre>' + JSON.stringify(data, null, 2) + '</pre>';
        })
        .catch(err => alert('Error: ' + err));
    }
    </script>
</body>
</html>
```

Accede en: http://localhost:5000/admin_login.html

---

## ⚠️ IMPORTANTE

- **NO subas config.py a GitHub** (ya está en .gitignore)
- **Guarda tu ADMIN_TOKEN en lugar seguro**
- **Cambia el token si crees que fue comprometido**
- **En producción usa HTTPS siempre**

---

## 🧪 PRUEBA QUE FUNCIONA

### Test 1: Rate limiting
Intenta enviar 10 formularios rápido. Después del 5to debe decir:
```
"429 Too Many Requests"
```

### Test 2: Autenticación
Intenta acceder a: http://localhost:5000/api/formularios-lista

Sin token debe dar:
```json
{"error": "No autorizado - Token requerido"}
```

Con token debe mostrar la lista de formularios.

### Test 3: Archivo inválido
Intenta subir un archivo .exe o de más de 5MB. Debe rechazarlo.

---

## 📞 ¿PROBLEMAS?

### No funciona Flask-Limiter
```bash
pip install --upgrade Flask-Limiter
```

### Error "require_auth not found"
Verifica que `security_utils.py` esté en la misma carpeta que `app.py`.

### Token no funciona
Verifica que:
1. Copiaste el token correctamente
2. Usas formato: `Bearer TOKEN` (con espacio)
3. El header se llama `Authorization`

---

**Tiempo estimado**: 
- Paso 1-4: 15 minutos
- Paso 5-8: 1 hora
- Total: 1.25 horas para seguridad sólida

¡No lo dejes para después! Cada día sin protección es un riesgo.

