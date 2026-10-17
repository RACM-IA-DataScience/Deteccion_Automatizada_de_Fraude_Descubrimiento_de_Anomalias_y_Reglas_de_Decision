"""
Módulo 4 KDD (Etapas 6 y 7):
- Evaluación Cuantitativa Multi-Métrica (ROC-AUC, PR-AUC, Recall, F1, Matrices de Confusión)
- Interpretación de Importancia de Variables (Random Forest Gini Importance)
- Extracción de Reglas de Decisión en Unidades Originales (Árbol Interpretable)
- Validación Empírica de Reglas de Negocio Accionables (Lift y Precisión)
"""

from pathlib import Path
from typing import Dict, Any, Tuple
import pandas as pd
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import seaborn as sns

from sklearn.tree import DecisionTreeClassifier, export_text, plot_tree
from sklearn.metrics import roc_curve, precision_recall_curve, roc_auc_score, average_precision_score


FEATURES_REGLAS = [
    "high_risk_country",
    "international_transaction",
    "card_present",
    "used_pin",
    "used_chip",
    "transactions_last_1h",
    "account_age_days",
    "transaction_hour",
    "distance_from_home_km",
    "distance_from_last_tx_km",
    "amount_vs_avg_ratio",
    "num_chargebacks_ever",
    "num_declined_last_30d",
]


