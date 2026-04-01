# Laporan Insight: Exploratory Data Analysis (EDA)

Berdasarkan analisis EDA komprehensif terhadap `indonesia_earthquake_cleaned.csv` (8.232 entri rekam jejak kegempaan), diperoleh temuan krusial yang akan menjadi landasan untuk tahap selanjutnya (*Data Preparation* & *Feature Engineering*):

## 1. Problematika Data Hilang (Missing Values)
Sebagian parameter penginderaan seismik absen dari observasi, mengakibatkan kepincangan rasio kelengkapan data.

- **Kekosongan Akut (> 80%)**: Fitur `dmin` (Jarak ke stasiun terdekat) hilang 88.3%, `horizontal_error` (91%), `num_stations_used` (84.8%), `minimum_distance` (91.1%), dan `scalar_moment` (87.8%).
  >**Rekomendasi Aksi**: Terlalu berisiko untuk menebak (imputasi) variabel dengan populasi defisit $\ge 80\%$. Fitur-fitur defek masif ini **harus di-drop**.
- **Kekosongan Level Sedang (50% - 70%)**: `gap`, `vertical_error`, `magnitude_error`, `standard_error`.
  >**Rekomendasi Aksi**: Ini didrop, karena lebih berorientasi paramater *uncertainty instrumentasi*, dan relevansinya kabur bagi prediksi empiris regresi regangan (`maxpga`).
- **Data Nodal Planes (Sekitar 23.5% Hilang)**: `nodal_plane_1_strike`, `dip`, `rake`, dll. 
  >**Rekomendasi Aksi**: Fitur fisis (*Strike/Dip/Rake*) cukup informatif dalam merepresentasikan tipe patahan (*thrust/normal/strike-slip*). Karena kekosongannya parsial, ini bisa coba *diimputasi* dengan KNN (*K-Nearest Neighbors*) pada fase Data Preparation atau dikoversi menjadi proksi diskrit pengelompokan wilayah saja.

## 2. Inspeksi Pencilan (Outliers) dan Distribusi
Statistik deskriptif terhadap label target:
- **`mag` (Magnitude)**: Rata-rata 6.13, memuncak ke skala Megathrust 9.1 (kemungkinan referensi gempa M 9.1 Aceh 2004 atau gempa besar historis lain). Variabel normal.
- **`depth_e` (Kedalaman)**: Rata-rata berkisar di kedalaman *shallow crustal* (50km), tetapi terentang maksimum 652km (*deep slab subduction* khas pertemuan lempeng Eurasia & Indo-Australia).

> [!CAUTION]  
> **Anomali Kritis Vektor `maxpga`**: Terdapat observasi PGA dengan nilai **-8.449**. Nilai maksimumnya juga sangat mencolok di titik **85.08**. Catatan: dalam kalkulasi umum, $max(\text{pga})$ memproyeksikan resultan besaran vektor akselerasi (harusnya *non-negative*, rentang umumnya 0 ~ beberapa *g*). Jika minus ini adalah *noise*/kode error sensor dari USGS, algoritma ML bakal limbung. **Tugas vital Data Prep: Drop seluruh baris yang punya label target minus (`maxpga` < 0)**.

## 3. Investigasi Multi-kolinearitas & Kebocoran Prediktor (Data Leakage)
Analisis korelatif Pearson memberikan ketegasan:

- **Kebocoran Masa Depan (R $\approx$ 0.8 - 0.9)**: Variabel seperti `maxpsa03`, `maxpsa10`, `maxpsa30`. Kuatnya ikatan linear variabel turunan spektrum gaya *(Pseudo-Spectral Acceleration)* nyaris sejajar sumbu *Y* terhadap target `maxpga`. 
  - **Tindakan Wajib**: Menghindari pemakaian variabel-variabel inter-observasi (sensor akhir pasca-kejadian) ini saat melatih ML agar mencegah *Data Leakage*.
- **Tingkat Korelasi Linear yang Rapuh**: Korelasi Pearson antara Magnitude `mag` dengan PGA sekadar (0.02) dan letalis Kedalaman `depth_e` justru negatif (-0.048).
  - Interpretasinya masuk akal! Propagasi atenuasi gempa dari pusat patahan (*hypocenter*) menuju sebidang titik tanah di permukaan sangat bergantung pada **Jarak dan Redaman Tanah**. Karakter korelasinya non-linear dan logaritmis ($Log_{10}$), di mana koefisien Pearson tradisional buta terhadapnya. 
  - **Urgensi Feature Engineering**: Harus meracik ulang jarak geometris hiposenter baru sebagai kompensasi rendahnya korelasi murni model linier. Rekonstruksi koordinat Haversine/Euclidean dari `latitude`, `longitude`, dan kedalaman `depth` dibutuhkan secara mendesak.
