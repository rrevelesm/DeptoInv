# 🔒 Utilidades de Seguridad
# Funciones para proteger el sistema contra ataques

import re
import os
import logging
from functools import wraps
from flask import request, jsonify
from datetime import datetime
from werkzeug.utils import secure_filename

# Configurar logging de seguridad
if not os.path.exists('logs'):
    os.makedirs('logs')

logging.basicConfig(
    filename='logs/seguridad.log',
    level=logging.WARNING,
    format='%(asctime)s - %(levelname)s - %(message)s'
)


# ============== AUTENTICACIÓN ==============

def require_auth(f):
    """Decorador para requerir autenticación en rutas protegidas"""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        # Obtener token del header
        auth_header = request.headers.get('Authorization')
        
        if not auth_header:
            log_acceso_denegado(request.remote_addr, request.path, "Sin token")
            return jsonify({'error': 'No autorizado - Token requerido'}), 401
        
        # Verificar formato "Bearer TOKEN"
        try:
            scheme, token = auth_header.split()
            if scheme.lower() != 'bearer':
                raise ValueError
        except ValueError:
            log_acceso_denegado(request.remote_addr, request.path, "Formato inválido")
            return jsonify({'error': 'Formato de autenticación inválido'}), 401
        
        # Verificar token (cargar desde config o variable de entorno)
        ADMIN_TOKEN = os.environ.get('ADMIN_TOKEN', 'token_temporal_desarrollo')
        if token != ADMIN_TOKEN:
            log_acceso_denegado(request.remote_addr, request.path, "Token inválido")
            return jsonify({'error': 'Token inválido'}), 401
        
        return f(*args, **kwargs)
    return decorated_function


# ============== VALIDACIÓN DE ENTRADA ==============

def validar_curp(curp):
    """Valida formato de CURP mexicana"""
    if not curp or len(curp) != 18:
        return False
    patron = r'^[A-Z]{4}\d{6}[HM][A-Z]{5}[A-Z0-9]\d$'
    return re.match(patron, curp.upper()) is not None


def validar_email(email):
    """Valida formato de email"""
    if not email:
        return False
    patron = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return re.match(patron, email) is not None


def validar_telefono(telefono):
    """Valida formato de teléfono (10 dígitos)"""
    if not telefono:
        return False
    patron = r'^\d{10}$'
    return re.match(patron, telefono) is not None


def limpiar_input(texto):
    """Elimina caracteres peligrosos de entrada de usuario"""
    if not texto:
        return ""
    # Remover caracteres que pueden usarse para inyección
    texto_limpio = re.sub(r'[<>\"\';&|`$]', '', str(texto))
    return texto_limpio.strip()


def validar_doi(doi):
    """Valida formato básico de DOI"""
    if not doi:
        return False
    patron = r'^10\.\d{4,}/[\S]+$'
    return re.match(patron, doi) is not None


# ============== VALIDACIÓN DE ARCHIVOS ==============

ALLOWED_EXTENSIONS = {'pdf', 'jpg', 'jpeg', 'png'}
MAX_FILE_SIZE = 5 * 1024 * 1024  # 5 MB

def archivo_permitido(filename):
    """Verifica si la extensión del archivo está permitida"""
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


def validar_archivo(archivo):
    """
    Valida archivo subido (tipo y tamaño)
    Lanza ValueError si el archivo no es válido
    """
    if not archivo or not archivo.filename:
        raise ValueError("No se proporcionó archivo")
    
    # Verificar extensión
    if not archivo_permitido(archivo.filename):
        raise ValueError(f"Tipo de archivo no permitido. Solo: {', '.join(ALLOWED_EXTENSIONS)}")
    
    # Verificar tamaño
    archivo.seek(0, os.SEEK_END)
    size = archivo.tell()
    archivo.seek(0)  # Regresar al inicio
    
    if size > MAX_FILE_SIZE:
        raise ValueError(f"Archivo excede el tamaño máximo de {MAX_FILE_SIZE // (1024*1024)}MB")
    
    if size == 0:
        raise ValueError("El archivo está vacío")
    
    return True


def generar_nombre_archivo_seguro(original_filename, prefijo="archivo"):
    """Genera un nombre de archivo seguro y único"""
    # Limpiar nombre original
    filename_seguro = secure_filename(original_filename)
    
    # Obtener extensión
    extension = os.path.splitext(filename_seguro)[1]
    
    # Generar nombre único con timestamp
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    nombre_final = f"{prefijo}_{timestamp}{extension}"
    
    return nombre_final


# ============== LOGGING DE SEGURIDAD ==============

def log_acceso_denegado(ip, ruta, razon):
    """Registra intento de acceso denegado"""
    logging.warning(f"ACCESO DENEGADO | IP: {ip} | Ruta: {ruta} | Razón: {razon}")


def log_actividad_sospechosa(ip, ruta, detalles):
    """Registra actividad sospechosa"""
    logging.warning(f"ACTIVIDAD SOSPECHOSA | IP: {ip} | Ruta: {ruta} | Detalles: {detalles}")


def log_error_validacion(ip, campo, valor_intentado):
    """Registra error de validación de entrada"""
    logging.warning(f"ERROR VALIDACIÓN | IP: {ip} | Campo: {campo} | Valor: {valor_intentado[:50]}")


def log_archivo_rechazado(ip, filename, razon):
    """Registra archivo rechazado"""
    logging.warning(f"ARCHIVO RECHAZADO | IP: {ip} | Archivo: {filename} | Razón: {razon}")


