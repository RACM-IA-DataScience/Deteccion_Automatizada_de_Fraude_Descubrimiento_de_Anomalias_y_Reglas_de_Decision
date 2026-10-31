# -*- coding: utf-8 -*-
"""
Script Maestro de Compilación Oficial de Entregables:
1. Documento Técnico del Proyecto KDD (Markdown y PDF Oficial de 9 Páginas).
2. Catálogo y Diccionario de Funciones KDD (Markdown y PDF Oficial de 8 Páginas).
"""

import subprocess
import sys
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent

print("=" * 70)
print("COMPILACIÓN OFICIAL DE ENTREGABLES KDD (DOCUMENTO TÉCNICO Y DICCIONARIO)")
print("=" * 70)

# 1. Generar Markdown
print("\n[1/3] Generando archivos Markdown...")
res_md = subprocess.run([sys.executable, str(BASE_DIR / "build_markdown_docs.py")], capture_output=True, text=True)
print(res_md.stdout)
if res_md.returncode != 0:
    print("Error:", res_md.stderr)

# 2. Compilar PDF Documento Técnico
print("\n[2/3] Compilando Documento Técnico PDF (9 Páginas)...")
res_dt = subprocess.run([sys.executable, str(BASE_DIR / "compilar_documento_tecnico_pdf.py")], capture_output=True, text=True)
print(res_dt.stdout)
if res_dt.returncode != 0:
    print("Error:", res_dt.stderr)

# 3. Compilar PDF Diccionario de Funciones
print("\n[3/3] Compilando Diccionario de Funciones PDF (8 Páginas)...")
res_df = subprocess.run([sys.executable, str(BASE_DIR / "compilar_diccionario_funciones_pdf.py")], capture_output=True, text=True)
print(res_df.stdout)
if res_df.returncode != 0:
    print("Error:", res_df.stderr)

print("=" * 70)
print("PROCESO COMPLETADO EXITOSAMENTE.")
print("=" * 70)
