---
name: prep-pipeline
description: Aturan besi Data Preparation, Sklearn Pipeline, Multi-Stage FS, dan Imbalance.
---
# ⚙️ ATURAN BESI DATA PREPARATION (ANTI-LEAKAGE)
1. **SPLIT FIRST (Non-Negotiable):** `train_test_split` (atau TimeSeriesSplit) SEBELUM fitting scaler/imputer apapun.
2. **Fit Only on Train:** Scaler/Imputer HANYA di-fit pada `X_train`.
3. **Sklearn Pipeline Encaspulation:** Seluruh transformasi terpusat pada Pipeline.
4. **Imbalanced Handling (SMOTE/Resampling):** WAJIB DI DALAM CV fold (`imblearn.pipeline.Pipeline`).
5. **Multi-Stage Feature Selection:** Terapkan Filter (VIF/Variance) -> Embedded (Lasso/Trees) -> Wrapper (RFECV) di dalam struktur pipeline.
