from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
from models import (
    init_db, get_session, Investigador, SNII, Proyecto, Publicacion,
    investigador_proyecto, investigador_publicacion
)
from datetime import datetime
import os
import secrets

# Intentar importar Flask-Limiter (opcional)
try:
    from flask_limiter import Limiter
    from flask_limiter.util import get_remote_address
    LIMITER_AVAILABLE = True
except ImportError:
    LIMITER_AVAILABLE = False
    print("⚠️  Flask-Limiter no instalado - Rate limiting desactivado")
    print("⚠️  Instala con: pip install Flask-Limiter")

# Importar utilidades de seguridad
from security_utils import (
    require_auth, validar_archivo, generar_nombre_archivo_seguro,
    validar_datos_investigador, sanitizar_datos_formulario,
    log_archivo_rechazado, log_actividad_sospechosa
)

app = Flask(__name__, static_folder='static')

# 🔒 CONFIGURACIÓN DE SEGURIDAD
# SECRET_KEY para sesiones seguras (en producción usar variable de entorno)
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', secrets.token_hex(32))

# CORS Restringido - Solo permitir orígenes específicos
CORS(app, resources={
    r"/api/formulario-investigador": {
        "origins": ["http://127.0.0.1:5000", "http://localhost:5000", "http://192.168.0.6:5000"],
        "methods": ["POST"],
        "allow_headers": ["Content-Type"]
    },
    r"/api/investigadores": {
        "origins": ["http://127.0.0.1:5000", "http://localhost:5000"],
        "methods": ["GET", "POST", "PUT", "DELETE"],
        "allow_headers": ["Content-Type", "Authorization"]
    }
})

# Rate Limiting - Protección contra DDoS y spam (si está disponible)
if LIMITER_AVAILABLE:
    limiter = Limiter(
        app=app,
        key_func=get_remote_address,
        default_limits=["200 per day", "50 per hour"],
        storage_uri="memory://"
    )
else:
    # Decorador dummy si no está Flask-Limiter
    class DummyLimiter:
        def limit(self, *args, **kwargs):
            def decorator(f):
                return f
            return decorator
    limiter = DummyLimiter()

# Inicializar base de datos
init_db()

# Ruta para el formulario de investigadores
@app.route('/formulario')
def formulario():
    return send_from_directory('static', 'formulario_investigador.html')

# Ruta para el panel de formularios
@app.route('/panel-formularios')
def panel_formularios():
    return send_from_directory('static', 'panel_formularios.html')

# API para listar formularios recibidos
@app.route('/api/formularios-lista', methods=['GET'])
@require_auth  # 🔒 Protegido - requiere token de admin
def listar_formularios():
    """Lista todos los formularios recibidos"""
    import json
    
    try:
        formularios_dir = 'formularios'
        if not os.path.exists(formularios_dir):
            return jsonify([])
        
        archivos = [f for f in os.listdir(formularios_dir) if f.endswith('.json')]
        formularios = []
        
        for archivo in archivos:
            try:
                ruta = os.path.join(formularios_dir, archivo)
                with open(ruta, 'r', encoding='utf-8') as f:
                    datos = json.load(f)
                    datos['_archivo'] = archivo
                    formularios.append(datos)
            except Exception as e:
                continue
        
        # Ordenar por timestamp descendente
        formularios.sort(key=lambda x: x.get('timestamp', ''), reverse=True)
        
        return jsonify(formularios)
    except Exception as e:
        return jsonify({'error': str(e)}), 400

