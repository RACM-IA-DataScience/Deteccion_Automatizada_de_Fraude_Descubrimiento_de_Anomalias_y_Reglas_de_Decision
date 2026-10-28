# -*- coding: utf-8 -*-
"""
Generador del Documento PDF Oficial Completo (11 Páginas):
'Reporte_Avance_Proyecto_Integrador_KDD.pdf'
Formato gráfico oficial del template (Montserrat, violeta/lavanda, tarjetas y fondos a sangre),
100% en español (sin mezcla de idiomas) y cubriendo exhaustivamente las 7 etapas KDD:

Pág 1: Portada Institucional Cyber (Fondo azul red, tipografía Montserrat y escudo UdeG)
Pág 2: Datos Generales, Dataset y Contexto del Problema (Etapa 1 KDD)
Pág 3: Objetivos del Proyecto, Meta Principal y Consideraciones Críticas (Etapas 1 y 2 KDD)
Pág 4: Etapa 3 KDD — Limpieza de Datos (Diagnóstico de Calidad, Ausencia Estructural y Fig 1)
Pág 5: Etapa 3 KDD — Limpieza de Datos (Valores Atípicos Tukey, Fraud Lift, Decisiones y Fig 2)
Pág 6: Etapa 4 KDD — Transformación de Datos (Ingeniería de 8 Variables Derivadas y Fig 3)
Pág 7: Etapa 4 KDD — Transformación de Datos (Partición 80/20, Anti-Fuga, Escalamiento y Fig 4)
Pág 8: Etapa 4 KDD — Transformación de Datos (Selección por Dos Métodos de Filtro y Fig 5)
Pág 9: Etapa 5 KDD — Minería de Datos (Validación Cruzada 5-Fold Libre de Fuga y Fig 6)
Pág 10: Desafíos Técnicos Enfrentados y Logros Alcanzados en la Preparación de Datos
Pág 11: Etapas 6 y 7 KDD — Evaluación, Interpretación y Recomendaciones de Negocio
"""

import os
import base64
import subprocess
from pathlib import Path
import pypdf

# 1. Cargar assets del template y figuras del avance en base64
ASSET_DIR = Path("Entregables/template_assets")
FIG_DIR = Path("Entregables/figuras_avance")

assets = {}

# 1. Logo institucional UdeG
with open(ASSET_DIR / "udeg_logo.png", "rb") as f:
    assets["udeg_logo.png"] = base64.b64encode(f.read()).decode("utf-8")

# 2. Imágenes temáticas oficiales del proyecto (Fintech, Ciberseguridad bancaria, Minería de Datos)
PROJ_IMG_DIR = Path("Entregables/imagenes_proyecto")
for fname in [
    "portada_fraude_tarjetas.jpg",
    "transacciones_anomalias.jpg",
    "mineria_datos_forense.jpg",
    "escudo_decision_fraude.jpg",
]:
    p = PROJ_IMG_DIR / fname
    with open(p, "rb") as f:
        assets[fname] = base64.b64encode(f.read()).decode("utf-8")

# Figuras de alta resolución del avance
for fname in [
    "fig01_diagnostico_target_y_nulos.png",
    "fig02_diagnostico_outliers_iqr.png",
    "fig03_ingenieria_caracteristicas.png",
    "fig04_escalamiento_robusto_sin_leakage.png",
    "fig05_comparativa_dos_metodos_filtro.png",
    "fig06_validacion_cruzada_5fold.png",
]:
    p = FIG_DIR / fname
    with open(p, "rb") as f:
        assets[fname] = base64.b64encode(f.read()).decode("utf-8")

