"""
Módulo 2 KDD (Etapa 4):
- Ingeniería de Características de Dominio Bancario (Amplificación de Señales Débiles)
- Codificación One-Hot de Variables Categóricas Nominales
- Partición Estratificada 80/20 (Prevención Estricta de Data Leakage)
- Transformación Híbrida: Compresión Logarítmica (np.log1p) + RobustScaler
- Selección Estadística de Variables mediante Prueba Chi-Cuadrado (χ²)
"""

from typing import Dict, Any, List
import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import RobustScaler
from sklearn.feature_selection import chi2


LOG_COLS = [
    "transaction_amount",
    "amount_last_1h",
    "amount_last_24h",
    "distance_from_home_km",
    "distance_from_last_tx_km",
    "amount_vs_avg_ratio",
]

NUM_COLS = [
    "transaction_amount",
    "transaction_hour",
    "customer_age",
    "account_age_days",
    "credit_limit",
    "credit_score",
    "num_cards_held",
    "transactions_last_1h",
    "transactions_last_24h",
    "transactions_last_7d",
    "amount_last_1h",
    "amount_last_24h",
    "days_since_last_transaction",
    "distance_from_home_km",
    "distance_from_last_tx_km",
    "amount_vs_avg_ratio",
    "avg_transaction_amount_30d",
    "std_transaction_amount_30d",
    "num_declined_last_30d",
    "num_chargebacks_ever",
    "velocity_tx_ratio_1h_24h",
    "velocity_amt_ratio_1h_24h",
    "credit_utilization_ratio",
    "zscore_amount_30d",
    "security_factors_count",
    "composite_risk_index",
]

CAT_COLS = [
    "merchant_category",
    "merchant_country",
    "transaction_day_of_week",
    "customer_gender",
    "transaction_channel",
    "device_type",
    "browser",
    "email_domain",
]


def construir_variables_derivadas(df_limpio: pd.DataFrame) -> pd.DataFrame:
    """Crea las 8 variables derivadas de dominio bancario sin fuga de información."""
    df = df_limpio.copy()
    df["velocity_tx_ratio_1h_24h"] = df["transactions_last_1h"] / (df["transactions_last_24h"] + 1.0)
    df["velocity_amt_ratio_1h_24h"] = df["amount_last_1h"] / (df["amount_last_24h"] + 1.0)
    df["credit_utilization_ratio"] = df["transaction_amount"] / (df["credit_limit"] + 1.0)
    df["zscore_amount_30d"] = (
        df["transaction_amount"] - df["avg_transaction_amount_30d"]
    ) / (df["std_transaction_amount_30d"] + 1.0)
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
    return df


def transformar_y_particionar(df_limpio: pd.DataFrame) -> Dict[str, Any]:
    """
    Ejecuta la Etapa 4 del proceso KDD:
    Ingeniería de características, One-Hot Encoding, Split Estratificado 80/20,
    escalamiento híbrido (log1p + RobustScaler) y ranking Chi-Cuadrado.
    """
    print("\n" + "=" * 88)
    print("MÓDULO 2 (ETAPA 4 KDD): TRANSFORMACIÓN, FEATURE ENGINEERING Y SELECCIÓN")
    print("=" * 88)

    df_feat = construir_variables_derivadas(df_limpio)
    df_encoded = pd.get_dummies(df_feat, columns=CAT_COLS, drop_first=True, dtype=int)

    X_orig = df_encoded.drop(columns=["is_fraud"]).copy()
    y = df_encoded["is_fraud"].copy()

    X_train_raw, X_test_raw, y_train, y_test = train_test_split(
        X_orig, y, test_size=0.20, random_state=42, stratify=y
    )

    X_train = X_train_raw.copy()
    X_test = X_test_raw.copy()

    X_train[LOG_COLS] = np.log1p(np.maximum(0, X_train[LOG_COLS]))
    X_test[LOG_COLS] = np.log1p(np.maximum(0, X_test[LOG_COLS]))

    scaler = RobustScaler()
    X_train[NUM_COLS] = scaler.fit_transform(X_train[NUM_COLS])
    X_test[NUM_COLS] = scaler.transform(X_test[NUM_COLS])

    # Selección estadística Chi-Cuadrado sobre variables binarias en X_train
    bin_cols: List[str] = [c for c in X_train.columns if set(X_train[c].unique()).issubset({0, 1})]
    chi_vals, p_vals = chi2(X_train[bin_cols], y_train)
    df_chi2 = pd.DataFrame({
        "Variable": bin_cols,
        "Chi2_Stat": chi_vals,
        "p_value": p_vals,
    }).sort_values("Chi2_Stat", ascending=False)

    print(f"[Etapa 4] Variables tras One-Hot Encoding: {X_train.shape[1]}")
    print(f"[Etapa 4] X_train: {X_train.shape} | X_test: {X_test.shape}")
    print("[Etapa 4] Top 8 Variables Binarias por Estadístico Chi-Cuadrado:")
    print(df_chi2.head(8).to_string(index=False))

    return {
        "df_feat": df_feat,
        "X_train_raw": X_train_raw,
        "X_test_raw": X_test_raw,
        "X_train": X_train,
        "X_test": X_test,
        "y_train": y_train,
        "y_test": y_test,
        "df_chi2": df_chi2,
        "num_cols": NUM_COLS,
    }
