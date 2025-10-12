"""
Script para inicializar la base de datos con datos de ejemplo
Ejecutar: python init_data.py
"""

import sys
import io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

from models import init_db, get_session, Investigador, SNII, Proyecto, Publicacion
from datetime import date

def init_sample_data():
    # Inicializar base de datos
    init_db()
    session = get_session()
    
    try:
        # Verificar si ya hay datos
        if session.query(Investigador).count() > 0:
            print("[!] La base de datos ya contiene datos. Saltando inicializacion.")
            return
        
        print("[*] Inicializando base de datos con datos de ejemplo...")
        
        # Crear investigadores
        investigadores = [
            Investigador(
                nombre="María",
                apellido_paterno="García",
                apellido_materno="López",
                email="maria.garcia@universidad.edu.mx",
                telefono="555-1234",
                especialidad="Inteligencia Artificial",
                grado_academico="Doctorado",
                institucion="Universidad Nacional",
                departamento="Ciencias Computacionales",
                fecha_ingreso=date(2015, 3, 1),
                estatus="Activo"
            ),
            Investigador(
                nombre="Juan",
                apellido_paterno="Martínez",
                apellido_materno="Hernández",
                email="juan.martinez@universidad.edu.mx",
                telefono="555-5678",
                especialidad="Biotecnología",
                grado_academico="Doctorado",
                institucion="Universidad Nacional",
                departamento="Biología Molecular",
                fecha_ingreso=date(2012, 8, 15),
                estatus="Activo"
            ),
            Investigador(
                nombre="Ana",
                apellido_paterno="Rodríguez",
                apellido_materno="Pérez",
                email="ana.rodriguez@universidad.edu.mx",
                telefono="555-9012",
                especialidad="Energías Renovables",
                grado_academico="Doctorado",
                institucion="Universidad Nacional",
                departamento="Ingeniería Ambiental",
                fecha_ingreso=date(2018, 1, 10),
                estatus="Activo"
            ),
            Investigador(
                nombre="Carlos",
                apellido_paterno="Sánchez",
                apellido_materno="Torres",
                email="carlos.sanchez@universidad.edu.mx",
                telefono="555-3456",
                especialidad="Nanomateriales",
                grado_academico="Doctorado",
                institucion="Universidad Nacional",
                departamento="Física Aplicada",
                fecha_ingreso=date(2010, 6, 1),
                estatus="Activo"
            ),
            Investigador(
                nombre="Laura",
                apellido_paterno="Fernández",
                apellido_materno="Ruiz",
                email="laura.fernandez@universidad.edu.mx",
                telefono="555-7890",
                especialidad="Neurociencias",
                grado_academico="Doctorado",
                institucion="Universidad Nacional",
                departamento="Medicina",
                fecha_ingreso=date(2016, 9, 1),
                estatus="Activo"
            )
        ]
        
        for inv in investigadores:
            session.add(inv)
        
        session.commit()
        print(f"[OK] {len(investigadores)} investigadores creados")
        
        # Crear registros SNII
        snii_records = [
            SNII(
                investigador_id=1,
                nivel="Nivel II",
                fecha_ingreso=date(2016, 1, 1),
                fecha_vigencia=date(2025, 12, 31),
                estatus="Vigente",
                numero_registro="12345",
                area_conocimiento="Ingeniería y Tecnología"
            ),
            SNII(
                investigador_id=2,
                nivel="Nivel III",
                fecha_ingreso=date(2013, 1, 1),
                fecha_vigencia=date(2026, 12, 31),
                estatus="Vigente",
                numero_registro="23456",
                area_conocimiento="Biología y Química"
            ),
            SNII(
                investigador_id=3,
                nivel="Nivel I",
                fecha_ingreso=date(2019, 1, 1),
                fecha_vigencia=date(2025, 12, 31),
                estatus="Vigente",
                numero_registro="34567",
                area_conocimiento="Ingeniería y Tecnología"
            ),
            SNII(
                investigador_id=4,
                nivel="Nivel III",
                fecha_ingreso=date(2011, 1, 1),
                fecha_vigencia=date(2026, 12, 31),
                estatus="Vigente",
                numero_registro="45678",
                area_conocimiento="Físico-Matemáticas"
            )
        ]
        
        for snii in snii_records:
            session.add(snii)
        
        session.commit()
        print(f"[OK] {len(snii_records)} registros SNII creados")
        
        # Crear proyectos
        proyectos = [
            Proyecto(
                titulo="Desarrollo de Algoritmos de Aprendizaje Profundo para Diagnóstico Médico",
                descripcion="Implementación de redes neuronales para detección temprana de enfermedades",
                tipo="Investigación",
                fuente_financiamiento="CONACyT",
                monto=1500000.00,
                fecha_inicio=date(2023, 1, 1),
                fecha_fin=date(2025, 12, 31),
                estatus="En curso",
                responsable_id=1
            ),
            Proyecto(
                titulo="Producción Sostenible de Biocombustibles",
                descripcion="Estudio de microorganismos para producción eficiente de bioetanol",
                tipo="Desarrollo",
                fuente_financiamiento="SENER",
                monto=2000000.00,
                fecha_inicio=date(2022, 6, 1),
                fecha_fin=date(2025, 5, 31),
                estatus="En curso",
                responsable_id=2
            ),
            Proyecto(
                titulo="Sistemas Fotovoltaicos de Alta Eficiencia",
                descripcion="Desarrollo de paneles solares de tercera generación",
                tipo="Innovación",
                fuente_financiamiento="Fundación México-EUA",
                monto=1800000.00,
                fecha_inicio=date(2023, 9, 1),
                fecha_fin=date(2026, 8, 31),
                estatus="En curso",
                responsable_id=3
            ),
            Proyecto(
                titulo="Nanomateriales para Almacenamiento de Energía",
                descripcion="Síntesis de grafeno para baterías de nueva generación",
                tipo="Investigación",
                fuente_financiamiento="CONACyT",
                monto=1200000.00,
                fecha_inicio=date(2021, 1, 1),
                fecha_fin=date(2024, 12, 31),
                estatus="En curso",
                responsable_id=4
            ),
            Proyecto(
                titulo="Estudio de Plasticidad Neuronal en Aprendizaje",
                descripcion="Investigación sobre mecanismos de memoria y aprendizaje",
                tipo="Investigación",
                fuente_financiamiento="NIH",
                monto=2500000.00,
                fecha_inicio=date(2022, 3, 1),
                fecha_fin=date(2027, 2, 28),
                estatus="En curso",
                responsable_id=5
            )
        ]
        
        for proy in proyectos:
            session.add(proy)
        
        session.commit()
        print(f"[OK] {len(proyectos)} proyectos creados")
        
        # Asociar investigadores a proyectos
        proyectos[0].investigadores.extend([investigadores[0], investigadores[4]])
        proyectos[1].investigadores.append(investigadores[1])
        proyectos[2].investigadores.extend([investigadores[2], investigadores[3]])
        proyectos[3].investigadores.append(investigadores[3])
        proyectos[4].investigadores.append(investigadores[4])
        
        session.commit()
        
        # Crear publicaciones
        publicaciones = [
            Publicacion(
                titulo="Deep Learning Approaches for Early Disease Detection: A Comprehensive Review",
                tipo="Artículo",
                revista_editorial="Journal of Medical Artificial Intelligence",
                anio=2023,
                volumen="15",
                paginas="234-256",
                doi="10.1234/jmai.2023.15.234",
                issn_isbn="1234-5678",
                url="https://journal.example.com/article/123",
                resumen="Revisión exhaustiva de técnicas de aprendizaje profundo aplicadas al diagnóstico médico temprano",
                palabras_clave="deep learning, medical diagnosis, neural networks, AI",
                indexada="Web of Science, Scopus",
                factor_impacto=4.5
            ),
            Publicacion(
                titulo="Sustainable Bioethanol Production Using Engineered Microorganisms",
                tipo="Artículo",
                revista_editorial="Biotechnology Advances",
                anio=2024,
                volumen="42",
                paginas="108-125",
                doi="10.5678/biotech.2024.42.108",
                issn_isbn="0734-9750",
                indexada="Web of Science, Scopus",
                factor_impacto=8.3
            ),
            Publicacion(
                titulo="Third-Generation Solar Cells: Materials and Efficiency",
                tipo="Artículo",
                revista_editorial="Renewable Energy Journal",
                anio=2024,
                volumen="88",
                paginas="445-467",
                doi="10.9012/rej.2024.88.445",
                issn_isbn="0960-1481",
                indexada="Web of Science, Scopus, SciELO",
                factor_impacto=6.7
            ),
            Publicacion(
                titulo="Graphene-Based Nanomaterials for Energy Storage Applications",
                tipo="Libro",
                revista_editorial="Springer Nature",
                anio=2023,
                issn_isbn="978-3-030-12345-6",
                resumen="Libro completo sobre aplicaciones del grafeno en almacenamiento de energía",
                palabras_clave="graphene, nanomaterials, energy storage, batteries"
            ),
            Publicacion(
                titulo="Neuroplasticity Mechanisms in Learning and Memory Formation",
                tipo="Artículo",
                revista_editorial="Nature Neuroscience",
                anio=2024,
                volumen="27",
                paginas="1523-1540",
                doi="10.1038/nn.2024.1523",
                issn_isbn="1097-6256",
                indexada="Web of Science, PubMed",
                factor_impacto=21.2
            ),
            Publicacion(
                titulo="Advances in Machine Learning for Biomedical Applications",
                tipo="Capítulo",
                revista_editorial="Academic Press",
                anio=2023,
                paginas="67-102",
                issn_isbn="978-0-12-345678-9",
                resumen="Capítulo sobre aplicaciones de ML en biomedicina"
            )
        ]
        
        for pub in publicaciones:
            session.add(pub)
        
        session.commit()
        print(f"[OK] {len(publicaciones)} publicaciones creadas")
        
        # Asociar autores a publicaciones
        publicaciones[0].autores.extend([investigadores[0], investigadores[4]])
        publicaciones[1].autores.append(investigadores[1])
        publicaciones[2].autores.append(investigadores[2])
        publicaciones[3].autores.append(investigadores[3])
        publicaciones[4].autores.append(investigadores[4])
        publicaciones[5].autores.extend([investigadores[0], investigadores[4]])
        
        session.commit()
        
        print("\n[OK] Base de datos inicializada correctamente!")
        print("\nResumen:")
        print(f"   - {len(investigadores)} Investigadores")
        print(f"   - {len(snii_records)} Registros SNII")
        print(f"   - {len(proyectos)} Proyectos")
        print(f"   - {len(publicaciones)} Publicaciones")
        print("\nAhora puedes iniciar el servidor con: python app.py")
        
    except Exception as e:
        session.rollback()
        print(f"[ERROR] Error al inicializar datos: {e}")
    finally:
        session.close()

if __name__ == "__main__":
    init_sample_data()