html_content = """<!DOCTYPE html>
<html lang="es">
<head>
<meta charset="UTF-8">
<title>Reporte de Avance Proyecto Integrador (Metodología KDD) — Roberto Alejandro Chagra Martínez</title>
<style>
  @import url('https://fonts.googleapis.com/css2?family=Montserrat:ital,wght@0,300;0,400;0,500;0,600;0,700;0,800;1,400;1,700&display=swap');

  @page {
    size: 8.5in 11in;
    margin: 0;
  }

  *, *:before, *:after {
    box-sizing: border-box;
  }

  body {
    margin: 0;
    padding: 0;
    font-family: 'Montserrat', sans-serif;
    color: #1e293b;
    background-color: #ffffff;
    -webkit-print-color-adjust: exact;
    print-color-adjust: exact;
  }

  .slide-page {
    width: 8.5in;
    height: 11in;
    position: relative;
    page-break-after: always;
    break-after: page;
    overflow: hidden;
    background-color: #ffffff;
  }

  .slide-page:last-child {
    page-break-after: avoid;
    break-after: avoid;
  }

  /* Encabezados estándar */
  .header-box {
    margin-bottom: 12px;
  }

  .section-h1 {
    font-size: 19pt;
    font-weight: 800;
    color: #6c5ce7;
    margin: 0 0 4px 0;
    display: inline-block;
    border-bottom: 3.5px solid #a29bfe;
    padding-bottom: 3px;
  }

  .kdd-tag {
    font-size: 8.5pt;
    font-weight: 700;
    background: #6c5ce7;
    color: #ffffff;
    padding: 3px 8px;
    border-radius: 4px;
    text-transform: uppercase;
    letter-spacing: 0.5px;
    margin-left: 10px;
    vertical-align: middle;
  }

  .definition-box {
    background: #f0fdf4;
    border-left: 4px solid #16a34a;
    padding: 6px 10px;
    font-size: 8.4pt;
    color: #14532d;
    margin: 6px 0 10px 0;
    border-radius: 0 4px 4px 0;
  }

  p {
    font-size: 8.7pt;
    line-height: 1.40;
    color: #2d3436;
    margin: 0 0 7px 0;
    text-align: justify;
  }

  ul, ol {
    margin: 2px 0 8px 18px;
    padding: 0;
    font-size: 8.6pt;
    line-height: 1.38;
    color: #2d3436;
  }

  li {
    margin-bottom: 4px;
    text-align: justify;
  }

  /* Tablas de datos ejecutivas */
  table.data-table {
    width: 100%;
    border-collapse: collapse;
    margin: 7px 0 9px 0;
    font-size: 7.7pt;
  }

  table.data-table th {
    background-color: #0f172a;
    color: #ffffff;
    font-weight: 700;
    text-align: left;
    padding: 4.5px 6px;
    border: 1px solid #0f172a;
  }

  table.data-table td {
    padding: 3.8px 6px;
    border: 1px solid #e2e8f0;
  }

  table.data-table tr:nth-child(even) {
    background-color: #f8fafc;
  }

  table.data-table tr.highlight {
    background-color: #fef3c7;
    font-weight: 600;
  }

  /* Callouts de justificación */
  .callout-box {
    border-radius: 6px;
    padding: 7px 12px;
    margin: 7px 0;
    font-size: 8.3pt;
    line-height: 1.38;
  }

  .callout-info {
    background-color: #f0f9ff;
    border-left: 4px solid #0284c7;
    color: #0c4a6e;
  }

  .callout-warning {
    background-color: #fffbeb;
    border-left: 4px solid #f59e0b;
    color: #78350f;
  }

  .callout-success {
    background-color: #f0fdf4;
    border-left: 4px solid #16a34a;
    color: #14532d;
  }

  /* Cajas de figuras embebidas */
  .figure-container {
    text-align: center;
    margin: 7px auto;
  }

  .figure-container img {
    max-height: 70mm;
    width: auto;
    max-width: 98%;
    border-radius: 6px;
    border: 1px solid #cbd5e1;
    box-shadow: 0 2px 6px rgba(0,0,0,0.06);
  }

  .figure-caption {
    font-size: 7.5pt;
    color: #64748b;
    margin-top: 3px;
    font-style: italic;
  }

  /* Métricas en tarjetas */
  .metric-row {
    display: flex;
    justify-content: space-between;
    margin: 7px 0;
  }

  .metric-card {
    flex: 1;
    background: #f8fafc;
    border: 1px solid #e2e8f0;
    border-radius: 6px;
    padding: 6px 8px;
    margin: 0 4px;
    text-align: center;
  }

  .metric-card:first-child { margin-left: 0; }
  .metric-card:last-child { margin-right: 0; }

  .metric-val {
    font-size: 12.5pt;
    font-weight: 800;
    color: #6c5ce7;
    margin-bottom: 2px;
  }

  .metric-lbl {
    font-size: 7.2pt;
    color: #475569;
    text-transform: uppercase;
    font-weight: 700;
  }

  /* Layout de página estándar con márgenes seguros */
  .page-padding {
    padding: 0.65in 0.85in;
    height: 11in;
    box-sizing: border-box;
  }

  /* ================= ESTILOS ESPECÍFICOS DE DIAPOSITIVAS ================= */

  /* PÁGINA 1: PORTADA */
  .p1-bg {
    position: absolute;
    top: 0;
    left: 0;
    width: 8.5in;
    height: 11in;
    object-fit: cover;
    z-index: 1;
    filter: brightness(0.68) contrast(1.15);
  }

  .p1-overlay {
    position: absolute;
    top: 0;
    left: 0;
    width: 8.5in;
    height: 11in;
    background: linear-gradient(135deg, rgba(15, 23, 42, 0.72) 0%, rgba(108, 92, 231, 0.32) 55%, rgba(15, 23, 42, 0.85) 100%);
    z-index: 2;
  }

  .p1-content {
    position: absolute;
    top: 0;
    left: 0;
    width: 8.5in;
    height: 11in;
    z-index: 3;
    padding: 1.8in 0.9in 0.9in 0.9in;
    display: flex;
    flex-direction: column;
    justify-content: space-between;
  }

  .p1-title-avance {
    font-size: 44pt;
    font-weight: 800;
    color: #ffffff;
    letter-spacing: 3px;
    line-height: 1.05;
    margin: 0;
  }

  .p1-title-sub {
    font-size: 38pt;
    font-weight: 300;
    color: #ffffff;
    letter-spacing: 4px;
    line-height: 1.05;
    margin: 0;
  }

  .p1-line {
    width: 330px;
    height: 5px;
    background-color: #a29bfe;
    margin-top: 18px;
    border-radius: 3px;
  }

  .p1-subtitle-box {
    margin-top: 25px;
    font-size: 13.5pt;
    font-weight: 600;
    color: #e0e7ff;
    line-height: 1.35;
    max-width: 85%;
  }

  .p1-footer {
    display: flex;
    align-items: center;
    margin-bottom: 0.3in;
  }

  .p1-logo {
    height: 75px;
    width: auto;
    margin-right: 20px;
  }

  .p1-institution {
    font-size: 19pt;
    font-weight: 700;
    color: #ffffff;
    line-height: 1.25;
  }

  .p1-subinstitution {
    font-size: 17pt;
    font-weight: 700;
    color: #ffffff;
    line-height: 1.25;
  }

  /* PÁGINA 2: DATOS GENERALES */
  .p2-top {
    height: 4.8in;
    padding: 0.65in 0.85in 0.4in 0.85in;
    display: flex;
    justify-content: space-between;
    background: #ffffff;
  }

  .p2-col-left { width: 48%; }
  .p2-col-right { width: 48%; }

  .p2-h1 {
    font-size: 20pt;
    font-weight: 700;
    color: #6c5ce7;
    margin: 0 0 10px 0;
    display: inline-block;
    border-bottom: 3.5px solid #a29bfe;
    padding-bottom: 4px;
  }

  .p2-item-title {
    font-size: 11pt;
    font-weight: 700;
    color: #6c5ce7;
    margin-top: 10px;
    margin-bottom: 2px;
  }

  .p2-item-desc {
    font-size: 10pt;
    color: #2d3436;
    margin: 0;
    line-height: 1.35;
  }

  .p2-bottom {
    height: 6.2in;
    position: relative;
    overflow: hidden;
  }

  .p2-bottom-bg {
    position: absolute;
    top: 0;
    left: 0;
    width: 100%;
    height: 100%;
    object-fit: cover;
    z-index: 1;
  }

  .p2-card {
    position: absolute;
    right: 0.65in;
    top: 0.65in;
    width: 4.2in;
    background: rgba(15, 23, 42, 0.90);
    border: 1px solid rgba(162, 155, 254, 0.45);
    border-radius: 10px;
    padding: 24px;
    color: #ffffff;
    z-index: 2;
    box-shadow: 0 8px 30px rgba(0,0,0,0.55);
    font-size: 9.8pt;
    line-height: 1.48;
    text-align: justify;
  }

  .p2-card h3 {
    margin: 0 0 10px 0;
    font-size: 12.5pt;
    font-weight: 700;
    color: #a29bfe;
    border-bottom: 2px solid rgba(162, 155, 254, 0.4);
    padding-bottom: 4px;
  }

  /* PÁGINA 3: OBJETIVOS Y METAS */
  .p3-top {
    height: 6.8in;
    padding: 0.6in 0.85in 0.3in 0.85in;
    background: #ffffff;
  }

  .p3-middle {
    display: flex;
    align-items: center;
    justify-content: space-between;
    margin-top: 10px;
  }

  .p3-hud {
    width: 2.2in;
    height: auto;
    border-radius: 8px;
    box-shadow: 0 3px 12px rgba(0,0,0,0.12);
  }

  .p3-goal-box { width: 4.2in; }

  .p3-goal-title {
    font-size: 14pt;
    font-weight: 700;
    color: #6c5ce7;
    margin: 0 0 6px 0;
  }

  .p3-bottom {
    height: 4.2in;
    background-color: #c4b5fd;
    padding: 0.45in 0.65in;
    display: flex;
    justify-content: space-between;
  }

  .p3-col {
    width: 31%;
    font-size: 8.4pt;
    line-height: 1.4;
    color: #1e293b;
    text-align: justify;
  }

  .p3-col-h {
    font-size: 11pt;
    font-weight: 800;
    color: #0f172a;
    margin: 0 0 6px 0;
    line-height: 1.25;
  }

  /* PÁGINA 10: DESAFÍOS Y LOGROS */
  .p10-top {
    height: 4.6in;
    position: relative;
    overflow: hidden;
  }

  .p10-top-bg {
    position: absolute;
    top: 0;
    left: 0;
    width: 100%;
    height: 100%;
    object-fit: cover;
  }

  .p10-bottom {
    height: 6.4in;
    padding: 0.55in 0.85in;
    display: flex;
    justify-content: space-between;
    background: #ffffff;
  }

  .p10-col-left { width: 47%; }
  .p10-col-right { width: 47%; }

  .p10-h-black {
    font-size: 20pt;
    font-weight: 800;
    color: #000000;
    margin: 0 0 12px 0;
    display: inline-block;
    border-bottom: 3.5px solid #000000;
    padding-bottom: 4px;
  }

  .p10-h-purple {
    font-size: 20pt;
    font-weight: 800;
    color: #6c5ce7;
    margin: 0 0 12px 0;
    display: inline-block;
    border-bottom: 3.5px solid #a29bfe;
    padding-bottom: 4px;
  }

  /* PÁGINA 11: RECOMENDACIONES */
  .p11-bg {
    position: absolute;
    top: 0;
    left: 0;
    width: 8.5in;
    height: 11in;
    object-fit: cover;
    z-index: 1;
  }

  .p11-card {
    position: absolute;
    right: 0.65in;
    top: 0.65in;
    width: 4.4in;
    background: rgba(255, 255, 255, 0.96);
    border: 1px solid rgba(162, 155, 254, 0.45);
    border-radius: 12px;
    padding: 26px;
    z-index: 2;
    box-shadow: 0 10px 35px rgba(0,0,0,0.50);
    font-size: 8.7pt;
    line-height: 1.45;
  }

  .p11-h1 {
    font-size: 18pt;
    font-weight: 800;
    color: #6c5ce7;
    margin: 0 0 12px 0;
    display: inline-block;
    border-bottom: 3.5px solid #a29bfe;
    padding-bottom: 4px;
  }
</style>
</head>
<body>

<!-- ========================================================================= -->
<!-- SLIDE 1: PORTADA OFICIAL (FONDO AZUL CIBERNÉTICO + ESCUDO UDG)            -->
<!-- ========================================================================= -->
<div class="slide-page">
  <img src="data:image/jpeg;base64,__portada_fraude_tarjetas.jpg__" class="p1-bg" alt="Portada Ciberseguridad Fraude en Tarjetas">
  <div class="p1-overlay"></div>
  <div class="p1-content">
    <div class="p1-titles">
      <div class="p1-title-avance">AVANCE</div>
      <div class="p1-title-sub">PROYECTO</div>
      <div class="p1-title-sub">INTEGRADOR</div>
      <div class="p1-line"></div>
      <div class="p1-subtitle-box">
        Detección Automatizada de Fraude en Tarjetas de Crédito:<br>
        <span style="color:#a29bfe; font-size:12pt; font-weight:400;">
          Proceso Completo de Preparación de Datos bajo la Metodología KDD (7 Etapas)
        </span>
      </div>
    </div>
    <div class="p1-footer">
      <img src="data:image/png;base64,__udeg_logo.png__" class="p1-logo" alt="Escudo Universidad de Guadalajara">
      <div>
        <div class="p1-institution">Universidad de Guadalajara</div>
        <div class="p1-subinstitution">Centro Universitario de Guadalajara</div>
      </div>
    </div>
  </div>
</div>

<!-- ========================================================================= -->
<!-- SLIDE 2: DATOS GENERALES, DATASET Y CONTEXTO DEL PROBLEMA (ETAPA 1 KDD)    -->
<!-- ========================================================================= -->
<div class="slide-page">
  <div class="p2-top">
    <div class="p2-col-left">
      <div class="p2-h1">Datos Generales:</div>
      <div class="p2-item-title">Programa Académico:</div>
      <div class="p2-item-desc">Licenciatura en Inteligencia Artificial y Ciencia de Datos.</div>
      <div class="p2-item-title">Materia:</div>
      <div class="p2-item-desc">Data Mining y Knowledge Discovery.</div>
      <div class="p2-item-title">Profesor Titular:</div>
      <div class="p2-item-desc">Milagros Contreras Elizalde.</div>
      <div class="p2-item-title">Alumno:</div>
      <div class="p2-item-desc">Roberto Alejandro Chagra Martinez (Código: <code>208447128</code>).</div>
    </div>
    <div class="p2-col-right">
      <div class="p2-item-title" style="margin-top:0; font-size:13pt;">Conjunto de Datos:</div>
      <div class="p2-item-desc" style="font-weight:600;">Credit Card Fraud Detection Dataset 2026.</div>
      <div class="p2-item-title">Fuente Oficial:</div>
      <div class="p2-item-desc">Kaggle (Calibrado con Reserva Federal, Nilson Report, FICO y BCE).</div>
      <div class="p2-item-desc" style="font-size:7.8pt; color:#0984e3; margin-top:4px; word-break:break-all;">
        [https://www.kaggle.com/datasets/mohankrishnathalla/credit-card-fraud-detection-dataset-2026/data]
      </div>
      <div class="p2-item-desc" style="margin-top:10px; font-size:8.6pt; color:#636e72;">
        <strong>Volumen y Clases:</strong> 100,000 transacciones · 43 variables iniciales · Desbalance severo: <strong>97.945% legítimas</strong> vs. <strong>2.055% fraudes</strong> (razón 1 : 47.66). Pérdida acumulada: <strong>$279,842.20 USD</strong>.
      </div>
    </div>
  </div>
  <div class="p2-bottom">
    <img src="data:image/jpeg;base64,__transacciones_anomalias.jpg__" class="p2-bottom-bg" alt="Telemetría de Transacciones y Radar de Anomalías">
    <div class="p2-card">
      <h3>Contexto del Dominio y Planteamiento del Problema (Etapa 1 KDD)</h3>
      El ecosistema global de pagos digitales enfrenta el reto crítico del fraude transaccional con tarjetas de crédito. En este conjunto de datos de 100,000 registros, las operaciones legítimas superan de forma abrumadora a los fraudes confirmados (97.945% vs 2.055%). Bajo la metodología KDD, la preparación de datos aborda la <strong>Paradoja de la Exactitud</strong> (donde un clasificador trivial obtendría 97.9% de exactitud pero 0.0% de sensibilidad ante fraudes millonarios), previene la <strong>Fuga de Información (Data Leakage)</strong> aislando estrictamente los datos de prueba, y resuelve la ausencia estructural en canales físicos sin inducir sesgo de selección.
    </div>
  </div>
</div>

<!-- ========================================================================= -->
<!-- SLIDE 3: OBJETIVOS DEL PROYECTO, METAS Y CONSIDERACIONES CRÍTICAS        -->
<!-- ========================================================================= -->
<div class="slide-page">
  <div class="p3-top">
    <div class="p2-h1" style="font-size:22pt;">Objetivos del Proyecto</div>
    <div class="definition-box">
      <strong>Definición Oficial KDD (Etapa 1):</strong> "Establecer qué se desea lograr y comprender el dominio o contexto del problema."
    </div>
    <p>
      Diseñar, implementar, justificar e interpretar el proceso completo de preparación de datos bajo la metodología KDD (7 etapas oficiales) sobre el dataset <code>credit_card_fraud_detection_2026.csv</code>, asegurando la eliminación de sesgos de selección, la prevención estricta de Fuga de Información, la creación de 8 variables derivadas de dominio, la reducción dimensional mediante dos métodos de filtro complementarios y la validación cruzada estratificada de 5 particiones.
    </p>
    <p>
      El proyecto trasciende la aplicación mecánica de algoritmos al fundamentar matemáticamente cada decisión analítica: imputación semántica estructural de valores faltantes, conservación de valores atípicos mediante el cálculo del <em>Fraud Lift</em>, y normalización híbrida (<code>log1p</code> + <code>RobustScaler</code>) calibrada únicamente con datos de entrenamiento.
    </p>
    <div class="p3-middle">
      <img src="data:image/jpeg;base64,__mineria_datos_forense.jpg__" class="p3-hud" alt="Minería de Datos y Análisis Forense">
      <div class="p3-goal-box">
        <div class="p3-goal-title">Meta Principal del Avance</div>
        <p style="margin-bottom:0;">
          Generar y validar una matriz de datos óptima de <strong>100,000 registros x 30 características predictivas</strong> libre de sobreajuste o fuga, alcanzando un desempeño de referencia en 5-Fold Stratified CV de <strong>ROC-AUC = 0.8523</strong> y <strong>PR-AUC = 0.1844</strong> (8.97 veces sobre el azar), lista para la minería avanzada y extracción de reglas explicables (<em>IF-THEN</em>).
        </p>
      </div>
    </div>
  </div>
  <div class="p3-bottom">
    <div class="p3-col">
      <div class="p3-col-h">Prevención de Fuga de Información</div>
      <strong>Protocolo Anti-Leakage Estricto:</strong> Se implementó la partición 80/20 estratificada antes de cualquier ajuste (<em>Split-Before-Fit</em>). Todos los codificadores, escaladores y selectores de características se calibran única y exclusivamente sobre los datos de entrenamiento, evitando contaminación con datos de prueba o validación.
    </div>
    <div class="p3-col">
      <div class="p3-col-h">Tratamiento Semántico y Outliers</div>
      <strong>Imputación sin Sesgo de Selección:</strong> Se diagnosticó que el 100% de los 41,709 nulos en <code>browser</code> son estructurales de canales presenciales (POS/ATM); se imputó <code>'No_Aplica_Fisico'</code>. Los <em>outliers</em> no se eliminaron porque concentran hasta <strong>3.26x más fraude</strong> en colas de velocidad.
    </div>
    <div class="p3-col">
      <div class="p3-col-h">Metodología KDD en 7 Etapas</div>
      <strong>Flujo Metodológico Riguroso:</strong> Ejecución secuencial y documentada de las 7 etapas de la metodología KDD: (1) Definición del objetivo, (2) Selección de datos, (3) Limpieza, (4) Transformación e Ingeniería, (5) Minería preliminar, (6) Evaluación cuantitativa y (7) Interpretación del conocimiento.
    </div>
  </div>
</div>

<!-- ========================================================================= -->
<!-- SLIDE 4: ETAPA 3 KDD — LIMPIEZA DE DATOS (DIAGNÓSTICO Y AUSENCIA)         -->
<!-- ========================================================================= -->
<div class="slide-page page-padding">
  <div class="header-box">
    <div class="section-h1">3. Etapa 3 KDD — Limpieza de Datos (Diagnóstico de Calidad)</div>
    <span class="kdd-tag">Fase 3 KDD</span>
    <div class="definition-box">
      <strong>Definición Oficial KDD:</strong> "Eliminar o corregir errores, inconsistencias, valores faltantes, duplicados, etc."
    </div>
  </div>

  <h3 style="color:#1e3a8a; font-size:10.5pt; margin:6px 0 3px 0;">3.1 Diagnóstico de Valores Faltantes (Ausencia Estructural)</h3>
  <p>
    Se auditó la totalidad de las 43 columnas del dataset. El análisis reveló que <strong>42 de las 43 características presentan un 0.0% de valores nulos</strong>. Únicamente la columna <code>browser</code> exhibe valores ausentes: <strong>41,709 registros nulos (41.71%)</strong>.
  </p>
  <p>
    Para determinar el mecanismo generador de los datos ausentes (MCAR, MAR o MNAR), se cruzó <code>browser.isnull()</code> contra el canal operativo (<code>transaction_channel</code>) y el dispositivo (<code>device_type</code>):
  </p>

  <table class="data-table" style="text-align:center;">
    <tr>
      <th style="text-align:left;">Canal Operativo (<code>transaction_channel</code>)</th>
      <th>Transacciones Totales</th>
      <th>Valores Nulos en <code>browser</code></th>
      <th>Porcentaje de Nulos</th>
      <th>Mecanismo Generador</th>
    </tr>
    <tr>
      <td style="text-align:left;"><strong>Terminal Punto de Venta (In-store)</strong></td>
      <td>35,777</td>
      <td>35,777</td>
      <td style="color:#dc2626; font-weight:700;">100.0%</td>
      <td>Ausencia Estructural (MNAR)</td>
    </tr>
    <tr>
      <td style="text-align:left;"><strong>Cajero Automático (ATM)</strong></td>
      <td>5,932</td>
      <td>5,932</td>
      <td style="color:#dc2626; font-weight:700;">100.0%</td>
      <td>Ausencia Estructural (MNAR)</td>
    </tr>
    <tr>
      <td style="text-align:left;"><strong>Comercio Electrónico (Online)</strong></td>
      <td>47,605</td>
      <td>0</td>
      <td style="color:#16a34a; font-weight:700;">0.0%</td>
      <td>Completitud Total</td>
    </tr>
    <tr>
      <td style="text-align:left;"><strong>Aplicación Móvil (Mobile App)</strong></td>
      <td>10,686</td>
      <td>0</td>
      <td style="color:#16a34a; font-weight:700;">0.0%</td>
      <td>Completitud Total</td>
    </tr>
    <tr class="highlight" style="text-align:left;">
      <td><strong>Total Consolidado</strong></td>
      <td style="text-align:center;">100,000</td>
      <td style="text-align:center;">41,709</td>
      <td style="text-align:center;">41.71%</td>
      <td style="text-align:center;">100% Concentrado en Canal Físico</td>
    </tr>
  </table>

  <h3 style="color:#1e3a8a; font-size:10.5pt; margin:6px 0 3px 0;">3.2 Diagnóstico de Duplicados e Inconsistencias</h3>
  <p>
    Se comprobaron <strong>0 registros duplicados</strong> en la matriz y <strong>0 duplicados de llave primaria</strong> (<code>transaction_id</code>). Se verificó que no existen montos negativos, edades inválidas ni distancias negativas, confirmando la consistencia física de las mediciones.
  </p>

  <div class="figure-container">
    <img src="data:image/png;base64,__fig01_diagnostico_target_y_nulos.png__" alt="Diagnóstico Target y Nulos">
    <div class="figure-caption">Figura 1: Panel A: Desbalance severo (97.9% vs 2.1%). Panel B: Modalidades de fraude confirmadas. Panel C: Ausencia estructural de browser concentrada al 100% en transacciones presenciales (In-store y ATM).</div>
  </div>
</div>

<!-- ========================================================================= -->
<!-- SLIDE 5: ETAPA 3 KDD — LIMPIEZA DE DATOS (OUTLIERS Y DECISIONES)          -->
<!-- ========================================================================= -->
<div class="slide-page page-padding">
  <div class="header-box">
    <div class="section-h1">3. Etapa 3 KDD — Limpieza de Datos (Tratamiento y Outliers)</div>
    <span class="kdd-tag">Fase 3 KDD</span>
  </div>

  <h3 style="color:#1e3a8a; font-size:10.5pt; margin:4px 0 3px 0;">3.3 Diagnóstico Estadístico de Valores Atípicos (Criterio 1.5 &times; IQR de Tukey)</h3>
  <p>
    En distribuciones financieras con colas pesadas, el criterio paramétrico ($\mu \pm 3\sigma$) se distorsiona por los propios valores extremos. Por ello, se aplicó el método no paramétrico de <strong>Tukey</strong> con el rango intercuartílico $\text{IQR} = Q_3 - Q_1$, evaluando las observaciones por encima del límite superior $Q_3 + 1.5 \times \text{IQR}$:
  </p>

  <table class="data-table" style="font-size:7.6pt;">
    <tr>
      <th>Variable Numérica</th>
      <th>Límite Sup. (1.5&times;IQR)</th>
      <th>Registros Atípicos</th>
      <th>% Atípicos</th>
      <th>Fraudes en Outliers</th>
      <th>Tasa Fraude en Outliers</th>
      <th>Tasa Fraude Normal</th>
      <th>Multiplicador de Fraude (Lift)</th>
    </tr>
    <tr class="highlight">
      <td><code>transactions_last_1h</code></td>
      <td>2.50 tx</td>
      <td>8,327</td>
      <td>8.33%</td>
      <td>464</td>
      <td><strong>5.57%</strong></td>
      <td>1.71%</td>
      <td><strong style="color:#b91c1c;">3.26x más fraude</strong></td>
    </tr>
    <tr>
      <td><code>amount_last_1h</code></td>
      <td>$310.95 USD</td>
      <td>5,702</td>
      <td>5.70%</td>
      <td>269</td>
      <td>4.72%</td>
      <td>1.90%</td>
      <td><strong>2.48x más fraude</strong></td>
    </tr>
    <tr>
      <td><code>amount_vs_avg_ratio</code></td>
      <td>3.03x</td>
      <td>4,510</td>
      <td>4.51%</td>
      <td>211</td>
      <td>4.68%</td>
      <td>1.93%</td>
      <td><strong>2.42x más fraude</strong></td>
    </tr>
    <tr>
      <td><code>distance_from_last_tx_km</code></td>
      <td>200.74 km</td>
      <td>7,858</td>
      <td>7.86%</td>
      <td>275</td>
      <td>3.50%</td>
      <td>1.93%</td>
      <td><strong>1.81x más fraude</strong></td>
    </tr>
    <tr>
      <td><code>transaction_amount</code></td>
      <td>$376.10 USD</td>
      <td>6,192</td>
      <td>6.19%</td>
      <td>193</td>
      <td>3.12%</td>
      <td>1.99%</td>
      <td><strong>1.57x más fraude</strong></td>
    </tr>
  </table>

  <h3 style="color:#1e3a8a; font-size:10.5pt; margin:6px 0 3px 0;">3.4 Justificación de las Decisiones de Limpieza Tomadas</h3>
  <ol>
    <li>
      <strong>Imputación Semántica de <code>browser</code> (Sin Sesgo de Selección):</strong> Eliminar las 41,709 filas nulas causaría un sesgo devastador, destruyendo todo el canal físico del banco. Imputar con la moda ("Chrome") inventaría navegadores web en cajeros físicos. Se asignó la categoría semántica <strong><code>'No_Aplica_Fisico'</code></strong>, reteniendo el 100% de los registros con 0 nulos.
    </li>
    <li>
      <strong>Conservación Absoluta de Valores Atípicos:</strong> La tabla demuestra que las colas concentran hasta <strong>3.26 veces más fraude</strong>. Recortarlos mutilaría la señal discriminante más valiosa de los ataques de velocidad. Se conservaron intactos y su estabilización se resolvió mediante escalado robusto.
    </li>
  </ol>

  <div class="figure-container">
    <img src="data:image/png;base64,__fig02_diagnostico_outliers_iqr.png__" alt="Diagnóstico Outliers IQR">
    <div class="figure-caption">Figura 2: Diagnóstico Tukey 1.5&times;IQR. En las colas atípicas de transactions_last_1h y amount_last_1h, la tasa de fraude se dispara hasta 5.57%, probando la conveniencia de preservar los valores extremos.</div>
  </div>
</div>

<!-- ========================================================================= -->
<!-- SLIDE 6: ETAPA 4 KDD — TRANSFORMACIÓN (FEATURE ENGINEERING)               -->
<!-- ========================================================================= -->
<div class="slide-page page-padding">
  <div class="header-box">
    <div class="section-h1">4. Etapa 4 KDD — Transformación (Ingeniería de Características)</div>
    <span class="kdd-tag">Fase 4 KDD</span>
    <div class="definition-box">
      <strong>Definición Oficial KDD:</strong> "Convertir, normalizar, reducir o transformar los datos a un formato adecuado."
    </div>
  </div>

  <h3 style="color:#1e3a8a; font-size:10.5pt; margin:4px 0 3px 0;">4.1 Creación de 8 Variables Derivadas y Justificación de su Utilidad</h3>
  <p>
    Para superar el ocultamiento del fraude en señales multidimensionales débiles, se diseñaron <strong>8 variables derivadas</strong> basadas en principios bancarios de velocidad, desviación crediticia y seguridad:
  </p>

  <table class="data-table" style="font-size:7.5pt;">
    <tr>
      <th>Variable Derivada</th>
      <th>Formulación Matemática</th>
      <th>Media (Legítima)</th>
      <th>Media (Fraude)</th>
      <th>Ratio Discriminante</th>
      <th>Racional Financiero y Utilidad de Negocio</th>
    </tr>
    <tr class="highlight">
      <td><code>composite_risk_index</code></td>
      <td>Suma ponderada de 8 banderas</td>
      <td>0.88 banderas</td>
      <td><strong>2.94 banderas</strong></td>
      <td><strong>3.34x más alto</strong></td>
      <td>Índice compuesto de alertas tempranas (velocidad, noche, país riesgoso, etc.).</td>
    </tr>
    <tr>
      <td><code>credit_utilization_ratio</code></td>
      <td>Monto / Límite de Crédito</td>
      <td>0.0195</td>
      <td><strong>0.0384</strong></td>
      <td><strong>1.97x más alto</strong></td>
      <td>Mide la fracción del margen crediticio consumida en una sola operación.</td>
    </tr>
    <tr>
      <td><code>velocity_tx_ratio_1h_24h</code></td>
      <td>Tx en 1h / (Tx en 24h + 1)</td>
      <td>0.1770</td>
      <td><strong>0.2974</strong></td>
      <td><strong>1.68x más alto</strong></td>
      <td>Detecta ráfagas veloces de compras en 1h respecto al acumulado diario.</td>
    </tr>
    <tr>
      <td><code>velocity_amt_ratio_1h_24h</code></td>
      <td>Monto 1h / (Monto 24h + 1)</td>
      <td>0.1764</td>
      <td><strong>0.2949</strong></td>
      <td><strong>1.67x más alto</strong></td>
      <td>Identifica ataques de drenado patrimonial rápido en intervalos cortos.</td>
    </tr>
    <tr>
      <td><code>zscore_amount_30d</code></td>
      <td>(Monto - Media30d) / Desv30d</td>
      <td>-0.0076</td>
      <td><strong>+0.2858</strong></td>
      <td><strong>Salto positivo</strong></td>
      <td>Desviación del monto actual frente al patrón de consumo mensual del titular.</td>
    </tr>
    <tr>
      <td><code>is_night_tx</code></td>
      <td>Indicador hora en [0, 5]</td>
      <td>25.10%</td>
      <td><strong>32.85%</strong></td>
      <td><strong>1.31x más alto</strong></td>
      <td>Compras en horario de madrugada cuando el cliente tarda más en alertar.</td>
    </tr>
    <tr>
      <td><code>is_new_account</code></td>
      <td>Antigüedad cuenta &le; 90 días</td>
      <td>12.28%</td>
      <td><strong>17.52%</strong></td>
      <td><strong>1.43x más alto</strong></td>
      <td>Detecta cuentas fraudulentas recién abiertas e identidades sintéticas.</td>
    </tr>
    <tr>
      <td><code>security_factors_count</code></td>
      <td>Chip + PIN + Tarjeta Presente</td>
      <td>1.43 factores</td>
      <td><strong>0.87 factores</strong></td>
      <td><strong>-39.2% menor</strong></td>
      <td>Índice de blindaje: a menor autenticación física, mayor vulnerabilidad.</td>
    </tr>
  </table>

  <div class="figure-container">
    <img src="data:image/png;base64,__fig03_ingenieria_caracteristicas.png__" alt="Ingeniería de Características">
    <div class="figure-caption">Figura 3: Distribución del poder discriminante de las 8 variables derivadas creadas. Destaca composite_risk_index, donde la tasa de fraude escala exponencialmente de 0.04% (nivel 0) a 87.50% (nivel 8).</div>
  </div>
</div>

<!-- ========================================================================= -->
<!-- SLIDE 7: ETAPA 4 KDD — TRANSFORMACIÓN (PARTICIÓN Y ESCALAMIENTO)          -->
<!-- ========================================================================= -->
<div class="slide-page page-padding">
  <div class="header-box">
    <div class="section-h1">4. Etapa 4 KDD — Transformación (Partición y Escalamiento)</div>
    <span class="kdd-tag">Fase 4 KDD</span>
  </div>

  <h3 style="color:#1e3a8a; font-size:10.5pt; margin:4px 0 3px 0;">4.2 Partición Estratificada 80/20 y Prevención de Fuga de Información</h3>
  <p>
    Para evitar la contaminación del conjunto de prueba, la matriz enriquecida (100,000 registros &times; 43 predictores) se dividió mediante <strong>muestreo estratificado (<code>StratifiedShuffleSplit</code>)</strong> en una proporción 80/20:
  </p>
  <ul>
    <li><strong>Conjunto de Entrenamiento (<code>X_train_df</code>):</strong> <strong>80,000 transacciones</strong> (78,356 legítimas y 1,644 fraudes &rarr; <strong>2.0550% de fraude</strong>).</li>
    <li><strong>Conjunto de Prueba (<code>X_test_df</code>):</strong> <strong>20,000 transacciones</strong> (19,589 legítimas y 411 fraudes &rarr; <strong>2.0550% de fraude</strong>).</li>
  </ul>
  <div class="callout-box callout-success">
    <strong>Protocolo Estricto Anti-Leakage (Split-Before-Fit):</strong>
    La partición se ejecutó <strong>antes de cualquier ajuste numérico o categórico</strong>. Todas las transformaciones se calibran exclusivamente con <code>.fit()</code> sobre <code>X_train_df</code>, y se aplican con <code>.transform()</code> sobre <code>X_test_df</code>. Se garantiza así cero fuga de información.
  </div>

  <h3 style="color:#1e3a8a; font-size:10.5pt; margin:6px 0 3px 0;">4.3 Codificación Categórica y Escalamiento Híbrido</h3>
  <ol>
    <li>
      <strong>Codificación Categórica Nominal (<code>OneHotEncoder</code>):</strong>
      Se aplicó sobre las 8 variables nominales con <code>handle_unknown='ignore'</code> y <code>sparse_output=False</code>, ajustado solo en <code>X_train_df</code>. Esto expandió las variables categóricas en 57 columnas binarias limpias.
    </li>
    <li>
      <strong>Escalamiento Numérico Híbrido (<code>np.log1p</code> + <code>RobustScaler</code>):</strong>
      Para domesticar las colas asimétricas sin eliminar <em>outliers</em>, se aplicó primero la compresión logarítmica $\tilde{x} = \ln(x + 1)$ (<code>np.log1p</code>), seguida de <code>RobustScaler</code> (centrado en la mediana y dividido entre el IQR), calculado <strong>únicamente en entrenamiento</strong>.
    </li>
  </ol>

  <table class="data-table" style="font-size:7.6pt; text-align:center;">
    <tr>
      <th style="text-align:left;">Métrica de Verificación Matemática</th>
      <th>Distribución Cruda (USD)</th>
      <th>Tras <code>np.log1p</code> + <code>RobustScaler</code> (Train)</th>
      <th>Evaluación en Test (Sin Fuga)</th>
    </tr>
    <tr>
      <td style="text-align:left;"><strong>Mediana ($Q_2$)</strong></td>
      <td>$52.27 USD</td>
      <td><strong>0.0000</strong> (Centrado exacto)</td>
      <td>-0.0028 (Estabilidad perfecta)</td>
    </tr>
    <tr>
      <td style="text-align:left;"><strong>Rango Intercuartílico ($\text{IQR}$)</strong></td>
      <td>$124.64 USD</td>
      <td><strong>1.0000</strong> (Escala normalizada)</td>
      <td>0.9984 (Sin deformación)</td>
    </tr>
    <tr>
      <td style="text-align:left;"><strong>Dimensión de la Matriz $X$</strong></td>
      <td>34 columnas crudas</td>
      <td><strong>91 columnas continuas/binarias</strong></td>
      <td>91 columnas continuas/binarias</td>
    </tr>
  </table>

  <div class="figure-container">
    <img src="data:image/png;base64,__fig04_escalamiento_robusto_sin_leakage.png__" alt="Escalamiento Robusto">
    <div class="figure-caption">Figura 4: Estabilización morfológica de transaction_amount. La asimetría extrema original (Panel A) se convierte en una campana unimodal simétrica centrada en 0.0 con IQR = 1.0 (Panel B), domesticando los outliers para modelos lineales.</div>
  </div>
</div>

<!-- ========================================================================= -->
<!-- SLIDE 8: ETAPA 4 KDD — TRANSFORMACIÓN (SELECCIÓN POR FILTROS)             -->
<!-- ========================================================================= -->
<div class="slide-page page-padding">
  <div class="header-box">
    <div class="section-h1">4. Etapa 4 KDD — Transformación (Selección por Filtros)</div>
    <span class="kdd-tag">Fase 4 KDD</span>
  </div>

  <h3 style="color:#1e3a8a; font-size:10.5pt; margin:4px 0 3px 0;">4.4 Aplicación y Comparación de Dos Métodos de Filtro</h3>
  <p>
    Para reducir la dimensionalidad de 91 a un espacio compacto y evitar la maldición de la dimensionalidad, se aplicaron sobre <code>X_train</code> y <code>y_train</code> dos métodos de filtro de fundamentos teóricos complementarios:
  </p>
  <ul>
    <li><strong>Método 1 (Paramétrico / Lineal): Prueba $F$ de ANOVA (<code>f_classif</code>) y $\chi^2$:</strong> Mide la razón de varianzas inter-clase vs intra-clase, asumiendo monotonicidad y linealidad de separación.</li>
    <li><strong>Método 2 (No Paramétrico / No Lineal): Información Mutua de Shannon (<code>mutual_info_classif</code>):</strong> Basada en entropía informacional ($I(X;Y) = H(Y) - H(Y|X)$). Cuantifica la reducción de incertidumbre sin asumir formas funcionales ni linealidad.</li>
  </ul>

  <table class="data-table" style="font-size:7.4pt;">
    <tr>
      <th>Top Ranking</th>
      <th>Característica</th>
      <th>Estadístico ANOVA $F$ / $\chi^2$</th>
      <th>Ranking ($F$)</th>
      <th>Información Mutua (nats)</th>
      <th>Ranking (MI)</th>
      <th>Consenso / Tipo de Señal</th>
    </tr>
    <tr class="highlight">
      <td><strong>#1</strong></td>
      <td><code>composite_risk_index</code></td>
      <td><strong>3,719.82</strong> ($p < 10^{-300}$)</td>
      <td>#1</td>
      <td><strong>0.01945 nats</strong></td>
      <td>#1</td>
      <td><strong style="color:#0369a1;">Consenso Absoluto (Filtro 1 y 2)</strong></td>
    </tr>
    <tr>
      <td><strong>#2</strong></td>
      <td><code>velocity_tx_ratio_1h_24h</code></td>
      <td>781.45</td>
      <td>#2</td>
      <td>0.00762 nats</td>
      <td>#2</td>
      <td>Consenso (Velocidad transaccional)</td>
    </tr>
    <tr>
      <td><strong>#3</strong></td>
      <td><code>transactions_last_1h</code></td>
      <td>644.20</td>
      <td>#3</td>
      <td>0.00684 nats</td>
      <td>#3</td>
      <td>Consenso (Frecuencia en 1 hora)</td>
    </tr>
    <tr>
      <td><strong>#4</strong></td>
      <td><code>credit_utilization_ratio</code></td>
      <td>512.18</td>
      <td>#4</td>
      <td>0.00591 nats</td>
      <td>#4</td>
      <td>Consenso (Compromiso del límite)</td>
    </tr>
    <tr>
      <td><strong>#5</strong></td>
      <td><code>security_factors_count</code></td>
      <td>438.90</td>
      <td>#5</td>
      <td>0.00512 nats</td>
      <td>#5</td>
      <td>Consenso (Autenticación fuerte)</td>
    </tr>
    <tr>
      <td><strong>#6</strong></td>
      <td><code>velocity_amt_ratio_1h_24h</code></td>
      <td>389.74</td>
      <td>#6</td>
      <td>0.00481 nats</td>
      <td>#6</td>
      <td>Consenso (Drenado monetario)</td>
    </tr>
    <tr>
      <td><strong>#7</strong></td>
      <td><code>browser_No_Aplica_Fisico</code></td>
      <td>215.30</td>
      <td>#11</td>
      <td>0.00455 nats</td>
      <td>#7</td>
      <td>Consenso (Imputación semántica)</td>
    </tr>
    <tr style="background:#fef3c7;">
      <td><strong>#14 (Divergencia)</strong></td>
      <td><code>account_age_days</code></td>
      <td>68.42 (Bajo poder lineal)</td>
      <td>#31</td>
      <td><strong>0.00392 nats</strong> (Alto poder)</td>
      <td>#14</td>
      <td><strong>Captura no lineal de umbral (MI)</strong></td>
    </tr>
  </table>

  <h3 style="color:#1e3a8a; font-size:10.5pt; margin:6px 0 3px 0;">4.5 Interpretación y Selección del Subconjunto Óptimo (30 Características)</h3>
  <p>
    Ambos métodos arrojaron un <strong>80.0% de coincidencia en el Top 25 (20 de 25 variables compartidas)</strong>. El Filtro 1 priorizó banderas geográficas de alta pureza lineal (<code>high_risk_country</code>, <code>merchant_country_China</code>), mientras que el Filtro 2 rescató variables continuas con relaciones no lineales escalonadas como <strong><code>account_age_days</code></strong> (el riesgo no cae linealmente, sino en escalón tras 90 días). Al unificar el consenso se seleccionó un subconjunto compacto de <strong>30 características óptimas (reducción del 67.0% de dimensionalidad)</strong>.
  </p>

  <div class="figure-container">
    <img src="data:image/png;base64,__fig05_comparativa_dos_metodos_filtro.png__" alt="Comparativa Métodos de Filtro">
    <div class="figure-caption">Figura 5: Comparativa espejo entre la Prueba F de ANOVA (Panel A) y la Información Mutua de Shannon (Panel B). Se observa el consenso abrumador en composite_risk_index y variables de velocidad, junto con el rescate no lineal de account_age_days.</div>
  </div>
</div>

<!-- ========================================================================= -->
<!-- SLIDE 9: ETAPA 5 KDD — MINERÍA DE DATOS (VALIDACIÓN CRUZADA 5-FOLD)       -->
<!-- ========================================================================= -->
<div class="slide-page page-padding">
  <div class="header-box">
    <div class="section-h1">5. Etapa 5 KDD — Minería de Datos (Validación Cruzada 5-Fold)</div>
    <span class="kdd-tag">Fase 5 KDD</span>
    <div class="definition-box">
      <strong>Definición Oficial KDD:</strong> "Aplicar algoritmos para descubrir patrones, identificar relaciones y realizar predicciones a partir de los datos."
    </div>
  </div>

  <h3 style="color:#1e3a8a; font-size:10.5pt; margin:4px 0 3px 0;">5.1 Esquema de Validación Cruzada de 5 Particiones (StratifiedKFold)</h3>
  <p>
    Dado el desbalance de clases (2.055%), una sola partición de validación presentaría varianza estocástica. Se configuró una <strong>Validación Cruzada Estratificada de 5 Particiones (<code>StratifiedKFold(n_splits=5, shuffle=True, random_state=42)</code>)</strong> sobre los 80,000 registros de entrenamiento:
  </p>

  <table class="data-table" style="font-size:7.5pt; text-align:center;">
    <tr>
      <th>Pliegue (Fold)</th>
      <th>Registros Train (Pliegue)</th>
      <th>Fraudes Train</th>
      <th>Registros Val (Pliegue)</th>
      <th>Fraudes Val</th>
      <th>ROC-AUC</th>
      <th>PR-AUC</th>
      <th>Sensibilidad (Recall)</th>
      <th>F1-Score</th>
    </tr>
    <tr>
      <td><strong>Pliegue 1</strong></td>
      <td>64,000</td>
      <td>1,315 (2.055%)</td>
      <td>16,000</td>
      <td>329 (2.056%)</td>
      <td>0.8654</td>
      <td>0.2012</td>
      <td>78.42%</td>
      <td>0.1985</td>
    </tr>
    <tr>
      <td><strong>Pliegue 2</strong></td>
      <td>64,000</td>
      <td>1,315 (2.055%)</td>
      <td>16,000</td>
      <td>329 (2.056%)</td>
      <td>0.8412</td>
      <td>0.1725</td>
      <td>73.86%</td>
      <td>0.1794</td>
    </tr>
    <tr>
      <td><strong>Pliegue 3</strong></td>
      <td>64,000</td>
      <td>1,315 (2.055%)</td>
      <td>16,000</td>
      <td>329 (2.056%)</td>
      <td>0.8598</td>
      <td>0.1944</td>
      <td>79.03%</td>
      <td>0.1941</td>
    </tr>
    <tr>
      <td><strong>Pliegue 4</strong></td>
      <td>64,000</td>
      <td>1,316 (2.056%)</td>
      <td>16,000</td>
      <td>328 (2.050%)</td>
      <td>0.8395</td>
      <td>0.1689</td>
      <td>72.56%</td>
      <td>0.1742</td>
    </tr>
    <tr>
      <td><strong>Pliegue 5</strong></td>
      <td>64,000</td>
      <td>1,315 (2.055%)</td>
      <td>16,000</td>
      <td>329 (2.056%)</td>
      <td>0.8557</td>
      <td>0.1852</td>
      <td>76.60%</td>
      <td>0.1883</td>
    </tr>
    <tr class="highlight">
      <td><strong>Promedio &plusmn; &sigma;</strong></td>
      <td><strong>64,000</strong></td>
      <td><strong>1,315.2 (2.055%)</strong></td>
      <td><strong>16,000</strong></td>
      <td><strong>328.8 (2.055%)</strong></td>
      <td><strong>0.8523 &plusmn; 0.0104</strong></td>
      <td><strong>0.1844 &plusmn; 0.0156</strong></td>
      <td><strong>76.09% &plusmn; 3.30%</strong></td>
      <td><strong>0.1869 &plusmn; 0.0101</strong></td>
    </tr>
  </table>

  <h3 style="color:#1e3a8a; font-size:10.5pt; margin:6px 0 3px 0;">5.2 Protocolo de Prevención de Fuga Intra-Pliegue y Modelado Predictivo</h3>
  <p>
    Para garantizar que ningún cálculo global contamine los pliegues de validación, se implementó un <strong>Pipeline de <code>scikit-learn</code></strong> donde:
  </p>
  <ol>
    <li>En cada iteración, el escalador robusto y el selector de características se ajustan (<code>.fit()</code>) <strong>exclusivamente sobre los 64,000 registros de entrenamiento del pliegue</strong>.</li>
    <li>Los 16,000 registros de validación actúan como datos inéditos y solo se transforman (<code>.transform()</code>).</li>
    <li>El modelo predictivo de referencia (Regresión Logística balanceada) alcanza un <strong>ROC-AUC = 0.8523</strong> y un <strong>PR-AUC = 0.1844</strong> (multiplicando por <strong>8.97 veces</strong> el rendimiento del azar: $0.0206$).</li>
  </ol>

  <div class="figure-container">
    <img src="data:image/png;base64,__fig06_validacion_cruzada_5fold.png__" alt="Validación Cruzada 5-Fold">
    <div class="figure-caption">Figura 6: Desempeño métrico a través de los 5 pliegues de validación cruzada estratificada. Se aprecia la mínima variabilidad (&plusmn;0.0104 en ROC-AUC), demostrando que la matriz de datos preparada es altamente estable y generalizable.</div>
  </div>
</div>

<!-- ========================================================================= -->
<!-- SLIDE 10: DESAFÍOS TÉCNICOS ENFRENTADOS Y LOGROS ALCANZADOS               -->
<!-- ========================================================================= -->
<div class="slide-page">
  <div class="p10-top">
    <img src="data:image/jpeg;base64,__mineria_datos_forense.jpg__" class="p10-top-bg" alt="Desafíos de Minería de Datos y Complejidad Transaccional">
  </div>
  <div class="p10-bottom">
    <div class="p10-col-left">
      <div class="p10-h-black">Desafíos Técnicos</div>
      <ul class="p4-list">
        <li><strong>Paradoja de la Exactitud:</strong> Desbalance severo de 97.945% legítimas vs 2.055% fraudes (1:47.66). Una métrica de Exactitud global engaña y oculta el 100% de los fraudes millonarios.</li>
        <li><strong>Ausencia Estructural Masiva:</strong> 41,709 registros nulos en <code>browser</code> (41.71%). Descartar estas filas habría eliminado todo el canal presencial del banco, sesgando por completo el modelo.</li>
        <li><strong>Riesgo Crítico de Fuga de Información:</strong> Identificación de variables post-evento (<code>fraud_type</code> y <code>fraud_amount_lost</code>) que de incluirse en el entrenamiento causarían un engañoso F1=1.0000 inútil en producción.</li>
        <li><strong>Colas Asimétricas y Multidimensionalidad:</strong> Distribuciones con severo sesgo a la derecha y dispersión extrema que desestabilizan modelos paramétricos lineales.</li>
      </ul>
    </div>
    <div class="p10-col-right">
      <div class="p10-h-purple">Logros y Resultados</div>
      <ul class="p4-list">
        <li><strong>100% de Registros Conservados:</strong> Imputación semántica de <code>browser = 'No_Aplica_Fisico'</code> con 0% de pérdida muestral, resolviendo el problema con 0 nulos resultantes.</li>
        <li><strong>Ingeniería de 8 Variables Derivadas:</strong> Creación de <code>composite_risk_index</code> (#1 absoluto en ambos filtros) y ratios de velocidad con Fraud Lift de hasta 3.34x.</li>
        <li><strong>Normalización Híbrida sin Fuga:</strong> Compresión <code>log1p</code> + <code>RobustScaler</code> centrada en mediana 0.0000 e IQR 1.0000 ajustada estrictamente sobre <code>X_train</code>.</li>
        <li><strong>Reducción Dimensional del 67%:</strong> Consenso del 80% en Top 25 entre ANOVA F / Chi2 e Información Mutua, depurando de 91 a 30 predictores óptimos.</li>
        <li><strong>5-Fold Stratified CV Libre de Fuga:</strong> Validación cruzada con ROC-AUC = 0.8523 y PR-AUC = 0.1844 (8.97 veces sobre el azar) con varianza mínima (±0.0104).</li>
      </ul>
    </div>
  </div>
</div>

<!-- ========================================================================= -->
<!-- SLIDE 11: ETAPAS 6 Y 7 KDD — EVALUACIÓN, INTERPRETACIÓN Y CONCLUSIONES    -->
<!-- ========================================================================= -->
<div class="slide-page">
  <img src="data:image/jpeg;base64,__escudo_decision_fraude.jpg__" class="p11-bg" alt="Escudo de Decisión Antifraude y Autorización">
  <div class="p11-card">
    <div class="p11-h1">Conclusiones y Recomendaciones KDD</div>
    <div class="definition-box" style="margin-top:2px; margin-bottom:8px;">
      <strong>Etapas 6 y 7 KDD:</strong> "Determinar si los resultados son útiles y válidos; y convertir los resultados en conocimiento."
    </div>
    <ul class="p5-list">
      <li><strong>Conclusión 1 (Limpieza sin Sesgo):</strong> Mantener la imputación semántica en canales presenciales (<code>'No_Aplica_Fisico'</code>). Esto retiene la totalidad de la muestra bancaria y aporta una variable altamente discriminante (#7 en Información Mutua).</li>
      <li><strong>Conclusión 2 (Preservación de Outliers):</strong> Conservar los valores atípicos que concentran hasta 3.26x más fraude, estabilizando su escala mediante transformaciones robustas en lugar de truncarlos o eliminarlos.</li>
      <li><strong>Conclusión 3 (Ingeniería de Características):</strong> Priorizar variables de aceleración a corto plazo (<code>velocity_tx_ratio_1h_24h</code>) y el índice de riesgo compuesto (<code>composite_risk_index</code>, variable #1 unánime) en el motor de detección.</li>
      <li><strong>Conclusión 4 (Sinergia de Filtros):</strong> Emplear conjuntamente filtros lineales (ANOVA F / Chi2) y no lineales (Información Mutua) para capturar tanto pureza geográfica como efectos de umbral escalonado (ej. <code>account_age_days</code>).</li>
      <li><strong>Recomendación hacia Minería Avanzada:</strong> Desplegar el subconjunto de 30 variables en clasificadores ensemble (Random Forest, Gradient Boosting) y detección no supervisada (Isolation Forest), extrayendo <strong>reglas de decisión Si-Entonces (IF-THEN)</strong> para motores de autorización en tiempo real.</li>
    </ul>
  </div>
</div>

</body>
</html>
"""

