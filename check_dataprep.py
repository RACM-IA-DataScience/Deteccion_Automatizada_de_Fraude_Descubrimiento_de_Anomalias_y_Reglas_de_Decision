import sys, pathlib
from pathlib import Path
sys.path.insert(0, "src/Entrega_Modular_de_Ingeniería_de_Software_en_Python")
from fase1_seleccion_y_limpieza import cargar_y_seleccionar_datos, limpiar_y_diagnosticar_outliers
from fase2_transformacion_y_seleccion import transformar_y_particionar

csv = Path("Datasets/credit_card_fraud_detection_2026.csv")
out = Path("results")
_, df_sel = cargar_y_seleccionar_datos(csv, out)
df_limpio, df_iqr = limpiar_y_diagnosticar_outliers(df_sel, out)
res = transformar_y_particionar(df_limpio)
print("PHASE1_OK shape", df_sel.shape, "-> limpio", df_limpio.shape)
print("PHASE2_OK X_train", res["X_train"].shape, "X_test", res["X_test"].shape)
print("PHASE2 dummy_cols:", res["X_train"].shape[1] - 25, "total:", res["X_train"].shape[1])
print("PHASE2 expect_drop_fraud:", res["X_train"].shape[1])
print("TOP CHISQ:", res["df_chi2"].head(5)[["Variable", "Chi2_Stat"]].to_dict("records"))
