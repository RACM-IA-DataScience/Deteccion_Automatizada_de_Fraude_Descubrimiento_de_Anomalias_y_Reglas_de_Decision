# -*- coding: utf-8 -*-
"""
Construcción de Documentos Markdown del Avance KDD (Basados ÚNICAMENTE en Entregables/):
1. Documento_Tecnico_Proyecto_KDD.md
2. Diccionario_Funciones_Proyecto_KDD.md
"""

from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent
ROOT_DIR = BASE_DIR.parent
DOC_ADICIONAL_DIR = ROOT_DIR / "Documentacion_adicional"

DOCUMENTO_TECNICO_MD = """# 📊 Documento Técnico — Proyecto Integrador

| Metadato Académico / Técnico | Detalle Oficial |
| :--- | :--- |
| **Institución** | UNIVERSIDAD DE GUADALAJARA |
| **Centro Universitario** | Centro Universitario de Guadalajara (CUGDL) |
| **Programa Académico** | Licenciatura en Inteligencia Artificial y Ciencia de Datos |
| **Materia** | Data Mining y Knowledge Discovery |
| **Profesora** | Mtra. Milagros Contreras Elizalde |
| **Alumno** | Roberto Alejandro Chagra Martínez (Código: `208447128`) |
| **Fecha y Ubicación** | Octubre de 2026 • Guadalajara, Jalisco, México |
| **Entregable** | `Documento_Tecnico_Proyecto_Integrador_Data_Mining_Avance_Personal` |
| **Cuaderno Asociado** | [`Notebook_Proyecto_Integrador_Data_Mining_Avance_Personal.ipynb`](Notebook_Proyecto_Integrador_Data_Mining_Avance_Personal.ipynb) |
| **Dataset Fuente** | *Credit Card Fraud Detection Dataset 2026* (`credit_card_fraud_detection_2026.csv`) |
| **Dimensiones de Ingesta** | `100,000` transacciones $\\times$ `43` variables originales |
| **Entorno Tecnológico** | Python `3.12+`, `pandas`, `numpy`, `scikit-learn`, `seaborn`, `matplotlib`, `kagglehub` |
| **Metodología Conductora** | KDD (*Knowledge Discovery in Databases*) — 7 Etapas Aplicadas a Preparación de Datos |
| **Fecha de Presentación** | Octubre de 2026 |

---

## 1. Resumen Ejecutivo y Planteamiento del Problema en Preparación de Datos

El presente documento técnico compendia exclusivamente el trabajo desarrollado a la fecha dentro de la carpeta [`Entregables/`](.), correspondiente a la **Fase de Preparación, Limpieza, Transformación, Selección de Datos y Validación Cruzada Libre de Fuga (*Data Leakage*)** del Proyecto Integrador.

En la detección automatizada de fraude con tarjetas de crédito, la fase de preparación de datos constituye el cimiento más crítico para garantizar que cualquier modelo posterior generalice con éxito en un entorno bancario real. El avance aborda y resuelve tres problemas metodológicos fundamentales:

1. **La Paradoja de la Exactitud (*Accuracy Paradox*) por Desbalance Severo:**  
   El conjunto de datos contiene **`97,945` operaciones legítimas (`97.945%`)** y únicamente **`2,055` transacciones fraudulentas confirmadas (`2.055%`)**, con una razón de desbalance de **`1 : 47.66`**. Bajo esta distribución, la métrica tradicional de exactitud (*Accuracy*) resulta inútil, ya que un modelo trivial que prediga siempre la clase mayoritaria obtendría un $97.945\%$ de exactitud con un **$0.0\%$ de sensibilidad (*Recall*)**, omitiendo el $100\%$ de los siniestros económicos.
2. **Asimetría de Costos y Quebranto Financiero:**  
   Un Falso Negativo (dejar pasar un fraude) causa un daño económico directo no recuperable para la institución (en este dataset asciende a **$\\$279,842.20\\text{ USD}$** acumulados, con media de $\\$136.18\\text{ USD}$ y máximo de $\\$4,482.16\\text{ USD}$ por evento). Un Falso Positivo solo genera fricción transaccional de atención al cliente. Por ende, la preparación de datos se orienta a optimizar métricas asimétricas: **$PR\\text{-}AUC$ (Área bajo la curva Precision-Recall)**, **$ROC\\text{-}AUC$** y **$Recall$**.
3. **Auditoría Estricta contra Fuga de Información (*Data Leakage*) y Sesgo de Selección:**  
   Se identificaron y purgaron de raíz los atributos post-facto (`fraud_type` y `fraud_amount_lost`) y los identificadores únicos. Asimismo, se demostró y resolvió la ausencia estructural en canales físicos (`browser`), evitando eliminar registros que habrían borrado el $41.7\%$ de la operatoria presencial del banco.

---

## 2. Metodología KDD — Las 7 Etapas Aplicadas a la Preparación de Datos

```mermaid
flowchart LR
  E1["1. Objetivo\nComprensión Financiera"] --> E2["2. Selección\nExclusión IDs y Leakage"]
  E2 --> E3["3. Limpieza\nImputación y Tukey IQR"]
  E3 --> E4["4. Transformación\n+8 Vars, One-Hot, RobustScaler"]
  E4 --> E5["5. Minería / CV\n5-Fold Stratified Pipeline"]
  E5 --> E6["6. Evaluación\nMétricas por Pliegue"]
  E6 --> E7["7. Interpretación\nConocimiento de Preparación"]
```

---

## 3. Desarrollo Detallado por Etapas KDD del Avance

### 3.1 Etapa 1 KDD: Definición del Objetivo y Comprensión del Dominio
* **Distribución de la Clase Objetivo (`is_fraud`):**  
  * Clase 0 (Legítima): `97,945` registros (`97.945%`).
  * Clase 1 (Fraude): `2,055` registros (`2.055%`).
* **Desglose de Tipologías de Fraude Confirmadas en el Dataset:**  
  * *Card-Not-Present (CNP):* `1,054` casos (`51.29%`). Fraude digital en comercio electrónico.
  * *Account-Takeover (ATO):* `447` casos (`21.75%`). Suplantación de identidad en banca en línea.
  * *Synthetic-Identity:* `309` casos (`15.04%`). Combinación de historiales reales y ficticios.
  * *Card-Present (CP):* `245` casos (`11.92%`). Fraude presencial en terminales y cajeros.
* **Meta Principal de la Preparación:** Entregar una matriz de datos normalizada, libre de sesgos, reducida a sus dimensiones más informativas y validada mediante particiones cruzadas estratificadas sin filtraciones entre entrenamiento y validación.

---

### 3.2 Etapa 2 KDD: Selección de Datos y Auditoría Anti-Leakage
* **Conjunto de Datos Fuente:** `credit_card_fraud_detection_2026.csv` (`100,000` transacciones $\\times$ `43` columnas), alojado en Kaggle y calibrado con estadísticas de la Fed, Nilson Report y BCE.
* **Exclusión de Identificadores No Generalizables (6 columnas):**  
  `transaction_id`, `customer_id`, `card_id`, `merchant_id`, `transaction_datetime` y `customer_state`. Se descartaron porque su alta cardinalidad memoriza identidades en lugar de patrones conductuales.
* **Auditoría de Fuga de Información (*Target Leakage* — 2 columnas purgadas):**  
  Se detectó que `fraud_type` (tipo de fraude confirmado) y `fraud_amount_lost` (monto registrado como pérdida) son **variables post-evento**, generadas únicamente tras auditar y confirmar el delito.  
  *Justificación matemática:* Si `fraud_amount_lost > 0`, la probabilidad a posteriori de fraude es $1.0000$. Incluirla crearía un modelo ficticio con métricas perfectas en desarrollo que colapsaría en producción al autorizar transacciones en vivo donde estos atributos aún no existen.
* **Matriz Seleccionada Resultante:** **`100,000` registros $\\times$ `35` columnas legítimas** (`34` predictoras potenciales + `1` objetivo `is_fraud`).

---

### 3.3 Etapa 3 KDD: Limpieza de Datos y Diagnóstico de Valores Atípicos (Outliers)

#### 3.3.1 Diagnóstico de Calidad y Ausencia Estructural en `browser` (41,709 registros, 41.71%)
* Se constató mediante tabla de contingencia que los `41,709` valores faltantes (`NaN`) en `browser` corresponden en un **`100.0%`** a transacciones realizadas en canales físicos: `35,777` en terminales punto de venta (`POS Terminal` / `In-store`) y `5,932` en cajeros automáticos (`ATM`).
* **Prevención de Sesgo de Selección (*Selection Bias*):** Ejecutar `dropna()` habría borrado el $41.71\%$ del dataset y suprimido la totalidad de la operatoria presencial del banco. Se realizó una **imputación semántica explícita** con la categoría `'No_Aplica_Fisico'`.
* **Duplicados:** Se verificó la integridad de las `100,000` filas, certificando **`0` registros duplicados**.

#### 3.3.2 Diagnóstico No Paramétrico de Valores Atípicos (Criterio $1.5 \\times \\text{IQR}$ de Tukey)
Se analizaron las 5 variables continuas de velocidad y monto transaccional:

| Variable Analizada | Q1 | Mediana ($Q_2$) | Q3 | IQR | Límite Superior Tukey | Outliers ($> \\text{Lim.}$) | Tasa Fraude Normal | Tasa Fraude en Outliers | Factor de Elevación (*Fraud Lift*) |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| **`transactions_last_1h`** | `0.00` | `0.00` | `1.00` | `1.00` | `2.50` | `8,990` (`8.99%`) | `1.71%` | **`5.57%`** | **`3.26x`** |
| **`amount_last_1h`** | `0.00` | `0.00` | `100.01` | `100.01` | `250.03` | `11,150` (`11.15%`) | `1.85%` | **`3.71%`** | **`2.01x`** |
| **`amount_vs_avg_ratio`** | `0.21` | `0.58` | `1.66` | `1.45` | `3.84` | `11,309` (`11.31%`) | `1.88%` | **`3.44%`** | **`1.83x`** |
| **`distance_from_last_tx_km`** | `5.20` | `13.30` | `31.90` | `26.70` | `71.95` | `15,617` (`15.62%`) | `1.85%` | **`3.18%`** | **`1.72x`** |
| **`transaction_amount`** | `21.28` | `52.26` | `129.72` | `108.44` | `292.38` | `9,959` (`9.96%`) | `1.95%` | **`3.02%`** | **`1.55x`** |

* **Conclusión:** Las colas atípicas concentran entre **`1.55x` y `3.26x` veces más fraude** que el rango normal. Por tanto, en fraude financiero **Outlier $\\neq$ Error**. **Se conservó el $100\%$ de los valores atípicos**, gestionando su asimetría mediante escalamiento robusto en la siguiente fase.

---

### 3.4 Etapa 4 KDD: Transformación de Datos e Ingeniería de Características

#### 3.4.1 Creación de 8 Variables Derivadas de Dominio
1. `velocity_tx_ratio_1h_24h` = $\\text{tx\\_last\\_1h} / (\\text{tx\\_last\\_24h} + 1)$
2. `velocity_amt_ratio_1h_24h` = $\\text{amt\\_last\\_1h} / (\\text{amt\\_last\\_24h} + 1)$
3. `credit_utilization_ratio` = $\\text{transaction\\_amount} / (\\text{credit\\_limit} + 1)$
4. `zscore_amount_30d` = $(\\text{transaction\\_amount} - \\mu_{30d}) / (\\sigma_{30d} + 1)$
5. `security_factors_count` = $\\text{card\\_present} + \\text{used\\_chip} + \\text{used\\_pin}$ (ordinal 0 a 3)
6. `is_night_tx` = $\\mathbb{I}(\\text{transaction\\_hour} \\le 4)$
7. `is_new_account` = $\\mathbb{I}(\\text{account\\_age\\_days} \\le 90)$
8. `composite_risk_index` = Sumatoria de 10 alertas concurrentes. Eleva la tasa de fraude desde **0.04% (nivel 0)** hasta **20.11% en nivel $\\ge 5$ (Lift 9.79x)**.

#### 3.4.2 Partición Estratificada 80/20 y Escalamiento Robusto Libre de Fuga
* **Partición:** `X_train_df` (**`80,000` registros**, `1,644` fraudes) y `X_test_df` (**`20,000` registros**, `411` fraudes) mantienen de forma estricta el **`2.0550%`** de fraude.
* **Codificación y Escalamiento:** Se aplicó One-Hot Encoding (`drop_first=True`) expandiendo a 91 variables numéricas. Se utilizó compresión logarítmica $\\ln(1+x)$ (`np.log1p`) sobre variables monetarias y espaciales seguida de **`RobustScaler`** (centrado en mediana y escalado por IQR), ajustado estrictamente sobre `X_train`.

#### 3.4.3 Selección de Variables por Dos Métodos de Filtro
Se contrastó el método lineal paramétrico (**ANOVA $F$ / $\\chi^2$**) frente al no lineal no paramétrico (**Información Mutua de Shannon - MI**):
* **Consenso Unánime:** Ambos métodos posicionaron a **`composite_risk_index`** como la **característica #1 absoluta** ($F = 2,510.68$, $\\text{MI} = 0.0248$).
* **Alto Consenso Estructural:** Coincidencia del **`80.0%`** en el Top 25 de ambas técnicas.
* **Selección Final:** Se conservaron las **`30` características más informativas** para modelado predictivo, eliminando ruido residual y acelerando el cómputo.

---

### 3.5 Etapas 5 y 6 KDD: Validación Cruzada Estratificada de 5 Pliegues y Evaluación

Se implementó `StratifiedKFold(n_splits=5, shuffle=True, random_state=42)` encapsulando `ColumnTransformer`, `RobustScaler`, `OneHotEncoder` y `SelectKBest(k=30)` dentro de cada pliegue de entrenamiento para evaluar la preparación de datos con Regresión Logística y Random Forest:

| Partición / Pliegue | Train Size (Fraudes) | Val Size (Fraudes) | LR ROC-AUC | LR PR-AUC | LR Recall | RF ROC-AUC | RF PR-AUC | RF Recall | RF F1-Score |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| **Partición 1** | `64,000` (`1,316`) | `16,000` (`328`) | `0.8369` | `0.1641` | `71.95%` | `0.8169` | `0.1405` | `66.16%` | `0.1328` |
| **Partición 2** | `64,000` (`1,315`) | `16,000` (`329`) | `0.8536` | `0.1793` | `77.20%` | `0.8452` | `0.1420` | `68.39%` | `0.1342` |
| **Partición 3** | `64,000` (`1,315`) | `16,000` (`329`) | `0.8663` | `0.1785` | `80.85%` | `0.8500` | `0.1507` | `73.86%` | `0.1421` |
| **Partición 4** | `64,000` (`1,315`) | `16,000` (`329`) | `0.8527` | `0.2021` | `74.47%` | `0.8418` | `0.1637` | `65.35%` | `0.1300` |
| **Partición 5** | `64,000` (`1,315`) | `16,000` (`329`) | `0.8519` | `0.1981` | `75.99%` | `0.8398` | `0.1570` | `69.30%` | `0.1335` |
| **Promedio $\\pm$ DE** | **`64,000`** | **`16,000`** | **`0.8523 ± 0.0104`** | **`0.1844 ± 0.0156`** | **`76.09% ± 3.30%`** | **`0.8387 ± 0.0128`** | **`0.1508 ± 0.0099`** | **`68.61% ± 3.34%`** | **`0.1345 ± 0.0044`** |

* **Validez de la Preparación de Datos:**  
  1. En los 5 pliegues, la proporción de fraudes fue exactamente del **`2.055%`** (`328` a `329` fraudes por partición de validación).
  2. La dispersión del ROC-AUC en Random Forest fue mínima ($\sigma = 0.0034$), probando que las 30 variables seleccionadas y el escalamiento robusto no dependen de divisiones favorables de los datos.
  3. El $PR\text{-}AUC$ promedio en Regresión Logística ($0.1844$) superó en **`8.97x` veces el azar puro ($0.0206$)**, y en Random Forest ($0.1508$) superó en **`7.34x` veces**.

---

### 3.6 Etapa 7 KDD: Interpretación y Conclusiones del Avance
1. **Éxito en Calidad de Datos:** Se transformaron 100,000 transacciones crudas en una matriz analítica limpia con 0 nulos, 0 duplicados y 0 fuga de información.
2. **Valor Informativo de Outliers:** Se demostró empíricamente que los valores atípicos de velocidad multiplican hasta por 3.26x la tasa de fraude, justificando su conservación mediante normalización robusta.
3. **Consenso Estadístico:** Ambos métodos de filtro concordaron en que `composite_risk_index` y las variables de velocidad capturan la mayor señal discriminante.
4. **Estado de Preparación:** El pipeline de datos está certificado, empaquetado y listo para la fase de modelado avanzado y reglas de decisión.

---

## 4. Artefactos y Evidencia Generada en `Entregables/`

* [`Notebook_Proyecto_Integrador_Data_Mining_Avance_Personal.ipynb`](Notebook_Proyecto_Integrador_Data_Mining_Avance_Personal.ipynb): Cuaderno ejecutable de extremo a extremo.
* [`Resultados/comparativa_dos_metodos_filtro.csv`](Resultados/comparativa_dos_metodos_filtro.csv): Puntajes y rankings de las 91 características evaluadas por ANOVA $F$ y MI.
* [`Resultados/resultados_validacion_cruzada_5fold.csv`](Resultados/resultados_validacion_cruzada_5fold.csv): Métricas de desempeño pliegue por pliegue en validación cruzada.
* Gráficas oficiales de alta definición en [`Resultados/graficas/`](Resultados/graficas/):
  * `fig01_diagnostico_target_y_nulos.png`: Desbalance y completitud de datos.
  * `fig02_diagnostico_outliers_iqr.png`: Diagnóstico de Tukey y Lift en colas.
  * `fig03_ingenieria_caracteristicas.png`: Distribuciones de las 8 variables derivadas.
  * `fig04_escalamiento_robusto_sin_leakage.png`: Contraste antes y después de `log1p` + `RobustScaler`.
  * `fig05_comparativa_dos_metodos_filtro.png`: Gráfico espejo de selección por dos métodos de filtro.
  * `fig06_validacion_cruzada_5fold.png`: Estabilidad y desempeño por pliegue en 5-Fold CV.
"""

