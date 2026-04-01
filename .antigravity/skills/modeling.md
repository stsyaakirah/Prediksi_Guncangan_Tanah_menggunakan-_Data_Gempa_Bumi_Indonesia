---
name: modeling
description: Eksperimen ML, Hyperparameter Tuning, dan Latency Tracking.
---
# 🧠 STANDAR EKSPERIMEN MODELING & MLOPS
1. **SOTA Compliance:** Wajib mengikutsertakan algoritma/metode yang direkomendasikan dalam dokumen SLR (Systematic Literature Review) proyek ini.
2. **Baseline Wajib:** Mulai dengan `DummyClassifier/Regressor`.
3. **Tuning Protocol:** Gunakan Optuna/RandomizedSearchCV HANYA pada `X_train`. DILARANG menggunakan Test Set untuk tuning!
4. **Industry Tracking (Wajib):** Log hasil wajib mencatat 'Inference Latency' (rata-rata waktu prediksi ms/baris).
