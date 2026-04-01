# Fase 3: Data Audit & Profiling (Initial Assessment)

## 1. Gambaran Umum (Dataset Overview)
- **Sumber Data:** `data/raw/indonesia_earthquake_cleaned.csv`
- **Variabel Target (Label):** `maxpga` (Peak Ground Acceleration)
- **Fitur Prediktor Utama:** `mag` (Magnitudo), `depth_e` (Kedalaman), `latitude_e`, `longitude_e`
- **Fitur Ekstra:** `maxpsa03`, `maxpsa10`, `maxpsa30`, observasi stasiun (`rms`, `gap`, `num_stations_used`), pengukuran error horizontal & vertikal.

## 2. Pengecekan Kualitas Data Berdasarkan Sampel
Dari inspeksi struktural awal pada raw dataset (800 baris pertama), ditemukan beberapa anomali/pola data sebagai berikut:

### A. Missing Values (Nilai Kosong)
- Terdapat cukup banyak entri kosong (`NaN`) pada fitur tambahan seperti parameter bidang sesar (`nodal_plane_1_strike`, `nodal_plane_1_dip`, `scalar_moment`, dll.).
- Fitur koordinat hiposenter (`latitude_e`, `longitude_e`), magnitudo (`mag`), dan kedalaman (`depth_e`) secara umum terisi penuh (sebagai mandatory features data kegempaan).
- Variabel target `maxpga` dan target spektral (`maxpsa`) tampaknya memiliki baris di mana *records* bernilai kosong / 0 / sangat kecil. Ini harus dikonfirmasi lebih lanjut karena baris dengan PGA yang kosong/anomali tidak dapat dipakai untuk pemodelan (memerlukan tahapan *drop/imputation*).

### B. Duplikasi / Redundansi Baris
- Ditemukan **duplikasi waktu pencatatan (timestamp) secara beruntun**.
  - *Contoh:* Gempa pada `1970-01-01 00:18:24.022...` tercatat hingga lebih dari 10 baris terpisah dengan variasi kecil pada metrik pelaporan stasiun (contoh: `dmin`, `rms`, atau `num_stations_used` berbeda tapi `mag` dan posisinya sama).
- Ini adalah masalah klasik pencatatan seismograf berulang dari stasiun berbeda atau revisi agensi pelapor. Diperlukan tahap *deduplikasi* berdasarkan Waktu (`time`) yang persis sama, untuk mencegah redundansi / *data leakage* di mana gempa yang sama diprediksi ulang di dataset latih.

### C. Analisis Geospasial
- Nilai koordinat Latitude berkisar di rentang tropis khatulistiwa, dan Longitude merepresentasikan wilayah Indonesia membujur dari barat ke timur (95.0 hingga ~141.0).
- Kedalaman (`depth_e`) memiliki rentang yang bervariasi (e.g., *shallow* 10km hingga *deep earthquakes* di atas 100km-500km). Perilaku atenuasi PGA sangat sensitif terhadap kedalaman, sehingga nilai yang tidak wajar harus dibersihkan.

## 3. Rencana Tindak Lanjut (Action Plan) di Data Preparation
1. **Deduplikasi Spesifik:** Membersihkan gempa berulang dengan menyeleksi baris menggunakan nilai stasiun pengukur terbanyak (`num_stations_used`) atau galat terkecil (`rms`/`gap`). Alternatif paling sederhana: `pd.drop_duplicates(subset=['time'])`.
2. **Penanganan Missing Targets:** Eksklusi spesifik (*Drop NaN*) pada baris di mana `maxpga` bernilai kosong atau tidak masuk akal (misal negatif, atau sama dengan 0.0). *Regression base* wajib memiliki target kuat.
3. **Feature Engineering Jarak:** Variabel independen harus ditambahkan melalui formula trigonometri/geodesi: 
   - Konversi koordinat `latitude_e` dan `longitude_e` stasiun vs episenter menjadi parameter jarak absolut (Jarak Hiposenter). Mengingat stasiun tidak dituliskan koordinatnya (hanya tercatat jarak absolut di beberapa row seperti `minimum_distance` atau dmin). Kita perlu memastikan *distance metrics* mana yang kita gunakan sebagai input prediktor, karena redaman akselerasi tanah (atenuasi lokal) proporsional terhadap log(Jarak).
4. **Transformasi Skala (Scaling):** Sebagian besar nilai atenuasi Ground Motion dimodelkan dalam logaritma basis natural ($\ln(PGA)$ atau $\log_{10}(PGA)$). Distribusi `maxpga` yang ekstrim dan *right-skewed* memerlukan Log-Scaling di *Pre-processing pipeline*.

*(Dokumen ini siap dijadikan dasar komparasi untuk penyusunan kode pembersihan data).*