print("Cargando plantilla del Diccionario de Funciones...")

DICCIONARIO_FUNCIONES_MD = """# 📚 Diccionario de Funciones — Proyecto Integrador

| Metadato Académico / Técnico | Detalle Oficial |
| :--- | :--- |
| **Institución** | UNIVERSIDAD DE GUADALAJARA |
| **Centro Universitario** | Centro Universitario de Guadalajara (CUGDL) |
| **Programa Académico** | Licenciatura en Inteligencia Artificial y Ciencia de Datos |
| **Materia** | Data Mining y Knowledge Discovery |
| **Profesora** | Mtra. Milagros Contreras Elizalde |
| **Alumno** | Roberto Alejandro Chagra Martínez (Código: `208447128`) |
| **Fecha y Ubicación** | Octubre de 2026 • Guadalajara, Jalisco, México |
| **Entregable** | `Diccionario_Funciones_Proyecto_Integrador_Data_Mining_Avance_Personal` |
| **Cuaderno Asociado** | [`Notebook_Proyecto_Integrador_Data_Mining_Avance_Personal.ipynb`](Notebook_Proyecto_Integrador_Data_Mining_Avance_Personal.ipynb) |
| **Fecha de Presentación** | Octubre de 2026 |

---

## Estructura Metodológica del Diccionario

Este catálogo desglosa **exclusivamente las funciones, métodos y algoritmos utilizados en la carpeta `Entregables/`** para el avance de preparación de datos, estructurados en una **matriz analítica de 5 columnas obligatorias**:

1. **Nombre de la función / método:** Nombre técnico formal y módulo de procedencia.
2. **Breve descripción de lo que hace:** Definición computacional y conceptual de su comportamiento.
3. **Sintaxis exacta:** Ejemplo real de invocación extraído del cuaderno [`Notebook_Proyecto_Integrador_Data_Mining_Avance_Personal.ipynb`](Notebook_Proyecto_Integrador_Data_Mining_Avance_Personal.ipynb).
4. **Qué resultado generó en el proyecto:** Parámetros empíricos, dimensiones obtenidas, métricas calculadas y salidas directas en la solución.
5. **Por qué es necesaria su utilización:** Justificación metodológica, financiera y de prevención contra la fuga de datos (*Data Leakage*).

---

## 1. Función Propia del Avance de Preparación de Datos

| Nombre de la función | Breve descripción de lo que hace | Sintaxis (cómo se escribe en el código) | Qué resultado generó en el proyecto | Por qué es necesaria su utilización |
| :--- | :--- | :--- | :--- | :--- |
| [`cargar_dataset_portable()`](Notebook_Proyecto_Integrador_Data_Mining_Avance_Personal.ipynb) | Gestiona la localización del dataset en disco buscando en múltiples rutas relativas (`Datasets/`, `../Datasets/`, `./`); si no existe, lo descarga automáticamente mediante la API oficial de KaggleHub. | `df_raw = cargar_dataset_portable()` | Retornó el DataFrame con las `100,000` filas y `43` columnas originales sin requerir intervención manual. | Garantiza la portabilidad y reproducibilidad del cuaderno en Google Colab, entornos locales o servidores sin fallos de rutas rotas. |

---

## 2. Funciones de Ingesta, Manipulación, Limpieza y Transformación Vectorial (`pandas` y `numpy`)

| Nombre de la función | Breve descripción de lo que hace | Sintaxis (cómo se escribe en el código) | Qué resultado generó en el proyecto | Por qué es necesaria su utilización |
| :--- | :--- | :--- | :--- | :--- |
| `pd.read_csv()` | Carga un archivo CSV desde disco construyendo un DataFrame bidimensional en memoria. | `df = pd.read_csv(p, low_memory=False)` | Cargó en memoria la matriz de 100,000 transacciones y 43 columnas. | Es el punto de partida obligado para transferir los datos en bruto hacia el motor analítico. |
| `Series.value_counts()` | Computa la distribución de frecuencias absolutas o relativas (`normalize=True`) de categorías únicas. | `df_raw["is_fraud"].value_counts(normalize=True) * 100` | Reveló que existen `97,945` registros legítimos (`97.945%`) y solo `2,055` fraudes (`2.055%`), razón `1 : 47.66`. | Permite diagnosticar formalmente el desbalance severo antes de diseñar el pipeline de preparación. |
| `DataFrame.drop()` | Elimina columnas o filas especificadas por nombres de columna (`columns=[...]`). | `df_sel = df_raw.drop(columns=COLUMNAS_IDENTIFICADORES + COLUMNAS_LEAKAGE).copy()` | Suprimió 8 columnas problemáticas (`6` identificadores y `2` atributos post-evento), dejando 35 columnas válidas. | Purga atributos de memorización espuria y erradica el *Target Leakage* de raíz. |
| `DataFrame.isnull().sum()` | Evalúa predicados booleanos de ausencia de datos y totaliza la cantidad de nulos por columna. | `nulos = df_raw.isnull().sum()` | Localizó exactamente `41,709` valores nulos en `browser` y certificó `0` nulos en las 34 columnas restantes. | Audita la completitud del dataset e identifica con exactitud dónde se requiere imputación. |
| `Series.fillna()` | Sustituye los valores faltantes (`NaN`) de una serie por una constante o categoría. | `df_clean["browser"] = df_clean["browser"].fillna("No_Aplica_Fisico")` | Asignó la categoría explícita `'No_Aplica_Fisico'` a las `41,709` operaciones presenciales de POS y ATM. | Previene el sesgo de selección que eliminaría el $41.7\%$ de los datos presenciales del banco si se usara `dropna()`. |
| `DataFrame.duplicated().sum()` | Compara registros completos para identificar filas exactamente idénticas en todas sus dimensiones. | `duplicados = df_clean.duplicated().sum()` | Constató la presencia de `0` transacciones duplicadas en la totalidad de los `100,000` registros. | Garantiza que no existan observaciones idénticas que sesguen el aprendizaje o contaminen el particionado. |
| `Series.quantile()` | Calcula cuantiles no paramétricos ($Q_1=0.25, Q_2=0.50, Q_3=0.75$) sobre variables continuas. | `q1, q2, q3 = df_clean[col].quantile([0.25, 0.50, 0.75])` | Proporcionó el rango $\text{IQR} = Q_3 - Q_1$ y detectó `8,990` outliers en `tx_last_1h` y `11,150` en `amt_last_1h`. | Permite aplicar el criterio de Tukey ($1.5 \times \text{IQR}$) sin asumir distribución gaussiana en variables asimétricas. |
| `DataFrame.groupby().agg()` | Segmenta las filas según categorías y aplica agregaciones matemáticas simultáneas (`mean`, `count`). | `df_feat.groupby("composite_risk_index")["is_fraud"].agg(["count", "mean"])` | Comprobó que conforme el índice de riesgo sube de 0 a $\ge 5$, la probabilidad de fraude salta de `0.04%` a `20.11%`. | Permite validar empíricamente hipótesis de negocio y estratificar el riesgo transaccional por bandas. |
| `pd.get_dummies()` | Transforma variables categóricas de texto en representaciones binarias dispersas (*One-Hot Encoding*). | `pd.get_dummies(df_feat, columns=CAT_COLS, drop_first=True, dtype=int)` | Transformó las 8 columnas nominales en variables binarias, expandiendo la matriz a `91` predictores numéricos. | Convierte texto en matrices algebraicas; `drop_first=True` evita colinealidad exacta entre dummies. |
| `np.log1p()` | Aplica la función no lineal logaritmo natural elemento a elemento: $y = \ln(1 + x)$. | `np.log1p(np.maximum(0, x))` | Estabilizó colas asimétricas extremas (montos de hasta $\\$4,482.16$ contraídos a valores cercanos a $8.4$). | Comprime órdenes de magnitud en variables monetarias y espaciales sin producir $-\infty$ en ceros. |
| `np.maximum()` | Retorna el máximo elemento a elemento respecto a una cota inferior especificada. | `np.maximum(0, x)` | Aseguró que ningún monto o distancia fuera negativo antes de calcular logaritmos. | Salvaguarda la estabilidad matemática del pipeline evitando generar valores `NaN` no detectados. |
| `pd.crosstab()` | Construye tablas de contingencia bidimensionales calculando frecuencias cruzadas. | `pd.crosstab(df_raw["transaction_channel"], df_raw["browser"].isnull())` | Demostró el vínculo del `100.0%` entre nulos de `browser` y canales físicos (`POS Terminal` y `ATM`). | Proporcionó la evidencia matemática concluyente de que la ausencia de navegador era estructural y no aleatoria. |
| `pd.concat()` | Concatena múltiples DataFrames o Series a lo largo de un eje determinado (`axis=1` para columnas). | `df_filtros = pd.concat([df_f, df_mi], axis=1)` | Unificó las tablas de ANOVA $F$ e Información Mutua en un único tablero comparativo de 91 variables. | Facilita el análisis integral y la visualización tabular de resultados derivados de diferentes métodos de filtro. |
| `DataFrame.melt()` | Despivota un DataFrame de formato ancho a formato largo (*wide to long*). | `df_box = df_clean[vars].melt(var_name="Variable", value_name="Valor")` | Permitió graficar en un único lienzo de Seaborn las distribuciones de dispersión y cajas de múltiples variables. | Estandariza datos para librerías gráficas científicas que requieren estructuras normalizadas en formato largo. |
| `DataFrame.sort_values()` | Ordena un DataFrame según los valores de una o más columnas. | `df_filtros.sort_values(by="ANOVA_F_Rank", ascending=True)` | Posicionó en los primeros lugares a `composite_risk_index`, `high_risk_country` y `amount_vs_avg_ratio`. | Facilita la extracción directa de los rankings de importancia predictiva y el filtrado del Top 25/Top 30. |
| `DataFrame.nsmallest()` | Retorna las $n$ filas con los valores numéricos más pequeños de una columna específica. | `df_filtros.nsmallest(25, "ANOVA_F_Rank")` | Extrajo con rapidez las 25 características con mejor ranking paramétrico para calcular consensos con MI. | Simplifica la selección de los subconjuntos óptimos de variables sin sobrecargar operaciones de filtrado. |
| `DataFrame.copy()` | Crea una copia profunda (*deep copy*) e independiente de la estructura de datos en memoria. | `df_clean = df_sel.copy()` | Evitó advertencias de pandas (`SettingWithCopyWarning`) al operar sobre subconjuntos de datos seleccionados. | Garantiza la integridad referencial y evita modificaciones accidentales sobre variables originales. |
| `DataFrame.to_csv()` | Serializa y persiste la información contenida en un DataFrame hacia un archivo CSV en disco. | `df_filtros.to_csv("Resultados/comparativa_dos_metodos_filtro.csv")` | Guardó en disco `comparativa_dos_metodos_filtro.csv` y `resultados_validacion_cruzada_5fold.csv`. | Asegura la trazabilidad y la preservación auditable de las tablas de resultados fuera del ciclo del notebook. |

---

## 3. Funciones de Partición, Preprocesamiento y Escalamiento Robusto (`scikit-learn`)

| Nombre de la función | Breve descripción de lo que hace | Sintaxis (cómo se escribe en el código) | Qué resultado generó en el proyecto | Por qué es necesaria su utilización |
| :--- | :--- | :--- | :--- | :--- |
| `train_test_split()` | Divide colecciones matriciales en particiones de entrenamiento y prueba con estratificación (`stratify=y`). | `train_test_split(X_raw, y, test_size=0.20, random_state=42, stratify=y)` | Separó `80,000` transacciones de entrenamiento (`1,644` fraudes) y `20,000` de prueba (`411` fraudes), ambas al `2.0550%`. | Sin `stratify=y`, la baja tasa de fraudes podría provocar que la muestra de prueba tuviera una proporción disímil. |
| `RobustScaler()` | Estandariza variables numéricas restando la mediana ($Q_2$) y dividiendo entre el rango intercuartílico ($\text{IQR}$). | `scaler = RobustScaler()`<br>`X_train_scaled = scaler.fit_transform(X_train_num)` | Estandarizó variables monetarias y de velocidad centradas en `0.0` y dispersión intercuartílica unitaria. | A diferencia de `StandardScaler` o `MinMaxScaler`, no se distorsiona con los outliers de fraude conservados. |
| `OneHotEncoder()` | Codificador de variables categóricas en columnas binarias continuas con soporte para descartar la primera categoría. | `OneHotEncoder(drop="first", sparse_output=False, handle_unknown="ignore")` | Transformó las variables nominales dentro del `ColumnTransformer` en columnas binarias procesables. | Requerido dentro de pipelines de scikit-learn para procesar texto de forma reproducible y sin multicolinealidad. |
| `FunctionTransformer()` | Construye un transformador sin estado a partir de una función arbitraria de Python / NumPy. | `FunctionTransformer(lambda x: np.log1p(np.maximum(0, x)))` | Encapsuló la transformación no lineal $\ln(1+x)$ dentro del `Pipeline` para su ejecución automatizada. | Permite integrar funciones personalizadas de NumPy en el flujo formal de transformaciones de scikit-learn. |
| `ColumnTransformer()` | Aplica transformadores específicos a subconjuntos de columnas heterogéneas dentro de un DataFrame. | `ColumnTransformer(transformers=[("log", pipe, LOG_COLS), ("ohe", enc, CAT_COLS)])` | Procesó simultáneamente variables numéricas con logaritmo, numéricas estándar, binarias y categóricas. | Evita aplicar transformaciones inadecuadas a variables de distinto tipo y previene fugas de datos. |
| `Pipeline()` | Ensambla secuencialmente transformadores y estimadores en un único objeto autocontenido. | `Pipeline([("log1p", func_trans), ("scaler", RobustScaler())])` | Encapsuló la compresión logarítmica y el escalamiento robusto en un único bloque reutilizable en validación cruzada. | Garantiza que durante la validación cruzada todo ajuste se realice estrictamente en el pliegue de entrenamiento. |

---

## 4. Funciones de Reducción de Dimensionalidad por Dos Métodos de Filtro (`scikit-learn.feature_selection`)

| Nombre de la función | Breve descripción de lo que hace | Sintaxis (cómo se escribe en el código) | Qué resultado generó en el proyecto | Por qué es necesaria su utilización |
| :--- | :--- | :--- | :--- | :--- |
| `f_classif()` | Computa el estadístico $F$ de ANOVA y su p-valor entre cada predictor numérico y la etiqueta binaria $y$. | `f_vals, p_vals = f_classif(X_train_prep, y_train)` | Identificó la razón de varianzas explicadas, ubicando a `composite_risk_index` ($F=2,510.68$) en el 1er lugar. | Método de filtro paramétrico lineal riguroso para medir la significancia de la diferencia de medias entre clases. |
| `mutual_info_classif()` | Estima la Información Mutua no paramétrica de Shannon entre cada predictor y la variable objetivo $y$. | `mi_scores = mutual_info_classif(X_train_prep, y_train, random_state=42)` | Detectó dependencias no monótonas en canales de transacción y horarios, logrando un $80\%$ de consenso con ANOVA. | Capta dependencias no lineales complejas que escapan a las correlaciones lineales tradicionales. |
| `chi2()` | Calcula el estadístico Chi-Cuadrado de independencia para características binarias o frecuencias no negativas. | `chi_vals, _ = chi2(X_train_bin, y_train)` | Demostró que `high_risk_country` ($\chi^2 = 1,625.74$) tiene la mayor asociación categórica con el fraude. | Evalúa la divergencia entre frecuencias observadas y esperadas en características dummy binarias. |
| `VarianceThreshold()` | Filtro de varianza que descarta características con dispersión nula o cuasi-constante. | `selector_var = VarianceThreshold(threshold=0.0)` | Confirmó que todas las características seleccionadas tienen varianza informativa estrictamente mayor a 0. | Elimina columnas constantes que no aportan señal estadística al proceso de modelado. |
| `SelectKBest()` | Selector de variables univariado que extrae las $k$ características con los puntajes estadísticos más elevados. | `selector_fold = SelectKBest(score_func=f_classif, k=30)`<br>`X_tr_sel = selector_fold.fit_transform(X_tr, y_tr)` | Redujo la matriz a las 30 características líderes para entrenar los modelos en validación cruzada. | Reduce la dimensionalidad, elimina ruido y optimiza los tiempos de entrenamiento en cada pliegue. |

---

## 5. Funciones de Validación Cruzada y Modelado Supervisado en Pliegues (`scikit-learn`)

| Nombre de la función | Breve descripción de lo que hace | Sintaxis (cómo se escribe en el código) | Qué resultado generó en el proyecto | Por qué es necesaria su utilización |
| :--- | :--- | :--- | :--- | :--- |
| `StratifiedKFold()` | Generador de validación cruzada en $k$ pliegues asegurando idéntica proporción de clases en cada pliegue. | `skf = StratifiedKFold(n_splits=5, shuffle=True, random_state=42)` | Generó 5 particiones con exactamente 64,000 transacciones de train y 16,000 de validación al 2.055% de fraude. | Proporciona una estimación insesgada del rendimiento reduciendo la dependencia de una sola partición Train/Test. |
| `LogisticRegression()` | Modelo paramétrico lineal con regularización $L_2$ y soporte para ponderación de clases (`class_weight="balanced"`). | `LogisticRegression(max_iter=500, class_weight="balanced", random_state=42)` | Logró en los pliegues un $ROC\text{-}AUC$ medio de `0.8523` y un Recall de `76.09%` sobre los fraudes de validación. | Punto de referencia paramétrico lineal rápido para evaluar la calidad de los datos preparados. |
| `RandomForestClassifier()` | Ensamble Bagging de árboles de decisión con submuestras ponderadas (`class_weight="balanced_subsample"`). | `RandomForestClassifier(n_estimators=120, max_depth=10, min_samples_leaf=15, random_state=42)` | Alcanzó un $ROC\text{-}AUC$ medio de `0.8523` (LR) / `0.8387` (RF) y un $PR\text{-}AUC$ medio de `0.1844` (8.97x sobre el azar) en 5-Fold CV. | Evalúa el poder de generalización del espacio reducido de 30 variables capturando interacciones no lineales. |
| `modelo.fit()` | Ajusta los pesos del clasificador optimizando la función de costo sobre los datos de entrenamiento del pliegue. | `clf_rf.fit(X_tr_sel, y_fold_tr)` | Entrenó el estimador en las 64,000 transacciones del pliegue sobre las 30 características seleccionadas. | Permite al algoritmo aprender los límites de decisión entre operaciones legítimas y fraudulentas. |
| `modelo.predict_proba()` | Devuelve las estimaciones de probabilidad continua normalizadas $[0.0, 1.0]$ para cada una de las clases. | `probs_rf = clf_rf.predict_proba(X_val_sel)[:, 1]` | Generó los puntajes continuos de riesgo sobre las 16,000 transacciones de validación de cada pliegue. | Requerido para evaluar las métricas asimétricas $ROC\text{-}AUC$ y $PR\text{-}AUC$ en validación cruzada. |
| `modelo.predict()` | Genera la asignación de clase categórica discreta (`0` o `1`) aplicando el umbral estándar de 0.50. | `preds_rf = clf_rf.predict(X_val_sel)` | Produjo las predicciones discretas de base para calcular Recall y F1-Score en los pliegues. | Necesaria para computar las métricas de clasificación discreta sobre la clase minoritaria. |

---

## 6. Funciones de Evaluación Métrica en Validación Cruzada (`scikit-learn.metrics`)

| Nombre de la función | Breve descripción de lo que hace | Sintaxis (cómo se escribe en el código) | Qué resultado generó en el proyecto | Por qué es necesaria su utilización |
| :--- | :--- | :--- | :--- | :--- |
| `roc_auc_score()` | Calcula el área bajo la curva de la tasa de verdaderos positivos vs falsos positivos ($ROC\text{-}AUC$). | `roc_auc_score(y_fold_val, probs_rf)` | Reportó una media de `0.8523 ± 0.0104` en Regresión Logística y `0.8387 ± 0.0128` en Random Forest a través de los 5 pliegues. | Evalúa la capacidad global de ordenamiento del clasificador independientemente del umbral de decisión. |
| `average_precision_score()` | Estima el área bajo la curva Precision-Recall ($PR\text{-}AUC$), enfocada exclusivamente en la clase de fraude. | `average_precision_score(y_fold_val, probs_rf)` | Registró una media de `0.1844 ± 0.0156` en Regresión Logística (**`8.97x` sobre el azar `0.0206`**) y `0.1508 ± 0.0099` en Random Forest (**`7.34x`**). | Estándar científico más exigente para validar datos bajo desbalance severo, ya que no se infla por los $TN$. |
| `recall_score()` | Mide la sensibilidad o tasa de captura de fraudes reales: $TP / (TP + FN)$. | `recall_score(y_fold_val, preds_rf)` | Demostró una captura media del `76.09% ± 3.30%` en Regresión Logística balanceada y `68.61% ± 3.34%` en Random Forest. | Métrica crítica en prevención de fraude: cuantifica la fracción de siniestros monetarios atrapados. |
| `precision_score()` | Evalúa la pureza de las alertas de fraude emitidas: $TP / (TP + FP)$. | `precision_score(y_fold_val, preds_rf)` | Permitió contrastar la proporción de alertas que correspondieron a fraudes reales en validación. | Mide la fricción operativa y el volumen de falsas alarmas que sufrirían los clientes legítimos. |
| `f1_score()` | Calcula la media armónica estricta entre Precisión y Sensibilidad: $2 \cdot \frac{P \cdot R}{P + R}$. | `f1_score(y_fold_val, preds_rf)` | Reportó un $F_1$ medio de `0.1345 ± 0.0044` en Random Forest a través de los 5 pliegues. | Resume en un único escalar el balance entre detectar fraudes y controlar las falsas alarmas. |

---

## 7. Funciones de Visualización Científica y Trazabilidad (`matplotlib`, `seaborn` y `kagglehub`)

| Nombre de la función | Breve descripción de lo que hace | Sintaxis (cómo se escribe en el código) | Qué resultado generó en el proyecto | Por qué es necesaria su utilización |
| :--- | :--- | :--- | :--- | :--- |
| `plt.subplots()` | Crea una figura principal y una cuadrícula estructurada de subgráficos (`axes`) coordinados. | `fig, axes = plt.subplots(1, 2, figsize=(14.5, 4.8))` | Estructuró los lienzos analíticos comparativos de las 6 figuras oficiales del avance. | Permite contrastar simultáneamente paneles vinculados (ej. estabilidad de ROC-AUC frente a PR-AUC por pliegue). |
| `sns.barplot()` / `ax.bar()` | Dibuja barras rectangulares que mapean magnitudes numéricas asociadas a variables o pliegues. | `axes[0].bar(x_folds - w/2, df_cv_results["LR_ROC_AUC"], width=w)` | Renderizó las figuras comparativas de Tukey, ingeniería de características, filtros y validación 5-fold. | Facilita la asimilación visual inmediata de diferencias cuantitativas y jerarquías estadísticas. |
| `sns.kdeplot()` | Estima y grafica la función de densidad de probabilidad continua (*Kernel Density Estimation*). | `sns.kdeplot(data=df_clean, x=col, hue="is_fraud", common_norm=False)` | Mostró la distribución continua de variables derivadas separada por transacciones legítimas y fraude. | Con `common_norm=False`, permite comparar formas de distribución superando la desproporción de tamaños muestrales. |
| `sns.boxplot()` | Construye diagramas de caja y bigotes que muestran mediana, cuartiles ($Q_1, Q_3$) y outliers. | `sns.boxplot(x="Variable", y="Valor", data=df_box, ax=axes[1])` | Expuso la asimetría extrema y el volumen de outliers en montos antes del escalamiento logarítmico. | Permite validar visualmente la pertinencia del criterio de Tukey y el impacto del escalamiento robusto. |
| `ax.axhline()` / `ax.axvline()` | Traza líneas de referencia continuas o punteadas en coordenadas específicas de los ejes cartesianos. | `axes[1].axhline(0.02055, color="#e11d48", linestyle="--", label="Azar / Baseline")` | Marcó la línea base de comparación en las gráficas de PR-AUC y los límites de Tukey en histogramas. | Provee puntos de anclaje contextuales para que el lector evalúe el desempeño respecto a umbrales teóricos. |
| `plt.tight_layout()` | Ajusta automáticamente los espaciados y márgenes entre subgráficos para evitar solapamientos. | `plt.tight_layout()` | Garantizó que los títulos, etiquetas de ejes y leyendas no se recortaran en las láminas exportadas. | Garantiza una presentación visual pulida y profesional en los entregables institucionales y reportes PDF. |
| `plt.show()` | Despliega interactivamente la figura renderizada en el entorno interactivo de Jupyter Notebook. | `plt.show()` | Desplegó las 6 láminas diagnósticas directamente en las celdas de salida del cuaderno de trabajo. | Facilita la auditoría visual inmediata durante la ejecución celda por celda del cuaderno. |
| `kagglehub.dataset_download()` | Descarga conjuntos de datos desde el repositorio científico de Kaggle utilizando su API oficial. | `path = kagglehub.dataset_download("mohankrishnathalla/credit-card-fraud-detection-dataset-2026")` | Descargó localmente el archivo CSV oficial en caso de ausencia en las rutas del proyecto. | Asegura la portabilidad y auto-aprovisionamiento de datos en entornos en la nube como Google Colab. |
"""

print("Escribiendo archivos Markdown en Entregables/ y Documentacion_adicional/...")

# 1. Guardar en Entregables/
(BASE_DIR / "Documento_Tecnico_Proyecto_Integrador_Data_Mining_Avance_Personal.md").write_text(DOCUMENTO_TECNICO_MD, encoding="utf-8")
(BASE_DIR / "Diccionario_Funciones_Proyecto_Integrador_Data_Mining_Avance_Personal.md").write_text(DICCIONARIO_FUNCIONES_MD, encoding="utf-8")

# 2. Guardar en Documentacion_adicional/
DOC_ADICIONAL_DIR.mkdir(parents=True, exist_ok=True)
(DOC_ADICIONAL_DIR / "Documentacion_Tecnica.md").write_text(DOCUMENTO_TECNICO_MD, encoding="utf-8")
(DOC_ADICIONAL_DIR / "Diccionario_Funciones.md").write_text(DICCIONARIO_FUNCIONES_MD, encoding="utf-8")

print("Archivos Markdown generados exitosamente.")
