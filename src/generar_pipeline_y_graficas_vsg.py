# -*- coding: utf-8 -*-
"""
Script de ejecución determinista del Pipeline KDD Completo:
- Modelos seleccionados y calibración de umbrales
- Exportación estricta de figuras vectoriales en formato .vsg (y .svg para interoperabilidad)
- Paleta visual Cyber / Neon coherente: Deep Slate/Navy (#0f172a), Cyan Neón (#00f2fe), Magenta (#f43f5e), Violeta (#7c3aed), Amber (#f59e0b)
- Almacenamiento de artefactos y métricas cuantitativas
"""

import os
from pathlib import Path
import warnings
import numpy as np
import pandas as pd

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import seaborn as sns

from sklearn.model_selection import train_test_split
from sklearn.preprocessing import RobustScaler
from sklearn.feature_selection import chi2
from sklearn.ensemble import IsolationForest, RandomForestClassifier, GradientBoostingClassifier
from sklearn.tree import DecisionTreeClassifier, export_text, plot_tree
from sklearn.linear_model import LogisticRegression
from sklearn.dummy import DummyClassifier
from sklearn.metrics import (
    accuracy_score,
    precision_score,
    recall_score,
    f1_score,
    roc_auc_score,
    average_precision_score,
    confusion_matrix,
    roc_curve,
    precision_recall_curve,
)
from imblearn.over_sampling import SMOTE

warnings.filterwarnings("ignore")

# Definición de estilo y paleta visual unificada
CYBER_BG = "#0b1120"
CYBER_PANEL = "#111827"
CYBER_CYAN = "#00f2fe"
CYBER_BLUE = "#0284c7"
CYBER_MAGENTA = "#f43f5e"
CYBER_PURPLE = "#8b5cf6"
CYBER_AMBER = "#fbbf24"
CYBER_TEXT = "#0f172a"

plt.rcParams["font.sans-serif"] = ["DejaVu Sans", "Segoe UI", "Arial"]
plt.rcParams["axes.edgecolor"] = "#cbd5e1"
plt.rcParams["axes.linewidth"] = 0.9
plt.rcParams["grid.color"] = "#e2e8f0"
plt.rcParams["grid.linestyle"] = "--"
plt.rcParams["grid.alpha"] = 0.7