# API para exportar formularios a Excel
@app.route('/api/exportar-formularios-excel', methods=['GET'])
@require_auth  # 🔒 Protegido - requiere token de admin
@limiter.limit("10 per hour")  # Límite de descargas
def exportar_excel_endpoint():
    """Exporta todos los formularios a Excel y lo descarga"""
    import json
    import pandas as pd
    from flask import send_file
    from datetime import datetime as dt
    
    try:
        formularios_dir = 'formularios'
        if not os.path.exists(formularios_dir):
            return jsonify({'error': 'No hay formularios'}), 404
        
        archivos = [f for f in os.listdir(formularios_dir) if f.endswith('.json')]
        
        if not archivos:
            return jsonify({'error': 'No hay formularios para exportar'}), 404
        
        datos_investigadores = []
        
        for archivo in archivos:
            try:
                ruta = os.path.join(formularios_dir, archivo)
                with open(ruta, 'r', encoding='utf-8') as f:
                    datos = json.load(f)
                
                # Procesar proyectos
                proyectos_texto = []
                if 'proyectosVigentes' in datos and datos['proyectosVigentes']:
                    for proy in datos['proyectosVigentes']:
                        proyectos_texto.append(f"{proy.get('categoria', 'N/A')}: {proy.get('nombre', 'N/A')}")
                proyectos_str = '\n'.join(proyectos_texto) if proyectos_texto else 'Sin proyectos'
                
                # Procesar líneas
                lineas_str = '\n'.join(datos.get('lineasInvestigacion', [])) if datos.get('lineasInvestigacion') else 'N/A'
                
                # Procesar publicaciones
                pubs_texto = []
                if 'publicaciones2025' in datos and datos['publicaciones2025']:
                    for pub in datos['publicaciones2025']:
                        pubs_texto.append(f"{pub.get('tipo', 'N/A')}: {pub.get('doi', 'N/A')}")
                pubs_str = '\n'.join(pubs_texto) if pubs_texto else 'Sin publicaciones 2025'
                
                fila = {
                    'Nombre Completo': datos.get('nombreCompleto', ''),
                    'CURP': datos.get('curp', ''),
                    'Fecha Nacimiento': datos.get('fechaNacimiento', ''),
                    'Género': datos.get('genero', ''),
                    'Clave Empleado': datos.get('claveEmpleado', ''),
                    'Categoría': datos.get('categoria', ''),
                    'Correo Institucional': datos.get('correoInstitucional', ''),
                    'Teléfono': datos.get('telefonoCelular', '') if datos.get('aceptaContacto') == 'Si' else 'N/A',
                    'Tiene Proyecto': datos.get('tieneProyectoVigente', 'No'),
                    'Proyectos': proyectos_str,
                    'Beca EDI': datos.get('nivelEDI', '') if datos.get('cuentaBecaEDI') == 'Si' else 'No',
                    'SNII': datos.get('nivelSNII', '') if datos.get('cuentaSNII') == 'Si' else 'No',
                    'SNII Vigencia': f"{datos.get('sniiInicio', '')} - {datos.get('sniiFinal', '')}" if datos.get('cuentaSNII') == 'Si' else 'N/A',
                    'ORCID': datos.get('orcid', ''),
                    'Líneas Investigación': lineas_str,
                    'Publicaciones 2025': pubs_str,
                    'Fecha Registro': datos.get('timestamp', '')
                }
                
                datos_investigadores.append(fila)
            except:
                continue
        
        df = pd.DataFrame(datos_investigadores)
        df = df.sort_values('Fecha Registro', ascending=False)
        
        # Crear archivo Excel
        timestamp = dt.now().strftime('%Y%m%d_%H%M%S')
        nombre_excel = f'Formularios_UPIIZ_{timestamp}.xlsx'
        
        with pd.ExcelWriter(nombre_excel, engine='openpyxl') as writer:
            df.to_excel(writer, sheet_name='Investigadores', index=False)
            worksheet = writer.sheets['Investigadores']
            
            for column in worksheet.columns:
                max_length = 0
                column_letter = column[0].column_letter
                for cell in column:
                    try:
                        if len(str(cell.value)) > max_length:
                            max_length = len(str(cell.value))
                    except:
                        pass
                adjusted_width = min(max_length + 2, 50)
                worksheet.column_dimensions[column_letter].width = adjusted_width
        
        return send_file(nombre_excel, as_attachment=True, download_name=nombre_excel)
    except Exception as e:
        return jsonify({'error': str(e)}), 400

# ============== RUTAS DE INVESTIGADORES ==============

