# -*- coding: utf-8 -*-
"""
Compilador Oficial del Documento Técnico del Avance KDD en formato PDF
Basado ÚNICAMENTE en la carpeta Entregables/ (Preparación de Datos, Selección y 5-Fold CV).
Estilo visual institucional del reporte de avance (Montserrat, violeta/lavanda, tarjetas y fondos a sangre).
"""

import os
import shutil
import base64
import subprocess
from pathlib import Path
import pypdf

BASE_DIR = Path(__file__).resolve().parent
ROOT_DIR = BASE_DIR.parent
DOC_ADICIONAL_DIR = ROOT_DIR / "Documentacion_adicional"
CHROME_PATH = r"C:\Program Files\Google\Chrome\Application\chrome.exe"

print("Cargando assets y figuras exclusivas de Entregables/ en base64...")

assets = {}

# 1. Logo institucional UdeG
logo_path = BASE_DIR / "imagenes_proyecto" / "template_assets" / "udeg_logo.png"
with open(logo_path, "rb") as f:
    assets["udeg_logo.png"] = base64.b64encode(f.read()).decode("utf-8")

# 2. Imágenes temáticas oficiales de Entregables/imagenes_proyecto/
PROJ_IMG_DIR = BASE_DIR / "imagenes_proyecto"
for fname in [
    "portada_fraude_tarjetas.jpg",
    "transacciones_anomalias.jpg",
    "mineria_datos_forense.jpg",
    "escudo_decision_fraude.jpg",
]:
    p = PROJ_IMG_DIR / fname
    with open(p, "rb") as f:
        assets[fname] = base64.b64encode(f.read()).decode("utf-8")

# 3. Gráficas analíticas de alta resolución exclusivas de Entregables/Resultados/graficas/
GRAFICAS_DIR = BASE_DIR / "Resultados" / "graficas"
for fname in [
    "fig01_diagnostico_target_y_nulos.png",
    "fig02_diagnostico_outliers_iqr.png",
    "fig03_ingenieria_caracteristicas.png",
    "fig04_escalamiento_robusto_sin_leakage.png",
    "fig05_comparativa_dos_metodos_filtro.png",
    "fig06_validacion_cruzada_5fold.png",
]:
    p = GRAFICAS_DIR / fname
    with open(p, "rb") as f:
        assets[fname] = base64.b64encode(f.read()).decode("utf-8")

print(f"Total de imágenes cargadas: {len(assets)}")

