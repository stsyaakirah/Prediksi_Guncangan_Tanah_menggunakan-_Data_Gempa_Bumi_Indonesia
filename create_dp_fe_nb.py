import os
import nbformat as nbf

# Pastikan folder notebooks ada
os.makedirs('notebooks', exist_ok=True)
os.makedirs('data/processed', exist_ok=True)

nb = nbf.v4.new_notebook()

nb['cells'] = [
    nbf.v4.new_markdown_cell('# Data Preparation & Feature Engineering\nNotebook ini didedikasikan untuk mengawinkan data gempa dan lokasi sensor (*Spatial Join*) guna menemukan **Jarak Hiposenter ($R_{hypo}$)** yang merupakan pilar Ground Motion Prediction Equation (GMPE). Selain itu, skrip akan membersihkan variabel bocor (*leakage*) dan nilai rekam yang cacat.'),
    
    nbf.v4.new_code_cell('import pandas as pd\nimport numpy as np\nfrom sklearn.impute import KNNImputer\nfrom sklearn.neighbors import BallTree\nfrom sklearn.preprocessing import StandardScaler\nimport warnings\n\nwarnings.filterwarnings("ignore")'),
    
    nbf.v4.new_markdown_cell('## 1. Data Loading\nMemuat dataset event Gempa dan detail lokasi kumpulan Sensor (Stasiun).'),
    
    nbf.v4.new_code_cell('df_gempa = pd.read_csv("../data/raw/indonesia_earthquake_cleaned.csv")\ndf_sensor = pd.read_csv("../data/raw/katalog_sensor.tsv", sep="\\t")\n\nprint(f"Shape Gempa Awal: {df_gempa.shape}")\nprint(f"Jumlah Stasiun Sensor: {df_sensor.shape[0]}")'),
    
    nbf.v4.new_markdown_cell('## 2. Pembersihan Data (Data Cleaning)\\n\\n**Alat Tindakan & Alasan Pemilihan:**\\n- **Menghapus baris (Removing Data) PGA <= 0**: Nilai percepatan tanah tidak mungkin negatif dalam konteks pencatatan riil, melainkan sebuah sinyal eror/kosong dari instrumen BMKG. Kami *me-remove* baris ini karena jika diimputasi, model regresi secara fisika kehilangan keaslian (sensitivitas magnitudo-jarak jadi rusak).\\n- **Drop Features (Pencegahan Leakage)**: Kolom seperti `maxpsa03`, `maxmmi` harus dibuang mutlak. Mengapa? Karena variabel-variabel tersebut merekam intensitas observasi *setelah* gempa terjadi. Jika kita menggunakan informasi pasca-bencana ini untuk memprediksi guncangan tanah (PGA), kita melakukan *Data Leakage* parah yang akan membuat model menipu diri sendiri seolah nilai akurasinya 99%.\\n- **Drop Fitur Berlubang Parah**: Kolom instrumen murni (`rms`, `num_stations_used`, dll) yang kosong lebih dari 80-90% tidak bisa dibantu dengan cara imputer rata-rata. Pemaksaan imputasi pada data mayoritas absen akan menciptakan "distribusi fiktif" yang mendistorsi varians data aslinya.'),
    
    nbf.v4.new_code_cell('''# Menghapus PGA anomali/Log-Error
df_clean = df_gempa[df_gempa['maxpga'] > 0].copy()

# List kolom drop karena Leakage & Dominasi Missing Values
cols_to_drop = [
    'time', 'maxpsa03', 'maxpsa10', 'maxpsa30', 'maxmmi', 
    'dmin', 'horizontal_error', 'azimuthal_gap', 'num_stations_used', 
    'num_phases_used', 'minimum_distance', 'scalar_moment', 
    'gap', 'vertical_error', 'magnitude_error', 'standard_error', 'rms'
]
df_clean.drop(columns=cols_to_drop, inplace=True, errors='ignore')

print(f"Shape Gempa pasca Pembersihan Kasar: {df_clean.shape}")'''),

    nbf.v4.new_markdown_cell('## 3. Imputasi K-Nearest Neighbors (KNN)\\n\\n**Alasan Penggunaan KNN pada "Nodal Planes":**\\nKita mendapati kolom yang menyiratkan tipe bidang sesar gempa (*Nodal Planes strike/dip/rake*) masing-masing kosong sekitar 23%. \\nMengapa menggunakan **Imputasi KNN (K-Nearest Neighbors)** dibanding `Mean` (rata-rata) atau `Median`?\\n- Karena karakteristik geometri Patahan/Bidang Sesar sangat terikat secara geologis dan spasial. \\n- Gempa yang kedalaman dan koordinat geografisnya mirip, cenderung memiliki bidang patahan sesar (dip/strike) yang mirip juga (akibat lempeng subduksi yang sama).\\n- Dengan metode KNN (mengambil 5 titik vektor fitur terdekat), kita *menebak* sudut patahan yang bolong menggunakan sudut dari barisan gempa yang memiliki identitas magnitudo dan letak pembanding di sekitarnya. Ini mempertahankan autokorelasi spasial data patahan.'),
    
    nbf.v4.new_code_cell('''nodal_cols = [
    'nodal_plane_1_strike', 'nodal_plane_1_dip', 'nodal_plane_1_rake',
    'nodal_plane_2_strike', 'nodal_plane_2_dip', 'nodal_plane_2_rake'
]

# Imputasi menggunakan 5 tetangga terdekat berdasarkan vektor fitur yang tersisa
knn_imputer = KNNImputer(n_neighbors=5)
df_clean[nodal_cols] = knn_imputer.fit_transform(df_clean[nodal_cols])

print("Sisa missing value di dataset utama:")
print(df_clean.isnull().sum().sum())'''),

    nbf.v4.new_markdown_cell('## 4. Analitik Spasial Geometris (Feature Engineering)\\n\\n**Alasan Tindakan Ekstraksi Ekstrim:**\\n- Dataset aslinya tidak punya fitur terpenting untuk analisis GMPE: `Jarak`. \\n- Solusi yang kami ambil adalah mengawinkan katalog gempa dengan titik koordinat sensor stasiun BMKG.\\n- Kami menebak jarak stasiun pencatat `maxpga` tertinggi menggunakan pencarian tetangga terdekat berbasis geometri polar radius (algoritma `BallTree` dengan formula *Haversine* lengkungan bumi).\\n- **Kenapa `BallTree` dan Haversine?**: Mencari jarak antara ribuan gempa dan ribuan stasiun membutuhkan komputasi matriks yang massif. `BallTree` mengelompokkan partisi stasiun ke dalam percabangan bola sehingga komputasi spasial dieksekusi kurang dari 1 detik secara efisien.\\n- **Kenapa membuat fitur elevasi?**: Ketinggian stasiun (mdpl/meter) secara empiris lemah terkait dengan "kekerasaan batu tapak" ($V_{s30}$). Stasiun gunung lebih keras dibanding tanah basin dangkal. Ini menjadi substitusi proksi darurat kita.'),
    
    nbf.v4.new_code_cell('''# Menghalau elevation Kosong pada df_sensor dengan median lokal stasiun
df_sensor['elevation'] = pd.to_numeric(df_sensor['elevation'], errors='coerce')
df_sensor['elevation'] = df_sensor['elevation'].fillna(df_sensor['elevation'].median())

# Membangun Pohon Spasial dari Stasiun
st_coords_rad = np.radians(df_sensor[['latitude', 'longitude']])
tree = BallTree(st_coords_rad, metric='haversine')

# Kueri jarak Episenter Gempa ke Pohon Stasiun (K=1, artinya 1 terdekat)
eq_coords_rad = np.radians(df_clean[['latitude_e', 'longitude_e']])
dist_rad, indices = tree.query(eq_coords_rad, k=1)

# Mengkorversikan jarak Radian Haversine ke Kilometer (Jari-jari Bumi = 6371 km)
R_EARTH_KM = 6371.0
df_clean['R_epi_km'] = dist_rad.flatten() * R_EARTH_KM

# Feature Engineering: Hypocenter Distance (Dalil Pythagoras spasial + kedalaman)
df_clean['R_hypo_km'] = np.sqrt(df_clean['R_epi_km']**2 + df_clean['depth_e']**2)

# Mengambil proksi Elevasi stasiun terdekat (Bisa mewakili secara lemah profil Vs30 tapak)
df_clean['closest_station_elevation'] = df_sensor.iloc[indices.flatten()]['elevation'].values

df_clean[['latitude_e', 'longitude_e', 'R_epi_km', 'depth_e', 'R_hypo_km', 'closest_station_elevation']].head()'''),

    nbf.v4.new_markdown_cell('## 5. Target Logarithmic Transformation\nAtenuasi GMPE meniscayakan distribusi eksponensial. Mentransformasi `maxpga` ke $Log_{10}$.'),
    
    nbf.v4.new_code_cell('''df_clean['log_maxpga'] = np.log10(df_clean['maxpga'])
df_clean = df_clean.drop(columns=['maxpga']) # Membuang log linear karena digantikan oleh log_maxpga

print("Distribusi Target log_maxpga:")
display(df_clean['log_maxpga'].describe())'''),

    nbf.v4.new_markdown_cell('## 6. Penskalaan & Ekspor Final\nMelakukan *Standard Scaling* pada prediktor agar seimbang pergerakan gradiennya dalam model ML nanti.'),
    
    nbf.v4.new_code_cell('''# Menyiapkan Matriks Input Fitur
target_col = 'log_maxpga'
features = [c for c in df_clean.columns if c != target_col]

scaler = StandardScaler()
df_clean[features] = scaler.fit_transform(df_clean[features])

# Simpan Dataset Matang
final_path = "../data/processed/model_ready_data.csv"
df_clean.to_csv(final_path, index=False)

print(f"Data final untuk dilatih ML telah diekspor ke {final_path}!")
print(f"Jumlah final baris/kolom: {df_clean.shape}")''')
]

with open('notebooks/02_data_prep_and_feature_engineering.ipynb', 'w', encoding='utf-8') as f:
    nbf.write(nb, f)

print("Notebook Data Prep FE berhasil di-generate!")