@app.route('/api/investigadores', methods=['GET'])
@require_auth  # 🔒 Protegido - requiere token de admin
def get_investigadores():
    session = get_session()
    try:
        investigadores = session.query(Investigador).all()
        return jsonify([inv.to_dict() for inv in investigadores])
    finally:
        session.close()

@app.route('/api/investigadores/<int:id>', methods=['GET'])
@require_auth  # 🔒 Protegido
def get_investigador(id):
    session = get_session()
    try:
        investigador = session.query(Investigador).get(id)
        if not investigador:
            return jsonify({'error': 'Investigador no encontrado'}), 404
        
        data = investigador.to_dict()
        # Agregar información adicional
        data['snii'] = investigador.snii.to_dict() if investigador.snii else None
        data['proyectos'] = [p.to_dict() for p in investigador.proyectos]
        data['publicaciones'] = [p.to_dict() for p in investigador.publicaciones]
        
        return jsonify(data)
    finally:
        session.close()

@app.route('/api/investigadores', methods=['POST'])
@require_auth  # 🔒 Protegido
def create_investigador():
    session = get_session()
    try:
        data = request.json
        investigador = Investigador(
            nombre=data['nombre'],
            apellido_paterno=data['apellido_paterno'],
            apellido_materno=data.get('apellido_materno'),
            email=data['email'],
            telefono=data.get('telefono'),
            especialidad=data.get('especialidad'),
            grado_academico=data.get('grado_academico'),
            institucion=data.get('institucion'),
            departamento=data.get('departamento'),
            fecha_ingreso=datetime.strptime(data['fecha_ingreso'], '%Y-%m-%d').date() if data.get('fecha_ingreso') else None,
            estatus=data.get('estatus', 'Activo')
        )
        session.add(investigador)
        session.commit()
        return jsonify(investigador.to_dict()), 201
    except Exception as e:
        session.rollback()
        return jsonify({'error': str(e)}), 400
    finally:
        session.close()

@app.route('/api/investigadores/<int:id>', methods=['PUT'])
@require_auth  # 🔒 Protegido
def update_investigador(id):
    session = get_session()
    try:
        investigador = session.query(Investigador).get(id)
        if not investigador:
            return jsonify({'error': 'Investigador no encontrado'}), 404
        
        data = request.json
        investigador.nombre = data.get('nombre', investigador.nombre)
        investigador.apellido_paterno = data.get('apellido_paterno', investigador.apellido_paterno)
        investigador.apellido_materno = data.get('apellido_materno', investigador.apellido_materno)
        investigador.email = data.get('email', investigador.email)
        investigador.telefono = data.get('telefono', investigador.telefono)
        investigador.especialidad = data.get('especialidad', investigador.especialidad)
        investigador.grado_academico = data.get('grado_academico', investigador.grado_academico)
        investigador.institucion = data.get('institucion', investigador.institucion)
        investigador.departamento = data.get('departamento', investigador.departamento)
        investigador.estatus = data.get('estatus', investigador.estatus)
        
        if data.get('fecha_ingreso'):
            investigador.fecha_ingreso = datetime.strptime(data['fecha_ingreso'], '%Y-%m-%d').date()
        
        session.commit()
        return jsonify(investigador.to_dict())
    except Exception as e:
        session.rollback()
        return jsonify({'error': str(e)}), 400
    finally:
        session.close()

@app.route('/api/investigadores/<int:id>', methods=['DELETE'])
@require_auth  # 🔒 Protegido
def delete_investigador(id):
    session = get_session()
    try:
        investigador = session.query(Investigador).get(id)
        if not investigador:
            return jsonify({'error': 'Investigador no encontrado'}), 404
        
        session.delete(investigador)
        session.commit()
        return jsonify({'mensaje': 'Investigador eliminado correctamente'})
    except Exception as e:
        session.rollback()
        return jsonify({'error': str(e)}), 400
    finally:
        session.close()

# ============== RUTAS DE SNII ==============

