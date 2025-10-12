"""
Script para importar SOLO proyectos APROBADOS (sin los que tienen "-")
"""

import sys
import io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

import pandas as pd
from models import init_db, get_session, Investigador, SNII, Proyecto, Publicacion
from datetime import date
import unicodedata
import re

def normalizar_nombre(nombre):
    """Normaliza un nombre eliminando acentos y convirtiendo a mayúsculas"""
    if not nombre or nombre in ['-', 'nan']:
        return None
    
    nombre = ''.join(
        c for c in unicodedata.normalize('NFD', str(nombre))
        if unicodedata.category(c) != 'Mn'
    )
    nombre = ' '.join(nombre.upper().split())
    return nombre

def generar_email_unico(nombre_original, usados):
    """Genera un email único"""
    partes = nombre_original.strip().split()
    
    if len(partes) >= 2:
        nombre = re.sub(r'[^a-z]', '', partes[0].lower())
        apellido = re.sub(r'[^a-z]', '', partes[1].lower())
        base_email = f"{nombre}.{apellido}@ipn.mx"
    else:
        nombre = re.sub(r'[^a-z]', '', nombre_original.lower())
        base_email = f"{nombre}@ipn.mx"
    
    email_final = base_email
    contador = 1
    while email_final in usados:
        email_final = base_email.replace('@ipn.mx', f'{contador}@ipn.mx')
        contador += 1
    
    usados.add(email_final)
    return email_final

