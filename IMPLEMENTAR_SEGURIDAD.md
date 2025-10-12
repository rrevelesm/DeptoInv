# 🛡️ Cómo Implementar Seguridad en tu Sistema

## 📋 PASO A PASO - Implementación Inmediata

### PASO 1: Instalar Dependencias de Seguridad

```bash
# En la terminal de tu proyecto:
pip install Flask-Limiter python-dotenv
```

### PASO 2: Generar Claves Seguras

```bash
# Ejecuta este comando para generar tus claves:
python config_ejemplo.py
```

Guarda las claves generadas en un lugar seguro (NO las subas a GitHub).

### PASO 3: Crear archivo de configuración

Crea un archivo llamado `config.py` (copia de `config_ejemplo.py`) y reemplaza las claves:

```python
# config.py
SECRET_KEY = 'la_clave_que_generaste_en_paso_2'
ADMIN_TOKEN = 'el_token_que_generaste_en_paso_2'
DEBUG = False  # False en producción
```

**IMPORTANTE**: Agrega `config.py` al `.gitignore`:

```bash
echo config.py >> .gitignore
```

### PASO 4: Agregar Rate Limiting al app.py

Agrega estas líneas al inicio de tu `app.py`:

```python
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address

# Después de crear app = Flask(...)
limiter = Limiter(
    app=app,
    key_func=get_remote_address,
    default_limits=["200 per day", "50 per hour"],
    storage_uri="memory://"
)
```

Luego protege la ruta del formulario:

```python
@app.route('/api/formulario-investigador', methods=['POST'])
@limiter.limit("5 per hour")  # Solo 5 formularios por hora por IP
def guardar_formulario_investigador():
    # ... tu código actual ...
```

### PASO 5: Agregar Validación de Archivos

Reemplaza el código de guardar archivos en `app.py`:

```python
from security_utils import validar_archivo, generar_nombre_archivo_seguro, log_archivo_rechazado

# En la función guardar_formulario_investigador():
if 'sniiConstancia' in request.files:
    archivo = request.files['sniiConstancia']
    if archivo and archivo.filename:
        try:
            # Validar archivo
            validar_archivo(archivo)
            
            # Generar nombre seguro
            nombre_archivo = generar_nombre_archivo_seguro(
                archivo.filename,
                prefijo=f"snii_{data.get('claveEmpleado', 'sin_clave')}"
            )
            
            # Guardar
            ruta_archivo = os.path.join('formularios/constancias_snii', nombre_archivo)
            archivo.save(ruta_archivo)
            data['sniiConstanciaArchivo'] = ruta_archivo
            
        except ValueError as e:
            log_archivo_rechazado(request.remote_addr, archivo.filename, str(e))
            return jsonify({'success': False, 'error': str(e)}), 400
```

### PASO 6: Proteger Rutas Administrativas

Para rutas como `/api/investigadores`, `/api/formularios-lista`, etc.:

```python
from security_utils import require_auth

@app.route('/api/formularios-lista', methods=['GET'])
@require_auth  # ← Agregar esta línea
def listar_formularios():
    # ... tu código actual ...
```

### PASO 7: Cambiar DEBUG Mode

En `app.py`, al final:

```python
if __name__ == '__main__':
    # Desarrollo local:
    # app.run(host='0.0.0.0', debug=True, port=5000)
    
    # Producción:
    import os
    DEBUG_MODE = os.environ.get('DEBUG', 'False').lower() == 'true'
    app.run(host='0.0.0.0', debug=DEBUG_MODE, port=5000)
```

### PASO 8: Agregar SECRET_KEY

Al inicio de `app.py`, después de crear la app:

```python
import os

app = Flask(__name__, static_folder='static')

# Agregar SECRET_KEY
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'clave-temporal-desarrollo')
```

---

## 🔐 PROTECCIÓN AVANZADA (Opcional pero Recomendado)

### Validar Datos del Formulario

```python
from security_utils import validar_datos_investigador, sanitizar_datos_formulario

@app.route('/api/formulario-investigador', methods=['POST'])
@limiter.limit("5 per hour")
def guardar_formulario_investigador():
    try:
        datos_json = request.form.get('datos')
        data = json.loads(datos_json) if datos_json else {}
        
        # Validar datos
        es_valido, errores = validar_datos_investigador(data)
        if not es_valido:
            return jsonify({
                'success': False,
                'error': 'Datos inválidos',
                'detalles': errores
            }), 400
        
        # Sanitizar datos
        data = sanitizar_datos_formulario(data)
        
        # ... continuar con tu código actual ...
```

