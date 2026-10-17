"""
Orquestador Principal de la Arquitectura Modular KDD
Ubicación: Entrega Modular de Ingeniería de Software en Python/orquestador_modular_kdd.py
Ejecuta secuencialmente los 4 módulos especializados del proyecto integrador:
  - Módulo 1: Selección de Datos, Limpieza y Diagnóstico de Outliers (Etapas 1-3 KDD)
  - Módulo 2: Transformación, Ingeniería de Señales Débiles y Selección χ² (Etapa 4 KDD)
  - Módulo 3: Minería de Anomalías (Isolation Forest), SMOTE y Clasificación (Etapa 5 KDD)
  - Módulo 4: Evaluación Multi-Métrica, Interpretación y Reglas de Decisión (Etapas 6-7 KDD)
"""

import sys
from pathlib import Path

# Asegura que el directorio actual de módulos esté en sys.path
MODULOS_DIR = Path(__file__).resolve().parent
PROJECT_ROOT = MODULOS_DIR.parent
if str(MODULOS_DIR) not in sys.path:
    sys.path.insert(0, str(MODULOS_DIR))

from fase1_seleccion_y_limpieza import (
    cargar_y_seleccionar_datos,
    limpiar_y_diagnosticar_outliers,
)
from fase2_transformacion_y_seleccion import transformar_y_particionar
from fase3_mineria_anomalias_y_clasificacion import ejecutar_mineria_datos
from fase4_evaluacion_y_reglas_decision import evaluar_e_interpretar_conocimiento


def main():
    csv_path = PROJECT_ROOT / "Datasets" / "credit_card_fraud_detection_2026.csv"
    out_dir = PROJECT_ROOT / "Resultados"

    # Fase 1 (Etapas 1, 2 y 3 KDD)
    _, df_seleccionado = cargar_y_seleccionar_datos(csv_path, out_dir)
    df_limpio, _ = limpiar_y_diagnosticar_outliers(df_seleccionado, out_dir)

    # Fase 2 (Etapa 4 KDD)
    datos_etapa4 = transformar_y_particionar(df_limpio)

    # Fase 3 (Etapa 5 KDD)
    datos_etapa5 = ejecutar_mineria_datos(datos_etapa4, out_dir)

    # Fase 4 (Etapas 6 y 7 KDD)
    evaluar_e_interpretar_conocimiento(datos_etapa4, datos_etapa5, out_dir)

    print("\n" + "=" * 88)
    print(f"[OK] Orquestación modular KDD finalizada con éxito. Resultados en: {out_dir}")
    print("=" * 88)


if __name__ == "__main__":
    main()
