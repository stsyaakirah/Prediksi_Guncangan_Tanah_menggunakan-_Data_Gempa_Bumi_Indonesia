🌍 Prediksi Guncangan Tanah (PGA) - Indonesia Seismic Data
Repositori ini berisi framework pemodelan Machine Learning untuk memprediksi Peak Ground Acceleration (PGA) berdasarkan katalog gempa bumi di wilayah Indonesia. Proyek ini dikembangkan menggunakan Antigravity MLOps Framework untuk memastikan integritas data dan akurasi model yang tinggi.

🚀 Fitur Utama
Protokol Anti-Leakage: Menggunakan imblearn.pipeline dan strategi Split-First untuk mencegah kebocoran data pada tahap Pre-processing dan Cross-Validation.

Analisis Geofisika: Integrasi fitur-fitur mekanika gempa untuk meningkatkan akurasi prediksi pada berbagai kondisi geologi.

Evaluasi Real-time: Pengukuran Inference Latency untuk memastikan model layak digunakan dalam sistem Early Earthquake Warning (EEW).

Analisis OOD (Out-of-Distribution): Pengujian ketahanan model terhadap skenario gempa ekstrem seperti Megathrust.

🛠️ Tech Stack
Language: Python

Libraries: Scikit-learn, XGBoost/CatBoost, Imbalanced-learn, Pandas, NumPy.

Framework: Antigravity MLOps v2.0.

📊 Metrik Evaluasi
Selain menggunakan metrik standar (MAE, RMSE, R²), proyek ini juga mengukur:

95% Confidence Interval melalui metode Bootstrapping.

Inference Speed (ms/row) untuk kebutuhan operasional seismik.