# Reemplazar placeholders de imágenes
for fname, b64 in assets.items():
    html_content = html_content.replace("__" + fname + "__", b64)

# Guardar HTML temporal
HTML_PATH = Path("slide_reporte_espanol_temp.html")
with open(HTML_PATH, "w", encoding="utf-8") as f:
    f.write(html_content)

print(f"HTML generado exitosamente: {HTML_PATH.resolve()}")

# Compilar a PDF usando Google Chrome Headless
CHROME_PATH = r"C:\Program Files\Google\Chrome\Application\chrome.exe"
PDF_PATH = Path("Entregables/Reporte_Avance_Proyecto_Integrador_KDD.pdf")

cmd = [
    CHROME_PATH,
    "--headless",
    "--disable-gpu",
    "--run-all-compositor-stages-before-draw",
    f"--print-to-pdf={PDF_PATH.resolve()}",
    "--no-pdf-header-footer",
    str(HTML_PATH.resolve()),
]

print("Compilando PDF de 11 páginas en formato oficial 100% en español...")
res = subprocess.run(cmd, capture_output=True, text=True)

if res.returncode == 0 and PDF_PATH.exists():
    print(f"PDF generado exitosamente en: {PDF_PATH.resolve()} ({PDF_PATH.stat().st_size:,} bytes)")
    reader = pypdf.PdfReader(str(PDF_PATH))
    print(f"Verificación PyPDF: Total de páginas = {len(reader.pages)}")
    for i in range(len(reader.pages)):
        lines = [l.strip() for l in reader.pages[i].extract_text().split("\n") if l.strip()]
        first_line = lines[0] if lines else "VACIA"
        print(f"  Pág {i+1}: {first_line[:75]}")
    HTML_PATH.unlink()
    print("Archivo temporal HTML eliminado.")
else:
    print(f"Error al generar PDF: {res.stderr}")
