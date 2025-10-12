# 🔒 Guía de Seguridad - Sistema de Gestión de Investigadores UPIIZ

## ⚠️ VULNERABILIDADES ACTUALES IDENTIFICADAS

### 🔴 CRÍTICAS (Resolver INMEDIATAMENTE)

1. **Sin Autenticación en Rutas Administrativas**
   - ❌ `/api/investigadores` - Cualquiera puede ver/modificar/eliminar
   - ❌ `/api/formularios-lista` - Información sensible expuesta
   - ❌ `/api/exportar-formularios-excel` - Descarga de datos sin restricción
   - 🎯 **Impacto**: Robo masivo de datos personales, CURP, teléfonos, etc.

2. **CORS Completamente Abierto**
   - ❌ `CORS(app)` permite peticiones desde CUALQUIER dominio
   - 🎯 **Impacto**: Sitios maliciosos pueden hacer peticiones a tu API

3. **Debug Mode en Producción**
   - ❌ `debug=True` expone stack traces, rutas internas, código
   - 🎯 **Impacto**: Atacantes ven estructura interna del sistema

4. **Sin Validación de Archivos Subidos**
   - ❌ No verifica tipo, tamaño, contenido de archivos
   - 🎯 **Impacto**: Pueden subir malware, scripts maliciosos, archivos gigantes

5. **Sin Rate Limiting**
   - ❌ Sin límite de peticiones por IP
   - 🎯 **Impacto**: Ataques DDoS, fuerza bruta, spam masivo

### 🟡 ALTAS (Resolver pronto)

6. **Sin CSRF Protection**
   - Formularios sin token de protección
   - 🎯 **Impacto**: Ataques de falsificación de peticiones

7. **Sin SECRET_KEY**
   - Flask necesita SECRET_KEY para sesiones seguras
   - 🎯 **Impacto**: Sesiones predecibles, fáciles de falsificar

8. **Datos Sensibles sin Encriptar**
   - CURP, teléfonos, emails en texto plano en JSON
   - 🎯 **Impacto**: Violación de privacidad si hay fuga

9. **Sin HTTPS**
   - Datos viajan sin cifrar por la red
   - 🎯 **Impacto**: Interceptación de datos (man-in-the-middle)

10. **Ruta Estática Insegura**
    - `/<path:path>` puede exponer archivos no deseados
    - 🎯 **Impacto**: Acceso a archivos del sistema

---

## 🛡️ SOLUCIONES IMPLEMENTADAS

### 1. Sistema de Autenticación

```python
# Protección con autenticación básica
from functools import wraps
from flask import request, jsonify
import secrets

# Generar token de acceso (guardar en variable de entorno)
ADMIN_TOKEN = "tu_token_super_secreto_aqui"

def require_auth(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        token = request.headers.get('Authorization')
        if not token or token != f"Bearer {ADMIN_TOKEN}":
            return jsonify({'error': 'No autorizado'}), 401
        return f(*args, **kwargs)
    return decorated_function

# Aplicar a rutas sensibles:
@app.route('/api/investigadores', methods=['GET'])
@require_auth
def get_investigadores():
    # ...
```

### 2. CORS Restringido

```python
from flask_cors import CORS

# Solo permitir tu dominio
CORS(app, resources={
    r"/api/*": {
        "origins": ["http://127.0.0.1:5000", "http://192.168.0.6:5000"],
        "methods": ["GET", "POST"],
        "allow_headers": ["Content-Type", "Authorization"]
    }
})
```

### 3. Rate Limiting

```python
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address

limiter = Limiter(
    app=app,
    key_func=get_remote_address,
    default_limits=["200 per day", "50 per hour"],
    storage_uri="memory://"
)

@app.route('/api/formulario-investigador', methods=['POST'])
@limiter.limit("5 per hour")  # Solo 5 formularios por hora por IP
def guardar_formulario_investigador():
    # ...
```

### 4. Validación de Archivos

```python
ALLOWED_EXTENSIONS = {'pdf', 'jpg', 'jpeg', 'png'}
MAX_FILE_SIZE = 5 * 1024 * 1024  # 5 MB

def archivo_permitido(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def validar_archivo(archivo):
    # Verificar extensión
    if not archivo_permitido(archivo.filename):
        raise ValueError("Solo se permiten archivos PDF, JPG o PNG")
    
    # Verificar tamaño
    archivo.seek(0, os.SEEK_END)
    size = archivo.tell()
    archivo.seek(0)
    if size > MAX_FILE_SIZE:
        raise ValueError("El archivo excede el tamaño máximo de 5MB")
    
    return True
```

### 5. Variables de Entorno

```python
# Crear archivo .env (NO subir a GitHub)
SECRET_KEY=tu_clave_super_secreta_aqui
ADMIN_TOKEN=token_de_acceso_admin
DATABASE_URL=sqlite:///depto_investigacion.db
DEBUG=False
ALLOWED_ORIGINS=http://localhost:5000,http://192.168.0.6:5000
```

