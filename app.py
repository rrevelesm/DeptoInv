from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
from models import (
    init_db, get_session, Investigador, SNII, Proyecto, Publicacion,
    investigador_proyecto, investigador_publicacion
)
from datetime import datetime
import os

app = Flask(__name__, static_folder='static')
CORS(app)

# Inicializar base de datos
init_db()

# ============== RUTAS DE INVESTIGADORES ==============

@app.route('/api/investigadores', methods=['GET'])
def get_investigadores():
    session = get_session()
    try:
        investigadores = session.query(Investigador).all()
        return jsonify([inv.to_dict() for inv in investigadores])
    finally:
        session.close()

@app.route('/api/investigadores/<int:id>', methods=['GET'])
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

@app.route('/formulario')
def formulario():
    return send_from_directory('static', 'formulario_investigador.html')

@app.route('/panel')
def panel():
    return send_from_directory('static', 'panel_formularios.html')

@app.route('/<path:path>')
def static_files(path):
    return send_from_directory('static', path)

if __name__ == '__main__':
    app.run(debug=True, port=5000)