# ============== VALIDACIÓN DE DATOS DE FORMULARIO ==============

def validar_datos_investigador(data):
    """
    Valida datos del formulario de investigador
    Retorna (es_valido, errores)
    """
    errores = []
    
    # Validar campos obligatorios
    campos_requeridos = ['nombres', 'apellidoPaterno', 'curp', 'correoInstitucional']
    for campo in campos_requeridos:
        if not data.get(campo) or not data.get(campo).strip():
            errores.append(f"Campo '{campo}' es obligatorio")
    
    # Validar CURP
    if data.get('curp') and not validar_curp(data['curp']):
        errores.append("CURP inválida")
        log_error_validacion(request.remote_addr, 'curp', data.get('curp', ''))
    
    # Validar email
    if data.get('correoInstitucional') and not validar_email(data['correoInstitucional']):
        errores.append("Email institucional inválido")
        log_error_validacion(request.remote_addr, 'email', data.get('correoInstitucional', ''))
    
    # Validar teléfono (si se proporciona)
    if data.get('telefonoCelular'):
        if not validar_telefono(data['telefonoCelular']):
            errores.append("Teléfono debe tener 10 dígitos")
            log_error_validacion(request.remote_addr, 'telefono', data.get('telefonoCelular', ''))
    
    # Validar DOIs (si se proporcionan)
    if data.get('publicaciones2025'):
        for i, pub in enumerate(data['publicaciones2025']):
            if pub.get('doi') and not validar_doi(pub['doi']):
                errores.append(f"DOI inválido en publicación {i+1}")
    
    return (len(errores) == 0, errores)


# ============== SANITIZACIÓN DE DATOS ==============

def sanitizar_datos_formulario(data):
    """Limpia y sanitiza datos del formulario antes de guardar"""
    if not isinstance(data, dict):
        return data
    
    datos_limpios = {}
    
    for key, value in data.items():
        if isinstance(value, str):
            # Limpiar strings
            datos_limpios[key] = limpiar_input(value)
        elif isinstance(value, list):
            # Limpiar listas recursivamente
            datos_limpios[key] = [
                sanitizar_datos_formulario(item) if isinstance(item, dict)
                else limpiar_input(item) if isinstance(item, str)
                else item
                for item in value
            ]
        elif isinstance(value, dict):
            # Limpiar diccionarios recursivamente
            datos_limpios[key] = sanitizar_datos_formulario(value)
        else:
            # Otros tipos (números, booleanos) pasar sin cambios
            datos_limpios[key] = value
    
    return datos_limpios


# ============== DETECCIÓN DE ATAQUES ==============

def detectar_inyeccion_sql(texto):
    """Detecta patrones comunes de inyección SQL"""
    if not texto:
        return False
    
    patrones_peligrosos = [
        r"(\bunion\b.*\bselect\b)",
        r"(\bdrop\b.*\btable\b)",
        r"(\binsert\b.*\binto\b)",
        r"(\bupdate\b.*\bset\b)",
        r"(\bdelete\b.*\bfrom\b)",
        r"(--)",
        r"(/\*.*\*/)",
        r"(xp_cmdshell)",
        r"(exec.*\()",
    ]
    
    texto_lower = texto.lower()
    for patron in patrones_peligrosos:
        if re.search(patron, texto_lower, re.IGNORECASE):
            log_actividad_sospechosa(
                request.remote_addr if request else 'unknown',
                'validacion',
                f"Posible inyección SQL detectada: {texto[:100]}"
            )
            return True
    
    return False


def detectar_xss(texto):
    """Detecta patrones comunes de XSS"""
    if not texto:
        return False
    
    patrones_peligrosos = [
        r"<script",
        r"javascript:",
        r"onerror=",
        r"onload=",
        r"onclick=",
        r"<iframe",
        r"eval\(",
    ]
    
    texto_lower = texto.lower()
    for patron in patrones_peligrosos:
        if re.search(patron, texto_lower, re.IGNORECASE):
            log_actividad_sospechosa(
                request.remote_addr if request else 'unknown',
                'validacion',
                f"Posible XSS detectado: {texto[:100]}"
            )
            return True
    
    return False


# ============== UTILIDADES DE VERIFICACIÓN ==============

def verificar_ip_bloqueada(ip):
    """Verifica si una IP está en la lista negra"""
    # Aquí podrías implementar un sistema de bloqueo de IPs
    # Por ahora, retorna False (ninguna IP bloqueada)
    BLACKLIST = []  # Agregar IPs maliciosas aquí
    return ip in BLACKLIST


def contar_intentos_recientes(ip, ventana_minutos=60):
    """Cuenta intentos de acceso recientes desde una IP"""
    # Implementación básica - en producción usar Redis o similar
    # Por ahora retorna 0
    return 0


# ============== EXPORTAR FUNCIONES ==============

__all__ = [
    'require_auth',
    'validar_curp',
    'validar_email',
    'validar_telefono',
    'validar_doi',
    'limpiar_input',
    'archivo_permitido',
    'validar_archivo',
    'generar_nombre_archivo_seguro',
    'validar_datos_investigador',
    'sanitizar_datos_formulario',
    'detectar_inyeccion_sql',
    'detectar_xss',
    'log_acceso_denegado',
    'log_actividad_sospechosa',
    'log_error_validacion',
    'log_archivo_rechazado',
]

