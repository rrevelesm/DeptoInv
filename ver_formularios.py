#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Script para ver formularios recibidos sin necesidad del servidor web
Autor: Sistema de Gestión UPIIZ
Fecha: 2025-10-14
"""

import json
import os
from datetime import datetime
from pathlib import Path

def leer_formularios():
    """Lee todos los formularios JSON del directorio"""
    formularios_dir = Path('formularios')
    
    if not formularios_dir.exists():
        print("❌ Error: No existe el directorio 'formularios'")
        return []
    
    archivos_json = list(formularios_dir.glob('*.json'))
    
    if not archivos_json:
        print("📋 No hay formularios registrados todavía")
        return []
    
    formularios = []
    for archivo in archivos_json:
        try:
            with open(archivo, 'r', encoding='utf-8') as f:
                datos = json.load(f)
                datos['_archivo'] = archivo.name
                formularios.append(datos)
        except Exception as e:
            print(f"⚠️  Error leyendo {archivo.name}: {e}")
    
    return formularios

def formatear_fecha(timestamp_str):
    """Formatea timestamp a fecha legible"""
    try:
        dt = datetime.fromisoformat(timestamp_str)
        return dt.strftime('%d/%m/%Y %H:%M')
    except:
        return timestamp_str

def mostrar_resumen(formularios):
    """Muestra resumen de todos los formularios"""
    print("\n" + "="*80)
    print("📊 RESUMEN DE FORMULARIOS RECIBIDOS - UPIIZ".center(80))
    print("="*80 + "\n")
    
    # Estadísticas generales
    total = len(formularios)
    con_proyecto = sum(1 for f in formularios if f.get('tieneProyectoVigente') == 'Si')
    con_edi = sum(1 for f in formularios if f.get('cuentaBecaEDI') == 'Si')
    con_snii = sum(1 for f in formularios if f.get('cuentaSNII') == 'Si')
    
    print("📈 ESTADÍSTICAS GENERALES")
    print("-" * 80)
    print(f"  Total de registros:           {total}")
    print(f"  Con proyecto vigente:         {con_proyecto} ({con_proyecto/total*100:.1f}%)")
    print(f"  Con beca EDI:                 {con_edi} ({con_edi/total*100:.1f}%)")
    print(f"  Con nombramiento SNII:        {con_snii} ({con_snii/total*100:.1f}%)")
    print()
    
    # Ordenar por fecha
    formularios_ordenados = sorted(
        formularios, 
        key=lambda x: x.get('timestamp', ''), 
        reverse=True
    )
    
    print("📋 LISTADO DE INVESTIGADORES")
    print("-" * 80)
    
    for i, form in enumerate(formularios_ordenados, 1):
        # Obtener nombre completo (manejar formatos nuevo y viejo)
        nombre = form.get('nombreCompleto') or \
                f"{form.get('nombres', '')} {form.get('apellidoPaterno', '')} {form.get('apellidoMaterno', '')}".strip()
        
        print(f"\n[{i}] {nombre}")
        print(f"    🆔 Clave: {form.get('claveEmpleado', 'N/A')}")
        print(f"    📧 Email: {form.get('correoInstitucional', 'N/A')}")
        print(f"    🎓 Categoría: {form.get('categoria', 'N/A')}")
        
        # Fecha de registro
        if form.get('timestamp'):
            print(f"    📅 Registrado: {formatear_fecha(form['timestamp'])}")
        
        # Distinciones
        distinciones = []
        if form.get('tieneProyectoVigente') == 'Si':
            distinciones.append('📊 Proyecto')
        if form.get('cuentaBecaEDI') == 'Si':
            distinciones.append(f"💰 EDI {form.get('nivelEDI', '')}")
        if form.get('cuentaSNII') == 'Si':
            distinciones.append(f"🏆 SNII {form.get('nivelSNII', '')}")
        
        if distinciones:
            print(f"    {' | '.join(distinciones)}")
        
        # Proyectos
        if form.get('proyectosVigentes'):
            print(f"    📊 Proyectos: {len(form['proyectosVigentes'])}")
            for proy in form['proyectosVigentes']:
                print(f"       • {proy.get('categoria', 'N/A')}: {proy.get('nombre', 'Sin nombre')[:50]}")
        
        # Líneas de investigación
        if form.get('lineasInvestigacion'):
            print(f"    🔬 Líneas de investigación: {len(form['lineasInvestigacion'])}")
        
        # Publicaciones 2025
        if form.get('publicaciones2025'):
            print(f"    📚 Publicaciones 2025: {len(form['publicaciones2025'])}")
        
        # ORCID
        if form.get('orcid'):
            print(f"    🔗 ORCID: {form['orcid']}")

def mostrar_detalle(formularios):
    """Muestra detalle de un investigador específico"""
    print("\n" + "="*80)
    print("🔍 VER DETALLE DE INVESTIGADOR".center(80))
    print("="*80 + "\n")
    
    for i, form in enumerate(formularios, 1):
        nombre = form.get('nombreCompleto') or \
                f"{form.get('nombres', '')} {form.get('apellidoPaterno', '')}".strip()
        print(f"[{i}] {nombre} - {form.get('claveEmpleado', 'N/A')}")
    
    try:
        seleccion = int(input("\nSelecciona el número del investigador (0 para salir): "))
        
        if seleccion == 0:
            return
        
        if 1 <= seleccion <= len(formularios):
            form = formularios[seleccion - 1]
            print("\n" + "="*80)
            print(json.dumps(form, indent=2, ensure_ascii=False))
            print("="*80)
        else:
            print("❌ Número inválido")
    except ValueError:
        print("❌ Entrada inválida")
    except KeyboardInterrupt:
        print("\n\n👋 Saliendo...")

def menu_principal():
    """Menú principal interactivo"""
    formularios = leer_formularios()
    
    if not formularios:
        print("\n📭 No hay formularios para mostrar")
        input("\nPresiona Enter para salir...")
        return
    
    while True:
        print("\n" + "="*80)
        print("🎓 PANEL DE FORMULARIOS - UPIIZ".center(80))
        print("="*80)
        print("\n[1] Ver resumen de todos los formularios")
        print("[2] Ver detalle de un investigador específico")
        print("[3] Exportar a Excel (requiere pandas)")
        print("[0] Salir")
        
        try:
            opcion = input("\nSelecciona una opción: ").strip()
            
            if opcion == '0':
                print("\n👋 ¡Hasta luego!")
                break
            elif opcion == '1':
                mostrar_resumen(formularios)
                input("\n\n📌 Presiona Enter para continuar...")
            elif opcion == '2':
                mostrar_detalle(formularios)
                input("\n\n📌 Presiona Enter para continuar...")
            elif opcion == '3':
                exportar_excel(formularios)
                input("\n\n📌 Presiona Enter para continuar...")
            else:
                print("❌ Opción no válida")
        except KeyboardInterrupt:
            print("\n\n👋 ¡Hasta luego!")
            break

def exportar_excel(formularios):
    """Exporta formularios a Excel"""
    try:
        import pandas as pd
        from datetime import datetime as dt
        
        print("\n📊 Exportando a Excel...")
        
        datos_investigadores = []
        
        for form in formularios:
            # Nombre completo
            nombre = form.get('nombreCompleto') or \
                    f"{form.get('nombres', '')} {form.get('apellidoPaterno', '')} {form.get('apellidoMaterno', '')}".strip()
            
            # Procesar proyectos
            proyectos_texto = []
            if form.get('proyectosVigentes'):
                for proy in form['proyectosVigentes']:
                    proyectos_texto.append(f"{proy.get('categoria', 'N/A')}: {proy.get('nombre', 'N/A')}")
            proyectos_str = '\n'.join(proyectos_texto) if proyectos_texto else 'Sin proyectos'
            
            # Procesar líneas
            lineas_str = '\n'.join(form.get('lineasInvestigacion', [])) if form.get('lineasInvestigacion') else 'N/A'
            
            # Procesar publicaciones
            pubs_texto = []
            if form.get('publicaciones2025'):
                for pub in form['publicaciones2025']:
                    pubs_texto.append(f"{pub.get('tipo', 'N/A')}: {pub.get('doi', 'N/A')}")
            pubs_str = '\n'.join(pubs_texto) if pubs_texto else 'Sin publicaciones 2025'
            
            fila = {
                'Nombre Completo': nombre,
                'CURP': form.get('curp', ''),
                'Fecha Nacimiento': form.get('fechaNacimiento', ''),
                'Género': form.get('genero', ''),
                'Clave Empleado': form.get('claveEmpleado', ''),
                'Categoría': form.get('categoria', ''),
                'Correo Institucional': form.get('correoInstitucional', ''),
                'Teléfono': form.get('telefonoCelular', '') if form.get('aceptaContacto') == 'Si' else 'N/A',
                'Tiene Proyecto': form.get('tieneProyectoVigente', 'No'),
                'Proyectos': proyectos_str,
                'Beca EDI': form.get('nivelEDI', '') if form.get('cuentaBecaEDI') == 'Si' else 'No',
                'SNII': form.get('nivelSNII', '') if form.get('cuentaSNII') == 'Si' else 'No',
                'SNII Vigencia': f"{form.get('sniiInicio', '')} - {form.get('sniiFinal', '')}" if form.get('cuentaSNII') == 'Si' else 'N/A',
                'ORCID': form.get('orcid', ''),
                'Líneas Investigación': lineas_str,
                'Publicaciones 2025': pubs_str,
                'Fecha Registro': form.get('timestamp', '')
            }
            
            datos_investigadores.append(fila)
        
        df = pd.DataFrame(datos_investigadores)
        df = df.sort_values('Fecha Registro', ascending=False)
        
        # Crear archivo Excel
        timestamp = dt.now().strftime('%Y%m%d_%H%M%S')
        nombre_excel = f'Formularios_Investigadores_UPIIZ_{timestamp}.xlsx'
        
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
        
        print(f"\n✅ Archivo exportado: {nombre_excel}")
        print(f"📂 Ubicación: {os.path.abspath(nombre_excel)}")
        
    except ImportError:
        print("\n❌ Error: pandas no está instalado")
        print("💡 Instala con: pip install pandas openpyxl")
    except Exception as e:
        print(f"\n❌ Error al exportar: {e}")

if __name__ == '__main__':
    # Configurar encoding para Windows
    import sys
    if sys.platform == 'win32':
        import io
        sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
    
    try:
        menu_principal()
    except KeyboardInterrupt:
        print("\n\n¡Hasta luego!")
    except Exception as e:
        print(f"\nError inesperado: {e}")
        input("\nPresiona Enter para salir...")

