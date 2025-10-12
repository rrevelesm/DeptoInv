"""
Script para exportar todos los formularios de investigadores a Excel
Ejecutar: python exportar_formularios_excel.py
"""

import sys
import io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

import json
import os
import pandas as pd
from datetime import datetime

def exportar_formularios_a_excel():
    """Lee todos los formularios JSON y los exporta a Excel"""
    
    formularios_dir = 'formularios'
    
    if not os.path.exists(formularios_dir):
        print("[!] No existe la carpeta 'formularios'")
        print("[*] Aún no se han recibido formularios")
        return
    
    # Leer todos los archivos JSON
    archivos_json = [f for f in os.listdir(formularios_dir) if f.endswith('.json')]
    
    if not archivos_json:
        print("[!] No hay formularios para exportar")
        return
    
    print(f"[*] Encontrados {len(archivos_json)} formularios")
    print("[*] Procesando datos...\n")
    
    datos_investigadores = []
    
    for archivo in archivos_json:
        try:
            ruta = os.path.join(formularios_dir, archivo)
            with open(ruta, 'r', encoding='utf-8') as f:
                datos = json.load(f)
            
            # Procesar proyectos vigentes
            proyectos_texto = []
            if 'proyectosVigentes' in datos and datos['proyectosVigentes']:
                for proy in datos['proyectosVigentes']:
                    proyectos_texto.append(f"{proy.get('categoria', 'N/A')}: {proy.get('nombre', 'N/A')}")
            proyectos_str = '\n'.join(proyectos_texto) if proyectos_texto else 'Sin proyectos'
            
            # Procesar líneas de investigación
            lineas_str = '\n'.join(datos.get('lineasInvestigacion', [])) if datos.get('lineasInvestigacion') else 'N/A'
            
            # Procesar publicaciones 2025
            pubs_texto = []
            if 'publicaciones2025' in datos and datos['publicaciones2025']:
                for pub in datos['publicaciones2025']:
                    pubs_texto.append(f"{pub.get('tipo', 'N/A')}: {pub.get('doi', 'N/A')}")
            pubs_str = '\n'.join(pubs_texto) if pubs_texto else 'Sin publicaciones 2025'
            
            # Crear fila de datos
            fila = {
                # Datos personales
                'Nombre Completo': datos.get('nombreCompleto', ''),
                'CURP': datos.get('curp', ''),
                'Fecha Nacimiento': datos.get('fechaNacimiento', ''),
                'Género': datos.get('genero', ''),
                'Clave Empleado': datos.get('claveEmpleado', ''),
                'Categoría': datos.get('categoria', ''),
                'Correo Institucional': datos.get('correoInstitucional', ''),
                'Acepta Contacto Telefónico': datos.get('aceptaContacto', 'No'),
                'Teléfono Celular': datos.get('telefonoCelular', '') if datos.get('aceptaContacto') == 'Si' else 'N/A',
                
                # Proyectos vigentes
                'Tiene Proyecto Vigente': datos.get('tieneProyectoVigente', 'No'),
                'Proyectos': proyectos_str,
                
                # Beca EDI
                'Tiene Beca EDI': datos.get('cuentaBecaEDI', 'No'),
                'Nivel EDI': datos.get('nivelEDI', '') if datos.get('cuentaBecaEDI') == 'Si' else 'N/A',
                
                # SNII
                'Tiene SNII': datos.get('cuentaSNII', 'No'),
                'Nivel SNII': datos.get('nivelSNII', '') if datos.get('cuentaSNII') == 'Si' else 'N/A',
                'SNII Inicio': datos.get('sniiInicio', '') if datos.get('cuentaSNII') == 'Si' else 'N/A',
                'SNII Término': datos.get('sniiFinal', '') if datos.get('cuentaSNII') == 'Si' else 'N/A',
                'Constancia SNII': datos.get('sniiConstanciaArchivo', '') if datos.get('cuentaSNII') == 'Si' else 'N/A',
                
                # ORCID
                'ORCID': datos.get('orcid', ''),
                
                # Líneas de investigación
                'Líneas de Investigación': lineas_str,
                
                # Productividad 2025
                'Publicaciones 2025': pubs_str,
                
                # Metadata
                'Fecha Registro': datos.get('timestamp', ''),
                'Archivo JSON': archivo
            }
            
            datos_investigadores.append(fila)
            print(f"[✓] {datos.get('nombreCompleto', 'Sin nombre')}")
            
        except Exception as e:
            print(f"[ERROR] {archivo}: {e}")
            continue
    
    if not datos_investigadores:
        print("[!] No se pudieron procesar formularios")
        return
    
    # Crear DataFrame
    df = pd.DataFrame(datos_investigadores)
    
    # Ordenar por fecha de registro
    df = df.sort_values('Fecha Registro', ascending=False)
    
    # Generar nombre de archivo con timestamp
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    nombre_excel = f'Formularios_Investigadores_UPIIZ_{timestamp}.xlsx'
    
    # Exportar a Excel con formato
    with pd.ExcelWriter(nombre_excel, engine='openpyxl') as writer:
        df.to_excel(writer, sheet_name='Investigadores', index=False)
        
        # Obtener worksheet para formato
        worksheet = writer.sheets['Investigadores']
        
        # Ajustar ancho de columnas
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
    
    print(f"\n{'='*70}")
    print(f"[OK] EXPORTACIÓN COMPLETADA")
    print(f"{'='*70}")
    print(f"Total de investigadores: {len(datos_investigadores)}")
    print(f"Archivo generado: {nombre_excel}")
    print(f"\n[*] Archivo Excel creado exitosamente")
    print(f"[*] Ubicación: {os.path.abspath(nombre_excel)}")

if __name__ == "__main__":
    print("="*70)
    print("  EXPORTACIÓN DE FORMULARIOS A EXCEL")
    print("  UPIIZ - Departamento de Investigación")
    print("="*70)
    print()
    
    exportar_formularios_a_excel()