### Configurar CORS Restrictivo

Reemplaza `CORS(app)` por:

```python
from flask_cors import CORS

CORS(app, resources={
    r"/api/*": {
        "origins": [
            "http://127.0.0.1:5000",
            "http://192.168.0.6:5000"
            # Agregar tu dominio de producción
        ],
        "methods": ["GET", "POST"],
        "allow_headers": ["Content-Type", "Authorization"]
    }
})
```

---

## 🔑 CÓMO USAR EL TOKEN DE ADMIN

Para acceder a rutas protegidas desde el navegador o Postman:

1. En el **header** de la petición:
   ```
   Authorization: Bearer tu_token_admin_aqui
   ```

2. Ejemplo con JavaScript:
   ```javascript
   fetch('http://localhost:5000/api/formularios-lista', {
       headers: {
           'Authorization': 'Bearer tu_token_admin_aqui'
       }
   })
   ```

3. Ejemplo con curl:
   ```bash
   curl -H "Authorization: Bearer tu_token_admin_aqui" \
        http://localhost:5000/api/formularios-lista
   ```

---

## ⚠️ IMPORTANTES - NO OLVIDAR

### 1. Agregar al .gitignore

```
# .gitignore
config.py
.env
logs/
*.log
__pycache__/
*.pyc
*.db
formularios/*.json
formularios/constancias_snii/*
```

### 2. Variables de Entorno en PythonAnywhere

Cuando subas a producción, configura las variables:

1. Ve a la pestaña "Web"
2. Busca "Environment variables"
3. Agrega:
   - `SECRET_KEY`: tu_clave_secreta
   - `ADMIN_TOKEN`: tu_token_admin
   - `DEBUG`: False

### 3. Crear carpeta de logs

```bash
mkdir logs
```

---

## 🧪 PROBAR LA SEGURIDAD

### Test 1: Rate Limiting
```bash
# Intenta enviar 10 formularios rápido (debe bloquear después de 5)
for i in {1..10}; do
  curl -X POST http://localhost:5000/api/formulario-investigador
  echo "Intento $i"
  sleep 1
done
```

### Test 2: Autenticación
```bash
# Sin token (debe fallar)
curl http://localhost:5000/api/formularios-lista

# Con token (debe funcionar)
curl -H "Authorization: Bearer tu_token" \
     http://localhost:5000/api/formularios-lista
```

### Test 3: Archivo Inválido
Intenta subir un archivo .exe o muy grande (debe rechazar).

---

## 📊 MONITOREO

### Ver logs de seguridad:
```bash
# Windows
type logs\seguridad.log

# Linux/Mac
cat logs/seguridad.log

# Ver solo las últimas 20 líneas
tail -20 logs/seguridad.log
```

### Buscar intentos de acceso denegado:
```bash
# Windows
findstr "ACCESO DENEGADO" logs\seguridad.log

# Linux/Mac
grep "ACCESO DENEGADO" logs/seguridad.log
```

---

## 🚨 CHECKLIST PRE-PRODUCCIÓN

Antes de desplegar en PythonAnywhere o servidor público:

- [ ] SECRET_KEY configurado y único
- [ ] ADMIN_TOKEN configurado y seguro
- [ ] DEBUG = False
- [ ] Rate limiting activo
- [ ] Validación de archivos implementada
- [ ] Rutas admin protegidas con @require_auth
- [ ] CORS configurado restrictivamente
- [ ] Logs funcionando
- [ ] .gitignore actualizado
- [ ] Variables de entorno en servidor
- [ ] Backup de base de datos configurado

---

## 🆘 SOLUCIÓN DE PROBLEMAS

### Error: "No module named 'flask_limiter'"
```bash
pip install Flask-Limiter
```

### Error: "ADMIN_TOKEN not set"
Crea el archivo `config.py` con tu token.

### Los logs no se crean
```bash
mkdir logs
```

### Rate limit muy estricto en desarrollo
Cambiar a: `@limiter.limit("20 per hour")` durante pruebas

---

## 📞 CONTACTO DE EMERGENCIA

Si detectas un ataque o brecha de seguridad:

1. Detén el servidor inmediatamente
2. Revisa los logs: `logs/seguridad.log`
3. Cambia ADMIN_TOKEN y SECRET_KEY
4. Analiza los archivos JSON en `formularios/`
5. Verifica la base de datos

---

**Última actualización**: 12 de octubre de 2025
**Nivel de protección**: Básico → Intermedio