```python
# En app.py
from dotenv import load_dotenv
import os

load_dotenv()

app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')
DEBUG_MODE = os.getenv('DEBUG', 'False').lower() == 'true'
```

### 6. Input Validation

```python
from flask import request
import re

def validar_curp(curp):
    patron = r'^[A-Z]{4}\d{6}[HM][A-Z]{5}[A-Z0-9]\d$'
    return re.match(patron, curp) is not None

def validar_email(email):
    patron = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return re.match(patron, email) is not None

def limpiar_input(texto):
    # Remover caracteres peligrosos
    return re.sub(r'[<>\"\';&|]', '', texto)
```

### 7. Logging de Seguridad

```python
import logging
from datetime import datetime

# Configurar logging
logging.basicConfig(
    filename='logs/seguridad.log',
    level=logging.WARNING,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

def log_acceso_sospechoso(ip, ruta, razon):
    logging.warning(f"IP: {ip} | Ruta: {ruta} | Razón: {razon}")
```

### 8. HTTPS (Para Producción)

```bash
# Usar Nginx como proxy reverso con SSL
# O en PythonAnywhere automáticamente tienes HTTPS
```

---

## 📋 CHECKLIST DE IMPLEMENTACIÓN

### Inmediato (Hoy mismo)
- [ ] Agregar autenticación a rutas administrativas
- [ ] Configurar CORS restrictivo
- [ ] Cambiar `debug=False` en producción
- [ ] Validar archivos subidos
- [ ] Agregar rate limiting al formulario

### Esta Semana
- [ ] Implementar SECRET_KEY
- [ ] Crear archivo .env para secretos
- [ ] Agregar validación de entrada (CURP, email, etc.)
- [ ] Implementar logging de seguridad
- [ ] Limitar ruta estática

### Antes de Producción
- [ ] Habilitar HTTPS
- [ ] Encriptar datos sensibles en DB
- [ ] Implementar CSRF protection
- [ ] Hacer backup automático de datos
- [ ] Implementar monitoreo de actividad sospechosa

---

## 🚨 RECOMENDACIONES DE DESPLIEGUE

### Para Desarrollo (Local)
```python
if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True, port=5000)
```

### Para Producción (PythonAnywhere)
```python
if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=False, port=5000)
```

O usar servidor WSGI como Gunicorn:
```bash
gunicorn --bind 0.0.0.0:5000 --workers 4 app:app
```

---

## 📊 MONITOREO Y ALERTAS

### Qué Monitorear
1. Intentos de acceso no autorizado
2. Múltiples peticiones desde misma IP
3. Archivos con extensiones sospechosas
4. Peticiones a rutas que no existen
5. Errores 500 frecuentes

### Herramientas
- **Fail2Ban**: Bloquea IPs con comportamiento sospechoso
- **Sentry**: Monitoreo de errores en tiempo real
- **CloudFlare**: Protección DDoS y firewall

---

## 🔐 BUENAS PRÁCTICAS

1. **Nunca expongas credenciales en código**
   - Usa variables de entorno
   - Archivo `.env` en `.gitignore`

2. **Principio de mínimo privilegio**
   - Usuarios solo acceden a lo que necesitan
   - Panel admin separado del formulario público

3. **Validar todo input del usuario**
   - Nunca confíes en datos del frontend
   - Valida en servidor siempre

4. **Mantén dependencias actualizadas**
   ```bash
   pip list --outdated
   pip install --upgrade nombre_paquete
   ```

5. **Backups regulares**
   - Base de datos diaria
   - Formularios guardados en múltiples lugares

6. **Revisar logs regularmente**
   - Detectar patrones de ataque
   - Identificar vulnerabilidades

---

## 📞 EN CASO DE ATAQUE

### Si detectas actividad sospechosa:

1. **Detén el servidor** inmediatamente
   ```bash
   # Buscar proceso Python
   tasklist | findstr python
   # Matar proceso
   taskkill /F /PID [número_proceso]
   ```

2. **Revisa los logs**
   - `logs/seguridad.log`
   - Logs del servidor

3. **Cambia credenciales**
   - Tokens de acceso
   - Contraseñas de admin

4. **Analiza daños**
   - ¿Se modificó la base de datos?
   - ¿Se accedió a archivos sensibles?
   - ¿Se descargó información?

5. **Reporta el incidente**
   - Documenta fecha, hora, tipo de ataque
   - Notifica a autoridades si hay robo de datos

---

## 📚 RECURSOS ADICIONALES

- [OWASP Top 10](https://owasp.org/www-project-top-ten/) - Vulnerabilidades web más críticas
- [Flask Security](https://flask.palletsprojects.com/en/2.3.x/security/)
- [Python Security Best Practices](https://python.readthedocs.io/en/stable/library/security_warnings.html)

---

**Última actualización**: 12 de octubre de 2025
**Responsable**: Departamento de Investigación UPIIZ