@app.route('/api/snii', methods=['GET'])
def get_snii():
    session = get_session()
    try:
        registros = session.query(SNII).all()
        result = []
        for snii in registros:
            data = snii.to_dict()
            data['investigador'] = snii.investigador.to_dict()
            result.append(data)
        return jsonify(result)
    finally:
        session.close()

@app.route('/api/snii/<int:id>', methods=['GET'])
def get_snii_by_id(id):
    session = get_session()
    try:
        snii = session.query(SNII).get(id)
        if not snii:
            return jsonify({'error': 'Registro SNII no encontrado'}), 404
        
        data = snii.to_dict()
        data['investigador'] = snii.investigador.to_dict()
        return jsonify(data)
    finally:
        session.close()

@app.route('/api/snii', methods=['POST'])
def create_snii():
    session = get_session()
    try:
        data = request.json
        snii = SNII(
            investigador_id=data['investigador_id'],
            nivel=data['nivel'],
            fecha_ingreso=datetime.strptime(data['fecha_ingreso'], '%Y-%m-%d').date() if data.get('fecha_ingreso') else None,
            fecha_vigencia=datetime.strptime(data['fecha_vigencia'], '%Y-%m-%d').date() if data.get('fecha_vigencia') else None,
            estatus=data.get('estatus', 'Vigente'),
            numero_registro=data.get('numero_registro'),
            area_conocimiento=data.get('area_conocimiento')
        )
        session.add(snii)
        session.commit()
        return jsonify(snii.to_dict()), 201
    except Exception as e:
        session.rollback()
        return jsonify({'error': str(e)}), 400
    finally:
        session.close()

@app.route('/api/snii/<int:id>', methods=['PUT'])
def update_snii(id):
    session = get_session()
    try:
        snii = session.query(SNII).get(id)
        if not snii:
            return jsonify({'error': 'Registro SNII no encontrado'}), 404
        
        data = request.json
        snii.nivel = data.get('nivel', snii.nivel)
        snii.estatus = data.get('estatus', snii.estatus)
        snii.numero_registro = data.get('numero_registro', snii.numero_registro)
        snii.area_conocimiento = data.get('area_conocimiento', snii.area_conocimiento)
        
        if data.get('fecha_ingreso'):
            snii.fecha_ingreso = datetime.strptime(data['fecha_ingreso'], '%Y-%m-%d').date()
        if data.get('fecha_vigencia'):
            snii.fecha_vigencia = datetime.strptime(data['fecha_vigencia'], '%Y-%m-%d').date()
        
        session.commit()
        return jsonify(snii.to_dict())
    except Exception as e:
        session.rollback()
        return jsonify({'error': str(e)}), 400
    finally:
        session.close()

@app.route('/api/snii/<int:id>', methods=['DELETE'])
def delete_snii(id):
    session = get_session()
    try:
        snii = session.query(SNII).get(id)
        if not snii:
            return jsonify({'error': 'Registro SNII no encontrado'}), 404
        
        session.delete(snii)
        session.commit()
        return jsonify({'mensaje': 'Registro SNII eliminado correctamente'})
    except Exception as e:
        session.rollback()
        return jsonify({'error': str(e)}), 400
    finally:
        session.close()

# ============== RUTAS DE PROYECTOS ==============

@app.route('/api/proyectos', methods=['GET'])
def get_proyectos():
    session = get_session()
    try:
        proyectos = session.query(Proyecto).all()
        return jsonify([p.to_dict() for p in proyectos])
    finally:
        session.close()

@app.route('/api/proyectos/<int:id>', methods=['GET'])
def get_proyecto(id):
    session = get_session()
    try:
        proyecto = session.query(Proyecto).get(id)
        if not proyecto:
            return jsonify({'error': 'Proyecto no encontrado'}), 404
        
        data = proyecto.to_dict()
        data['investigadores'] = [inv.to_dict() for inv in proyecto.investigadores]
        return jsonify(data)
    finally:
        session.close()

