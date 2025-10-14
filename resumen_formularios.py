#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Script simple para mostrar resumen de formularios"""

import json
import os
from pathlib import Path
from datetime import datetime

# Configurar encoding para Windows
import sys
if sys.platform == 'win32':
    import io
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

def main():
    formularios_dir = Path('formularios')
    
    if not formularios_dir.exists():
        print("Error: No existe el directorio 'formularios'")
        return
    
    archivos_json = list(formularios_dir.glob('*.json'))
    
    if not archivos_json:
        print("No hay formularios registrados")
        return
    
    formularios = []
    for archivo in archivos_json:
        try:
            with open(archivo, 'r', encoding='utf-8') as f:
                datos = json.load(f)
                formularios.append(datos)
        except Exception as e:
            print(f"Error leyendo {archivo.name}: {e}")
    
    print("\n" + "="*80)
    print("  RESUMEN DE FORMULARIOS RECIBIDOS - UPIIZ".center(80))
    print("="*80 + "\n")
    
    # Estadísticas
    total = len(formularios)
    con_proyecto = sum(1 for f in formularios if f.get('tieneProyectoVigente') == 'Si')
    con_edi = sum(1 for f in formularios if f.get('cuentaBecaEDI') == 'Si')
    con_snii = sum(1 for f in formularios if f.get('cuentaSNII') == 'Si')
    
    print("ESTADISTICAS GENERALES")
    print("-" * 80)
    print(f"  Total de registros:           {total}")
    print(f"  Con proyecto vigente:         {con_proyecto}")
    print(f"  Con beca EDI:                 {con_edi}")
    print(f"  Con nombramiento SNII:        {con_snii}")
    print()
    
    print("LISTADO DE INVESTIGADORES")
    print("-" * 80)
    
    for i, form in enumerate(formularios, 1):
        nombre = form.get('nombreCompleto', 'N/A')
        print(f"\n[{i}] {nombre}")
        print(f"    Clave: {form.get('claveEmpleado', 'N/A')}")
        print(f"    Email: {form.get('correoInstitucional', 'N/A')}")
        print(f"    Categoria: {form.get('categoria', 'N/A')}")
        
        if form.get('timestamp'):
            try:
                dt = datetime.fromisoformat(form['timestamp'])
                fecha = dt.strftime('%d/%m/%Y %H:%M')
                print(f"    Registrado: {fecha}")
            except:
                pass
        
        # Distinciones
        distinciones = []
        if form.get('tieneProyectoVigente') == 'Si':
            distinciones.append('Proyecto')
        if form.get('cuentaBecaEDI') == 'Si':
            distinciones.append(f"EDI {form.get('nivelEDI', '')}")
        if form.get('cuentaSNII') == 'Si':
            distinciones.append(f"SNII {form.get('nivelSNII', '')}")
        
        if distinciones:
            print(f"    {' | '.join(distinciones)}")
        
        # Proyectos
        if form.get('proyectosVigentes'):
            print(f"    Proyectos: {len(form['proyectosVigentes'])}")
            for proy in form['proyectosVigentes']:
                print(f"       - {proy.get('categoria', 'N/A')}: {proy.get('nombre', 'Sin nombre')}")
        
        # Líneas
        if form.get('lineasInvestigacion'):
            print(f"    Lineas de investigacion: {len(form['lineasInvestigacion'])}")
            for linea in form['lineasInvestigacion']:
                print(f"       - {linea}")
        
        # ORCID
        if form.get('orcid'):
            print(f"    ORCID: {form['orcid']}")
    
    print("\n" + "="*80 + "\n")

if __name__ == '__main__':
    main()

