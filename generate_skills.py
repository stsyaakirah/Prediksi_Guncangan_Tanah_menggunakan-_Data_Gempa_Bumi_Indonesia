import os

def create_skill_files():
    # Pastikan direktori dibuat dengan benar
    skill_dir = ".antigravity/skills"
    os.makedirs(skill_dir, exist_ok=True)
    print(f"📁 Membangun direktori {skill_dir}...")

    # Menggunakan dictionary untuk menampung konten
    skills = {
        "data-audit.md": """---
name: data-audit
description: Panduan wajib untuk EDA, audit data, dan deteksi kebocoran (leakage).
---
# 📊 STANDAR AUDIT DATA & EDA (Q1 & INDUSTRY STANDARD)
1. **Rubin's Missing Data Framework:** Kategorikan missing value menjadi MCAR, MAR, atau MNAR. Imputasi berbasis MNAR memerlukan fitur indikator (is_missing).
2. **Leakage Taxonomy Audit:** - Hapus post-treatment features (Target Leakage).
   - Pastikan ID Column tidak berkorelasi dengan target.
   - Deteksi Temporal Leakage (jangan gunakan random split pada data waktu).
3. **Representativeness:** Cek survivorship bias atau class imbalance.
""",

        "prep-pipeline.md": """---
name: prep-pipeline
description: Aturan besi Data Preparation, Sklearn Pipeline, Multi-Stage FS, dan Imbalance.
---
# ⚙️ ATURAN BESI DATA PREPARATION (ANTI-LEAKAGE)
1. **SPLIT FIRST (Non-Negotiable):** `train_test_split` (atau TimeSeriesSplit) SEBELUM fitting scaler/imputer apapun.
2. **Fit Only on Train:** Scaler/Imputer HANYA di-fit pada `X_train`.
3. **Sklearn Pipeline Encaspulation:** Seluruh transformasi terpusat pada Pipeline.
4. **Imbalanced Handling (SMOTE/Resampling):** WAJIB DI DALAM CV fold (`imblearn.pipeline.Pipeline`).
5. **Multi-Stage Feature Selection:** Terapkan Filter (VIF/Variance) -> Embedded (Lasso/Trees) -> Wrapper (RFECV) di dalam struktur pipeline.
""",

        "modeling.md": """---
name: modeling
description: Eksperimen ML, Hyperparameter Tuning, dan Latency Tracking.
---
# 🧠 STANDAR EKSPERIMEN MODELING & MLOPS
1. **SOTA Compliance:** Wajib mengikutsertakan algoritma/metode yang direkomendasikan dalam dokumen SLR (Systematic Literature Review) proyek ini.
2. **Baseline Wajib:** Mulai dengan `DummyClassifier/Regressor`.
3. **Tuning Protocol:** Gunakan Optuna/RandomizedSearchCV HANYA pada `X_train`. DILARANG menggunakan Test Set untuk tuning!
4. **Industry Tracking (Wajib):** Log hasil wajib mencatat 'Inference Latency' (rata-rata waktu prediksi ms/baris).
""",

        "evaluation.md": """---
name: evaluation
description: Evaluasi Test Set, Confidence Intervals, Calibration, dan Cost Matrix.
---
# 🏆 STANDAR EVALUASI FINAL (Q1 JOURNAL & ENTERPRISE)
1. **One-Time Use:** Test Set HANYA boleh diprediksi SATU KALI oleh model pemenang.
2. **95% Confidence Intervals (CI):** WAJIB hitung CI menggunakan Bootstrapping pada hasil `y_pred` vs `y_true`. (Jangan melatih ulang model untuk bootstrapping).
3. **Probability Calibration:** Jika memungkinkan, evaluasi Expected Calibration Error (ECE) atau Brier Score.
4. **Explainability:** Buat ringkasan SHAP (Global Summary & Local Waterfall plot).
""",

        "reporting.md": """---
name: reporting
description: Penulisan Model Card, OOD Generalization, dan paper akademik.
---
# 🎓 STANDAR PELAPORAN & DEPLOYMENT
1. **Google Model Card & Drift Monitoring:** Susun limitasi, faktor evaluasi, dan rancangan pemantauan Data Drift (PSI/KS-Test).
2. **Integritas Akademik (Q1 Reviewer Standard):**
   - Bahas potensi kelemahan lewat analisis "Out-of-Distribution (OOD) Generalization".
   - DILARANG mengklaim kemampuan model melampaui rentang data yang diobservasi.
   - Wajib mencantumkan bagian "Keterbatasan Metode/Dataset".
3. **Artifact Output:** Full pipeline diekspor rapi via `joblib/ONNX`.
"""
    }

    # Loop untuk menulis file
    for filename, content in skills.items():
        filepath = os.path.join(skill_dir, filename)
        try:
            with open(filepath, "w", encoding="utf-8") as f:
                f.write(content)
            print(f"✅ Berhasil membuat/memperbarui: {filepath}")
        except Exception as e:
            print(f"❌ Gagal membuat {filename}: {e}")

    print("\n🎉 SETUP SKILL FILES FINAL SELESAI!")

if __name__ == "__main__":
    create_skill_files()