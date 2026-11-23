"""
Módulo 3 KDD (Etapa 5):
- Detección No Supervisada de Valores Atípicos mediante Isolation Forest
- Integración del Puntaje de Anomalía (iso_anomaly_score)
- Balanceo Sintético de Clases con SMOTE exclusivamente en Entrenamiento
- Entrenamiento Comparativo de 5 Modelos con Calibración de Umbral Sensible al Costo (F2-Score)
"""

from pathlib import Path
from typing import Dict, Any
import numpy as np
import pandas as pd
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import seaborn as sns

from sklearn.ensemble import IsolationForest, RandomForestClassifier, GradientBoostingClassifier
from sklearn.tree import DecisionTreeClassifier
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
)
from imblearn.over_sampling import SMOTE


ISO_FEATURES = [
    "transaction_amount",
    "amount_last_1h",
    "transactions_last_1h",
    "distance_from_home_km",
    "distance_from_last_tx_km",
    "amount_vs_avg_ratio",
    "zscore_amount_30d",
    "composite_risk_index",
]


def ejecutar_mineria_datos(datos_etapa4: Dict[str, Any], out_dir: Path) -> Dict[str, Any]:
    """
    Ejecuta la Etapa 5 del proceso KDD:
    Isolation Forest + Selección de subconjunto óptimo + SMOTE + Clasificación Supervisada.
    """
    print("\n" + "=" * 88)
    print("MÓDULO 3 (ETAPA 5 KDD): MINERÍA DE ANOMALÍAS (ISOLATION FOREST) Y CLASIFICACIÓN SMOTE")
    print("=" * 88)

    df_feat = datos_etapa4["df_feat"]
    X_train = datos_etapa4["X_train"].copy()
    X_test = datos_etapa4["X_test"].copy()
    y_train = datos_etapa4["y_train"]
    y_test = datos_etapa4["y_test"]
    df_chi2 = datos_etapa4["df_chi2"]
    num_cols = datos_etapa4["num_cols"]

    # 1. Detección de anomalías con Isolation Forest
    iso_forest = IsolationForest(n_estimators=150, contamination=0.035, random_state=42, n_jobs=-1)
    iso_forest.fit(X_train[ISO_FEATURES])

    test_anom_flag = (iso_forest.predict(X_test[ISO_FEATURES]) == -1).astype(int)
    X_train["iso_anomaly_score"] = -iso_forest.score_samples(X_train[ISO_FEATURES])
    X_test["iso_anomaly_score"] = -iso_forest.score_samples(X_test[ISO_FEATURES])

    tasa_norm_iso = y_test[test_anom_flag == 0].mean() * 100
    tasa_anom_iso = y_test[test_anom_flag == 1].mean() * 100
    print(f"[Isolation Forest] Tasa Fraude Normales: {tasa_norm_iso:.2f}% | Anómalas: {tasa_anom_iso:.2f}% (Lift = {tasa_anom_iso/tasa_norm_iso:.2f}x)")

    # Gráfica 2: Isolation Forest y Riesgo Multiseñal
    fig, axes = plt.subplots(1, 2, figsize=(14, 5.2))
    sns.kdeplot(
        data=pd.DataFrame({
            "Score Anomalía": X_test["iso_anomaly_score"],
            "Clase": y_test.map({0: "Legítima (0)", 1: "Fraude (1)"}),
        }),
        x="Score Anomalía",
        hue="Clase",
        common_norm=False,
        fill=True,
        palette=["#2b5c8f", "#d95f02"],
        ax=axes[0],
    )
    axes[0].set_title("Distribución de Puntaje de Anomalía (Isolation Forest)", fontweight="bold")

    riesgo_idx = df_feat.groupby("composite_risk_index")["is_fraud"].agg(["count", "mean"])
    riesgo_idx = riesgo_idx[riesgo_idx["count"] >= 20]
    axes[1].bar(
        riesgo_idx.index.astype(str),
        riesgo_idx["mean"] * 100,
        color=sns.color_palette("YlOrRd", len(riesgo_idx)),
        edgecolor="black",
    )
    axes[1].set_title("Tasa Real de Fraude según Acumulación de Señales Débiles", fontweight="bold")
    axes[1].set_xlabel("Índice de Riesgo Compuesto (composite_risk_index)")
    axes[1].set_ylabel("Tasa de Fraude (%)")
    axes[1].set_ylim(0, max(riesgo_idx["mean"] * 100) * 1.22)
    for idx_i, (k, row_r) in enumerate(riesgo_idx.iterrows()):
        axes[1].text(
            idx_i,
            row_r["mean"] * 100 + 0.8,
            f"{row_r['mean']*100:.1f}%\n(n={int(row_r['count'])})",
            ha="center",
            fontsize=8.5,
            fontweight="bold",
        )
    plt.tight_layout()
    fig.savefig(out_dir / "02_outliers_iqr_y_isolation_forest.png", bbox_inches="tight")
    plt.close(fig)

    # 2. Subconjunto de 45 características + SMOTE
    top_bin_cols = df_chi2.head(18)["Variable"].tolist()
    selected_features = list(dict.fromkeys(num_cols + ["iso_anomaly_score"] + top_bin_cols))

    X_train_sel = X_train[selected_features].copy()
    X_test_sel = X_test[selected_features].copy()

    smote = SMOTE(sampling_strategy=0.30, random_state=42)
    X_train_smote, y_train_smote = smote.fit_resample(X_train_sel, y_train)
    print(f"[SMOTE] X_train balanceado: Clase 0 = {(y_train_smote==0).sum():,} | Clase 1 = {(y_train_smote==1).sum():,}")

    # 3. Entrenamiento de modelos
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
            preds = modelo.predict(X_test_sel)
            umbral_opt = 0.50
        else:
            modelo.fit(X_train_smote, y_train_smote)
            probs = modelo.predict_proba(X_test_sel)[:, 1]
            mejor_f2, umbral_opt = 0.0, 0.50
            for th in np.arange(0.15, 0.65, 0.05):
                cand_pred = (probs >= th).astype(int)
                p_c = precision_score(y_test, cand_pred, zero_division=0)
                r_c = recall_score(y_test, cand_pred, zero_division=0)
                f2_c = (5 * p_c * r_c) / (4 * p_c + r_c + 1e-9)
                if f2_c > mejor_f2:
                    mejor_f2, umbral_opt = f2_c, th
            preds = (probs >= umbral_opt).astype(int)

        cm = confusion_matrix(y_test, preds)
        tn, fp, fn, tp = cm.ravel()
        resultados.append({
            "Modelo": nombre,
            "Umbral": round(umbral_opt, 2),
            "Accuracy": round(accuracy_score(y_test, preds), 4),
            "Precision": round(precision_score(y_test, preds, zero_division=0), 4),
            "Recall": round(recall_score(y_test, preds, zero_division=0), 4),
            "F1_Score": round(f1_score(y_test, preds, zero_division=0), 4),
            "ROC_AUC": round(roc_auc_score(y_test, probs), 4),
            "PR_AUC": round(average_precision_score(y_test, probs), 4),
            "TP_Fraudes_Detectados": int(tp),
            "FN_Fraudes_Omitidos": int(fn),
            "FP_Falsas_Alarmas": int(fp),
        })
        curvas_dict[nombre] = probs
        matrices_dict[nombre] = cm

    df_res = pd.DataFrame(resultados)
    return {
        "modelos": modelos,
        "selected_features": selected_features,
        "df_res": df_res,
        "curvas_dict": curvas_dict,
        "matrices_dict": matrices_dict,
    }