def evaluar_e_interpretar_conocimiento(
    datos_etapa4: Dict[str, Any],
    datos_etapa5: Dict[str, Any],
    out_dir: Path,
) -> Tuple[pd.DataFrame, pd.DataFrame]:
    """
    Ejecuta las Etapas 6 y 7 del proceso KDD:
    Genera reportes visuales de evaluación, extrae el árbol de reglas y valida las reglas de negocio.
    """
    print("\n" + "=" * 88)
    print("MÓDULO 4 (ETAPAS 6-7 KDD): EVALUACIÓN COMPARATIVA Y REGLAS DE DECISIÓN")
    print("=" * 88)

    df_feat = datos_etapa4["df_feat"]
    X_train_raw = datos_etapa4["X_train_raw"]
    y_train = datos_etapa4["y_train"]
    y_test = datos_etapa4["y_test"]
    df_chi2 = datos_etapa4["df_chi2"]

    modelos = datos_etapa5["modelos"]
    selected_features = datos_etapa5["selected_features"]
    df_res = datos_etapa5["df_res"]
    curvas_dict = datos_etapa5["curvas_dict"]
    matrices_dict = datos_etapa5["matrices_dict"]

    print("[Etapa 6] Tabla Comparativa de Modelos en X_test (20,000 transacciones):")
    print(df_res.to_string(index=False))
    df_res.to_csv(out_dir / "resumen_modelos_kdd.csv", index=False)

    # Gráfica 3: Importancia de características (Random Forest) + Chi-Cuadrado
    rf_model = modelos["4. Random Forest (SMOTE)"]
    imp_series = pd.Series(rf_model.feature_importances_, index=selected_features).sort_values(ascending=False).head(15)

    fig, axes = plt.subplots(1, 2, figsize=(15, 5.8))
    sns.barplot(x=imp_series.values, y=imp_series.index, palette="Blues_r", ax=axes[0], edgecolor="black")
    axes[0].set_title("Top 15 Características Más Importantes (Random Forest + SMOTE)", fontweight="bold")
    axes[0].set_xlabel("Importancia Relativa (Gini Importance)")

    top_chi_plot = df_chi2.head(12)
    sns.barplot(x=top_chi_plot["Chi2_Stat"], y=top_chi_plot["Variable"], palette="Purples_r", ax=axes[1], edgecolor="black")
    axes[1].set_title("Top 12 Variables Binarias/Categóricas (Estadístico Chi-Cuadrado χ²)", fontweight="bold")
    axes[1].set_xlabel("Estadístico χ²")
    plt.tight_layout()
    fig.savefig(out_dir / "03_seleccion_variables_importancia.png", bbox_inches="tight")
    plt.close(fig)

    # Gráfica 4: Curvas ROC y Precision-Recall
    fig, axes = plt.subplots(1, 2, figsize=(14, 5.5))
    for nombre, probs in curvas_dict.items():
        fpr, tpr, _ = roc_curve(y_test, probs)
        roc_val = roc_auc_score(y_test, probs)
        axes[0].plot(fpr, tpr, lw=2, label=f"{nombre} (AUC = {roc_val:.3f})")

        prec_c, rec_c, _ = precision_recall_curve(y_test, probs)
        pr_val = average_precision_score(y_test, probs)
        axes[1].plot(rec_c, prec_c, lw=2, label=f"{nombre} (PR-AUC = {pr_val:.3f})")

    axes[0].plot([0, 1], [0, 1], "k--", lw=1)
    axes[0].set_title("Curvas ROC en Conjunto de Prueba (n = 20,000)", fontweight="bold")
    axes[0].set_xlabel("Tasa de Falsos Positivos (FPR)")
    axes[0].set_ylabel("Tasa de Verdaderos Positivos (Recall / TPR)")
    axes[0].legend(loc="lower right", fontsize=8.5)

    axes[1].set_title("Curvas Precision-Recall (Desbalanceo 2.05% Fraude)", fontweight="bold")
    axes[1].set_xlabel("Sensibilidad / Recall (Fraudes Detectados)")
    axes[1].set_ylabel("Precisión (Valor Predictivo Positivo)")
    axes[1].legend(loc="upper right", fontsize=8.5)
    plt.tight_layout()
    fig.savefig(out_dir / "04_comparativa_modelos_curvas_roc_pr.png", bbox_inches="tight")
    plt.close(fig)

    # Gráfica 5: Matrices de Confusión
    fig, axes = plt.subplots(2, 2, figsize=(13, 10))
    nombres_ml = [k for k in matrices_dict.keys() if "Dummy" not in k]
    for ax, nombre in zip(axes.flatten(), nombres_ml):
        cm = matrices_dict[nombre]
        sns.heatmap(
            cm,
            annot=True,
            fmt="d",
            cmap="YlGnBu",
            cbar=False,
            xticklabels=["Pred: Legítima (0)", "Pred: Fraude (1)"],
            yticklabels=["Real: Legítima (0)", "Real: Fraude (1)"],
            ax=ax,
            annot_kws={"size": 12, "weight": "bold"},
        )
        fila_m = df_res[df_res["Modelo"] == nombre].iloc[0]
        ax.set_title(
            f"{nombre}\nRecall: {fila_m['Recall']*100:.1f}% | F1: {fila_m['F1_Score']:.3f} | ROC-AUC: {fila_m['ROC_AUC']:.3f}",
            fontweight="bold",
        )
    plt.tight_layout()
    fig.savefig(out_dir / "05_matrices_confusion.png", bbox_inches="tight")
    plt.close(fig)

    # Etapa 7: Extracción de reglas de decisión en unidades originales
    dt_interpretable = DecisionTreeClassifier(
        max_depth=4, min_samples_leaf=120, class_weight="balanced", random_state=42
    )
    dt_interpretable.fit(X_train_raw[FEATURES_REGLAS], y_train)
    reglas_texto = export_text(dt_interpretable, feature_names=FEATURES_REGLAS, decimals=2)
    (out_dir / "reglas_decision_fraude.txt").write_text(reglas_texto, encoding="utf-8")

    dt_plot = DecisionTreeClassifier(
        max_depth=3, min_samples_leaf=150, class_weight="balanced", random_state=42
    )
    dt_plot.fit(X_train_raw[FEATURES_REGLAS], y_train)
    fig, ax = plt.subplots(figsize=(20, 9))
    plot_tree(
        dt_plot,
        feature_names=FEATURES_REGLAS,
        class_names=["Legítima", "FRAUDE"],
        filled=True,
        rounded=True,
        impurity=False,
        proportion=True,
        fontsize=10,
        ax=ax,
    )
    ax.set_title("Árbol de Decisión Interpretable para Detección Automatizada de Fraude (Profundidad = 3)", fontsize=14, fontweight="bold")
    plt.tight_layout()
    fig.savefig(out_dir / "06_arbol_reglas_decision.png", bbox_inches="tight")
    plt.close(fig)

    # Validación cuantitativa de las 5 reglas accionables
    reglas_negocio = [
        (
            "Regla R1 (Riesgo Crítico Internacional + Velocidad)",
            (df_feat["high_risk_country"] == 1) & (df_feat["card_present"] == 0) & (df_feat["transactions_last_1h"] >= 3),
        ),
        (
            "Regla R2 (País de Alto Riesgo + Cuenta Nueva <= 90 días)",
            (df_feat["high_risk_country"] == 1) & (df_feat["account_age_days"] <= 90),
        ),
        (
            "Regla R3 (Madrugada 00-04h + Internacional + Sin Tarjeta Presente)",
            (df_feat["transaction_hour"] <= 4) & (df_feat["international_transaction"] == 1) & (df_feat["card_present"] == 0),
        ),
        (
            "Regla R4 (Monto Desviado >4.8x Promedio + Historial Contracargos >=2)",
            (df_feat["amount_vs_avg_ratio"] > 4.8) & (df_feat["num_chargebacks_ever"] >= 2) & (df_feat["card_present"] == 0),
        ),
        (
            "Regla R5 (Acumulación Multiseñal: composite_risk_index >= 5)",
            (df_feat["composite_risk_index"] >= 5),
        ),
    ]

    tasa_base = df_feat["is_fraud"].mean() * 100
    tabla_reglas = []
    for nombre_r, mascara in reglas_negocio:
        n_casos = int(mascara.sum())
        n_fraudes = int(df_feat.loc[mascara, "is_fraud"].sum())
        tasa_r = (n_fraudes / n_casos * 100) if n_casos > 0 else 0.0
        tabla_reglas.append({
            "Regla_Decision": nombre_r,
            "Transacciones_Activadas": n_casos,
            "Fraudes_Capturados": n_fraudes,
            "Precision_Regla_%": round(tasa_r, 2),
            "Lift_vs_Azar": round(tasa_r / tasa_base, 2),
        })
    df_reglas_val = pd.DataFrame(tabla_reglas)
    df_reglas_val.to_csv(out_dir / "reglas_negocio_validadas.csv", index=False)

    print("\n[Etapa 7] Reglas de Decisión Accionables Validadas:")
    print(df_reglas_val.to_string(index=False))
    return df_res, df_reglas_val