# Plantilla HTML
html_content = """<!DOCTYPE html>
<html lang="es">
<head>
<meta charset="UTF-8">
<title>Documento Técnico del Avance KDD 2026 - Preparación de Datos</title>
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

  .page-padding {
    padding: 0.55in 0.80in 0.45in 0.80in;
    height: 11in;
    box-sizing: border-box;
    display: flex;
    flex-direction: column;
    justify-content: space-between;
  }

  .header-box {
    margin-bottom: 6px;
  }

  .section-h1 {
    font-size: 17pt;
    font-weight: 800;
    color: #6c5ce7;
    margin: 0 0 3px 0;
    display: inline-block;
    border-bottom: 3.5px solid #a29bfe;
    padding-bottom: 2px;
  }

  .kdd-tag {
    font-size: 8pt;
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
    padding: 5px 10px;
    font-size: 8.2pt;
    color: #14532d;
    margin: 4px 0 8px 0;
    border-radius: 0 4px 4px 0;
    line-height: 1.35;
  }

  p {
    font-size: 8.5pt;
    line-height: 1.38;
    color: #2d3436;
    margin: 0 0 6px 0;
    text-align: justify;
  }

  ul, ol {
    margin: 2px 0 6px 16px;
    padding: 0;
    font-size: 8.3pt;
    line-height: 1.36;
    color: #2d3436;
  }

  li {
    margin-bottom: 3px;
    text-align: justify;
  }

  table.data-table {
    width: 100%;
    border-collapse: collapse;
    margin: 5px 0 7px 0;
    font-size: 7.5pt;
  }

  table.data-table th {
    background-color: #0f172a;
    color: #ffffff;
    font-weight: 700;
    text-align: left;
    padding: 4px 6px;
    border: 1px solid #0f172a;
  }

  table.data-table td {
    padding: 3.5px 6px;
    border: 1px solid #e2e8f0;
    vertical-align: middle;
  }

  table.data-table tr:nth-child(even) {
    background-color: #f8fafc;
  }

  table.data-table tr.highlight {
    background-color: #fef3c7;
    font-weight: 600;
  }

  .callout-box {
    border-radius: 6px;
    padding: 6px 10px;
    margin: 5px 0;
    font-size: 8.1pt;
    line-height: 1.35;
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

  .figure-container {
    text-align: center;
    margin: 5px auto;
  }

  .figure-container img {
    max-height: 64mm;
    width: auto;
    max-width: 98%;
    border-radius: 6px;
    border: 1px solid #cbd5e1;
    box-shadow: 0 2px 6px rgba(0,0,0,0.06);
  }

  .figure-caption {
    font-size: 7.3pt;
    color: #64748b;
    margin-top: 3px;
    font-style: italic;
  }

  .metric-row {
    display: flex;
    justify-content: space-between;
    margin: 5px 0 7px 0;
    gap: 8px;
  }

  .metric-card {
    flex: 1;
    background: #f8fafc;
    border: 1px solid #e2e8f0;
    border-radius: 6px;
    padding: 5px 7px;
    text-align: center;
  }

  .metric-val {
    font-size: 12pt;
    font-weight: 800;
    color: #6c5ce7;
    margin-bottom: 1px;
  }

  .metric-lbl {
    font-size: 6.8pt;
    color: #475569;
    text-transform: uppercase;
    font-weight: 700;
  }

  .footer-bar {
    display: flex;
    justify-content: space-between;
    align-items: center;
    border-top: 1px solid #e2e8f0;
    padding-top: 5px;
    font-size: 7.3pt;
    color: #64748b;
    font-weight: 600;
  }

  .p1-bg {
    position: absolute;
    top: 0;
    left: 0;
    width: 8.5in;
    height: 11in;
    object-fit: cover;
    z-index: 1;
    filter: brightness(0.65) contrast(1.15);
  }

  .p1-overlay {
    position: absolute;
    top: 0;
    left: 0;
    width: 8.5in;
    height: 11in;
    background: linear-gradient(135deg, rgba(15, 23, 42, 0.78) 0%, rgba(108, 92, 231, 0.35) 55%, rgba(15, 23, 42, 0.90) 100%);
    z-index: 2;
  }

  .p1-content {
    position: absolute;
    top: 0;
    left: 0;
    width: 8.5in;
    height: 11in;
    z-index: 3;
    padding: 1.6in 0.9in 0.8in 0.9in;
    display: flex;
    flex-direction: column;
    justify-content: space-between;
  }

  .p1-title-main {
    font-size: 38pt;
    font-weight: 800;
    color: #ffffff;
    letter-spacing: 2px;
    line-height: 1.05;
    margin: 0;
  }

  .p1-title-sub {
    font-size: 24pt;
    font-weight: 300;
    color: #e0e7ff;
    letter-spacing: 3px;
    line-height: 1.15;
    margin: 6px 0 0 0;
  }

  .p1-line {
    width: 320px;
    height: 5px;
    background-color: #a29bfe;
    margin-top: 16px;
    border-radius: 3px;
  }

  .p1-subtitle-box {
    margin-top: 22px;
    font-size: 11.5pt;
    font-weight: 500;
    color: #f1f5f9;
    line-height: 1.40;
    max-width: 90%;
    background: rgba(15, 23, 42, 0.45);
    padding: 12px 16px;
    border-radius: 8px;
    border: 1px solid rgba(162, 155, 254, 0.3);
  }

  .p1-footer {
    display: flex;
    align-items: center;
    margin-bottom: 0.2in;
  }

  .p1-logo {
    height: 95px;
    width: auto;
    margin-right: 18px;
  }

  .p1-institution {
    font-size: 16pt;
    font-weight: 700;
    color: #ffffff;
    line-height: 1.25;
  }

  .p1-institution {
    font-size: 13pt;
    font-weight: 800;
    color: #ffffff;
    line-height: 1.25;
    letter-spacing: 0.5px;
  }

  .p1-subinstitution {
    font-size: 10.5pt;
    font-weight: 700;
    color: #e0e7ff;
    line-height: 1.3;
  }

  .p1-data-item {
    font-size: 9.2pt;
    font-weight: 500;
    color: #cbd5e1;
    line-height: 1.35;
  }

  .p1-date {
    font-size: 8.8pt;
    font-weight: 600;
    color: #a29bfe;
    margin-top: 2px;
  }

  .badge-purple {
    display: inline-block;
    background: #ede9fe;
    color: #6c5ce7;
    font-weight: 700;
    font-size: 7.2pt;
    padding: 2px 6px;
    border-radius: 4px;
    border: 1px solid #ddd6fe;
  }
</style>
</head>
<body>

<!-- ========================================== -->
<!-- PÁGINA 1: PORTADA EJECUTIVA DEL AVANCE     -->
<!-- ========================================== -->
<div class="slide-page">
  <img class="p1-bg" src="data:image/jpeg;base64,__ASSET_portada_fraude_tarjetas.jpg__" alt="Fondo Cyber Fraude">
  <div class="p1-overlay"></div>
  <div class="p1-content">
    <div>
      <h1 class="p1-title-main">DOCUMENTO TÉCNICO</h1>
      <h2 class="p1-title-sub">PROYECTO INTEGRADOR</h2>
      <div class="p1-line"></div>
    </div>

    <div class="p1-footer">
      <img class="p1-logo" src="data:image/png;base64,__ASSET_udeg_logo.png__" alt="Escudo UdeG">
      <div class="p1-data-list">
        <div class="p1-institution">UNIVERSIDAD DE GUADALAJARA</div>
        <div class="p1-subinstitution">Centro Universitario de Guadalajara (CUGDL)</div>
        <div class="p1-data-item">Licenciatura en Inteligencia Artificial y Ciencia de Datos</div>
        <div class="p1-data-item">Data Mining y Knowledge Discovery</div>
        <div class="p1-data-item">Profesora: Mtra. Milagros Contreras Elizalde</div>
        <div class="p1-data-item">Alumno: Roberto Alejandro Chagra Martínez</div>
        <div class="p1-data-item p1-date">Octubre de 2026 &bull; Guadalajara, Jalisco, México</div>
      </div>
    </div>
  </div>
</div>

<!-- ========================================== -->
<!-- PÁGINA 2: ETAPA 1 - OBJETIVO Y DESBALANCE  -->
<!-- ========================================== -->
<div class="slide-page">
  <div class="page-padding">
    <div>
      <div class="header-box">
        <h1 class="section-h1">1. Contexto Financiero y Planteamiento del Problema</h1>
        <span class="kdd-tag">Etapa 1 KDD: Objetivo</span>
      </div>
      <div class="definition-box">
        <strong>Definición del Objetivo KDD:</strong> Establecer qué se desea lograr y comprender el dominio bancario, modelando la asimetría de costos y la captura de señales débiles bajo desbalance severo de clases.
      </div>

      <div style="display: flex; justify-content: space-between; gap: 14px; margin-bottom: 8px;">
        <div style="flex: 1;">
          <p>En el procesamiento transaccional financiero, los fraudes se ocultan dentro de flujos masivos de operaciones normales. El avance de preparación de datos aborda tres desafíos metodológicos clave:</p>
          <ul>
            <li><strong>Paradoja de la Exactitud (Accuracy Paradox):</strong> Con <strong>97.945% de operaciones legítimas</strong> y apenas <strong>2.055% de fraude</strong> (razón 1:47.66), un modelo trivial que prediga siempre "Legítima" obtiene 97.95% de exactitud pero 0.0% de sensibilidad, dejando pasar todos los fraudes.</li>
            <li><strong>Asimetría de Costos:</strong> Un Falso Negativo (FN) genera pérdida económica directa para el banco (<strong>$279,842.20 USD</strong> acumulados en el dataset), mientras que un Falso Positivo (FP) solo genera fricción transaccional.</li>
            <li><strong>Tipologías Diversificadas:</strong> Card-Not-Present (51.29%), Account-Takeover (21.75%), Synthetic-Identity (15.04%) y Card-Present (11.92%).</li>
          </ul>
        </div>
        <div style="width: 44%;">
          <div style="position: relative; height: 165px; border-radius: 8px; overflow: hidden; border: 1px solid #cbd5e1; box-shadow: 0 4px 12px rgba(0,0,0,0.08);">
            <img src="data:image/jpeg;base64,__ASSET_transacciones_anomalias.jpg__" style="width: 100%; height: 100%; object-fit: cover; filter: brightness(0.85);" alt="Telemetría">
            <div style="position: absolute; bottom: 0; left: 0; right: 0; background: rgba(15,23,42,0.85); color: #ffffff; padding: 6px 10px; font-size: 7.2pt;">
              <strong>Telemetría Global:</strong> 100,000 transacciones calibradas con estadísticas de la Fed, Nilson Report y BCE.
            </div>
          </div>
        </div>
      </div>

      <div class="metric-row">
        <div class="metric-card">
          <div class="metric-val">100,000</div>
          <div class="metric-lbl">Transacciones Ingeridas</div>
        </div>
        <div class="metric-card">
          <div class="metric-val">2.055%</div>
          <div class="metric-lbl">Tasa de Fraude (1:47.66)</div>
        </div>
        <div class="metric-card">
          <div class="metric-val">$279,842</div>
          <div class="metric-lbl">Quebranto Financiero USD</div>
        </div>
        <div class="metric-card">
          <div class="metric-val">51.29%</div>
          <div class="metric-lbl">Fraude No Presencial (CNP)</div>
        </div>
      </div>

      <div class="figure-container">
        <img src="data:image/png;base64,__ASSET_fig01_diagnostico_target_y_nulos.png__" alt="Figura 1: Diagnóstico Target y Nulos">
        <div class="figure-caption">Figura 1: Desbalance de clases (97.945% vs 2.055%), distribución por tipología de fraude y diagnóstico de completitud por columna.</div>
      </div>
    </div>

    <div class="footer-bar">
      <span>Entregable: Documento_Tecnico_Proyecto_Integrador_Data_Mining_Avance_Personal</span>
      <span>Página 2 de 9</span>
    </div>
  </div>
</div>

<!-- ========================================== -->
<!-- PÁGINA 3: ETAPA 2 - SELECCIÓN Y ANTI-LEAK  -->
<!-- ========================================== -->
<div class="slide-page">
  <div class="page-padding">
    <div>
      <div class="header-box">
        <h1 class="section-h1">2. Selección de Datos y Auditoría Anti-Leakage</h1>
        <span class="kdd-tag">Etapa 2 KDD: Selección</span>
      </div>
      <div class="definition-box">
        <strong>Definición de Selección KDD:</strong> Elegir los datos relevantes para alcanzar el objetivo planteado, depurando variables irrelevantes y erradicando atributos con fuga de información temporal o causal.
      </div>

      <p>El conjunto de datos original cuenta con <strong>43 características</strong> distribuidas en 6 familias semánticas. La selección rigurosa aplicó dos filtros metodológicos fundamentales:</p>

      <table class="data-table">
        <thead>
          <tr>
            <th>Familia Semántica</th>
            <th>Variables Incluidas</th>
            <th>Acción / Criterio Metodológico</th>
          </tr>
        </thead>
        <tbody>
          <tr>
            <td><strong>1. Identificadores y Tiempo</strong></td>
            <td><code>transaction_id</code>, <code>customer_id</code>, <code>card_id</code>, <code>merchant_id</code>, <code>transaction_datetime</code>, <code>customer_state</code></td>
            <td><span class="badge-purple">Excluidas (6)</span> Cardinalidad masiva; inducirían memorización espuria en vez de generalización de patrones conductuales.</td>
          </tr>
          <tr class="highlight">
            <td><strong>2. Variables Post-Evento</strong></td>
            <td><code>fraud_type</code>, <code>fraud_amount_lost</code></td>
            <td><span style="background: #fee2e2; color: #b91c1c; font-weight: 700; padding: 2px 5px; border-radius: 4px;">PURGADAS POR FUGA (Target Leakage)</span> Registradas únicamente tras la auditoría confirmada del fraude. Su inclusión provocaría un modelo ficticio inviable en producción.</td>
          </tr>
          <tr>
            <td><strong>3. Atributos Comerciales</strong></td>
            <td><code>transaction_amount</code>, <code>merchant_category</code>, <code>merchant_country</code>, <code>transaction_hour</code>, <code>distance_from_home_km</code>, etc.</td>
            <td><span class="badge-purple">Conservadas (9)</span> Atributos monetarios, temporales y geográficos legítimos al momento de la autorización.</td>
          </tr>
          <tr>
            <td><strong>4. Perfil del Cliente</strong></td>
            <td><code>customer_age</code>, <code>customer_gender</code>, <code>account_age_days</code>, <code>credit_limit</code>, <code>credit_score</code>, <code>num_cards_held</code></td>
            <td><span class="badge-purple">Conservadas (6)</span> Perfil demográfico y comportamiento de crédito histórico del tarjetahabiente.</td>
          </tr>
          <tr>
            <td><strong>5. Velocidad Transaccional</strong></td>
            <td><code>transactions_last_1h</code>, <code>amount_last_1h</code>, <code>transactions_last_24h</code>, <code>amount_vs_avg_ratio</code>, <code>num_declined_last_30d</code>, etc.</td>
            <td><span class="badge-purple">Conservadas (10)</span> Métricas de frecuencia y ráfagas operativas recientes.</td>
          </tr>
          <tr>
            <td><strong>6. Canal y Dispositivo</strong></td>
            <td><code>transaction_channel</code>, <code>device_type</code>, <code>browser</code>, <code>card_present</code>, <code>used_chip</code>, <code>used_pin</code>, <code>high_risk_country</code></td>
            <td><span class="badge-purple">Conservadas (9)</span> Indicadores técnicos de autenticación, canal y factores de riesgo geográfico.</td>
          </tr>
        </tbody>
      </table>

      <div class="callout-box callout-warning">
        <strong>Justificación Matemática contra Fuga de Datos (Target Leakage):</strong> En <code>fraud_amount_lost</code>, si el monto perdido es $>0$, la probabilidad a posteriori de fraude es exactamente $1.0000$. Mantener esta columna otorgaría un área ROC-AUC artificial de $1.000$, pero al operar en tiempo real sobre transacciones que aún no han sido investigadas, el motor fallaría totalmente. La purga reduce el conjunto a <strong>35 columnas legítimas</strong> (34 predictoras + 1 target).
      </div>

      <div class="callout-box callout-info">
        <strong>Entregables Asociados:</strong> Esta fase se encuentra totalmente implementada y documentada en la celda 11 del cuaderno <code>Notebook_Proyecto_Integrador_Data_Mining_Avance_Personal.ipynb</code>.
      </div>
    </div>

    <div class="footer-bar">
      <span>Entregable: Documento_Tecnico_Proyecto_Integrador_Data_Mining_Avance_Personal</span>
      <span>Página 3 de 9</span>
    </div>
  </div>
</div>

<!-- ========================================== -->
<!-- PÁGINA 4: ETAPA 3 - LIMPIEZA Y OUTLIERS    -->
<!-- ========================================== -->
<div class="slide-page">
  <div class="page-padding">
    <div>
      <div class="header-box">
        <h1 class="section-h1">3. Limpieza de Datos y Diagnóstico de Outliers</h1>
        <span class="kdd-tag">Etapa 3 KDD: Limpieza</span>
      </div>
      <div class="definition-box">
        <strong>Definición de Limpieza KDD:</strong> Eliminar inconsistencias, resolver valores faltantes estructurales y diagnosticar valores atípicos mediante criterios estadísticos formales.
      </div>

      <p><strong>1. Tratamiento Estructural de Nulos en `browser` (41,709 registros, 41.71%):</strong> Se demostró mediante tabla cruzada que los 41,709 valores `NaN` corresponden exactamente al 100% de las transacciones en canales físicos (35,777 en <code>POS Terminal</code> y 5,932 en <code>ATM</code>). Eliminar registros mediante <code>dropna()</code> habría borrado toda la operatoria presencial del banco (Sesgo de Selección). Se realizó una imputación semántica explícita asignando la categoría <code>'No_Aplica_Fisico'</code>.</p>

      <p><strong>2. Diagnóstico no paramétrico de Valores Atípicos (Criterio 1.5 &times; IQR de Tukey):</strong></p>
      <table class="data-table">
        <thead>
          <tr>
            <th>Variable Analizada</th>
            <th>Q1</th>
            <th>Mediana</th>
            <th>Q3</th>
            <th>IQR</th>
            <th>Límite Sup.</th>
            <th>Outliers (> Lím. Sup.)</th>
            <th>Fraude Normal</th>
            <th>Fraude Outlier</th>
            <th>Fraud Lift</th>
          </tr>
        </thead>
        <tbody>
          <tr class="highlight">
            <td><strong>transactions_last_1h</strong></td>
            <td>0.00</td>
            <td>0.00</td>
            <td>1.00</td>
            <td>1.00</td>
            <td>2.50</td>
            <td>8,990 (8.99%)</td>
            <td>1.71%</td>
            <td><strong>5.57%</strong></td>
            <td><strong>3.26x</strong></td>
          </tr>
          <tr>
            <td><strong>amount_last_1h</strong></td>
            <td>0.00</td>
            <td>0.00</td>
            <td>100.01</td>
            <td>100.01</td>
            <td>250.03</td>
            <td>11,150 (11.15%)</td>
            <td>1.85%</td>
            <td><strong>3.71%</strong></td>
            <td><strong>2.01x</strong></td>
          </tr>
          <tr>
            <td><strong>amount_vs_avg_ratio</strong></td>
            <td>0.21</td>
            <td>0.58</td>
            <td>1.66</td>
            <td>1.45</td>
            <td>3.84</td>
            <td>11,309 (11.31%)</td>
            <td>1.88%</td>
            <td><strong>3.44%</strong></td>
            <td><strong>1.83x</strong></td>
          </tr>
          <tr>
            <td><strong>distance_from_last_tx_km</strong></td>
            <td>5.20</td>
            <td>13.30</td>
            <td>31.90</td>
            <td>26.70</td>
            <td>71.95</td>
            <td>15,617 (15.62%)</td>
            <td>1.85%</td>
            <td><strong>3.18%</strong></td>
            <td><strong>1.72x</strong></td>
          </tr>
          <tr>
            <td><strong>transaction_amount</strong></td>
            <td>21.28</td>
            <td>52.26</td>
            <td>129.72</td>
            <td>108.44</td>
            <td>292.38</td>
            <td>9,959 (9.96%)</td>
            <td>1.95%</td>
            <td><strong>3.02%</strong></td>
            <td><strong>1.55x</strong></td>
          </tr>
        </tbody>
      </table>

      <div class="callout-box callout-success">
        <strong>Conclusión de Negocio: Outlier &ne; Error:</strong> Las transacciones situadas en las colas de velocidad concentran hasta <strong>3.26 veces más probabilidad de fraude</strong> que el rango normal. Eliminar los outliers destruiría la señal más valiosa del banco. Se resolvió <strong>conservar el 100% de las transacciones atípicas</strong>, mitigando su dispersión mediante escalamiento robusto en la siguiente fase.
      </div>

      <div class="figure-container">
        <img src="data:image/png;base64,__ASSET_fig02_diagnostico_outliers_iqr.png__" alt="Figura 2: Diagnóstico Tukey IQR">
        <div class="figure-caption">Figura 2: Diagnóstico de límites Tukey (1.5xIQR) y elevación de la tasa de fraude en las colas atípicas de las variables de velocidad.</div>
      </div>
    </div>

    <div class="footer-bar">
      <span>Entregable: Documento_Tecnico_Proyecto_Integrador_Data_Mining_Avance_Personal</span>
      <span>Página 4 de 9</span>
    </div>
  </div>
</div>

<!-- ========================================== -->
<!-- PÁGINA 5: ETAPA 4 - TRANSFORMACIÓN E ING   -->
<!-- ========================================== -->
<div class="slide-page">
  <div class="page-padding">
    <div>
      <div class="header-box">
        <h1 class="section-h1">4. Transformación e Ingeniería de Características</h1>
        <span class="kdd-tag">Etapa 4 KDD: Transformación</span>
      </div>
      <div class="definition-box">
        <strong>Definición de Transformación KDD:</strong> Convertir, enriquecer y escalar los datos mediante variables derivadas, partición estratificada y normalización matemática robusta sin fuga.
      </div>

      <p>Se diseñaron y formalizaron <strong>8 variables derivadas de dominio financiero</strong> para desenmascarar señales débiles concurrentes:</p>

      <table class="data-table">
        <thead>
          <tr>
            <th>Variable Derivada</th>
            <th>Fórmula Matemática</th>
            <th>Justificación Financiera y Comportamiento</th>
          </tr>
        </thead>
        <tbody>
          <tr class="highlight">
            <td><strong>composite_risk_index</strong></td>
            <td>Conteo de 10 señales de alerta activas (0 a 10)</td>
            <td>Acumulador de 10 alertas concurrentes. Eleva la tasa de fraude desde <strong>0.04% (nivel 0)</strong> hasta <strong>20.11% en nivel &ge; 5 (Lift 9.79x)</strong>.</td>
          </tr>
          <tr>
            <td><strong>velocity_tx_ratio_1h_24h</strong></td>
            <td><code>tx_1h / (tx_24h + 1)</code></td>
            <td>Mide la concentración súbita de frecuencia transaccional en la última hora respecto a la ventana diaria.</td>
          </tr>
          <tr>
            <td><strong>velocity_amt_ratio_1h_24h</strong></td>
            <td><code>monto_1h / (monto_24h + 1)</code></td>
            <td>Detecta ráfagas de gasto monetario acelerado previas a la detección o reporte de tarjeta robada.</td>
          </tr>
          <tr>
            <td><strong>credit_utilization_ratio</strong></td>
            <td><code>monto_tx / (limite_credito + 1)</code></td>
            <td>Evalúa la porción del límite disponible que la transacción individual intenta agotar.</td>
          </tr>
          <tr>
            <td><strong>zscore_amount_30d</strong></td>
            <td><code>(monto_tx - media_30d) / (std_30d + 1)</code></td>
            <td>Desviaciones estándar respecto al hábito de consumo histórico personal a 30 días del tarjetahabiente.</td>
          </tr>
          <tr>
            <td><strong>security_factors_count</strong></td>
            <td><code>card_present + used_chip + used_pin</code></td>
            <td>Métrica ordinal (0 a 3) de barreras físicas de autenticación presentes en la operación.</td>
          </tr>
          <tr>
            <td><strong>is_night_tx</strong></td>
            <td><code>1 si transaction_hour &le; 4, sino 0</code></td>
            <td>Bandera booleana de operaciones efectuadas en la madrugada (ventana de vulnerabilidad crítica).</td>
          </tr>
          <tr>
            <td><strong>is_new_account</strong></td>
            <td><code>1 si account_age_days &le; 90, sino 0</code></td>
            <td>Identifica cuentas nuevas vulnerables a fraude de identidad sintética y apertura de cuentas mula.</td>
          </tr>
        </tbody>
      </table>

      <div style="display: flex; gap: 10px; margin: 4px 0;">
        <div style="flex: 1;">
          <div class="callout-box callout-info" style="margin: 0;">
            <strong>Partición Estratificada 80/20:</strong> Train (80,000 registros, 1,644 fraudes) y Test (20,000 registros, 411 fraudes) conservan de manera idéntica el <strong>2.0550% de tasa de fraude</strong> sin sesgo.
          </div>
        </div>
        <div style="flex: 1;">
          <div class="callout-box callout-success" style="margin: 0;">
            <strong>Escalamiento Robusto Híbrido:</strong> Se aplicó compresión logarítmica $\ln(1+x)$ seguida de <code>RobustScaler</code> (mediana e IQR) ajustado estrictamente sobre <code>X_train</code> para evitar filtración de escala hacia <code>X_test</code>.
          </div>
        </div>
      </div>

      <div class="figure-container">
        <img src="data:image/png;base64,__ASSET_fig04_escalamiento_robusto_sin_leakage.png__" alt="Figura 4: Escalamiento Robusto">
        <div class="figure-caption">Figura 4: Contraste de distribuciones en bruto con asimetría extrema vs normalización centrada y estabilizada mediante log1p + RobustScaler.</div>
      </div>
    </div>

    <div class="footer-bar">
      <span>Entregable: Documento_Tecnico_Proyecto_Integrador_Data_Mining_Avance_Personal</span>
      <span>Página 5 de 9</span>
    </div>
  </div>
</div>

<!-- ========================================== -->
<!-- PÁGINA 6: ETAPA 4 - DOS MÉTODOS DE FILTRO  -->
<!-- ========================================== -->
<div class="slide-page">
  <div class="page-padding">
    <div>
      <div class="header-box">
        <h1 class="section-h1">5. Reducción de Dimensionalidad por Dos Métodos de Filtro</h1>
        <span class="kdd-tag">Etapa 4 KDD: Reducción</span>
      </div>
      <div class="definition-box">
        <strong>Definición de Reducción de Dimensionalidad KDD:</strong> Seleccionar el subconjunto óptimo de características mediante contrastes estadísticos objetivos paramétricos y no paramétricos.
      </div>

      <p>Tras la codificación One-Hot, la matriz predictora alcanzó <strong>91 variables</strong>. Se contrastaron dos paradigmas estadísticos de filtrado sobre <code>X_train</code>:</p>
      <ul>
        <li><strong>Método 1 — Paramétrico / Lineal (ANOVA F-statistic / $\chi^2$):</strong> Evalúa diferencias entre medias grupales asumiendo relaciones lineales directas con la clase objetivo.</li>
        <li><strong>Método 2 — No Paramétrico / No Lineal (Información Mutua de Shannon - MI):</strong> Cuantifica la reducción de incertidumbre en la entropía del target $I(X; Y)$, capturando interacciones no monótonas y patrones complejos.</li>
      </ul>

      <div class="metric-row">
        <div class="metric-card">
          <div class="metric-val">80.0%</div>
          <div class="metric-lbl">Consenso en Top 25</div>
        </div>
        <div class="metric-card">
          <div class="metric-val">#1 Unánime</div>
          <div class="metric-lbl">composite_risk_index</div>
        </div>
        <div class="metric-card">
          <div class="metric-val">30 Vars</div>
          <div class="metric-lbl">Subconjunto Seleccionado</div>
        </div>
        <div class="metric-card">
          <div class="metric-val">Auditable</div>
          <div class="metric-lbl">comparativa_dos_metodos_filtro.csv</div>
        </div>
      </div>

      <div class="figure-container">
        <img src="data:image/png;base64,__ASSET_fig05_comparativa_dos_metodos_filtro.png__" alt="Figura 5: Comparativa de Métodos de Filtro">
        <div class="figure-caption">Figura 5: Ranking espejo ANOVA F vs Información Mutua de Shannon para las 30 características líderes de la preparación de datos.</div>
      </div>

      <div class="callout-box callout-info" style="margin-top: 6px;">
        <strong>Hallazgo Clave de Selección:</strong> Ambos métodos coinciden en que <code>composite_risk_index</code> concentra la mayor capacidad de separación ($F=2,510.68$, $MI=0.0248$). La Información Mutua rescató variables de canal y horarios que la prueba lineal subestimaba, seleccionando las <strong>30 características finales</strong> para la validación cruzada.
      </div>
    </div>

    <div class="footer-bar">
      <span>Entregable: Documento_Tecnico_Proyecto_Integrador_Data_Mining_Avance_Personal</span>
      <span>Página 6 de 9</span>
    </div>
  </div>
</div>

<!-- ========================================== -->
<!-- PÁGINA 7: ETAPA 5 - PIPELINE 5-FOLD CV     -->
<!-- ========================================== -->
<div class="slide-page">
  <div class="page-padding">
    <div>
      <div class="header-box">
        <h1 class="section-h1">6. Minería de Datos y Pipeline 5-Fold Libre de Fuga</h1>
        <span class="kdd-tag">Etapa 5 KDD: Minería / CV</span>
      </div>
      <div class="definition-box">
        <strong>Definición de Minería en Validación Cruzada:</strong> Implementar un protocolo riguroso de particiones cruzadas estratificadas donde todo el preprocesamiento, escalamiento y selección se ajustan exclusivamente en los datos de entrenamiento del pliegue.
      </div>

      <div style="display: flex; gap: 14px; margin-bottom: 8px;">
        <div style="flex: 1.1;">
          <p><strong>1. Arquitectura Anti-Leakage en 5-Fold Stratified CV:</strong></p>
          <ul>
            <li>Se configuró <code>StratifiedKFold(n_splits=5, shuffle=True, random_state=42)</code> sobre las 80,000 transacciones de entrenamiento.</li>
            <li>En cada partición, los 64,000 datos de entrenamiento del pliegue se aislaron de los 16,000 datos de validación.</li>
            <li>El <code>ColumnTransformer</code> (con <code>log1p</code>, <code>RobustScaler</code> y <code>OneHotEncoder</code>) y el <code>SelectKBest(k=30)</code> se ajustaron mediante <code>fit_transform()</code> <strong>únicamente sobre los 64,000 datos de train</strong> y se proyectaron con <code>transform()</code> sobre la validación.</li>
          </ul>

          <p><strong>2. Modelos Evaluados en Validación Cruzada:</strong></p>
          <ul>
            <li><strong>Regresión Logística:</strong> <code>class_weight="balanced"</code>, optimizando umbrales lineales bajo regularización L2.</li>
            <li><strong>Random Forest:</strong> <code>n_estimators=120, max_depth=10, min_samples_leaf=15</code> con <code>class_weight="balanced_subsample"</code> para capturar interacciones no lineales entre las 30 variables.</li>
          </ul>
        </div>
        <div style="flex: 0.9;">
          <div style="position: relative; height: 195px; border-radius: 8px; overflow: hidden; border: 1px solid #cbd5e1; box-shadow: 0 4px 12px rgba(0,0,0,0.08);">
            <img src="data:image/jpeg;base64,__ASSET_mineria_datos_forense.jpg__" style="width: 100%; height: 100%; object-fit: cover; filter: brightness(0.85);" alt="Minería Forense">
            <div style="position: absolute; bottom: 0; left: 0; right: 0; background: rgba(15,23,42,0.85); color: #ffffff; padding: 6px 10px; font-size: 7.2pt;">
              <strong>Validación Cruzada Estratificada:</strong> Blindaje total contra la fuga de varianza y escala entre particiones.
            </div>
          </div>
        </div>
      </div>

      <table class="data-table">
        <thead>
          <tr>
            <th>Componente del Pipeline</th>
            <th>Transformador / Estimador</th>
            <th>Parámetros de Configuración</th>
            <th>Garantía Anti-Fuga Metodológica</th>
          </tr>
        </thead>
        <tbody>
          <tr>
            <td><strong>Variables de Cola Pesada</strong></td>
            <td><code>FunctionTransformer + RobustScaler</code></td>
            <td>$\ln(1+x)$ + Mediana e IQR</td>
            <td>Se ajusta exclusivamente en <code>X_fold_tr</code>; ningún valor de validación altera la escala.</td>
          </tr>
          <tr>
            <td><strong>Variables Categóricas</strong></td>
            <td><code>OneHotEncoder</code></td>
            <td><code>drop="first", handle_unknown="ignore"</code></td>
            <td>Categorías infrecuentes no vistas en entrenamiento se ignoran sin colapsar el pipeline.</td>
          </tr>
          <tr>
            <td><strong>Selección Univariada</strong></td>
            <td><code>SelectKBest</code></td>
            <td><code>score_func=f_classif, k=30</code></td>
            <td>El ranking de importancia se calcula únicamente con etiquetas de entrenamiento del pliegue.</td>
          </tr>
        </tbody>
      </table>
    </div>

    <div class="footer-bar">
      <span>Entregable: Documento_Tecnico_Proyecto_Integrador_Data_Mining_Avance_Personal</span>
      <span>Página 7 de 9</span>
    </div>
  </div>
</div>

<!-- ========================================== -->
<!-- PÁGINA 8: ETAPA 6 - EVALUACIÓN 5 PLIEGUES  -->
<!-- ========================================== -->
<div class="slide-page">
  <div class="page-padding">
    <div>
      <div class="header-box">
        <h1 class="section-h1">7. Evaluación Cuantitativa en los 5 Pliegues de CV</h1>
        <span class="kdd-tag">Etapa 6 KDD: Evaluación</span>
      </div>
      <div class="definition-box">
        <strong>Definición de Evaluación KDD:</strong> Determinar la solidez y estabilidad de la preparación de datos mediante métricas asimétricas rigurosas calculadas pliegue por pliegue.
      </div>

      <p>Resultados extraídos de <code>Resultados/resultados_validacion_cruzada_5fold.csv</code> en el cuaderno de trabajo:</p>

      <table class="data-table">
        <thead>
          <tr>
            <th>Partición / Pliegue</th>
            <th>Train (Fraudes)</th>
            <th>Val (Fraudes)</th>
            <th>LR ROC-AUC</th>
            <th>LR PR-AUC</th>
            <th>LR Recall</th>
            <th>RF ROC-AUC</th>
            <th>RF PR-AUC</th>
            <th>RF Recall</th>
            <th>RF F1-Score</th>
          </tr>
        </thead>
        <tbody>
          <tr>
            <td><strong>Pliegue 1</strong></td>
            <td>64,000 (1,316)</td>
            <td>16,000 (328)</td>
            <td>0.8369</td>
            <td>0.1641</td>
            <td>71.95%</td>
            <td>0.8169</td>
            <td>0.1405</td>
            <td>66.16%</td>
            <td>0.1328</td>
          </tr>
          <tr>
            <td><strong>Pliegue 2</strong></td>
            <td>64,000 (1,315)</td>
            <td>16,000 (329)</td>
            <td>0.8536</td>
            <td>0.1793</td>
            <td>77.20%</td>
            <td>0.8452</td>
            <td>0.1420</td>
            <td>68.39%</td>
            <td>0.1342</td>
          </tr>
          <tr>
            <td><strong>Pliegue 3</strong></td>
            <td>64,000 (1,315)</td>
            <td>16,000 (329)</td>
            <td>0.8663</td>
            <td>0.1785</td>
            <td>80.85%</td>
            <td>0.8500</td>
            <td>0.1507</td>
            <td>73.86%</td>
            <td>0.1421</td>
          </tr>
          <tr>
            <td><strong>Pliegue 4</strong></td>
            <td>64,000 (1,315)</td>
            <td>16,000 (329)</td>
            <td>0.8527</td>
            <td>0.2021</td>
            <td>74.47%</td>
            <td>0.8418</td>
            <td>0.1637</td>
            <td>65.35%</td>
            <td>0.1300</td>
          </tr>
          <tr>
            <td><strong>Pliegue 5</strong></td>
            <td>64,000 (1,315)</td>
            <td>16,000 (329)</td>
            <td>0.8519</td>
            <td>0.1981</td>
            <td>75.99%</td>
            <td>0.8398</td>
            <td>0.1570</td>
            <td>69.30%</td>
            <td>0.1335</td>
          </tr>
          <tr class="highlight">
            <td><strong>Promedio &plusmn; DE</strong></td>
            <td><strong>64,000</strong></td>
            <td><strong>16,000</strong></td>
            <td><strong>0.8523 &plusmn; 0.0104</strong></td>
            <td><strong>0.1844 &plusmn; 0.0156</strong></td>
            <td><strong>76.09% &plusmn; 3.30%</strong></td>
            <td><strong>0.8387 &plusmn; 0.0128</strong></td>
            <td><strong>0.1508 &plusmn; 0.0099</strong></td>
            <td><strong>68.61% &plusmn; 3.34%</strong></td>
            <td><strong>0.1345 &plusmn; 0.0044</strong></td>
          </tr>
        </tbody>
      </table>

      <div class="figure-container">
        <img src="data:image/png;base64,__ASSET_fig06_validacion_cruzada_5fold.png__" alt="Figura 6: Validación Cruzada 5-Fold">
        <div class="figure-caption">Figura 6: Desempeño y estabilidad por pliegue en 5-Fold Stratified CV (A: Estabilidad ROC-AUC; B: PR-AUC sin leakage).</div>
      </div>

      <div class="callout-box callout-success" style="margin-top: 4px;">
                <strong>Conclusiones de la Evaluación:</strong> (1) La estabilidad del ROC-AUC (&sigma; &le; 0.0128) confirma total ausencia de sobreajuste;
        (2) El PR-AUC medio alcanza <strong>0.1844 en Regresión Logística (8.97x sobre el azar)</strong> y <strong>0.1508 en Random Forest (7.34x)</strong>; y
        (3) La captura media alcanza el <strong>76.09% de los fraudes en Regresión Logística</strong> y <strong>68.61% en Random Forest</strong> en validación estricta.</div>
    </div>

    <div class="footer-bar">
      <span>Entregable: Documento_Tecnico_Proyecto_Integrador_Data_Mining_Avance_Personal</span>
      <span>Página 8 de 9</span>
    </div>
  </div>
</div>

<!-- ========================================== -->
<!-- PÁGINA 9: ETAPA 7 - INTERPRETACIÓN AVANCE  -->
<!-- ========================================== -->
<div class="slide-page">
  <div class="page-padding">
    <div>
      <div class="header-box">
        <h1 class="section-h1">8. Interpretación del Conocimiento y Conclusiones del Avance</h1>
        <span class="kdd-tag">Etapa 7 KDD: Interpretación</span>
      </div>
      <div class="definition-box">
        <strong>Definición de Interpretación KDD:</strong> Convertir los hallazgos y diagnósticos técnicos en lecciones aprendidas, blindaje metodológico y decisiones estratégicas para el proyecto.
      </div>

      <p>La culminación de la fase de preparación de datos arroja cuatro conclusiones fundamentales de ingeniería y negocio:</p>

      <div style="display: flex; gap: 14px; margin-top: 6px;">
        <div style="flex: 1.1;">
          <div class="callout-box callout-success" style="margin: 0 0 6px 0;">
            <strong>1. Éxito en Integridad y Calidad de Datos:</strong>
            Se transformaron 100,000 transacciones crudas en una matriz analítica limpia con 0 nulos, 0 duplicados y 0 fuga de información. Se evitó el sesgo de selección que habría borrado el 41.71% de transacciones presenciales.
          </div>
          <div class="callout-box callout-info" style="margin: 0 0 6px 0;">
            <strong>2. Demostración Matemática: Outlier &ne; Error:</strong>
            El diagnóstico no paramétrico de Tukey probó que las transacciones atípicas concentran hasta 3.26x más fraude. Su conservación y estabilización con <code>RobustScaler</code> rescató la señal operativa más valiosa del banco.
          </div>
          <div class="callout-box callout-warning" style="margin: 0;">
            <strong>3. Estado de Preparación para la Entrega Final:</strong>
            Con las 30 características líderes validadas en 5 pliegues libres de fuga, el dataset queda formalmente certificado y listo para las etapas finales de modelado avanzado y extracción de reglas de decisión.
          </div>
        </div>
        <div style="flex: 0.9;">
          <div style="position: relative; height: 165px; border-radius: 8px; overflow: hidden; border: 1px solid #cbd5e1; box-shadow: 0 4px 12px rgba(0,0,0,0.08);">
            <img src="data:image/jpeg;base64,__ASSET_escudo_decision_fraude.jpg__" style="width: 100%; height: 100%; object-fit: cover; filter: brightness(0.85);" alt="Escudo de Decisión">
            <div style="position: absolute; bottom: 0; left: 0; right: 0; background: rgba(15,23,42,0.85); color: #ffffff; padding: 6px 10px; font-size: 7.2pt;">
              <strong>Preparación Certificada:</strong> Datos listos para la autorización y reglas de prevención bancaria.
            </div>
          </div>
        </div>
      </div>

      <p style="margin-top: 8px;"><strong>Inventario Oficial de Entregables Sincronizados en la Carpeta `Entregables/`:</strong></p>
      <ul>
        <li><code>Notebook_Proyecto_Integrador_Data_Mining_Avance_Personal.ipynb</code> (Cuaderno maestro ejecutado).</li>
        <li><code>Reporte_Proyecto_Integrador_Data_Mining_Avance_Personal.pdf</code> (Reporte gráfico oficial del avance).</li>
        <li><code>Resultados/comparativa_dos_metodos_filtro.csv</code> y <code>Resultados/resultados_validacion_cruzada_5fold.csv</code>.</li>
        <li>Gráficas de alta resolución <code>fig01</code> a <code>fig06</code> en <code>Resultados/graficas/</code>.</li>
      </ul>
    </div>

    <div class="footer-bar">
      <span>Entregable: Documento_Tecnico_Proyecto_Integrador_Data_Mining_Avance_Personal</span>
      <span>Página 9 de 9</span>
    </div>
  </div>
</div>

</body>
</html>
"""

