"""
Módulo 1 KDD (Etapas 1, 2 y 3):
- Definición del Objetivo y Carga de Datos
- Selección de Datos y Prevención de Fuga de Información (Data Leakage)
- Limpieza Estructural de Valores Faltantes (Prevención de Sesgo de Selección)
- Diagnóstico Estadístico de Valores Atípicos (Regla 1.5 x IQR de Tukey)
"""

from pathlib import Path
from typing import Tuple
import pandas as pd
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import seaborn as sns


COLUMNAS_IDENTIFICADORES = [
    "transaction_id",
    "customer_id",
    "card_id",
    "merchant_id",
    "transaction_datetime",
    "customer_state",
]

COLUMNAS_LEAKAGE = [
    "fraud_type",
    "fraud_amount_lost",
]

VARIABLES_OUTLIERS_IQR = [
    "transaction_amount",
    "amount_last_1h",
    "distance_from_home_km",
    "distance_from_last_tx_km",
    "amount_vs_avg_ratio",
    "transactions_last_1h",
]


def cargar_y_seleccionar_datos(csv_path: Path, out_dir: Path) -> Tuple[pd.DataFrame, pd.DataFrame]:
    """
    Ejecuta las Etapas 1 y 2 del proceso KDD:
    Carga el dataset original, perfila el desbalance y excluye columnas con Data Leakage.
    """
    df_raw = pd.read_csv(csv_path)
    conteo = df_raw["is_fraud"].value_counts()
    prop = df_raw["is_fraud"].value_counts(normalize=True) * 100
    perdida_total = df_raw["fraud_amount_lost"].sum()

    print("=" * 88)
    print("MÓDULO 1 (ETAPAS 1-3 KDD): SELECCIÓN, LIMPIEZA Y DIAGNÓSTICO DE OUTLIERS")
    print("=" * 88)
    print(f"[Etapa 1-2] Dataset original cargado: {df_raw.shape[0]:,} filas x {df_raw.shape[1]} columnas")
    print(f"  - Transacciones Legítimas (0):    {conteo[0]:,} ({prop[0]:.3f}%)")
    print(f"  - Transacciones Fraudulentas (1): {conteo[1]:,} ({prop[1]:.3f}%) | Ratio 1:{conteo[0]/conteo[1]:.1f}")
    print(f"  - Pérdida económica acumulada:    ${perdida_total:,.2f} USD")

    # Exportar gráfica de desbalance y tipologías
    out_dir.mkdir(exist_ok=True, parents=True)
    fig, axes = plt.subplots(1, 2, figsize=(14, 5))
    bars = axes[0].bar(
        ["Legítima (0)", "Fraude (1)"],
        [conteo[0], conteo[1]],
        color=["#2b5c8f", "#d95f02"],
        edgecolor="black",
        width=0.55,
    )
    axes[0].set_title("Desbalance Extremo de la Variable Objetivo (is_fraud)", fontweight="bold")
    axes[0].set_ylabel("Número de Transacciones")
    axes[0].set_ylim(0, 115000)
    for bar, pct in zip(bars, [prop[0], prop[1]]):
        axes[0].text(
            bar.get_x() + bar.get_width() / 2,
            bar.get_height() + 1800,
            f"{int(bar.get_height()):,}\n({pct:.2f}%)",
            ha="center",
            fontweight="bold",
        )

    df_fraudes = df_raw[df_raw["is_fraud"] == 1]
    tipo_counts = df_fraudes["fraud_type"].value_counts()
    sns.barplot(x=tipo_counts.values, y=tipo_counts.index, palette="OrRd_r", ax=axes[1], edgecolor="black")
    axes[1].set_title("Distribución por Tipología de Fraude (n = 2,055)", fontweight="bold")
    axes[1].set_xlabel("Cantidad de Casos de Fraude")
    axes[1].set_ylabel("Modalidad (fraud_type)")
    axes[1].set_xlim(0, max(tipo_counts.values) * 1.22)
    for i, v in enumerate(tipo_counts.values):
        axes[1].text(v + 15, i, f"{v:,} ({v/len(df_fraudes)*100:.1f}%)", va="center", fontweight="bold")

    plt.tight_layout()
    fig.savefig(out_dir / "01_desbalance_y_tipologias.png", bbox_inches="tight")
    plt.close(fig)

    # Exclusión formal de identificadores y variables con Data Leakage
    df_seleccionado = df_raw.drop(columns=COLUMNAS_IDENTIFICADORES + COLUMNAS_LEAKAGE).copy()
    print(f"[Etapa 2] Columnas descartadas por Data Leakage: {COLUMNAS_LEAKAGE}")
    print(f"[Etapa 2] Dimensiones tras Selección: {df_seleccionado.shape[0]:,} filas x {df_seleccionado.shape[1]} columnas")
    return df_raw, df_seleccionado


def limpiar_y_diagnosticar_outliers(df: pd.DataFrame, out_dir: Path) -> Tuple[pd.DataFrame, pd.DataFrame]:
    """
    Ejecuta la Etapa 3 del proceso KDD:
    Imputa estructuralmente 'browser' y evalúa valores atípicos mediante 1.5 x IQR.
    """
    df_limpio = df.copy()
    nulos_browser = df_limpio["browser"].isnull().sum()
    canales_nulos = df_limpio[df_limpio["browser"].isnull()]["transaction_channel"].value_counts().to_dict()
    print(f"\n[Etapa 3] Nulos detectados en 'browser': {nulos_browser:,} -> Origen por canal: {canales_nulos}")
    df_limpio["browser"] = df_limpio["browser"].fillna("No_Aplica_Fisico")
    print(f"[Etapa 3] Nulos tras imputación estructural: {df_limpio.isnull().sum().sum()} | Duplicados: {df_limpio.duplicated().sum()}")

    resumen_iqr = []
    for col in VARIABLES_OUTLIERS_IQR:
        q1, q2, q3 = df_limpio[col].quantile([0.25, 0.50, 0.75])
        iqr = q3 - q1
        lim_inf, lim_sup = q1 - 1.5 * iqr, q3 + 1.5 * iqr
        mask_out = (df_limpio[col] < lim_inf) | (df_limpio[col] > lim_sup)
        n_out = int(mask_out.sum())
        tasa_out = df_limpio.loc[mask_out, "is_fraud"].mean() * 100 if n_out > 0 else 0.0
        tasa_norm = df_limpio.loc[~mask_out, "is_fraud"].mean() * 100
        resumen_iqr.append({
            "Variable": col,
            "Q1": round(q1, 2),
            "Mediana": round(q2, 2),
            "Q3": round(q3, 2),
            "IQR": round(iqr, 2),
            "Lim_Sup": round(lim_sup, 2),
            "Outliers_Count": n_out,
            "Outliers_%": round(n_out / len(df_limpio) * 100, 2),
            "Tasa_Fraude_Normal_%": round(tasa_norm, 2),
            "Tasa_Fraude_Outlier_%": round(tasa_out, 2),
            "Lift_Riesgo": round(tasa_out / max(tasa_norm, 1e-6), 2),
        })

    df_iqr = pd.DataFrame(resumen_iqr)
    df_iqr.to_csv(out_dir / "diagnostico_outliers_iqr.csv", index=False)
    print("\n[Etapa 3] Diagnóstico de Valores Atípicos (1.5 x IQR):")
    print(df_iqr.to_string(index=False))
    return df_limpio, df_iqr