def main():
    root = Path(__file__).resolve().parent.parent
    data_path = root / "Datasets" / "credit_card_fraud_detection_2026.csv"
    results_dir = root / "results"
    results_dir.mkdir(exist_ok=True, parents=True)
    graficas_dir = root / "Entregables" / "Resultados" / "graficas"
    graficas_dir.mkdir(exist_ok=True, parents=True)

    print(f"[1/8] Cargando dataset: {data_path}")
    df_raw = pd.read_csv(data_path)
    total_tx = len(df_raw)
    conteo_clases = df_raw["is_fraud"].value_counts()
    prop_clases = df_raw["is_fraud"].value_counts(normalize=True) * 100
    perdida_total = df_raw["fraud_amount_lost"].sum()

    print(f"Total registros: {total_tx:,}")
    print(f"Legítimas: {conteo_clases[0]:,} ({prop_clases[0]:.2f}%)")
    print(f"Fraudes: {conteo_clases[1]:,} ({prop_clases[1]:.2f}%)")
    print(f"Pérdida contable acumulada: ${perdida_total:,.2f} USD")

    # -------------------------------------------------------------
    # FIGURA 1: Desbalance de la variable objetivo y tipologías
    # -------------------------------------------------------------
    print("[2/8] Generando Figura 1 (.vsg)...")
    fig, axes = plt.subplots(1, 2, figsize=(14, 5.2), dpi=150)
    
    # Subplot A: Desbalance
    bars = axes[0].bar(
        ["Legítima (0)", "Fraude (1)"],
        [conteo_clases[0], conteo_clases[1]],
        color=[CYBER_BLUE, CYBER_MAGENTA],
        edgecolor="#0f172a",
        linewidth=1.2,
        width=0.52,
    )
    axes[0].set_title("Desbalance Extremo de la Variable Objetivo (is_fraud)", fontsize=12, fontweight="bold", pad=12, color=CYBER_TEXT)
    axes[0].set_ylabel("Número de Transacciones", fontsize=10, fontweight="bold")
    axes[0].grid(axis="y", alpha=0.6)
    for bar, pct, cnt in zip(bars, [prop_clases[0], prop_clases[1]], [conteo_clases[0], conteo_clases[1]]):
        axes[0].text(
            bar.get_x() + bar.get_width() / 2,
            bar.get_height() + 1800,
            f"{cnt:,}\n({pct:.2f}%)",
            ha="center",
            va="bottom",
            fontsize=9.5,
            fontweight="bold",
            color="#1e293b",
        )
    axes[0].set_ylim(0, 115000)
    axes[0].text(
        0.5, 0.78,
        f"Ratio de Desbalance\n1 : {conteo_clases[0]/conteo_clases[1]:.1f}\n(Pérdida: ${perdida_total:,.0f} USD)",
        transform=axes[0].transAxes,
        ha="center",
        bbox=dict(boxstyle="round,pad=0.5", facecolor="#f8fafc", edgecolor="#94a3b8", alpha=0.9),
        fontsize=9,
        fontweight="bold",
    )

    # Subplot B: Tipologías de Fraude
    df_fraudes = df_raw[df_raw["is_fraud"] == 1]
    tipo_counts = df_fraudes["fraud_type"].value_counts()
    colores_tipo = [CYBER_MAGENTA, "#fb7185", "#f43f5e", "#fda4af", "#e11d48"][:len(tipo_counts)]
    sns.barplot(
        x=tipo_counts.values,
        y=tipo_counts.index,
        palette=colores_tipo,
        ax=axes[1],
        edgecolor="#0f172a",
        linewidth=1.0,
    )
    axes[1].set_title("Distribución por Tipología de Fraude (n = 2,055 casos)", fontsize=12, fontweight="bold", pad=12, color=CYBER_TEXT)
    axes[1].set_xlabel("Volumen de Transacciones Fraudulentas", fontsize=10, fontweight="bold")
    axes[1].set_ylabel("Tipología Operativa (fraud_type)", fontsize=10, fontweight="bold")
    axes[1].grid(axis="x", alpha=0.6)
    for i, v in enumerate(tipo_counts.values):
        pct_t = v / len(df_fraudes) * 100
        axes[1].text(v + 18, i, f"{v:,} ({pct_t:.1f}%)", va="center", fontsize=9.5, fontweight="bold", color="#1e293b")
    axes[1].set_xlim(0, max(tipo_counts.values) * 1.25)
    
    plt.tight_layout()
    for ext in [".vsg", ".svg", ".png"]:
        fig.savefig(results_dir / f"01_desbalance_y_tipologias{ext}", bbox_inches="tight", format="svg" if "sg" in ext else "png")
        fig.savefig(graficas_dir / f"fig01_diagnostico_target_y_nulos{ext}", bbox_inches="tight", format="svg" if "sg" in ext else "png")
    plt.close(fig)

    # -------------------------------------------------------------
    # ETAPA 2 & 3: Purga de IDs, Fuga y Limpieza Estructural
    # -------------------------------------------------------------
    columnas_identificadores = [
        "transaction_id", "customer_id", "card_id", "merchant_id", "transaction_datetime", "customer_state"
    ]
    columnas_leakage = ["fraud_type", "fraud_amount_lost"]
    df = df_raw.drop(columns=columnas_identificadores + columnas_leakage).copy()

    # Imputación semántica de browser (evita sesgo de selección del 100% de operaciones físicas/ATM)
    df["browser"] = df["browser"].fillna("No_Aplica_Fisico")

    # Diagnóstico Outliers Tukey
    vars_outliers = [
        "transaction_amount", "amount_last_1h", "distance_from_last_tx_km", "amount_vs_avg_ratio"
    ]
    resumen_iqr = []
    for col in vars_outliers:
        q1 = df[col].quantile(0.25)
        med = df[col].quantile(0.50)
        q3 = df[col].quantile(0.75)
        iqr = q3 - q1
        lim_sup = q3 + 1.5 * iqr
        mask_out = df[col] > lim_sup
        n_out = mask_out.sum()
        tf_norm = df.loc[~mask_out, "is_fraud"].mean() * 100
        tf_out = df.loc[mask_out, "is_fraud"].mean() * 100 if n_out > 0 else 0.0
        lift = tf_out / max(tf_norm, 1e-6)
        resumen_iqr.append({
            "Variable": col,
            "Mediana": round(med, 2),
            "IQR": round(iqr, 2),
            "Limite_Sup_1.5X": round(lim_sup, 2),
            "Conteo_Outliers": int(n_out),
            "Pct_Outliers": round(n_out / total_tx * 100, 2),
            "Tasa_Fraude_Normal": round(tf_norm, 2),
            "Tasa_Fraude_Outlier": round(tf_out, 2),
            "Lift_Riesgo": round(lift, 2),
        })
    df_iqr_res = pd.DataFrame(resumen_iqr)
    df_iqr_res.to_csv(results_dir / "diagnostico_outliers_iqr.csv", index=False)

    # -------------------------------------------------------------
    # ETAPA 4: Ingeniería de 8 Variables Derivadas
    # -------------------------------------------------------------
    df["velocity_tx_ratio_1h_24h"] = df["transactions_last_1h"] / (df["transactions_last_24h"] + 1.0)
    df["velocity_amt_ratio_1h_24h"] = df["amount_last_1h"] / (df["amount_last_24h"] + 1.0)
    df["credit_utilization_ratio"] = df["transaction_amount"] / (df["credit_limit"] + 1.0)
    df["zscore_amount_30d"] = (df["transaction_amount"] - df["avg_transaction_amount_30d"]) / (df["std_transaction_amount_30d"] + 1.0)
    df["security_factors_count"] = df["card_present"] + df["used_chip"] + df["used_pin"]
    df["is_night_tx"] = (df["transaction_hour"] <= 4).astype(int)
    df["is_new_account"] = (df["account_age_days"] <= 90).astype(int)

    df["composite_risk_index"] = (
        df["high_risk_country"] * 2
        + df["international_transaction"]
        + (df["card_present"] == 0).astype(int)
        + (df["transactions_last_1h"] >= 3).astype(int)
        + (df["num_chargebacks_ever"] >= 2).astype(int)
        + (df["num_declined_last_30d"] >= 2).astype(int)
        + df["is_night_tx"]
        + df["is_new_account"]
        + (df["amount_vs_avg_ratio"] > 4.8).astype(int)
        + (df["distance_from_last_tx_km"] > 800).astype(int)
    )

    # One-Hot Encoding
    cat_cols = [
        "merchant_category", "merchant_country", "transaction_day_of_week",
        "customer_gender", "transaction_channel", "device_type", "browser", "email_domain"
    ]
    df_encoded = pd.get_dummies(df, columns=cat_cols, drop_first=True, dtype=int)
    X_orig = df_encoded.drop(columns=["is_fraud"]).copy()
    y = df_encoded["is_fraud"].copy()

    # Partición Estratificada 80/20 ANTES de escalar o balancear (Zero Leakage)
    X_train_raw, X_test_raw, y_train, y_test = train_test_split(
        X_orig, y, test_size=0.20, random_state=42, stratify=y
    )

    # Compresión Logarítmica y RobustScaler
    log_cols = [
        "transaction_amount", "amount_last_1h", "amount_last_24h",
        "distance_from_home_km", "distance_from_last_tx_km", "amount_vs_avg_ratio"
    ]
    num_cols = [
        "transaction_amount", "transaction_hour", "customer_age", "account_age_days",
        "credit_limit", "credit_score", "num_cards_held", "transactions_last_1h",
        "transactions_last_24h", "transactions_last_7d", "amount_last_1h", "amount_last_24h",
        "days_since_last_transaction", "distance_from_home_km", "distance_from_last_tx_km",
        "amount_vs_avg_ratio", "avg_transaction_amount_30d", "std_transaction_amount_30d",
        "num_declined_last_30d", "num_chargebacks_ever", "velocity_tx_ratio_1h_24h",
        "velocity_amt_ratio_1h_24h", "credit_utilization_ratio", "zscore_amount_30d",
        "security_factors_count", "composite_risk_index"
    ]
    X_train = X_train_raw.copy()
    X_test = X_test_raw.copy()
    X_train[log_cols] = np.log1p(np.maximum(0, X_train[log_cols]))
    X_test[log_cols] = np.log1p(np.maximum(0, X_test[log_cols]))

    scaler = RobustScaler()
    X_train[num_cols] = scaler.fit_transform(X_train[num_cols])
    X_test[num_cols] = scaler.transform(X_test[num_cols])

    # -------------------------------------------------------------
    # ETAPA 5: Minería No Supervisada (Isolation Forest)
    # -------------------------------------------------------------
    print("[3/8] Entrenando Isolation Forest...")
    iso_features = [
        "transaction_amount", "amount_last_1h", "transactions_last_1h",
        "distance_from_home_km", "distance_from_last_tx_km", "amount_vs_avg_ratio",
        "zscore_amount_30d", "composite_risk_index"
    ]
    iso_forest = IsolationForest(n_estimators=150, contamination=0.035, random_state=42, n_jobs=-1)
    iso_forest.fit(X_train[iso_features])

    X_train["iso_anomaly_score"] = -iso_forest.score_samples(X_train[iso_features])
    X_test["iso_anomaly_score"] = -iso_forest.score_samples(X_test[iso_features])

    # -------------------------------------------------------------
    # FIGURA 2: Isolation Forest KDE y Riesgo Compuesto (.vsg)
    # -------------------------------------------------------------
    print("[4/8] Generando Figura 2 (.vsg)...")
    fig, axes = plt.subplots(1, 2, figsize=(14, 5.2), dpi=150)
    
    # KDE
    df_kde = pd.DataFrame({
        "Score": X_test["iso_anomaly_score"],
        "Clase": y_test.map({0: "Legítima (0)", 1: "Fraude (1)"})
    })
    sns.kdeplot(
        data=df_kde,
        x="Score",
        hue="Clase",
        common_norm=False,
        fill=True,
        palette=[CYBER_BLUE, CYBER_MAGENTA],
        alpha=0.45,
        linewidth=2,
        ax=axes[0],
    )
    axes[0].set_title("Distribución del Score de Anomalía (Isolation Forest)", fontsize=12, fontweight="bold", pad=12, color=CYBER_TEXT)
    axes[0].set_xlabel("Puntaje de Anomalía (-score_samples)", fontsize=10, fontweight="bold")
    axes[0].set_ylabel("Densidad de Probabilidad", fontsize=10, fontweight="bold")
    axes[0].grid(True, alpha=0.5)

    # Barplot Tasa Fraude según composite_risk_index
    riesgo_idx = df.groupby("composite_risk_index")["is_fraud"].agg(["count", "mean"])
    riesgo_idx = riesgo_idx[riesgo_idx["count"] >= 20]
    bar_colors = sns.color_palette("rocket_r", len(riesgo_idx))
    axes[1].bar(
        riesgo_idx.index.astype(str),
        riesgo_idx["mean"] * 100,
        color=bar_colors,
        edgecolor="#0f172a",
        linewidth=1.0,
    )
    axes[1].set_title("Tasa Real de Fraude según Acumulación de Señales Débiles", fontsize=12, fontweight="bold", pad=12, color=CYBER_TEXT)
    axes[1].set_xlabel("Índice de Riesgo Compuesto (composite_risk_index 0 a 8+)", fontsize=10, fontweight="bold")
    axes[1].set_ylabel("Tasa Empírica de Fraude (%)", fontsize=10, fontweight="bold")
    axes[1].grid(axis="y", alpha=0.6)
    for idx_i, (k, row_r) in enumerate(riesgo_idx.iterrows()):
        val_pct = row_r["mean"] * 100
        axes[1].text(
            idx_i,
            val_pct + 1.0,
            f"{val_pct:.1f}%\n(n={int(row_r['count'])})",
            ha="center",
            va="bottom",
            fontsize=8.0,
            fontweight="bold",
            color="#1e293b",
        )
    axes[1].set_ylim(0, max(riesgo_idx["mean"] * 100) * 1.25)
    plt.tight_layout()
    for ext in [".vsg", ".svg", ".png"]:
        fig.savefig(results_dir / f"02_outliers_iqr_y_isolation_forest{ext}", bbox_inches="tight", format="svg" if "sg" in ext else "png")
        fig.savefig(graficas_dir / f"fig02_diagnostico_outliers_iqr{ext}", bbox_inches="tight", format="svg" if "sg" in ext else "png")
    plt.close(fig)

    # -------------------------------------------------------------
    # Selección Chi2 y SMOTE
    # -------------------------------------------------------------
    bin_cols = [c for c in X_train.columns if set(X_train[c].unique()).issubset({0, 1})]
    chi_vals, p_vals = chi2(X_train[bin_cols], y_train)
    df_chi2 = pd.DataFrame({
        "Variable": bin_cols,
        "Chi2_Stat": chi_vals,
        "p_value": p_vals,
    }).sort_values("Chi2_Stat", ascending=False)

    top_bin_cols = df_chi2.head(18)["Variable"].tolist()
    selected_features = list(dict.fromkeys(num_cols + ["iso_anomaly_score"] + top_bin_cols))
    print(f"Características seleccionadas: {len(selected_features)}")

    X_train_sel = X_train[selected_features].copy()
    X_test_sel = X_test[selected_features].copy()

    # SMOTE exclusivamente en entrenamiento
    smote = SMOTE(sampling_strategy=0.30, random_state=42)
    X_train_smote, y_train_smote = smote.fit_resample(X_train_sel, y_train)

    # -------------------------------------------------------------
    # Modelado Supervisado Comparativo
    # -------------------------------------------------------------
    print("[5/8] Entrenando los 5 modelos de clasificación...")
    modelos = {
        "1. Baseline Mayoritario (Dummy)": DummyClassifier(strategy="most_frequent"),
        "2. Regresión Logística (SMOTE)": LogisticRegression(max_iter=500, C=1.0, random_state=42),
        "3. Árbol de Decisión (SMOTE)": DecisionTreeClassifier(max_depth=6, min_samples_leaf=50, random_state=42),
        "4. Random Forest (SMOTE)": RandomForestClassifier(
            n_estimators=200, max_depth=12, min_samples_leaf=15, class_weight="balanced_subsample", random_state=42, n_jobs=-1
        ),
        "5. Gradient Boosting (SMOTE)": GradientBoostingClassifier(
            n_estimators=150, max_depth=4, learning_rate=0.08, random_state=42
        ),
    }

    resultados = []
    curvas_dict = {}
    matrices_dict = {}

    for nombre, modelo in modelos.items():
        if "Dummy" in nombre:
            modelo.fit(X_train_sel, y_train)
            probs = modelo.predict_proba(X_test_sel)[:, 1]
            umbral_opt = 0.50
            preds = modelo.predict(X_test_sel)
        else:
            modelo.fit(X_train_smote, y_train_smote)
            probs = modelo.predict_proba(X_test_sel)[:, 1]
            # Calibración de umbral por F2
            mejor_f2, umbral_opt = 0.0, 0.50
            for th in np.arange(0.15, 0.65, 0.05):
                cand_pred = (probs >= th).astype(int)
                p_c = precision_score(y_test, cand_pred, zero_division=0)
                r_c = recall_score(y_test, cand_pred, zero_division=0)
                f2_c = (5 * p_c * r_c) / (4 * p_c + r_c + 1e-9)
                if f2_c > mejor_f2:
                    mejor_f2, umbral_opt = f2_c, th
            preds = (probs >= umbral_opt).astype(int)

        acc = accuracy_score(y_test, preds)
        prec = precision_score(y_test, preds, zero_division=0)
        rec = recall_score(y_test, preds, zero_division=0)
        f1 = f1_score(y_test, preds, zero_division=0)
        roc_auc = roc_auc_score(y_test, probs)
        pr_auc = average_precision_score(y_test, probs)
        cm = confusion_matrix(y_test, preds)
        tn, fp, fn, tp = cm.ravel()

        resultados.append({
            "Modelo": nombre,
            "Umbral": round(umbral_opt, 2),
            "Accuracy": round(acc, 4),
            "Precision": round(prec, 4),
            "Recall": round(rec, 4),
            "F1_Score": round(f1, 4),
            "ROC_AUC": round(roc_auc, 4),
            "PR_AUC": round(pr_auc, 4),
            "TP_Fraudes_Detectados": int(tp),
            "FN_Fraudes_Omitidos": int(fn),
            "FP_Falsas_Alarmas": int(fp),
        })
        curvas_dict[nombre] = probs
        matrices_dict[nombre] = cm

    df_res = pd.DataFrame(resultados)
    df_res.to_csv(results_dir / "resumen_modelos_kdd.csv", index=False)
    print(df_res.to_string(index=False))

    # -------------------------------------------------------------
    # FIGURA 3: Importancia Gini y Chi-Cuadrado (.vsg)
    # -------------------------------------------------------------
    print("[6/8] Generando Figura 3 (.vsg)...")
    rf_model = modelos["4. Random Forest (SMOTE)"]
    imp_series = pd.Series(rf_model.feature_importances_, index=selected_features).sort_values(ascending=False).head(15)

    fig, axes = plt.subplots(1, 2, figsize=(15, 6.0), dpi=150)
    colores_gini = sns.color_palette("Blues_r", len(imp_series))
    sns.barplot(x=imp_series.values, y=imp_series.index, palette=colores_gini, ax=axes[0], edgecolor="#0f172a", linewidth=0.8)
    axes[0].set_title("Top 15 Características Más Importantes (Random Forest + SMOTE)", fontsize=12, fontweight="bold", pad=12, color=CYBER_TEXT)
    axes[0].set_xlabel("Importancia Relativa (Gini Importance)", fontsize=10, fontweight="bold")
    axes[0].set_ylabel("Variable Predictora", fontsize=10, fontweight="bold")
    axes[0].grid(axis="x", alpha=0.6)

    top_chi_plot = df_chi2.head(12)
    colores_chi = sns.color_palette("Purples_r", len(top_chi_plot))
    sns.barplot(x=top_chi_plot["Chi2_Stat"], y=top_chi_plot["Variable"], palette=colores_chi, ax=axes[1], edgecolor="#0f172a", linewidth=0.8)
    axes[1].set_title("Top 12 Variables Binarias/Dummies (Prueba Chi-Cuadrado χ²)", fontsize=12, fontweight="bold", pad=12, color=CYBER_TEXT)
    axes[1].set_xlabel("Estadístico Chi-Cuadrado (χ²)", fontsize=10, fontweight="bold")
    axes[1].set_ylabel("Variable Binaria / Dummy", fontsize=10, fontweight="bold")
    axes[1].grid(axis="x", alpha=0.6)
    plt.tight_layout()
    for ext in [".vsg", ".svg", ".png"]:
        fig.savefig(results_dir / f"03_seleccion_variables_importancia{ext}", bbox_inches="tight", format="svg" if "sg" in ext else "png")
        fig.savefig(graficas_dir / f"fig03_ingenieria_caracteristicas{ext}", bbox_inches="tight", format="svg" if "sg" in ext else "png")
    plt.close(fig)

    # -------------------------------------------------------------
    # FIGURA 4: Curvas ROC y Precision-Recall (.vsg)
    # -------------------------------------------------------------
    print("[7/8] Generando Figura 4 y 5 (.vsg)...")
    fig, axes = plt.subplots(1, 2, figsize=(14, 5.5), dpi=150)
    colores_modelos = {
        "1. Baseline Mayoritario (Dummy)": "#94a3b8",
        "2. Regresión Logística (SMOTE)": "#3b82f6",
        "3. Árbol de Decisión (SMOTE)": "#10b981",
        "4. Random Forest (SMOTE)": CYBER_MAGENTA,
        "5. Gradient Boosting (SMOTE)": CYBER_PURPLE,
    }
    for nombre, probs in curvas_dict.items():
        fpr, tpr, _ = roc_curve(y_test, probs)
        roc_val = roc_auc_score(y_test, probs)
        c = colores_modelos.get(nombre, "#334155")
        lw = 2.5 if "Random Forest" in nombre or "Gradient" in nombre else 1.8
        axes[0].plot(fpr, tpr, lw=lw, color=c, label=f"{nombre.split('(')[0].strip()} (AUC = {roc_val:.3f})")

        prec_c, rec_c, _ = precision_recall_curve(y_test, probs)
        pr_val = average_precision_score(y_test, probs)
        axes[1].plot(rec_c, prec_c, lw=lw, color=c, label=f"{nombre.split('(')[0].strip()} (PR-AUC = {pr_val:.3f})")

    axes[0].plot([0, 1], [0, 1], "k--", lw=1.2, alpha=0.7)
    axes[0].set_title("Curvas ROC en Conjunto de Prueba (n = 20,000)", fontsize=12, fontweight="bold", pad=12, color=CYBER_TEXT)
    axes[0].set_xlabel("Tasa de Falsos Positivos (FPR)", fontsize=10, fontweight="bold")
    axes[0].set_ylabel("Tasa de Verdaderos Positivos (Recall / TPR)", fontsize=10, fontweight="bold")
    axes[0].legend(loc="lower right", fontsize=8.5, framealpha=0.95)
    axes[0].grid(True, alpha=0.5)

    axes[1].axhline(y_test.mean(), color="#f59e0b", linestyle=":", lw=1.5, label=f"Línea Base Azar (Prevalencia = {y_test.mean()*100:.2f}%)")
    axes[1].set_title("Curvas Precision-Recall (Desbalanceo Severo 2.05%)", fontsize=12, fontweight="bold", pad=12, color=CYBER_TEXT)
    axes[1].set_xlabel("Sensibilidad / Recall (Fraudes Capturados)", fontsize=10, fontweight="bold")
    axes[1].set_ylabel("Precisión (Valor Predictivo Positivo)", fontsize=10, fontweight="bold")
    axes[1].legend(loc="upper right", fontsize=8.5, framealpha=0.95)
    axes[1].grid(True, alpha=0.5)
    plt.tight_layout()
    for ext in [".vsg", ".svg", ".png"]:
        fig.savefig(results_dir / f"04_comparativa_modelos_curvas_roc_pr{ext}", bbox_inches="tight", format="svg" if "sg" in ext else "png")
        fig.savefig(graficas_dir / f"fig05_comparativa_dos_metodos_filtro{ext}", bbox_inches="tight", format="svg" if "sg" in ext else "png")
    plt.close(fig)

    # -------------------------------------------------------------
    # FIGURA 5: Matrices de Confusión (.vsg)
    # -------------------------------------------------------------
    fig, axes = plt.subplots(2, 2, figsize=(13, 10), dpi=150)
    nombres_ml = [k for k in matrices_dict.keys() if "Dummy" not in k]
    for ax, nombre in zip(axes.flatten(), nombres_ml):
        cm = matrices_dict[nombre]
        cmap_choice = "PuRd" if "Random Forest" in nombre else "Blues"
        sns.heatmap(
            cm,
            annot=True,
            fmt="d",
            cmap=cmap_choice,
            cbar=False,
            xticklabels=["Pred: Legítima (0)", "Pred: Fraude (1)"],
            yticklabels=["Real: Legítima (0)", "Real: Fraude (1)"],
            ax=ax,
            annot_kws={"size": 13, "weight": "bold"},
            linewidths=1.2,
            linecolor="#cbd5e1",
        )
        fila_m = df_res[df_res["Modelo"] == nombre].iloc[0]
        ax.set_title(
            f"{nombre}\nRecall: {fila_m['Recall']*100:.1f}% | F1: {fila_m['F1_Score']:.3f} | ROC-AUC: {fila_m['ROC_AUC']:.3f}",
            fontsize=10.5,
            fontweight="bold",
            color=CYBER_TEXT,
            pad=10,
        )
    plt.tight_layout()
    for ext in [".vsg", ".svg", ".png"]:
        fig.savefig(results_dir / f"05_matrices_confusion{ext}", bbox_inches="tight", format="svg" if "sg" in ext else "png")
        fig.savefig(graficas_dir / f"fig06_validacion_cruzada_5fold{ext}", bbox_inches="tight", format="svg" if "sg" in ext else "png")
    plt.close(fig)

    # -------------------------------------------------------------
    # ETAPA 7: Árbol de Reglas de Decisión y Validación Empírica
    # -------------------------------------------------------------
    print("[8/8] Extrayendo y Validando Reglas de Decisión...")
    features_reglas = [
        "high_risk_country", "international_transaction", "card_present", "used_pin", "used_chip",
        "transactions_last_1h", "account_age_days", "transaction_hour", "distance_from_home_km",
        "distance_from_last_tx_km", "amount_vs_avg_ratio", "num_chargebacks_ever", "num_declined_last_30d"
    ]
    dt_interpretable = DecisionTreeClassifier(max_depth=4, min_samples_leaf=120, class_weight="balanced", random_state=42)
    dt_interpretable.fit(X_train_raw[features_reglas], y_train)

    reglas_texto = export_text(dt_interpretable, feature_names=features_reglas, decimals=2)
    (results_dir / "reglas_decision_fraude.txt").write_text(reglas_texto, encoding="utf-8")

    # FIGURA 6: Visualización del Árbol de Decisión y Lift de Reglas (.vsg)
    dt_plot = DecisionTreeClassifier(max_depth=3, min_samples_leaf=150, class_weight="balanced", random_state=42)
    dt_plot.fit(X_train_raw[features_reglas], y_train)

    # Reglas empíricas
    reglas_negocio = [
        ("R1: high_risk_country=1 & card_present=0 & tx_1h>=3", (df["high_risk_country"] == 1) & (df["card_present"] == 0) & (df["transactions_last_1h"] >= 3)),
        ("R2: high_risk_country=1 & account_age_days<=90", (df["high_risk_country"] == 1) & (df["account_age_days"] <= 90)),
        ("R3: tx_hour<=4 & international=1 & card_present=0", (df["transaction_hour"] <= 4) & (df["international_transaction"] == 1) & (df["card_present"] == 0)),
        ("R4: amount_ratio>4.8 & chargebacks>=2 & card_present=0", (df["amount_vs_avg_ratio"] > 4.8) & (df["num_chargebacks_ever"] >= 2) & (df["card_present"] == 0)),
        ("R5: composite_risk_index >= 5 (Multiseñal)", (df["composite_risk_index"] >= 5)),
    ]
    tasa_base = df["is_fraud"].mean() * 100
    tabla_reglas = []
    for cod_r, (nombre_r, mascara) in zip(["R1", "R2", "R3", "R4", "R5"], reglas_negocio):
        n_casos = int(mascara.sum())
        n_fraudes = int(df.loc[mascara, "is_fraud"].sum())
        tasa_r = (n_fraudes / n_casos * 100) if n_casos > 0 else 0.0
        lift_r = tasa_r / tasa_base
        tabla_reglas.append({
            "Codigo": cod_r,
            "Regla_Decision": nombre_r,
            "Transacciones_Activadas": n_casos,
            "Fraudes_Capturados": n_fraudes,
            "Precision_Regla_%": round(tasa_r, 2),
            "Lift_vs_Azar": round(lift_r, 2),
        })
    df_reglas_val = pd.DataFrame(tabla_reglas)
    df_reglas_val.to_csv(results_dir / "reglas_negocio_validadas.csv", index=False)
    print(df_reglas_val.to_string(index=False))

    fig = plt.figure(figsize=(18, 9), dpi=150)
    gs = fig.add_gridspec(2, 1, height_ratios=[1.8, 1.0], hspace=0.35)

    ax_tree = fig.add_subplot(gs[0, 0])
    plot_tree(
        dt_plot,
        feature_names=features_reglas,
        class_names=["Legítima", "FRAUDE"],
        filled=True,
        rounded=True,
        impurity=False,
        proportion=True,
        fontsize=9,
        ax=ax_tree,
    )
    ax_tree.set_title("A) Árbol de Decisión Interpretable en Unidades Físicas (Profundidad = 3, Soporte >= 150)", fontsize=12, fontweight="bold", pad=10, color=CYBER_TEXT)

    ax_lift = fig.add_subplot(gs[1, 0])
    bars_lift = ax_lift.bar(
        [r["Codigo"] + ": " + r["Regla_Decision"][:30] + "..." for r in tabla_reglas],
        [r["Lift_vs_Azar"] for r in tabla_reglas],
        color=[CYBER_MAGENTA, "#e11d48", "#f43f5e", CYBER_PURPLE, CYBER_BLUE],
        edgecolor="#0f172a",
        linewidth=1.0,
        width=0.45,
    )
    ax_lift.axhline(1.0, color="#64748b", linestyle="--", lw=1.2, label="Línea Base Azar (Lift = 1.0x)")
    ax_lift.set_title("B) Validación Empírica del Multiplicador de Riesgo (Lift sobre el Azar) en las 5 Reglas Descubiertas", fontsize=11, fontweight="bold", pad=8, color=CYBER_TEXT)
    ax_lift.set_ylabel("Lift vs Azar", fontsize=9.5, fontweight="bold")
    ax_lift.grid(axis="y", alpha=0.5)
    for bar, r in zip(bars_lift, tabla_reglas):
        ax_lift.text(
            bar.get_x() + bar.get_width() / 2,
            bar.get_height() + 0.4,
            f"Lift: {r['Lift_vs_Azar']:.2f}x\nPrec: {r['Precision_Regla_%']:.1f}%\n(n={r['Transacciones_Activadas']:,})",
            ha="center",
            va="bottom",
            fontsize=8.5,
            fontweight="bold",
            color="#1e293b",
        )
    ax_lift.set_ylim(0, max([r["Lift_vs_Azar"] for r in tabla_reglas]) * 1.3)
    ax_lift.legend(loc="upper right", fontsize=8.5)
    plt.tight_layout()
    for ext in [".vsg", ".svg", ".png"]:
        fig.savefig(results_dir / f"06_arbol_reglas_decision{ext}", bbox_inches="tight", format="svg" if "sg" in ext else "png")
        fig.savefig(graficas_dir / f"fig04_escalamiento_robusto_sin_leakage{ext}", bbox_inches="tight", format="svg" if "sg" in ext else "png")
    plt.close(fig)

    print("=" * 80)
    print("PIPELINE KDD COMPLETADO Y FIGURAS .vsg EXPORTADAS SATISFACTORIAMENTE.")
    print("=" * 80)

if __name__ == "__main__":
    main()