@app.route('/api/proyectos', methods=['POST'])
def create_proyecto():
    session = get_session()
    try:
        data = request.json
        proyecto = Proyecto(
            clave_sip=data.get('clave_sip'),
            titulo=data['titulo'],
            descripcion=data.get('descripcion'),
            tipo=data.get('tipo'),
            fuente_financiamiento=data.get('fuente_financiamiento'),
            monto=data.get('monto'),
            fecha_inicio=datetime.strptime(data['fecha_inicio'], '%Y-%m-%d').date() if data.get('fecha_inicio') else None,
            fecha_fin=datetime.strptime(data['fecha_fin'], '%Y-%m-%d').date() if data.get('fecha_fin') else None,
            estatus=data.get('estatus', 'En curso'),
            responsable_id=data.get('responsable_id')
        )
        
        # Agregar investigadores al proyecto
        if 'investigadores_ids' in data:
            for inv_id in data['investigadores_ids']:
                investigador = session.query(Investigador).get(inv_id)
                if investigador:
                    proyecto.investigadores.append(investigador)
        
        session.add(proyecto)
        session.commit()
        return jsonify(proyecto.to_dict()), 201
    except Exception as e:
        session.rollback()
        return jsonify({'error': str(e)}), 400
    finally:
        session.close()

@app.route('/api/proyectos/<int:id>', methods=['PUT'])
def update_proyecto(id):
    session = get_session()
    try:
        proyecto = session.query(Proyecto).get(id)
        if not proyecto:
            return jsonify({'error': 'Proyecto no encontrado'}), 404
        
        data = request.json
        proyecto.clave_sip = data.get('clave_sip', proyecto.clave_sip)
        proyecto.titulo = data.get('titulo', proyecto.titulo)
        proyecto.descripcion = data.get('descripcion', proyecto.descripcion)
        proyecto.tipo = data.get('tipo', proyecto.tipo)
        proyecto.fuente_financiamiento = data.get('fuente_financiamiento', proyecto.fuente_financiamiento)
        proyecto.monto = data.get('monto', proyecto.monto)
        proyecto.estatus = data.get('estatus', proyecto.estatus)
        proyecto.responsable_id = data.get('responsable_id', proyecto.responsable_id)
        
        if data.get('fecha_inicio'):
            proyecto.fecha_inicio = datetime.strptime(data['fecha_inicio'], '%Y-%m-%d').date()
        if data.get('fecha_fin'):
            proyecto.fecha_fin = datetime.strptime(data['fecha_fin'], '%Y-%m-%d').date()
        
        # Actualizar investigadores
        if 'investigadores_ids' in data:
            proyecto.investigadores.clear()
            for inv_id in data['investigadores_ids']:
                investigador = session.query(Investigador).get(inv_id)
                if investigador:
                    proyecto.investigadores.append(investigador)
        
        session.commit()
        return jsonify(proyecto.to_dict())
    except Exception as e:
        session.rollback()
        return jsonify({'error': str(e)}), 400
    finally:
        session.close()

@app.route('/api/proyectos/<int:id>', methods=['DELETE'])
def delete_proyecto(id):
    session = get_session()
    try:
        proyecto = session.query(Proyecto).get(id)
        if not proyecto:
            return jsonify({'error': 'Proyecto no encontrado'}), 404
        
        session.delete(proyecto)
        session.commit()
        return jsonify({'mensaje': 'Proyecto eliminado correctamente'})
    except Exception as e:
        session.rollback()
        return jsonify({'error': str(e)}), 400
    finally:
        session.close()

# ============== RUTAS DE PUBLICACIONES ==============

@app.route('/api/publicaciones', methods=['GET'])
def get_publicaciones():
    session = get_session()
    try:
        publicaciones = session.query(Publicacion).all()
        return jsonify([p.to_dict() for p in publicaciones])
    finally:
        session.close()

@app.route('/api/publicaciones/<int:id>', methods=['GET'])
def get_publicacion(id):
    session = get_session()
    try:
        publicacion = session.query(Publicacion).get(id)
        if not publicacion:
            return jsonify({'error': 'Publicación no encontrada'}), 404
        
        data = publicacion.to_dict()
        data['autores'] = [autor.to_dict() for autor in publicacion.autores]
        return jsonify(data)
    finally:
        session.close()