# Reemplazo de tokens de assets
for k, v in assets.items():
    html_content = html_content.replace(f"__ASSET_{k}__", v)

HTML_PATH = BASE_DIR / "temp_doc_tecnico.html"
HTML_PATH.write_text(html_content, encoding="utf-8")
print(f"HTML temporal generado en: {HTML_PATH.resolve()}")

PDF_OUTPUT_ENTREGABLES = BASE_DIR / "Documento_Tecnico_Proyecto_Integrador_Data_Mining_Avance_Personal.pdf"
PDF_OUTPUT_DOC_ADICIONAL = DOC_ADICIONAL_DIR / "Documentacion_Tecnica.pdf"

cmd = [
    CHROME_PATH,
    "--headless",
    "--disable-gpu",
    "--run-all-compositor-stages-before-draw",
    f"--print-to-pdf={PDF_OUTPUT_ENTREGABLES.resolve()}",
    "--no-pdf-header-footer",
    str(HTML_PATH.resolve()),
]

print("Compilando Documento Técnico PDF (Avance Entregables)...")
res = subprocess.run(cmd, capture_output=True, text=True)

if res.returncode == 0 and PDF_OUTPUT_ENTREGABLES.exists():
    print(f"PDF generado exitosamente en: {PDF_OUTPUT_ENTREGABLES.resolve()} ({PDF_OUTPUT_ENTREGABLES.stat().st_size:,} bytes)")
    
    # Copiar a Documentacion_adicional
    shutil.copy2(PDF_OUTPUT_ENTREGABLES, PDF_OUTPUT_DOC_ADICIONAL)
    print(f"PDF copiado a: {PDF_OUTPUT_DOC_ADICIONAL.resolve()}")

    reader = pypdf.PdfReader(str(PDF_OUTPUT_ENTREGABLES))
    print(f"Verificación PyPDF: Total de páginas = {len(reader.pages)}")
    for i in range(len(reader.pages)):
        lines = [l.strip() for l in reader.pages[i].extract_text().split("\n") if l.strip()]
        first_line = lines[0] if lines else "VACIA"
        print(f"  Pág {i+1}: {first_line[:75]}")

    HTML_PATH.unlink()
    print("Archivo temporal HTML eliminado.")
else:
    print(f"Error al generar PDF: {res.stderr}")
