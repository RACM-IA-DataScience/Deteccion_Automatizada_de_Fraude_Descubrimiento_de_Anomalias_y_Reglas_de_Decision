"""
Paquete modular KDD para Detección Automatizada de Fraude en Tarjetas de Crédito (2026).
Divide el proceso completo de Knowledge Discovery in Databases en 4 módulos cohesivos:
  1. fase1_seleccion_y_limpieza: Etapas 1, 2 y 3 (Selección, Auditoría Data Leakage, Limpieza e IQR)
  2. fase2_transformacion_y_seleccion: Etapa 4 (Feature Engineering, Split 80/20, Log1p+RobustScaler, Chi2)
  3. fase3_mineria_anomalias_y_clasificacion: Etapa 5 (Isolation Forest, SMOTE y Entrenamiento de Modelos)
  4. fase4_evaluacion_y_reglas_decision: Etapas 6 y 7 (Evaluación ROC/PR, Importancia Gini y Reglas de Decisión)
"""
