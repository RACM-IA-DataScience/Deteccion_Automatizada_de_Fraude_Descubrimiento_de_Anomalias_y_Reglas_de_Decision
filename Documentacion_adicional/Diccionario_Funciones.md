# 📚 Diccionario de Funciones — Proyecto Integrador

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
| `Series.quantile()` | Calcula cuantiles no paramétricos ($Q_1=0.25, Q_2=0.50, Q_3=0.75$) sobre variables continuas. | `q1, q2, q3 = df_clean[col].quantile([0.25, 0.50, 0.75])` | Proporcionó el rango $	ext{IQR} = Q_3 - Q_1$ y detectó `8,990` outliers en `tx_last_1h` y `11,150` en `amt_last_1h`. | Permite aplicar el criterio de Tukey ($1.5 	imes 	ext{IQR}$) sin asumir distribución gaussiana en variables asimétricas. |
| `DataFrame.groupby().agg()` | Segmenta las filas según categorías y aplica agregaciones matemáticas simultáneas (`mean`, `count`). | `df_feat.groupby("composite_risk_index")["is_fraud"].agg(["count", "mean"])` | Comprobó que conforme el índice de riesgo sube de 0 a $\ge 5$, la probabilidad de fraude salta de `0.04%` a `20.11%`. | Permite validar empíricamente hipótesis de negocio y estratificar el riesgo transaccional por bandas. |
| `pd.get_dummies()` | Transforma variables categóricas de texto en representaciones binarias dispersas (*One-Hot Encoding*). | `pd.get_dummies(df_feat, columns=CAT_COLS, drop_first=True, dtype=int)` | Transformó las 8 columnas nominales en variables binarias, expandiendo la matriz a `91` predictores numéricos. | Convierte texto en matrices algebraicas; `drop_first=True` evita colinealidad exacta entre dummies. |
| `np.log1p()` | Aplica la función no lineal logaritmo natural elemento a elemento: $y = \ln(1 + x)$. | `np.log1p(np.maximum(0, x))` | Estabilizó colas asimétricas extremas (montos de hasta $\$4,482.16$ contraídos a valores cercanos a $8.4$). | Comprime órdenes de magnitud en variables monetarias y espaciales sin producir $-\infty$ en ceros. |
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
| `RobustScaler()` | Estandariza variables numéricas restando la mediana ($Q_2$) y dividiendo entre el rango intercuartílico ($	ext{IQR}$). | `scaler = RobustScaler()`<br>`X_train_scaled = scaler.fit_transform(X_train_num)` | Estandarizó variables monetarias y de velocidad centradas en `0.0` y dispersión intercuartílica unitaria. | A diferencia de `StandardScaler` o `MinMaxScaler`, no se distorsiona con los outliers de fraude conservados. |
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
| `LogisticRegression()` | Modelo paramétrico lineal con regularización $L_2$ y soporte para ponderación de clases (`class_weight="balanced"`). | `LogisticRegression(max_iter=500, class_weight="balanced", random_state=42)` | Logró en los pliegues un $ROC	ext{-}AUC$ medio de `0.8523` y un Recall de `76.09%` sobre los fraudes de validación. | Punto de referencia paramétrico lineal rápido para evaluar la calidad de los datos preparados. |
| `RandomForestClassifier()` | Ensamble Bagging de árboles de decisión con submuestras ponderadas (`class_weight="balanced_subsample"`). | `RandomForestClassifier(n_estimators=120, max_depth=10, min_samples_leaf=15, random_state=42)` | Alcanzó un $ROC	ext{-}AUC$ medio de `0.8523` (LR) / `0.8387` (RF) y un $PR	ext{-}AUC$ medio de `0.1844` (8.97x sobre el azar) en 5-Fold CV. | Evalúa el poder de generalización del espacio reducido de 30 variables capturando interacciones no lineales. |
| `modelo.fit()` | Ajusta los pesos del clasificador optimizando la función de costo sobre los datos de entrenamiento del pliegue. | `clf_rf.fit(X_tr_sel, y_fold_tr)` | Entrenó el estimador en las 64,000 transacciones del pliegue sobre las 30 características seleccionadas. | Permite al algoritmo aprender los límites de decisión entre operaciones legítimas y fraudulentas. |
| `modelo.predict_proba()` | Devuelve las estimaciones de probabilidad continua normalizadas $[0.0, 1.0]$ para cada una de las clases. | `probs_rf = clf_rf.predict_proba(X_val_sel)[:, 1]` | Generó los puntajes continuos de riesgo sobre las 16,000 transacciones de validación de cada pliegue. | Requerido para evaluar las métricas asimétricas $ROC	ext{-}AUC$ y $PR	ext{-}AUC$ en validación cruzada. |
| `modelo.predict()` | Genera la asignación de clase categórica discreta (`0` o `1`) aplicando el umbral estándar de 0.50. | `preds_rf = clf_rf.predict(X_val_sel)` | Produjo las predicciones discretas de base para calcular Recall y F1-Score en los pliegues. | Necesaria para computar las métricas de clasificación discreta sobre la clase minoritaria. |

---

## 6. Funciones de Evaluación Métrica en Validación Cruzada (`scikit-learn.metrics`)

| Nombre de la función | Breve descripción de lo que hace | Sintaxis (cómo se escribe en el código) | Qué resultado generó en el proyecto | Por qué es necesaria su utilización |
| :--- | :--- | :--- | :--- | :--- |
| `roc_auc_score()` | Calcula el área bajo la curva de la tasa de verdaderos positivos vs falsos positivos ($ROC	ext{-}AUC$). | `roc_auc_score(y_fold_val, probs_rf)` | Reportó una media de `0.8523 ± 0.0104` en Regresión Logística y `0.8387 ± 0.0128` en Random Forest a través de los 5 pliegues. | Evalúa la capacidad global de ordenamiento del clasificador independientemente del umbral de decisión. |
| `average_precision_score()` | Estima el área bajo la curva Precision-Recall ($PR	ext{-}AUC$), enfocada exclusivamente en la clase de fraude. | `average_precision_score(y_fold_val, probs_rf)` | Registró una media de `0.1844 ± 0.0156` en Regresión Logística (**`8.97x` sobre el azar `0.0206`**) y `0.1508 ± 0.0099` en Random Forest (**`7.34x`**). | Estándar científico más exigente para validar datos bajo desbalance severo, ya que no se infla por los $TN$. |
| `recall_score()` | Mide la sensibilidad o tasa de captura de fraudes reales: $TP / (TP + FN)$. | `recall_score(y_fold_val, preds_rf)` | Demostró una captura media del `76.09% ± 3.30%` en Regresión Logística balanceada y `68.61% ± 3.34%` en Random Forest. | Métrica crítica en prevención de fraude: cuantifica la fracción de siniestros monetarios atrapados. |
| `precision_score()` | Evalúa la pureza de las alertas de fraude emitidas: $TP / (TP + FP)$. | `precision_score(y_fold_val, preds_rf)` | Permitió contrastar la proporción de alertas que correspondieron a fraudes reales en validación. | Mide la fricción operativa y el volumen de falsas alarmas que sufrirían los clientes legítimos. |
| `f1_score()` | Calcula la media armónica estricta entre Precisión y Sensibilidad: $2 \cdot rac{P \cdot R}{P + R}$. | `f1_score(y_fold_val, preds_rf)` | Reportó un $F_1$ medio de `0.1345 ± 0.0044` en Random Forest a través de los 5 pliegues. | Resume en un único escalar el balance entre detectar fraudes y controlar las falsas alarmas. |

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
