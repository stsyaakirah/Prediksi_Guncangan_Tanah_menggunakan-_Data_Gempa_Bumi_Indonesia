# CRISP-DM Project Charter: Prediksi Peak Ground Acceleration (PGA)

## 1. Business Understanding

### 1.1. Latar Belakang
Gempa bumi merupakan salah satu bencana alam yang destruktif, khususnya di wilayah tektonik aktif seperti Indonesia. Analisis bahaya seismik (*Seismic Hazard Analysis*) difungsikan untuk mitigasi risiko kerusakan infrastruktur dan perencanaan tata ruang wilayah yang lebih aman. Model empiris tradisional (*Ground Motion Prediction Equations* / GMPEs) yang selama ini menjadi standar memiliki tingkat ketidakpastian (standar deviasi / sigma) yang tinggi. Karenanya, komputasi *Machine Learning* diformulasikan untuk mengeksplorasi hubungan non-linear dari tipe sesar, jarak, dan kondisi batuan dasar, guna menghasilkan estimasi level guncangan *Peak Ground Acceleration* (PGA) secara spesifik-lokasi dengan akurasi melampaui metode sebelumnya.

### 1.2. Tujuan Bisnis & Penelitian
- **Tujuan Utama**: Membangun model algoritma prediktif berbasis Machine Learning (Regresi) untuk mengestimasi nilai PGA dengan keandalan yang tinggi sekaligus menembus batas performa limitasi persamaan empiris GMPE konvensional.
- **Dampak Praktis (Deployment)**: Menempatkan metrik tingkat bahaya seismologi yang lebih kredibel, meminimalisir nilai bias atau ketidakpastian sigma. Estimasi tegangan sismik dirancang untuk sepenuhnya mempedomani tata laksana Peraturan **Standar Nasional SNI 1726:2019** tentang Standar Perencanaan Ketahanan Gempa untuk struktur bangunan. Targetnya dapat diterjemahkan menjadi rekomendasi acuan keselamatan struktural.

### 1.3. Kriteria Keberhasilan (Success Criteria)
- **Metrik Model ML**: Mentargetkan penurunan margin *error* yang ditunjukkan oleh nilai **RMSE** (*Root Mean Square Error*) dan **MAE** (*Mean Absolute Error*) yang jauh lebih rendah, serta metrik penjelasan varians determinasi **$R^2$** yang lebih tinggi dibandingkan performa *baseline* persamaan GMPE yang ada.
- **Evaluasi Saintifik Bisnis**: Keberhasilan menekan nilai standar deviasi (sigma) sehingga estimasi guncangan bisa lebih dipercaya.
- **Kriteria Terap (*Deliverables*)**: Mengungguli limitasi *notebook* akademik. Dirilisnya dasbor web interaktif visual yang responsif terhadap *real-time geospatial hazard mapping*, beserta *API/Library Python*.

---

## 2. Data Understanding

### 2.1. Kebutuhan Klasifikasi Data
Model membutuhkan pangkalan data rekaman gerak tanah berserta identifikasi komprehensif profil sumber gempa, medium rambat, hingga parameter instrumen target.
- **Domain Keilmuan**: Geofisika, Seismologi (Kategori General / Lainnya)
- **Modus Tugas (*Task*)**: Machine Learning - Regresi
- **Urgensi Privasi**: Data spasial bersifat makro, sehingga dinilai *Tidak Sensitif*.

### 2.2. Ketersediaan dan Sumber Akuisisi
- **Sumber Akuisisi Data**: Menarik agregasi data publik dari repositori **Kaggle** yang didigitalisasi berdasarkan gabungan pencatatan lembaga observasi kegempaan nasional **BMKG** (Badan Meteorologi, Klimatologi, dan Geofisika) dan global **USGS** (*United States Geological Survey*).
- **Cakupan Spasial Analisis**: Rekaman percepatan tanah diperuntukkan eksklusif pada batas teritorial lokal **Indonesia** guna mencerminkan karakteristik atenuasi seismik spesifik (*regional condition*).

### 2.3. Gambaran Atribut/Fitur
Fitur-fitur prediktor dominan yang disiapkan:
- **Parameter Sumber (Source)**: Metrik besaran energi *Magnitudo* ($M_w$) serta Kedalaman dari *hiposenter* pusat gempa.
- **Parameter Penjalaran (Path & Distance)**: Berbagai formulasi jarak propagasi robekan kerak bumi, menggunakan penyesuaian perhitungan matematis jarak rekahan sesar, utamanya $R_{jb}$ (*Joyner-Boore distance*) dan $R_{rup}$ (*Rupture distance*).
- **Karakteristik Tanah (Site Condition)**: Respons amplifikasi lapisan permukaan tanah melalui profil Kecepatan rambat gelombang geser di rentang 30 meter paling dangkal ($V_{s30}$).

---

## 3. Rencana Komprehensif: Data Preparation

### 3.1. Penanganan Fitur (*Feature Engineering* & Imputasi)
Dalam kerangka *proxy modelling*, kompensasi atas kolom amatan teknis yang berlubang/kosong (*missing parameters* seperti $R_{jb}$ atau titik bor $V_{s30}$) memerlukan metode perbaikan kualitas dataset terencana.
- Penggunaan rumusan konversi geodesi dengan kalkulasi jarak dari proyeksi titik lintang (*latitude*) dan bujur (*longitude*) episenter.
- Manipulasi nilai karakteristik tanah (*imputasi* $V_{s30}$) berlandaskan pengayaan sumber eksternal penunjuk landai lereng topografi (*topographic surface proxies/elevasi model terrain*).

### 3.2. Penyelarasan Kepatuhan & Standardisasi
- Mematuhi limitasi kriteria batas aman gempa maksimum (MCE) dan spektrum respons desain yang digariskan **SNI 1726:2019**, sehingga keluaran analitik ini diproyeksikan langsung melengkapi beban seismik rencana.

---

## 4. Modeling & Rencana Deployment (*Production Pipeline*)

### 4.1. Pemodelan Machine Learning Berkomparasi
- Mengukur kinerja silang skema algoritma *Regression*.
- Memilah nilai deviasi absolut berbanding dengan kurva *attenuation relation* persamaan *existing* GMPE referensi untuk pergerakan lempeng subduksi maupun megathrust di Indonesia.

### 4.2. Arsitektur Distribusi (Pengiriman Output Akhir)
- **Web-based Interactive Dashboard**: Sistem peraga analisis (*dashboard web*) untuk simulasi visual spasial yang responsif dan real-time. Membantu pengambil kebijakan serta insinyur mengeksplorasi ancaman getaran pada tapak tertentu secara langsung.
- **API endpoints / Open-Source Python Library**: Modularisasi perangkat lunak yang *plug-and-play*. Institusi perencanaan teknis serta periset mitigasi bencana lain bisa mengakses estimasi probabilitas bahaya tersebut untuk ditenun ke dalam rutinitas kerja komputasi independen mereka sendiri.