def importar_solo_aprobados():
    """Importa solo proyectos aprobados (sin los que tienen "-")"""
    
    # Limpiar base de datos
    session = get_session()
    try:
        print("[*] Limpiando base de datos...")
        session.query(Publicacion).delete()
        session.query(SNII).delete()
        session.query(Proyecto).delete()
        session.query(Investigador).delete()
        session.commit()
        print("[OK] Base de datos limpiada\n")
    except Exception as e:
        session.rollback()
        print(f"[ERROR] {e}")
        return
    finally:
        session.close()
    
    # Leer Excel
    print("[*] Leyendo archivo Excel...")
    df = pd.read_excel("Proyectos 2025 Investigación.xlsx")
    
    # FILTRAR SOLO PROYECTOS APROBADOS (sin "-" en columna Proyecto)
    print(f"[*] Total de proyectos en archivo: {len(df)}")
    df_aprobados = df[df['Proyecto'] != '-'].copy()
    print(f"[*] Proyectos APROBADOS (sin '-'): {len(df_aprobados)}")
    proyectos_rechazados = len(df) - len(df_aprobados)
    print(f"[!] Proyectos NO aprobados (filtrados): {proyectos_rechazados}\n")
    
    # Extraer investigadores únicos de proyectos APROBADOS
    investigadores_unicos = {}
    
    print("[*] Extrayendo investigadores de proyectos aprobados...")
    
    for _, row in df_aprobados.iterrows():
        # Investigador principal
        inv_nombre = str(row['Investigador']).strip()
        if inv_nombre and inv_nombre not in ['-', 'nan']:
            nombre_norm = normalizar_nombre(inv_nombre)
            if nombre_norm and nombre_norm not in investigadores_unicos:
                investigadores_unicos[nombre_norm] = inv_nombre
        
        # Participantes
        inv_part = str(row['Investigadores participantes']).strip()
        if inv_part and inv_part not in ['-', 'nan']:
            for nombre in inv_part.split(','):
                nombre = nombre.strip()
                if nombre:
                    nombre_norm = normalizar_nombre(nombre)
                    if nombre_norm and nombre_norm not in investigadores_unicos:
                        investigadores_unicos[nombre_norm] = nombre
    
    print(f"[OK] {len(investigadores_unicos)} investigadores únicos encontrados\n")
    
    # Crear investigadores y proyectos
    session = get_session()
    investigadores_db = {}
    emails_usados = set()
    proyectos_creados = 0
    
    try:
        # 1. Crear investigadores
        print("[*] Creando investigadores...")
        for nombre_norm, nombre_orig in sorted(investigadores_unicos.items()):
            partes = nombre_orig.split()
            
            if len(partes) >= 2:
                nombre = partes[0]
                apellido_paterno = partes[1]
                apellido_materno = ' '.join(partes[2:]) if len(partes) > 2 else None
            else:
                nombre = nombre_orig
                apellido_paterno = ""
                apellido_materno = None
            
            email = generar_email_unico(nombre_orig, emails_usados)
            
            nuevo_inv = Investigador(
                nombre=nombre,
                apellido_paterno=apellido_paterno,
                apellido_materno=apellido_materno,
                email=email,
                institucion="Instituto Politécnico Nacional",
                departamento="Departamento de Investigación",
                estatus="Activo",
                fecha_ingreso=date(2025, 1, 1)
            )
            
            session.add(nuevo_inv)
            session.flush()
            
            investigadores_db[nombre_norm] = nuevo_inv
            print(f"[+] {nombre_orig}")
        
        print(f"\n[OK] {len(investigadores_db)} investigadores creados\n")
        
        # 2. Crear solo proyectos APROBADOS
        print("[*] Creando proyectos APROBADOS...")
        for index, row in df_aprobados.iterrows():
            try:
                clave_sip = str(row['Clave SIP']) if not pd.isna(row['Clave SIP']) else None
                titulo = str(row['Título']).strip()
                inv_principal_nombre = str(row['Investigador']).strip()
                tipo_investigacion = str(row['Tipo de investigación']).strip()
                tipo_proyecto = str(row['Proyecto']).strip()
                corto_plazo = str(row['Corto plazo']).strip() if not pd.isna(row['Corto plazo']) else None
                mediano_plazo = str(row['Mediano plazo']).strip() if not pd.isna(row['Mediano plazo']) else None
                inv_participantes = str(row['Investigadores participantes']).strip()
                alumnos = str(row['Alumnos participantes']).strip()
                
                # Buscar investigador principal
                inv_principal_norm = normalizar_nombre(inv_principal_nombre)
                inv_principal = investigadores_db.get(inv_principal_norm)
                
                # Crear descripción
                desc_parts = []
                desc_parts.append(f"Tipo de proyecto: {tipo_proyecto}")
                if corto_plazo and corto_plazo not in ['nan', '-', 'x']:
                    desc_parts.append(f"Corto plazo: {corto_plazo}")
                if mediano_plazo and mediano_plazo not in ['nan', '-', 'x']:
                    desc_parts.append(f"Mediano plazo: {mediano_plazo}")
                if inv_participantes and inv_participantes not in ['-', 'nan']:
                    desc_parts.append(f"Investigadores: {inv_participantes}")
                if alumnos and alumnos not in ['-', 'nan']:
                    desc_parts.append(f"Alumnos: {alumnos}")
                
                descripcion = "\n\n".join(desc_parts) if desc_parts else None
                
                # Crear proyecto
                nuevo_proy = Proyecto(
                    clave_sip=clave_sip,
                    titulo=titulo,
                    descripcion=descripcion,
                    tipo=tipo_investigacion,
                    fuente_financiamiento="SIP - IPN",
                    fecha_inicio=date(2025, 1, 1),
                    fecha_fin=date(2025, 12, 31),
                    estatus="Aprobado",  # Marcar como Aprobado
                    responsable_id=inv_principal.id if inv_principal else None
                )
                
                # Agregar investigadores
                if inv_principal:
                    nuevo_proy.investigadores.append(inv_principal)
                
                # Agregar participantes
                if inv_participantes and inv_participantes not in ['-', 'nan']:
                    for nombre in inv_participantes.split(','):
                        nombre_norm = normalizar_nombre(nombre.strip())
                        if nombre_norm and nombre_norm in investigadores_db:
                            inv = investigadores_db[nombre_norm]
                            if inv not in nuevo_proy.investigadores:
                                nuevo_proy.investigadores.append(inv)
                
                session.add(nuevo_proy)
                session.flush()
                proyectos_creados += 1
                
                print(f"[{proyectos_creados}] {titulo[:60]}...")
                
            except Exception as e:
                print(f"[ERROR] Proyecto {index + 1}: {e}")
                continue
        
        # Commit
        session.commit()
        
        print(f"\n{'='*70}")
        print("[OK] IMPORTACION COMPLETADA - SOLO PROYECTOS APROBADOS")
        print(f"{'='*70}")
        print(f"Investigadores únicos: {len(investigadores_db)}")
        print(f"Proyectos APROBADOS importados: {proyectos_creados}")
        print(f"Proyectos RECHAZADOS (filtrados): {proyectos_rechazados}")
        
    except Exception as e:
        session.rollback()
        print(f"\n[ERROR] {e}")
        import traceback
        traceback.print_exc()
    finally:
        session.close()

if __name__ == "__main__":
    print("="*70)
    print("  IMPORTACION - SOLO PROYECTOS APROBADOS")
    print("  Instituto Politecnico Nacional")
    print("="*70)
    print()
    
    importar_solo_aprobados()
    
    print("\n[*] Base de datos actualizada con proyectos aprobados")
    print("[*] Reinicia el servidor para ver los cambios")