@app.route('/api/publicaciones', methods=['POST'])
def create_publicacion():
    session = get_session()
    try:
        data = request.json
        publicacion = Publicacion(
            titulo=data['titulo'],
            tipo=data.get('tipo'),
            revista_editorial=data.get('revista_editorial'),
            anio=data.get('anio'),
            volumen=data.get('volumen'),
            paginas=data.get('paginas'),
            doi=data.get('doi'),
            issn_isbn=data.get('issn_isbn'),
            url=data.get('url'),
            resumen=data.get('resumen'),
            palabras_clave=data.get('palabras_clave'),
            indexada=data.get('indexada'),
            factor_impacto=data.get('factor_impacto')
        )
        
        # Agregar autores
        if 'autores_ids' in data:
            for autor_id in data['autores_ids']:
                investigador = session.query(Investigador).get(autor_id)
                if investigador:
                    publicacion.autores.append(investigador)
        
        session.add(publicacion)
        session.commit()
        return jsonify(publicacion.to_dict()), 201
    except Exception as e:
        session.rollback()
        return jsonify({'error': str(e)}), 400
    finally:
        session.close()

@app.route('/api/publicaciones/<int:id>', methods=['PUT'])
def update_publicacion(id):
    session = get_session()
    try:
        publicacion = session.query(Publicacion).get(id)
        if not publicacion:
            return jsonify({'error': 'Publicación no encontrada'}), 404
        
        data = request.json
        publicacion.titulo = data.get('titulo', publicacion.titulo)
        publicacion.tipo = data.get('tipo', publicacion.tipo)
        publicacion.revista_editorial = data.get('revista_editorial', publicacion.revista_editorial)
        publicacion.anio = data.get('anio', publicacion.anio)
        publicacion.volumen = data.get('volumen', publicacion.volumen)
        publicacion.paginas = data.get('paginas', publicacion.paginas)
        publicacion.doi = data.get('doi', publicacion.doi)
        publicacion.issn_isbn = data.get('issn_isbn', publicacion.issn_isbn)
        publicacion.url = data.get('url', publicacion.url)
        publicacion.resumen = data.get('resumen', publicacion.resumen)
        publicacion.palabras_clave = data.get('palabras_clave', publicacion.palabras_clave)
        publicacion.indexada = data.get('indexada', publicacion.indexada)
        publicacion.factor_impacto = data.get('factor_impacto', publicacion.factor_impacto)
        
        # Actualizar autores
        if 'autores_ids' in data:
            publicacion.autores.clear()
            for autor_id in data['autores_ids']:
                investigador = session.query(Investigador).get(autor_id)
                if investigador:
                    publicacion.autores.append(investigador)
        
        session.commit()
        return jsonify(publicacion.to_dict())
    except Exception as e:
        session.rollback()
        return jsonify({'error': str(e)}), 400
    finally:
        session.close()

@app.route('/api/publicaciones/<int:id>', methods=['DELETE'])
def delete_publicacion(id):
    session = get_session()
    try:
        publicacion = session.query(Publicacion).get(id)
        if not publicacion:
            return jsonify({'error': 'Publicación no encontrada'}), 404
        
        session.delete(publicacion)
        session.commit()
        return jsonify({'mensaje': 'Publicación eliminada correctamente'})
    except Exception as e:
        session.rollback()
        return jsonify({'error': str(e)}), 400
    finally:
        session.close()

# ============== RUTAS DE ESTADÍSTICAS ==============

