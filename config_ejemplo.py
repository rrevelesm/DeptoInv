# 🔒 CONFIGURACIÓN DE SEGURIDAD - Ejemplo
# Copia este archivo como config.py y cambia los valores
# NUNCA subas config.py a GitHub (agregarlo a .gitignore)

import os
import secrets

class Config:
    """Configuración base del sistema"""
    
    # Generar nueva SECRET_KEY: python -c "import secrets; print(secrets.token_hex(32))"
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'cambiar_por_clave_secreta_generada'
    
    # Generar nuevo ADMIN_TOKEN: python -c "import secrets; print(secrets.token_urlsafe(32))"
    ADMIN_TOKEN = os.environ.get('ADMIN_TOKEN') or 'cambiar_por_token_admin_generado'
    
    # Base de datos
    DATABASE_URL = os.environ.get('DATABASE_URL') or 'sqlite:///depto_investigacion.db'
    
    # Modo debug (SIEMPRE False en producción)
    DEBUG = os.environ.get('DEBUG', 'False').lower() == 'true'
    
    # CORS - Orígenes permitidos
    ALLOWED_ORIGINS = [
        'http://127.0.0.1:5000',
        'http://localhost:5000',
        'http://192.168.0.6:5000',
        # Agregar tu dominio de producción aquí
        # 'https://tudominio.pythonanywhere.com'
    ]
    
    # Rate limiting
    RATE_LIMIT_FORMULARIO = '5 per hour'  # Máximo 5 formularios por hora por IP
    RATE_LIMIT_API = '100 per hour'       # Máximo 100 peticiones API por hora
    RATE_LIMIT_DOWNLOAD = '10 per hour'   # Máximo 10 descargas por hora
    
    # Archivos subidos
    MAX_FILE_SIZE_MB = 5
    MAX_FILE_SIZE = MAX_FILE_SIZE_MB * 1024 * 1024  # En bytes
    ALLOWED_EXTENSIONS = {'pdf', 'jpg', 'jpeg', 'png'}
    UPLOAD_FOLDER = 'formularios/constancias_snii'
    
    # Email (opcional)
    ADMIN_EMAIL = 'tu_email@upiiz.ipn.mx'
    
    # Logging
    LOG_FILE = 'logs/seguridad.log'
    LOG_LEVEL = 'WARNING'


class DevelopmentConfig(Config):
    """Configuración para desarrollo local"""
    DEBUG = True
    RATE_LIMIT_FORMULARIO = '20 per hour'  # Más permisivo para pruebas


class ProductionConfig(Config):
    """Configuración para producción"""
    DEBUG = False
    # En producción, SECRET_KEY y ADMIN_TOKEN DEBEN venir de variables de entorno
    # SECRET_KEY = os.environ.get('SECRET_KEY')  # Obligatorio
    # ADMIN_TOKEN = os.environ.get('ADMIN_TOKEN')  # Obligatorio


# Seleccionar configuración según entorno
config = {
    'development': DevelopmentConfig,
    'production': ProductionConfig,
    'default': DevelopmentConfig
}


# Función helper para generar tokens
def generar_secret_key():
    """Genera una SECRET_KEY segura"""
    return secrets.token_hex(32)


def generar_admin_token():
    """Genera un ADMIN_TOKEN seguro"""
    return secrets.token_urlsafe(32)


if __name__ == '__main__':
    print("🔐 Generador de Claves Seguras")
    print("="*50)
    print(f"SECRET_KEY:  {generar_secret_key()}")
    print(f"ADMIN_TOKEN: {generar_admin_token()}")
    print("="*50)
    print("⚠️  Guarda estas claves en un lugar seguro")
    print("⚠️  NO las compartas ni las subas a GitHub")

