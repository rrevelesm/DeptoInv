#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Script para generar Excel localmente desde los JSON
"""

import json
import os
import pandas as pd
from datetime import datetime
from pathlib import Path

# Configurar encoding para Windows
import sys
if sys.platform == 'win32':
    import io
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

def generar_excel():
    """Genera Excel con todos los formularios"""
    
    print("="*60)
    print("  GENERANDO EXCEL CON FORMULARIOS".center(60))
    print("="*60)
    print()
    
    formularios_dir = Path('formularios')
    
    if not formularios_dir.exists():
        print("Error: No existe el directorio 'formularios'")
        return
    
    archivos = [f for f in formularios_dir.glob('*.json')]
    
    if not archivos:
        print("No hay formularios para exportar")
        return
    
    print(f"Procesando {len(archivos)} formularios...")
    print()
    
    datos_investigadores = []
    
    for archivo in archivos:
        try:
            with open(archivo, 'r', encoding='utf-8') as f:
                datos = json.load(f)
            
            # Construir nombre completo (manejar formato nuevo y viejo)
            nombre_completo = datos.get('nombreCompleto')
            if not nombre_completo or nombre_completo == 'N/A':
                nombres = datos.get('nombres', '')
                apellido_pat = datos.get('apellidoPaterno', '')
                apellido_mat = datos.get('apellidoMaterno', '')
                nombre_completo = f"{nombres} {apellido_pat} {apellido_mat}".strip()
            
            # Procesar proyectos
            proyectos_texto = []
            if datos.get('proyectosVigentes'):
                for proy in datos['proyectosVigentes']:
                    proyectos_texto.append(f"{proy.get('categoria', 'N/A')}: {proy.get('nombre', 'N/A')}")
            proyectos_str = '\n'.join(proyectos_texto) if proyectos_texto else 'Sin proyectos'
            
            # Procesar líneas
            lineas_str = '\n'.join(datos.get('lineasInvestigacion', [])) if datos.get('lineasInvestigacion') else 'N/A'
            
            # Procesar publicaciones
            pubs_texto = []
            if datos.get('publicaciones2025'):
                for pub in datos['publicaciones2025']:
                    pubs_texto.append(f"{pub.get('tipo', 'N/A')}: {pub.get('doi', 'N/A')}")
            pubs_str = '\n'.join(pubs_texto) if pubs_texto else 'Sin publicaciones 2025'
            
            # Procesar redes
            redes_texto = []
            if datos.get('participaRedes') == 'Si':
                if datos.get('red1Nombre'):
                    redes_texto.append(f"Red 1: {datos.get('red1Nombre')} - {datos.get('red1Rol', 'N/A')}")
                if datos.get('red2Nombre'):
                    redes_texto.append(f"Red 2: {datos.get('red2Nombre')} - {datos.get('red2Rol', 'N/A')}")
            redes_str = '\n'.join(redes_texto) if redes_texto else 'No participa'
            
            fila = {
                'Nombre Completo': nombre_completo or 'N/A',
                'CURP': datos.get('curp', ''),
                'Fecha Nacimiento': datos.get('fechaNacimiento', ''),
                'Género': datos.get('genero', ''),
                'Clave Empleado': datos.get('claveEmpleado', ''),
                'Categoría': datos.get('categoria', ''),
                'Tipo Plaza': datos.get('tipoPlaza', ''),
                'Horas Contratación': datos.get('horasContratacion', ''),
                'Fecha Ingreso IPN': datos.get('fechaIngresoIPN', ''),
                'CVU': datos.get('cvu', ''),
                'Correo Institucional': datos.get('correoInstitucional', ''),
                'Teléfono': datos.get('telefonoCelular', '') if datos.get('aceptaContacto') == 'Si' else 'No proporcionado',
                'Tiene Proyecto': datos.get('tieneProyectoVigente', 'No'),
                'Proyectos': proyectos_str,
                'Beca EDI': datos.get('nivelEDI', '') if datos.get('cuentaBecaEDI') == 'Si' else 'No',
                'EDI Vigencia': f"{datos.get('ediInicio', '')} - {datos.get('ediFinal', '')}" if datos.get('cuentaBecaEDI') == 'Si' else 'N/A',
                'SNII': datos.get('nivelSNII', '') if datos.get('cuentaSNII') == 'Si' else 'No',
                'SNII Vigencia': f"{datos.get('sniiInicio', '')} - {datos.get('sniiFinal', '')}" if datos.get('cuentaSNII') == 'Si' else 'N/A',
                'Participa Redes': datos.get('participaRedes', 'No'),
                'Redes IPN': redes_str,
                'ORCID': datos.get('orcid', ''),
                'Líneas Investigación': lineas_str,
                'Publicaciones 2025': pubs_str,
                'Sugerencias': datos.get('sugerencias', ''),
                'Fecha Registro': datos.get('timestamp', '')
            }
            
            datos_investigadores.append(fila)
            print(f"  [OK] {nombre_completo or 'Sin nombre'} ({datos.get('claveEmpleado', 'N/A')})")
            
        except Exception as e:
            print(f"  [ERROR] {archivo.name}: {e}")
            continue
    
    if not datos_investigadores:
        print("\nNo se pudo procesar ningún formulario")
        return
    
    print()
    print("Creando archivo Excel...")
    
    # Crear DataFrame
    df = pd.DataFrame(datos_investigadores)
    df = df.sort_values('Fecha Registro', ascending=False)
    
    # Crear archivo Excel
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    nombre_excel = f'Formularios_Investigadores_UPIIZ_{timestamp}.xlsx'
    
    try:
        with pd.ExcelWriter(nombre_excel, engine='openpyxl') as writer:
            df.to_excel(writer, sheet_name='Investigadores', index=False)
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
        
        print()
        print("="*60)
        print("ARCHIVO EXCEL CREADO EXITOSAMENTE")
        print("="*60)
        print(f"Archivo: {nombre_excel}")
        print(f"Ubicacion: {os.path.abspath(nombre_excel)}")
        print(f"Registros: {len(datos_investigadores)}")
        print("="*60)
        print()
        print("El archivo Excel incluye:")
        print("  - Datos personales completos")
        print("  - Proyectos vigentes")
        print("  - Distinciones (EDI, SNII)")
        print("  - Redes de investigacion IPN")
        print("  - Lineas de investigacion")
        print("  - Publicaciones 2025")
        print("  - ORCID y sugerencias")
        print()
        
        # Abrir el archivo automáticamente
        print("Abriendo archivo Excel...")
        os.startfile(nombre_excel)
        
    except Exception as e:
        print(f"\nError al crear Excel: {e}")

if __name__ == '__main__':
    try:
        generar_excel()
    except Exception as e:
        print(f"Error: {e}")
    
    input("\nPresiona Enter para salir...")