@app.route('/api/formulario-investigador', methods=['POST'])
@limiter.limit("5 per hour")  # 🔒 Máximo 5 formularios por hora por IP
def guardar_formulario_investigador():
    """Guarda los datos del formulario de investigador con archivo adjunto"""
    import json
    from datetime import datetime as dt
    
    try:
        # Obtener datos JSON
        datos_json = request.form.get('datos')
        data = json.loads(datos_json) if datos_json else {}
        
        # 🔒 VALIDAR DATOS DEL FORMULARIO
        es_valido, errores = validar_datos_investigador(data)
        if not es_valido:
            log_actividad_sospechosa(
                request.remote_addr,
                '/api/formulario-investigador',
                f"Datos inválidos: {', '.join(errores)}"
            )
            return jsonify({
                'success': False,
                'error': 'Datos inválidos',
                'detalles': errores
            }), 400
        
        # 🔒 SANITIZAR DATOS (limpiar caracteres peligrosos)
        data = sanitizar_datos_formulario(data)
        
        # Crear directorios si no existen
        if not os.path.exists('formularios'):
            os.makedirs('formularios')
        if not os.path.exists('formularios/constancias_snii'):
            os.makedirs('formularios/constancias_snii')
        
        # Agregar timestamp
        data['timestamp'] = dt.now().isoformat()
        
        # 🔒 VALIDAR Y GUARDAR ARCHIVO SNII CON SEGURIDAD
        archivo_guardado = None
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
                    
                    # Guardar archivo
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
        
        # Guardar datos en archivo JSON
        filename = f"formularios/investigador_{data.get('claveEmpleado', 'sin_clave')}_{dt.now().strftime('%Y%m%d_%H%M%S')}.json"
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
        
        return jsonify({
            'success': True,
            'message': 'Formulario guardado exitosamente',
            'archivo': filename,
            'constancia_snii': archivo_guardado
        }), 201
    except Exception as e:
        # Log de error general
        log_actividad_sospechosa(
            request.remote_addr,
            '/api/formulario-investigador',
            f"Error: {str(e)}"
        )
        return jsonify({
            'success': False,
            'error': str(e)
        }), 400

@app.route('/api/estadisticas', methods=['GET'])
def get_estadisticas():
    session = get_session()
    try:
        stats = {
            'total_investigadores': session.query(Investigador).count(),
            'investigadores_activos': session.query(Investigador).filter_by(estatus='Activo').count(),
            'total_proyectos': session.query(Proyecto).count(),
            'proyectos_activos': session.query(Proyecto).filter_by(estatus='En curso').count(),
            'total_publicaciones': session.query(Publicacion).count(),
            'investigadores_snii': session.query(SNII).count(),
            'snii_vigentes': session.query(SNII).filter_by(estatus='Vigente').count()
        }
        return jsonify(stats)
    finally:
        session.close()

# ============== RUTA PRINCIPAL ==============

@app.route('/')
def index():
    return send_from_directory('static', 'index.html')

@app.route('/<path:path>')
def static_files(path):
    return send_from_directory('static', path)

if __name__ == '__main__':
    # host='0.0.0.0' permite acceso desde otras computadoras en la red local
    # 🔒 DEBUG MODE: False en producción, True solo en desarrollo
    DEBUG_MODE = os.environ.get('DEBUG', 'False').lower() == 'true'
    
    print("="*60)
    print("🔒 SERVIDOR INICIANDO CON SEGURIDAD")
    print("="*60)
    if LIMITER_AVAILABLE:
        print(f"🛡️  Rate Limiting: ✅ Activado (5 formularios/hora)")
    else:
        print(f"⚠️  Rate Limiting: ❌ DESACTIVADO (instalar Flask-Limiter)")
    print(f"🔐 Autenticación: ✅ Requerida en rutas admin")
    print(f"✅ Validación: ✅ Activada (CURP, email, archivos)")
    print(f"🔒 CORS: ✅ Restringido a localhost")
    print(f"⚙️  Debug Mode: {'ACTIVADO ⚠️' if DEBUG_MODE else 'DESACTIVADO ✅'}")
    if DEBUG_MODE:
        print("⚠️  ADVERTENCIA: Debug activo - NO usar en producción")
    if not LIMITER_AVAILABLE:
        print("")
        print("⚠️  INSTALA FLASK-LIMITER:")
        print("   pip install Flask-Limiter")
    print("="*60)
    print(f"📡 Servidor: http://127.0.0.1:5000")
    print(f"📋 Formulario: http://127.0.0.1:5000/formulario")
    print("="*60)
    
    app.run(host='0.0.0.0', debug=DEBUG_MODE, port=5000)


