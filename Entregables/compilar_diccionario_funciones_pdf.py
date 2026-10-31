# -*- coding: utf-8 -*-
"""
Compilador Oficial del Diccionario de Funciones del Avance KDD en formato PDF
Basado ÚNICAMENTE en la carpeta Entregables/ (Notebook y Scripts de Preparación de Datos).
Estilo visual institucional del reporte de avance (Montserrat, violeta/lavanda, tablas de 5 columnas).
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

print("Cargando assets para el Diccionario de Funciones del Avance...")

assets = {}

# 1. Logo institucional UdeG
logo_path = BASE_DIR / "imagenes_proyecto" / "template_assets" / "udeg_logo.png"
with open(logo_path, "rb") as f:
    assets["udeg_logo.png"] = base64.b64encode(f.read()).decode("utf-8")

# 2. Imágenes temáticas oficiales de Entregables/imagenes_proyecto/
PROJ_IMG_DIR = BASE_DIR / "imagenes_proyecto"
for fname in [
    "mineria_datos_forense.jpg",
    "transacciones_anomalias.jpg",
    "escudo_decision_fraude.jpg",
    "portada_fraude_tarjetas.jpg",
]:
    p = PROJ_IMG_DIR / fname
    with open(p, "rb") as f:
        assets[fname] = base64.b64encode(f.read()).decode("utf-8")

# Plantilla HTML
html_content = """<!DOCTYPE html>
<html lang="es">
<head>
<meta charset="UTF-8">
<title>Catálogo y Diccionario Técnico de Funciones del Avance KDD</title>
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
    padding: 0.52in 0.72in 0.42in 0.72in;
    height: 11in;
    box-sizing: border-box;
    display: flex;
    flex-direction: column;
    justify-content: space-between;
  }

  .header-box {
    margin-bottom: 5px;
  }

  .section-h1 {
    font-size: 16pt;
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
    padding: 4.5px 9px;
    font-size: 8pt;
    color: #14532d;
    margin: 3px 0 6px 0;
    border-radius: 0 4px 4px 0;
    line-height: 1.34;
  }

  p {
    font-size: 8.3pt;
    line-height: 1.35;
    color: #2d3436;
    margin: 0 0 5px 0;
    text-align: justify;
  }

  table.dict-table {
    width: 100%;
    border-collapse: collapse;
    margin: 4px 0 6px 0;
    font-size: 6.9pt;
    line-height: 1.28;
  }

  table.dict-table th {
    background-color: #0f172a;
    color: #ffffff;
    font-weight: 700;
    text-align: left;
    padding: 4px 5px;
    border: 1px solid #0f172a;
    font-size: 7.2pt;
  }

  table.dict-table td {
    padding: 3.2px 5px;
    border: 1px solid #e2e8f0;
    vertical-align: top;
  }

  table.dict-table tr:nth-child(even) {
    background-color: #f8fafc;
  }

  table.dict-table tr.highlight {
    background-color: #fef3c7;
    font-weight: 600;
  }

  code {
    font-family: 'Consolas', 'Courier New', monospace;
    font-size: 6.8pt;
    background: #ede9fe;
    color: #5b21b6;
    padding: 1px 3px;
    border-radius: 3px;
    border: 1px solid #ddd6fe;
    word-break: break-all;
  }

  .metric-row {
    display: flex;
    justify-content: space-between;
    margin: 4px 0 6px 0;
    gap: 8px;
  }

  .metric-card {
    flex: 1;
    background: #f8fafc;
    border: 1px solid #e2e8f0;
    border-radius: 6px;
    padding: 4px 6px;
    text-align: center;
  }

  .metric-val {
    font-size: 11pt;
    font-weight: 800;
    color: #6c5ce7;
  }

  .metric-lbl {
    font-size: 6.5pt;
    color: #475569;
    text-transform: uppercase;
    font-weight: 700;
  }

  .footer-bar {
    display: flex;
    justify-content: space-between;
    align-items: center;
    border-top: 1px solid #e2e8f0;
    padding-top: 4px;
    font-size: 7.2pt;
    color: #64748b;
    font-weight: 600;
  }

  .fn-name {
    font-weight: 700;
    color: #4338ca;
    font-size: 7.3pt;
  }

  .callout-box {
    border-radius: 6px;
    padding: 5px 8px;
    margin: 4px 0;
    font-size: 7.8pt;
    line-height: 1.34;
  }

  .callout-info {
    background-color: #f0f9ff;
    border-left: 4px solid #0284c7;
    color: #0c4a6e;
  }

  .callout-success {
    background-color: #f0fdf4;
    border-left: 4px solid #16a34a;
    color: #14532d;
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
    background: linear-gradient(135deg, rgba(15, 23, 42, 0.82) 0%, rgba(99, 102, 241, 0.35) 55%, rgba(15, 23, 42, 0.92) 100%);
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
    margin-top: 20px;
    font-size: 11.5pt;
    font-weight: 500;
    color: #f1f5f9;
    line-height: 1.40;
    max-width: 90%;
    background: rgba(15, 23, 42, 0.50);
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
</style>
</head>
<body>

<!-- ========================================== -->
<!-- PÁGINA 1: PORTADA DICCIONARIO              -->
<!-- ========================================== -->
<div class="slide-page">
  <img class="p1-bg" src="data:image/jpeg;base64,__ASSET_mineria_datos_forense.jpg__" alt="Fondo Minería Forense">
  <div class="p1-overlay"></div>
  <div class="p1-content">
    <div>
      <h1 class="p1-title-main">DICCIONARIO DE FUNCIONES</h1>
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
<!-- PÁGINA 2: SECCIÓN 1 Y 2 (INGESTA/EXPLORA)  -->
<!-- ========================================== -->
<div class="slide-page">
  <div class="page-padding">
    <div>
      <div class="header-box">
        <h1 class="section-h1">1. Función de Carga Portable y Exploración Inicial</h1>
        <span class="kdd-tag">Carga & Exploración</span>
      </div>
      <div class="definition-box">
        <strong>Funciones de Ingesta y Diagnóstico:</strong> Rutinas para cargar el conjunto de datos de forma portable e inspeccionar el desbalance y la integridad muestral en <code>Entregables/</code>.
      </div>

      <div class="metric-row">
        <div class="metric-card">
          <div class="metric-val">100,000</div>
          <div class="metric-lbl">Filas Ingeridas</div>
        </div>
        <div class="metric-card">
          <div class="metric-val">43 Vars</div>
          <div class="metric-lbl">Columnas Iniciales</div>
        </div>
        <div class="metric-card">
          <div class="metric-val">35 Vars</div>
          <div class="metric-lbl">Columnas Legítimas</div>
        </div>
        <div class="metric-card">
          <div class="metric-val">1:47.66</div>
          <div class="metric-lbl">Razón de Desbalance</div>
        </div>
      </div>

      <table class="dict-table">
        <thead>
          <tr>
            <th style="width: 17%;">Nombre de la Función</th>
            <th style="width: 20%;">Descripción Conceptual</th>
            <th style="width: 22%;">Sintaxis de Código</th>
            <th style="width: 20%;">Resultado en el Proyecto</th>
            <th style="width: 21%;">Por qué es Necesaria</th>
          </tr>
        </thead>
        <tbody>
          <tr>
            <td><span class="fn-name">cargar_dataset_portable()</span></td>
            <td>Localiza el CSV en rutas locales relativas o lo descarga mediante la API de KaggleHub.</td>
            <td><code>df_raw = cargar_dataset_portable()</code></td>
            <td>Cargó las 100,000 filas y 43 columnas de <code>credit_card_fraud_detection_2026.csv</code>.</td>
            <td>Garantiza reproducibilidad y portabilidad en Google Colab o entornos locales.</td>
          </tr>
          <tr>
            <td><span class="fn-name">pd.read_csv()</span></td>
            <td>Carga un archivo CSV desde disco construyendo un DataFrame bidimensional en memoria.</td>
            <td><code>df = pd.read_csv(p, low_memory=False)</code></td>
            <td>Cargó la matriz transaccional completa en memoria estructurada.</td>
            <td>Punto de entrada obligatorio para transferir los datos al motor analítico de Python.</td>
          </tr>
          <tr>
            <td><span class="fn-name">Series.value_counts()</span></td>
            <td>Calcula frecuencias absolutas o relativas (con <code>normalize=True</code>) de categorías únicas.</td>
            <td><code>df_raw["is_fraud"].value_counts(normalize=True)*100</code></td>
            <td>Reveló 97,945 legítimas (97.945%) y 2,055 fraudes (2.055%), razón 1:47.66.</td>
            <td>Diagnostica formalmente el desbalance severo antes de diseñar el pipeline.</td>
          </tr>
          <tr>
            <td><span class="fn-name">DataFrame.drop()</span></td>
            <td>Remueve columnas o filas especificadas mediante nombres de columna.</td>
            <td><code>df_sel = df_raw.drop(columns=COL_ID + COL_LEAK).copy()</code></td>
            <td>Suprimió 8 columnas problemáticas (6 IDs y 2 post-evento), dejando 35 válidas.</td>
            <td>Elimina variables de memorización y erradica el Target Leakage de raíz.</td>
          </tr>
          <tr>
            <td><span class="fn-name">DataFrame.isnull().sum()</span></td>
            <td>Evalúa presencia de valores nulos celda por celda y totaliza la cantidad por columna.</td>
            <td><code>nulos = df_raw.isnull().sum()</code></td>
            <td>Identificó exactamente 41,709 nulos en <code>browser</code> y 0 en las demás.</td>
            <td>Audita la completitud del conjunto y localiza intervenciones de imputación.</td>
          </tr>
          <tr>
            <td><span class="fn-name">Series.fillna()</span></td>
            <td>Reemplaza valores nulos (<code>NaN</code>) por un escalar, texto o valor estadístico.</td>
            <td><code>df_clean["browser"] = df_clean["browser"].fillna("No_Aplica_Fisico")</code></td>
            <td>Asignó la categoría explícita a las 41,709 operaciones presenciales (POS/ATM).</td>
            <td>Evita la eliminación destructiva del 41.7% de los datos presenciales del banco.</td>
          </tr>
          <tr>
            <td><span class="fn-name">DataFrame.duplicated().sum()</span></td>
            <td>Verifica si existen filas idénticas repetidas en todas las variables.</td>
            <td><code>dups = df_clean.duplicated().sum()</code></td>
            <td>Certificó la presencia de 0 transacciones duplicadas en las 100,000 filas.</td>
            <td>Garantiza que no existan observaciones idénticas que sesguen el aprendizaje.</td>
          </tr>
        </tbody>
      </table>
    </div>

    <div class="footer-bar">
      <span>Entregable: Diccionario_Funciones_Proyecto_Integrador_Data_Mining_Avance_Personal</span>
      <span>Página 2 de 8</span>
    </div>
  </div>
</div>

<!-- ========================================== -->
<!-- PÁGINA 3: SECCIÓN 2 (CONT) - OUTLIERS/TRANS -->
<!-- ========================================== -->
<div class="slide-page">
  <div class="page-padding">
    <div>
      <div class="header-box">
        <h1 class="section-h1">2. Agregación, Diagnóstico IQR y Transformación</h1>
        <span class="kdd-tag">Pandas & NumPy</span>
      </div>
      <div class="definition-box">
        <strong>Cuantiles y Transformaciones Matemáticas:</strong> Funciones para calcular límites no paramétricos de Tukey, validar tablas cruzadas y normalizar con logaritmos en <code>Entregables/</code>.
      </div>

      <div class="metric-row">
        <div class="metric-card">
          <div class="metric-val">1.5 x IQR</div>
          <div class="metric-lbl">Criterio de Tukey Aplicado</div>
        </div>
        <div class="metric-card">
          <div class="metric-val">Lift 3.26x</div>
          <div class="metric-lbl">Fraude en Outliers tx_1h</div>
        </div>
        <div class="metric-card">
          <div class="metric-val">log1p</div>
          <div class="metric-lbl">Estabilización ln(1+x)</div>
        </div>
        <div class="metric-card">
          <div class="metric-val">100% POS/ATM</div>
          <div class="metric-lbl">Ausencia Estructural Browser</div>
        </div>
      </div>

      <table class="dict-table">
        <thead>
          <tr>
            <th style="width: 17%;">Nombre de la Función</th>
            <th style="width: 20%;">Descripción Conceptual</th>
            <th style="width: 22%;">Sintaxis de Código</th>
            <th style="width: 20%;">Resultado en el Proyecto</th>
            <th style="width: 21%;">Por qué es Necesaria</th>
          </tr>
        </thead>
        <tbody>
          <tr>
            <td><span class="fn-name">Series.quantile()</span></td>
            <td>Calcula cuantiles no paramétricos ($Q_1=0.25, Q_2=0.50, Q_3=0.75$).</td>
            <td><code>q1, q2, q3 = df_clean[col].quantile([0.25, 0.50, 0.75])</code></td>
            <td>Calculó el IQR y detectó 8,990 outliers en <code>tx_last_1h</code> y 11,150 en <code>amt_last_1h</code>.</td>
            <td>Permite aplicar el criterio de Tukey sin suponer distribución normal.</td>
          </tr>
          <tr>
            <td><span class="fn-name">DataFrame.groupby().agg()</span></td>
            <td>Segmenta datos por categorías y computa agregaciones múltiples simultáneas.</td>
            <td><code>df_feat.groupby("composite_risk_index")["is_fraud"].agg(["count","mean"])</code></td>
            <td>Demostró que al subir el índice de 0 a &ge;5, la tasa salta de 0.04% a 20.11%.</td>
            <td>Valida empíricamente hipótesis de negocio y estratifica el riesgo crediticio.</td>
          </tr>
          <tr>
            <td><span class="fn-name">pd.get_dummies()</span></td>
            <td>Codifica columnas de texto en representaciones binarias dispersas (One-Hot Encoding).</td>
            <td><code>pd.get_dummies(df_feat, columns=CAT_COLS, drop_first=True, dtype=int)</code></td>
            <td>Convirtió las 8 variables nominales expandiendo el espacio a 91 variables.</td>
            <td>Transforma texto en matrices algebraicas; <code>drop_first=True</code> evita colinealidad.</td>
          </tr>
          <tr>
            <td><span class="fn-name">np.log1p()</span></td>
            <td>Aplica la función matemática logaritmo natural elemento a elemento: $y = \ln(1 + x)$.</td>
            <td><code>np.log1p(np.maximum(0, x))</code></td>
            <td>Comprimió montos de hasta $4,482 USD a valores cercanos a 8.4 sin dispersión.</td>
            <td>Estabiliza variables monetarias asimétricas sin producir $-\infty$ en ceros.</td>
          </tr>
          <tr>
            <td><span class="fn-name">np.maximum()</span></td>
            <td>Retorna el valor máximo elemento a elemento respecto a una cota especificada.</td>
            <td><code>np.maximum(0, x)</code></td>
            <td>Aseguró que ningún valor monetario fuera numéricamente negativo antes del logaritmo.</td>
            <td>Previene la aparición de valores indeterminados <code>NaN</code> en operaciones matemáticas.</td>
          </tr>
          <tr>
            <td><span class="fn-name">pd.crosstab()</span></td>
            <td>Construye tablas de contingencia calculando frecuencias cruzadas entre factores.</td>
            <td><code>pd.crosstab(df_raw["transaction_channel"], df_raw["browser"].isnull())</code></td>
            <td>Demostró que el 100% de nulos de <code>browser</code> pertenecían a canales físicos POS/ATM.</td>
            <td>Provee la evidencia matemática concluyente de ausencia por diseño.</td>
          </tr>
          <tr>
            <td><span class="fn-name">pd.concat()</span></td>
            <td>Concatena estructuras tabulares a lo largo de un eje determinado (columnas).</td>
            <td><code>df_filtros = pd.concat([df_f, df_mi], axis=1)</code></td>
            <td>Unificó los resultados de ANOVA F e Información Mutua en una sola tabla comparativa.</td>
            <td>Facilita el análisis integral y la visualización tabular de métricas combinadas.</td>
          </tr>
          <tr>
            <td><span class="fn-name">DataFrame.melt()</span></td>
            <td>Despivota una tabla de formato ancho a formato largo (*wide to long*).</td>
            <td><code>df_box = df_clean[vars].melt(var_name="Variable", value_name="Valor")</code></td>
            <td>Permitió graficar simultáneamente en Seaborn las cajas de dispersión de múltiples variables.</td>
            <td>Estandariza matrices numéricas para librerías gráficas científicas avanzadas.</td>
          </tr>
        </tbody>
      </table>
    </div>

    <div class="footer-bar">
      <span>Entregable: Diccionario_Funciones_Proyecto_Integrador_Data_Mining_Avance_Personal</span>
      <span>Página 3 de 8</span>
    </div>
  </div>
</div>

<!-- ========================================== -->
<!-- PÁGINA 4: SECCIÓN 2 Y 3 (PARTICIÓN Y SCALE)-->
<!-- ========================================== -->
<div class="slide-page">
  <div class="page-padding">
    <div>
      <div class="header-box">
        <h1 class="section-h1">3. Tablas, Partición y Escalamiento Robusto</h1>
        <span class="kdd-tag">Pandas & Scikit-Learn</span>
      </div>
      <div class="definition-box">
        <strong>Partición Estratificada y Normalización:</strong> Funciones para dividir sin sesgo y escalar sin fuga de información matemática hacia los conjuntos de validación y prueba en <code>Entregables/</code>.
      </div>

      <div class="metric-row">
        <div class="metric-card">
          <div class="metric-val">80/20</div>
          <div class="metric-lbl">Split Estratificado Train/Test</div>
        </div>
        <div class="metric-card">
          <div class="metric-val">2.055%</div>
          <div class="metric-lbl">Tasa Idéntica en Particiones</div>
        </div>
        <div class="metric-card">
          <div class="metric-val">RobustScaler</div>
          <div class="metric-lbl">Ajuste Estricto en Train</div>
        </div>
        <div class="metric-card">
          <div class="metric-val">Auditable</div>
          <div class="metric-lbl">Exportación CSV de Resultados</div>
        </div>
      </div>

      <table class="dict-table">
        <thead>
          <tr>
            <th style="width: 17%;">Nombre de la Función</th>
            <th style="width: 20%;">Descripción Conceptual</th>
            <th style="width: 22%;">Sintaxis de Código</th>
            <th style="width: 20%;">Resultado en el Proyecto</th>
            <th style="width: 21%;">Por qué es Necesaria</th>
          </tr>
        </thead>
        <tbody>
          <tr>
            <td><span class="fn-name">DataFrame.sort_values()</span></td>
            <td>Ordena registros ascendentemente o descendentemente según una o más columnas.</td>
            <td><code>df_filtros.sort_values(by="ANOVA_F_Rank", ascending=True)</code></td>
            <td>Ubicó en las primeras posiciones a <code>composite_risk_index</code> y <code>high_risk_country</code>.</td>
            <td>Extrae los rankings jerárquicos de importancia predictiva de forma directa.</td>
          </tr>
          <tr>
            <td><span class="fn-name">DataFrame.nsmallest()</span></td>
            <td>Extrae las $n$ filas con los valores numéricos más pequeños de una columna específica.</td>
            <td><code>df_filtros.nsmallest(25, "ANOVA_F_Rank")</code></td>
            <td>Seleccionó el Top 25 de características para calcular el consenso porcentual con MI.</td>
            <td>Optimiza operaciones de filtrado rápido sobre tablas de resultados analíticos.</td>
          </tr>
          <tr>
            <td><span class="fn-name">DataFrame.copy()</span></td>
            <td>Genera una copia profunda (*deep copy*) e independiente de la estructura y datos.</td>
            <td><code>df_feat = df_clean.copy()</code></td>
            <td>Evitó advertencias de memoria (<code>SettingWithCopyWarning</code>) en transformaciones.</td>
            <td>Garantiza aislamiento referencial evitando modificaciones sobre el objeto original.</td>
          </tr>
          <tr>
            <td><span class="fn-name">DataFrame.to_csv()</span></td>
            <td>Serializa y escribe la información tabular hacia un archivo CSV persistente en disco.</td>
            <td><code>df_filtros.to_csv("Resultados/comparativa...csv")</code></td>
            <td>Guardó en disco <code>comparativa_dos_metodos_filtro.csv</code> y <code>resultados_cv.csv</code>.</td>
            <td>Asegura la trazabilidad y la preservación auditable de los resultados fuera de RAM.</td>
          </tr>
          <tr>
            <td><span class="fn-name">train_test_split()</span></td>
            <td>Divide matrices en Train y Test con estratificación de etiquetas (<code>stratify=y</code>).</td>
            <td><code>train_test_split(X_raw, y, test_size=0.20, random_state=42, stratify=y)</code></td>
            <td>Separó 80,000 registros para Train y 20,000 para Test, ambos con 2.0550% de fraude.</td>
            <td>Evita que la partición aleatoria altere la proporción natural de clases en prueba.</td>
          </tr>
          <tr>
            <td><span class="fn-name">RobustScaler()</span></td>
            <td>Escala restando la mediana ($Q_2$) y dividiendo entre el rango intercuartílico ($\text{IQR}$).</td>
            <td><code>scaler = RobustScaler()</code><br><code>X_tr_num = scaler.fit_transform(X_tr_num)</code></td>
            <td>Estandarizó variables numéricas sin verse afectado por las ráfagas de fraude.</td>
            <td>A diferencia de StandardScaler, no colapsa su escala ante la presencia de outliers legítimos.</td>
          </tr>
          <tr>
            <td><span class="fn-name">OneHotEncoder()</span></td>
            <td>Codificador categórico para matrices de entrada con soporte para omitir la primera categoría.</td>
            <td><code>OneHotEncoder(drop="first", sparse_output=False)</code></td>
            <td>Transformó las columnas de texto dentro del <code>ColumnTransformer</code> de forma reproducible.</td>
            <td>Requerido en transformadores para procesar texto sin introducir colinealidad exacta.</td>
          </tr>
        </tbody>
      </table>
    </div>

    <div class="footer-bar">
      <span>Entregable: Diccionario_Funciones_Proyecto_Integrador_Data_Mining_Avance_Personal</span>
      <span>Página 4 de 8</span>
    </div>
  </div>
</div>

<!-- ========================================== -->
<!-- PÁGINA 5: SECCIÓN 3 Y 4 (PIPELINES Y FILTROS)-->
<!-- ========================================== -->
<div class="slide-page">
  <div class="page-padding">
    <div>
      <div class="header-box">
        <h1 class="section-h1">4. Pipelines y Reducción por Dos Métodos de Filtro</h1>
        <span class="kdd-tag">Pipelines & Filtros</span>
      </div>
      <div class="definition-box">
        <strong>Encapsulación y Selección Univariada:</strong> Transformadores compuestos y filtros estadísticos contrastados (paramétrico vs no paramétrico) implementados en <code>Entregables/</code>.
      </div>

      <div class="metric-row">
        <div class="metric-card">
          <div class="metric-val">ColumnTransformer</div>
          <div class="metric-lbl">Preprocesamiento Compuesto</div>
        </div>
        <div class="metric-card">
          <div class="metric-val">ANOVA F</div>
          <div class="metric-lbl">Filtro Paramétrico Lineal</div>
        </div>
        <div class="metric-card">
          <div class="metric-val">Información Mutua</div>
          <div class="metric-lbl">Filtro No Lineal de Shannon</div>
        </div>
        <div class="metric-card">
          <div class="metric-val">SelectKBest (30)</div>
          <div class="metric-lbl">Subconjunto Seleccionado</div>
        </div>
      </div>

      <table class="dict-table">
        <thead>
          <tr>
            <th style="width: 17%;">Nombre de la Función</th>
            <th style="width: 20%;">Descripción Conceptual</th>
            <th style="width: 22%;">Sintaxis de Código</th>
            <th style="width: 20%;">Resultado en el Proyecto</th>
            <th style="width: 21%;">Por qué es Necesaria</th>
          </tr>
        </thead>
        <tbody>
          <tr>
            <td><span class="fn-name">FunctionTransformer()</span></td>
            <td>Envuelve funciones de Python/NumPy en un transformador estándar de scikit-learn.</td>
            <td><code>FunctionTransformer(lambda x: np.log1p(np.maximum(0, x)))</code></td>
            <td>Permitió aplicar la compresión $\ln(1+x)$ dentro del Pipeline de forma modular.</td>
            <td>Integra operaciones matemáticas personalizadas en flujos de scikit-learn.</td>
          </tr>
          <tr>
            <td><span class="fn-name">ColumnTransformer()</span></td>
            <td>Aplica transformadores independientes a columnas específicas según su tipo semántico.</td>
            <td><code>ColumnTransformer([("log", pipe, LOG_COLS), ("ohe", enc, CAT_COLS)])</code></td>
            <td>Procesó simultáneamente variables de cola pesada, numéricas estándar y categóricas.</td>
            <td>Evita transformaciones inapropiadas a columnas dispares y previene fugas de datos.</td>
          </tr>
          <tr>
            <td><span class="fn-name">Pipeline()</span></td>
            <td>Encapsula transformadores secuenciales en un único estimador reproducible.</td>
            <td><code>log_scale_pipe = Pipeline([("log1p", ft), ("scaler", RobustScaler())])</code></td>
            <td>Unificó la compresión logarítmica y el escalamiento robusto en un bloque modular.</td>
            <td>Garantiza que el escalador se ajuste únicamente sobre los pliegues de entrenamiento.</td>
          </tr>
          <tr>
            <td><span class="fn-name">f_classif()</span></td>
            <td>Calcula el estadístico F de ANOVA unidireccional y p-valores entre predictores y clases.</td>
            <td><code>f_vals, p_vals = f_classif(X_tr_prep, y_train)</code></td>
            <td>Identificó que <code>composite_risk_index</code> ($F=2,510.68$) lidera la varianza explicada.</td>
            <td>Filtro paramétrico lineal para evaluar diferencias de medias entre clases.</td>
          </tr>
          <tr>
            <td><span class="fn-name">mutual_info_classif()</span></td>
            <td>Estima la Información Mutua no paramétrica de Shannon entre variables y el target $y$.</td>
            <td><code>mi = mutual_info_classif(X_tr_prep, y_train, random_state=42)</code></td>
            <td>Capturó dependencias no lineales en horarios y canales, logrando 80% de consenso con ANOVA.</td>
            <td>Detecta relaciones no monótonas complejas que escapan a correlaciones lineales.</td>
          </tr>
          <tr>
            <td><span class="fn-name">chi2()</span></td>
            <td>Calcula el estadístico Chi-Cuadrado de independencia para variables discretas o binarias.</td>
            <td><code>chi_vals, _ = chi2(X_tr_bin, y_train)</code></td>
            <td>Demostró que <code>high_risk_country</code> ($\chi^2=1,625.74$) tiene la mayor asociación.</td>
            <td>Permite evaluar la dependencia estadística en características categóricas dummy.</td>
          </tr>
          <tr>
            <td><span class="fn-name">VarianceThreshold()</span></td>
            <td>Descarta columnas con varianza idéntica o inferior a un umbral determinado.</td>
            <td><code>VarianceThreshold(threshold=0.0)</code></td>
            <td>Confirmó que todas las características seleccionadas tienen varianza informativa $>0$.</td>
            <td>Elimina variables cuasi-constantes que solo aportan redundancia o ruido.</td>
          </tr>
          <tr>
            <td><span class="fn-name">SelectKBest()</span></td>
            <td>Extrae automáticamente las $k$ características con los puntajes estadísticos más altos.</td>
            <td><code>selector_fold = SelectKBest(score_func=f_classif, k=30)</code></td>
            <td>Redujo la dimensionalidad a las 30 características líderes para entrenar en cada pliegue.</td>
            <td>Elimina ruido estadístico y optimiza los tiempos de convergencia de los modelos.</td>
          </tr>
        </tbody>
      </table>
    </div>

    <div class="footer-bar">
      <span>Entregable: Diccionario_Funciones_Proyecto_Integrador_Data_Mining_Avance_Personal</span>
      <span>Página 5 de 8</span>
    </div>
  </div>
</div>

<!-- ========================================== -->
<!-- PÁGINA 6: SECCIÓN 5 - MODELADO EN PLIEGUES -->
<!-- ========================================== -->
<div class="slide-page">
  <div class="page-padding">
    <div>
      <div class="header-box">
        <h1 class="section-h1">5. Validación Cruzada y Modelado Supervisado en Pliegues</h1>
        <span class="kdd-tag">CV & Modelado</span>
      </div>
      <div class="definition-box">
        <strong>Protocolo de Modelado Libre de Fuga:</strong> Particiones estratificadas y ajuste de clasificadores supervisados para auditar la calidad predictiva de los datos preparados en <code>Entregables/</code>.
      </div>

      <div class="metric-row">
        <div class="metric-card">
          <div class="metric-val">5 Pliegues</div>
          <div class="metric-lbl">StratifiedKFold con Shuffle</div>
        </div>
        <div class="metric-card">
          <div class="metric-val">64,000 / 16,000</div>
          <div class="metric-lbl">Train / Val por Pliegue</div>
        </div>
        <div class="metric-card">
          <div class="metric-val">Regresión Logística</div>
          <div class="metric-lbl">Baseline Lineal Balanceado</div>
        </div>
        <div class="metric-card">
          <div class="metric-val">Random Forest</div>
          <div class="metric-lbl">Ensamble Bagging Balanceado</div>
        </div>
      </div>

      <table class="dict-table">
        <thead>
          <tr>
            <th style="width: 17%;">Nombre de la Función</th>
            <th style="width: 20%;">Descripción Conceptual</th>
            <th style="width: 22%;">Sintaxis de Código</th>
            <th style="width: 20%;">Resultado en el Proyecto</th>
            <th style="width: 21%;">Por qué es Necesaria</th>
          </tr>
        </thead>
        <tbody>
          <tr>
            <td><span class="fn-name">StratifiedKFold()</span></td>
            <td>Generador de particiones cruzadas que asegura idéntica proporción de clases en cada pliegue.</td>
            <td><code>skf = StratifiedKFold(n_splits=5, shuffle=True, random_state=42)</code></td>
            <td>Generó 5 particiones con exactamente 64,000 train y 16,000 val manteniendo 2.055% de fraude.</td>
            <td>Estima de forma insesgada el poder de generalización reduciendo varianza de muestreo.</td>
          </tr>
          <tr>
            <td><span class="fn-name">LogisticRegression()</span></td>
            <td>Modelo lineal paramétrico con regularización $L_2$ y ponderación balanceada de clases.</td>
            <td><code>LogisticRegression(max_iter=500, class_weight="balanced", random_state=42)</code></td>
            <td>Logró en los pliegues un ROC-AUC medio de 0.8523 y un Recall del 76.09%.</td>
            <td>Punto de referencia paramétrico lineal para evaluar la calidad de los datos preparados.</td>
          </tr>
          <tr>
            <td><span class="fn-name">RandomForestClassifier()</span></td>
            <td>Ensamble Bagging de árboles con submuestras balanceadas (<code>class_weight="balanced_subsample"</code>).</td>
            <td><code>RandomForestClassifier(n_estimators=120, max_depth=10, min_samples_leaf=15)</code></td>
            <td>Alcanzó un ROC-AUC medio de 0.8523 (LR) / 0.8387 (RF) y un PR-AUC medio de 0.1844 (8.97x sobre el azar).</td>
            <td>Evalúa el poder de generalización del espacio reducido capturando interacciones no lineales.</td>
          </tr>
          <tr>
            <td><span class="fn-name">modelo.fit()</span></td>
            <td>Ajusta los parámetros del clasificador sobre los datos de entrenamiento del pliegue.</td>
            <td><code>clf_rf.fit(X_tr_sel, y_fold_tr)</code></td>
            <td>Entrenó el estimador en las 64,000 transacciones del pliegue sobre las 30 variables.</td>
            <td>Permite al algoritmo aprender las fronteras de decisión entre legítimas y fraude.</td>
          </tr>
          <tr>
            <td><span class="fn-name">modelo.predict_proba()</span></td>
            <td>Retorna probabilidades continuas normalizadas $[0.0, 1.0]$ para cada una de las clases.</td>
            <td><code>probs_rf = clf_rf.predict_proba(X_val_sel)[:, 1]</code></td>
            <td>Generó las puntuaciones continuas de riesgo sobre las 16,000 transacciones de validación.</td>
            <td>Requerido para evaluar las métricas asimétricas ROC-AUC y PR-AUC en cada pliegue.</td>
          </tr>
          <tr>
            <td><span class="fn-name">modelo.predict()</span></td>
            <td>Genera la asignación de clase categórica discreta (0 o 1) aplicando el umbral de 0.50.</td>
            <td><code>preds_rf = clf_rf.predict(X_val_sel)</code></td>
            <td>Produjo las predicciones discretas de base para calcular Recall y F1 en validación.</td>
            <td>Necesaria para computar las métricas de clasificación discreta sobre la clase minoritaria.</td>
          </tr>
        </tbody>
      </table>
    </div>

    <div class="footer-bar">
      <span>Entregable: Diccionario_Funciones_Proyecto_Integrador_Data_Mining_Avance_Personal</span>
      <span>Página 6 de 8</span>
    </div>
  </div>
</div>

<!-- ========================================== -->
<!-- PÁGINA 7: SECCIÓN 6 - MÉTRICAS DE PLIEGUES -->
<!-- ========================================== -->
<div class="slide-page">
  <div class="page-padding">
    <div>
      <div class="header-box">
        <h1 class="section-h1">6. Funciones de Evaluación Métrica en Validación Cruzada</h1>
        <span class="kdd-tag">Métricas Asimétricas</span>
      </div>
      <div class="definition-box">
        <strong>Evaluación Asimétrica de la Preparación:</strong> Métricas enfocadas en la clase minoritaria de fraude para certificar la estabilidad inter-pliegues de la preparación de datos en <code>Entregables/</code>.
      </div>

      <div class="metric-row">
        <div class="metric-card">
          <div class="metric-val">0.8523 &plusmn; 0.0104</div>
          <div class="metric-lbl">Media ROC-AUC Random Forest</div>
        </div>
        <div class="metric-card">
          <div class="metric-val">0.1844 &plusmn; 0.0156</div>
          <div class="metric-lbl">Media PR-AUC (8.97x Azar)</div>
        </div>
        <div class="metric-card">
          <div class="metric-val">76.09% &plusmn; 3.30%</div>
          <div class="metric-lbl">Recall Fraude en Validación</div>
        </div>
        <div class="metric-card">
          <div class="metric-val">0.1345 &plusmn; 0.0044</div>
          <div class="metric-lbl">F1-Score Balanceado</div>
        </div>
      </div>

      <table class="dict-table">
        <thead>
          <tr>
            <th style="width: 17%;">Nombre de la Función</th>
            <th style="width: 20%;">Descripción Conceptual</th>
            <th style="width: 22%;">Sintaxis de Código</th>
            <th style="width: 20%;">Resultado en el Proyecto</th>
            <th style="width: 21%;">Por qué es Necesaria</th>
          </tr>
        </thead>
        <tbody>
          <tr>
            <td><span class="fn-name">roc_auc_score()</span></td>
            <td>Calcula el área bajo la curva Característica Operativa del Receptor ($ROC\text{-}AUC$).</td>
            <td><code>roc_auc_score(y_fold_val, probs_rf)</code></td>
            <td>Reportó una media de 0.8523 ± 0.0104 en Regresión Logística y 0.8387 ± 0.0128 en Random Forest a través de los 5 pliegues.</td>
            <td>Evalúa la capacidad de ordenamiento del clasificador independientemente del umbral.</td>
          </tr>
          <tr>
            <td><span class="fn-name">average_precision_score()</span></td>
            <td>Calcula el área bajo la curva Precision-Recall ($PR\text{-}AUC$) sobre la clase minoritaria.</td>
            <td><code>average_precision_score(y_fold_val, probs_rf)</code></td>
            <td>Registró una media de 0.1844 ± 0.0156 en Regresión Logística (8.97x sobre el azar) y 0.1508 ± 0.0099 en Random Forest (7.34x).</td>
            <td>Estándar científico más exigente para validar datos bajo desbalance, sin inflarse por TN.</td>
          </tr>
          <tr>
            <td><span class="fn-name">recall_score()</span></td>
            <td>Mide la sensibilidad o tasa de captura de fraudes reales: $TP / (TP + FN)$.</td>
            <td><code>recall_score(y_fold_val, preds_rf)</code></td>
            <td>Demostró una captura media del 76.09% en Regresión Logística balanceada y 68.61% en Random Forest.</td>
            <td>Métrica crítica en prevención de fraude: cuantifica la fracción de siniestros prevenidos.</td>
          </tr>
          <tr>
            <td><span class="fn-name">precision_score()</span></td>
            <td>Evalúa la pureza de las alertas de fraude emitidas: $TP / (TP + FP)$.</td>
            <td><code>precision_score(y_fold_val, preds_rf)</code></td>
            <td>Permitió contrastar la proporción de alertas que correspondieron a fraudes reales en validación.</td>
            <td>Mide la fricción operativa y el volumen de falsas alarmas que sufrirían clientes legítimos.</td>
          </tr>
          <tr>
            <td><span class="fn-name">f1_score()</span></td>
            <td>Calcula la media armónica estricta entre Precisión y Sensibilidad: $2 \cdot \frac{P \cdot R}{P + R}$.</td>
            <td><code>f1_score(y_fold_val, preds_rf)</code></td>
            <td>Reportó un $F_1$ medio de 0.1345 con $\sigma = 0.0044$ en Random Forest a través de los 5 pliegues.</td>
            <td>Resume en un único escalar el balance entre detectar fraudes y controlar falsas alarmas.</td>
          </tr>
        </tbody>
      </table>
    </div>

    <div class="footer-bar">
      <span>Entregable: Diccionario_Funciones_Proyecto_Integrador_Data_Mining_Avance_Personal</span>
      <span>Página 7 de 8</span>
    </div>
  </div>
</div>

<!-- ========================================== -->
<!-- PÁGINA 8: SECCIÓN 7 - GRÁFICAS & TRAZA     -->
<!-- ========================================== -->
<div class="slide-page">
  <div class="page-padding">
    <div>
      <div class="header-box">
        <h1 class="section-h1">7. Visualización Científica, Trazabilidad y Certificación</h1>
        <span class="kdd-tag">Gráficas & Trazabilidad</span>
      </div>
      <div class="definition-box">
        <strong>Comunicación Visual y Repositorio Oficial:</strong> Funciones para la renderización de láminas diagnósticas de alta resolución y certificación de reproducibilidad del avance en <code>Entregables/</code>.
      </div>

      <div class="metric-row">
        <div class="metric-card">
          <div class="metric-val">6 Figuras</div>
          <div class="metric-lbl">Láminas Analíticas Oficiales</div>
        </div>
        <div class="metric-card">
          <div class="metric-val">2 CSVs</div>
          <div class="metric-lbl">Resultados en Carpeta Resultados/</div>
        </div>
        <div class="metric-card">
          <div class="metric-val">KaggleHub</div>
          <div class="metric-lbl">Auto-Aprovisionamiento de Datos</div>
        </div>
        <div class="metric-card">
          <div class="metric-val">Colab / Local</div>
          <div class="metric-lbl">Ejecución Multi-Entorno</div>
        </div>
      </div>

      <table class="dict-table">
        <thead>
          <tr>
            <th style="width: 17%;">Nombre de la Función</th>
            <th style="width: 20%;">Descripción Conceptual</th>
            <th style="width: 22%;">Sintaxis de Código</th>
            <th style="width: 20%;">Resultado en el Proyecto</th>
            <th style="width: 21%;">Por qué es Necesaria</th>
          </tr>
        </thead>
        <tbody>
          <tr>
            <td><span class="fn-name">plt.subplots()</span></td>
            <td>Crea una figura principal y una cuadrícula estructurada de subgráficos (axes) coordinados.</td>
            <td><code>fig, axes = plt.subplots(1, 2, figsize=(14.5, 4.8))</code></td>
            <td>Estructuró los lienzos analíticos comparativos de las 6 figuras oficiales del avance.</td>
            <td>Permite contrastar simultáneamente paneles vinculados sin saturar el reporte.</td>
          </tr>
          <tr>
            <td><span class="fn-name">sns.barplot() / ax.bar()</span></td>
            <td>Dibuja barras rectangulares que mapean magnitudes numéricas asociadas a variables o pliegues.</td>
            <td><code>axes[0].bar(x_folds - w/2, df_cv["LR_ROC_AUC"], width=w)</code></td>
            <td>Renderizó las figuras comparativas de Tukey, ingeniería de características, filtros y 5-fold CV.</td>
            <td>Facilita la asimilación visual inmediata de diferencias cuantitativas y jerarquías.</td>
          </tr>
          <tr>
            <td><span class="fn-name">sns.kdeplot()</span></td>
            <td>Estima y grafica la función de densidad de probabilidad continua (*Kernel Density Estimation*).</td>
            <td><code>sns.kdeplot(data=df_clean, x=col, hue="is_fraud", common_norm=False)</code></td>
            <td>Mostró la distribución continua de variables derivadas separada por legítimas y fraude.</td>
            <td>Con <code>common_norm=False</code>, permite comparar formas de distribución superando el desbalance.</td>
          </tr>
          <tr>
            <td><span class="fn-name">sns.boxplot()</span></td>
            <td>Construye diagramas de caja y bigotes que muestran mediana, cuartiles y outliers de Tukey.</td>
            <td><code>sns.boxplot(x="Variable", y="Valor", data=df_box, ax=axes[1])</code></td>
            <td>Expuso la asimetría extrema y el volumen de outliers en montos antes de normalizar con log1p.</td>
            <td>Valida visualmente la pertinencia del criterio de Tukey y el impacto del escalamiento robusto.</td>
          </tr>
          <tr>
            <td><span class="fn-name">ax.axhline() / ax.axvline()</span></td>
            <td>Traza líneas de referencia continuas o discontinuas en coordenadas específicas.</td>
            <td><code>axes[1].axhline(0.02055, color="#e11d48", linestyle="--", label="Azar")</code></td>
            <td>Marcó la línea base de comparación en las gráficas de PR-AUC y los límites de Tukey.</td>
            <td>Proporciona puntos de referencia contextuales para evaluar la calidad predictiva frente al azar.</td>
          </tr>
          <tr>
            <td><span class="fn-name">plt.tight_layout()</span></td>
            <td>Ajusta automáticamente los márgenes y espaciados entre paneles para evitar solapamientos.</td>
            <td><code>plt.tight_layout()</code></td>
            <td>Aseguró que títulos, etiquetas de ejes y leyendas no sufrieran recortes visuales indeseados.</td>
            <td>Garantiza un acabado estético impecable en las figuras integradas en el notebook y reportes PDF.</td>
          </tr>
          <tr>
            <td><span class="fn-name">plt.show()</span></td>
            <td>Despliega interactivamente la figura renderizada en el entorno interactivo de Jupyter.</td>
            <td><code>plt.show()</code></td>
            <td>Desplegó las 6 láminas diagnósticas directamente en las celdas de salida del cuaderno.</td>
            <td>Facilita la auditoría visual inmediata durante la ejecución celda por celda.</td>
          </tr>
          <tr>
            <td><span class="fn-name">kagglehub.dataset_download()</span></td>
            <td>Descarga conjuntos de datos desde el repositorio de Kaggle utilizando su API oficial.</td>
            <td><code>kagglehub.dataset_download("mohankrishnathalla/credit-card-fraud...")</code></td>
            <td>Descargó localmente el archivo CSV oficial en caso de ausencia en las rutas del proyecto.</td>
            <td>Asegura la portabilidad y auto-aprovisionamiento de datos en Google Colab o servidores remotos.</td>
          </tr>
        </tbody>
      </table>

      <div class="callout-box callout-success" style="margin-top: 4px;">
        <strong>Certificación del Avance:</strong> La totalidad de las funciones listadas en este catálogo corresponden con fidelidad 100% al código ejecutado en <code>Notebook_Proyecto_Integrador_Data_Mining_Avance_Personal.ipynb</code> dentro de la carpeta <code>Entregables/</code>. El proceso de preparación de datos es completamente determinista y reproducible bajo Python 3.12 y scikit-learn.
      </div>
    </div>

    <div class="footer-bar">
      <span>Entregable: Diccionario_Funciones_Proyecto_Integrador_Data_Mining_Avance_Personal</span>
      <span>Página 8 de 8</span>
    </div>
  </div>
</div>

</body>
</html>
"""

# Reemplazo de tokens de assets
for k, v in assets.items():
    html_content = html_content.replace(f"__ASSET_{k}__", v)

HTML_PATH = BASE_DIR / "temp_diccionario_funciones.html"
HTML_PATH.write_text(html_content, encoding="utf-8")
print(f"HTML temporal generado en: {HTML_PATH.resolve()}")

PDF_OUTPUT_ENTREGABLES = BASE_DIR / "Diccionario_Funciones_Proyecto_Integrador_Data_Mining_Avance_Personal.pdf"
PDF_OUTPUT_DOC_ADICIONAL = DOC_ADICIONAL_DIR / "Diccionario_Funciones.pdf"

cmd = [
    CHROME_PATH,
    "--headless",
    "--disable-gpu",
    "--run-all-compositor-stages-before-draw",
    f"--print-to-pdf={PDF_OUTPUT_ENTREGABLES.resolve()}",
    "--no-pdf-header-footer",
    str(HTML_PATH.resolve()),
]

print("Compilando Diccionario de Funciones PDF (Avance Entregables)...")
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
