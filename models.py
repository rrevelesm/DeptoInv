from datetime import datetime
from sqlalchemy import create_engine, Column, Integer, String, Text, Date, Float, ForeignKey, Table
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, sessionmaker

Base = declarative_base()

# Tabla de relación muchos a muchos entre investigadores y proyectos
investigador_proyecto = Table('investigador_proyecto', Base.metadata,
    Column('investigador_id', Integer, ForeignKey('investigadores.id')),
    Column('proyecto_id', Integer, ForeignKey('proyectos.id'))
)

# Tabla de relación muchos a muchos entre investigadores y publicaciones
investigador_publicacion = Table('investigador_publicacion', Base.metadata,
    Column('investigador_id', Integer, ForeignKey('investigadores.id')),
    Column('publicacion_id', Integer, ForeignKey('publicaciones.id'))
)

class Investigador(Base):
    __tablename__ = 'investigadores'
    
    id = Column(Integer, primary_key=True)
    nombre = Column(String(100), nullable=False)
    apellido_paterno = Column(String(100), nullable=False)
    apellido_materno = Column(String(100))
    email = Column(String(150), unique=True, nullable=False)
    telefono = Column(String(20))
    especialidad = Column(String(200))
    grado_academico = Column(String(100))
    institucion = Column(String(200))
    departamento = Column(String(200))
    fecha_ingreso = Column(Date)
    estatus = Column(String(50), default='Activo')  # Activo, Inactivo, Jubilado
    
    # Relaciones
    snii = relationship('SNII', back_populates='investigador', uselist=False)
    proyectos = relationship('Proyecto', secondary=investigador_proyecto, back_populates='investigadores')
    publicaciones = relationship('Publicacion', secondary=investigador_publicacion, back_populates='autores')
    
    def to_dict(self):
        return {
            'id': self.id,
            'nombre': self.nombre,
            'apellido_paterno': self.apellido_paterno,
            'apellido_materno': self.apellido_materno,
            'nombre_completo': f"{self.nombre} {self.apellido_paterno} {self.apellido_materno or ''}".strip(),
            'email': self.email,
            'telefono': self.telefono,
            'especialidad': self.especialidad,
            'grado_academico': self.grado_academico,
            'institucion': self.institucion,
            'departamento': self.departamento,
            'fecha_ingreso': self.fecha_ingreso.isoformat() if self.fecha_ingreso else None,
            'estatus': self.estatus
        }

class SNII(Base):
    __tablename__ = 'snii'
    
    id = Column(Integer, primary_key=True)
    investigador_id = Column(Integer, ForeignKey('investigadores.id'), unique=True)
    nivel = Column(String(50))  # Candidato, I, II, III, Emérito
    fecha_ingreso = Column(Date)
    fecha_vigencia = Column(Date)
    estatus = Column(String(50), default='Vigente')  # Vigente, Vencido, En evaluación
    numero_registro = Column(String(50))
    area_conocimiento = Column(String(200))
    
    # Relaciones
    investigador = relationship('Investigador', back_populates='snii')
    
    def to_dict(self):
        return {
            'id': self.id,
            'investigador_id': self.investigador_id,
            'nivel': self.nivel,
            'fecha_ingreso': self.fecha_ingreso.isoformat() if self.fecha_ingreso else None,
            'fecha_vigencia': self.fecha_vigencia.isoformat() if self.fecha_vigencia else None,
            'estatus': self.estatus,
            'numero_registro': self.numero_registro,
            'area_conocimiento': self.area_conocimiento
        }

class Proyecto(Base):
    __tablename__ = 'proyectos'
    
    id = Column(Integer, primary_key=True)
    clave_sip = Column(String(50))  # Clave SIP del proyecto
    titulo = Column(String(300), nullable=False)
    descripcion = Column(Text)
    tipo = Column(String(100))  # Investigación, Desarrollo, Innovación
    fuente_financiamiento = Column(String(200))
    monto = Column(Float)
    fecha_inicio = Column(Date)
    fecha_fin = Column(Date)
    estatus = Column(String(50), default='En curso')  # Planeado, En curso, Finalizado, Cancelado
    responsable_id = Column(Integer, ForeignKey('investigadores.id'))
    
    # Relaciones
    responsable = relationship('Investigador', foreign_keys=[responsable_id])
    investigadores = relationship('Investigador', secondary=investigador_proyecto, back_populates='proyectos')
    
    def to_dict(self):
        responsable_nombre = None
        if self.responsable:
            responsable_nombre = f"{self.responsable.nombre} {self.responsable.apellido_paterno} {self.responsable.apellido_materno or ''}".strip()
        
        return {
            'id': self.id,
            'clave_sip': self.clave_sip,
            'titulo': self.titulo,
            'descripcion': self.descripcion,
            'tipo': self.tipo,
            'fuente_financiamiento': self.fuente_financiamiento,
            'monto': self.monto,
            'fecha_inicio': self.fecha_inicio.isoformat() if self.fecha_inicio else None,
            'fecha_fin': self.fecha_fin.isoformat() if self.fecha_fin else None,
            'estatus': self.estatus,
            'responsable_id': self.responsable_id,
            'responsable_nombre': responsable_nombre
        }

class Publicacion(Base):
    __tablename__ = 'publicaciones'
    
    id = Column(Integer, primary_key=True)
    titulo = Column(String(500), nullable=False)
    tipo = Column(String(100))  # Artículo, Libro, Capítulo, Conferencia, Tesis
    revista_editorial = Column(String(200))
    anio = Column(Integer)
    volumen = Column(String(50))
    paginas = Column(String(50))
    doi = Column(String(100))
    issn_isbn = Column(String(50))
    url = Column(String(500))
    resumen = Column(Text)
    palabras_clave = Column(String(500))
    indexada = Column(String(100))  # WoS, Scopus, SciELO, etc.
    factor_impacto = Column(Float)
    
    # Relaciones
    autores = relationship('Investigador', secondary=investigador_publicacion, back_populates='publicaciones')
    
    def to_dict(self):
        return {
            'id': self.id,
            'titulo': self.titulo,
            'tipo': self.tipo,
            'revista_editorial': self.revista_editorial,
            'anio': self.anio,
            'volumen': self.volumen,
            'paginas': self.paginas,
            'doi': self.doi,
            'issn_isbn': self.issn_isbn,
            'url': self.url,
            'resumen': self.resumen,
            'palabras_clave': self.palabras_clave,
            'indexada': self.indexada,
            'factor_impacto': self.factor_impacto
        }

# Función para inicializar la base de datos
def init_db():
    engine = create_engine('sqlite:///depto_investigacion.db')
    Base.metadata.create_all(engine)
    return engine

# Función para obtener la sesión
def get_session():
    engine = create_engine('sqlite:///depto_investigacion.db')
    Session = sessionmaker(bind=engine)
    return Session()


