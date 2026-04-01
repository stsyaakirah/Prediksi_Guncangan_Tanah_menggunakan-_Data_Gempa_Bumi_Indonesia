---
name: evaluation
description: Evaluasi Test Set, Confidence Intervals, Calibration, dan Cost Matrix.
---
# 🏆 STANDAR EVALUASI FINAL (Q1 JOURNAL & ENTERPRISE)
1. **One-Time Use:** Test Set HANYA boleh diprediksi SATU KALI oleh model pemenang.
2. **95% Confidence Intervals (CI):** WAJIB hitung CI menggunakan Bootstrapping pada hasil `y_pred` vs `y_true`. (Jangan melatih ulang model untuk bootstrapping).
3. **Probability Calibration:** Jika memungkinkan, evaluasi Expected Calibration Error (ECE) atau Brier Score.
4. **Explainability:** Buat ringkasan SHAP (Global Summary & Local Waterfall plot).
