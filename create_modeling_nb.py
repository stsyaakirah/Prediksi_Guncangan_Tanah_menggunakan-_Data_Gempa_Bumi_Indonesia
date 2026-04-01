import nbformat as nbf
import os

os.makedirs('notebooks', exist_ok=True)

nb = nbf.v4.new_notebook()

nb['cells'] = [
    nbf.v4.new_markdown_cell('# Predictive Modeling & Ablation Study\n\nSelamat datang di arena utama GMPE. Pada *notebook* ini, kita tidak hanya memanggil satu algoritma ML, melainkan melakukan perlombaan simultan terhadap **16 Varian Skenario (Ablation Study)** untuk mengevaluasi parameter *Feature Selection*, algoritma *Scaling*, dan arsitektur *Machine Learning* yang membuahkan metrik prediksi PGA terbaik.'),
    
    nbf.v4.new_code_cell('import pandas as pd\nimport numpy as np\nimport matplotlib.pyplot as plt\nimport seaborn as sns\n\nfrom sklearn.model_selection import train_test_split\nfrom sklearn.preprocessing import MinMaxScaler, StandardScaler\nfrom sklearn.linear_model import LinearRegression\nfrom sklearn.ensemble import RandomForestRegressor\nfrom sklearn.svm import SVR\nfrom xgboost import XGBRegressor\nfrom sklearn.metrics import mean_squared_error, mean_absolute_error, r2_score\n\nimport warnings\nwarnings.filterwarnings("ignore")'),
    
    nbf.v4.new_markdown_cell('## 1. Data Inject & Ablation Setup\nMemuat *dataset* yang memuat nilai target logaritmik fisika `log_maxpga`. \nSecara fundamental, kita mendefinisikan Dua Kubu Fitur:\n- **Fisika Dasar (GMPE Asli)**: `mag`, `R_hypo_km`, `depth_e`.\n- **Fisika Kompleks (Sesar & Topografi)**: Menambahkan aspek geometri patahan gempabumi (`nodal_planes`) dan `closest_station_elevation`.'),

    nbf.v4.new_code_cell('''# Load Data Matang
df = pd.read_csv("../data/processed/model_ready_data.csv")

target_col = 'log_maxpga'
y = df[target_col]
X_all = df.drop(columns=[target_col])

# Skenario Ablasi: Seleksi Fitur
features_basic = ['mag', 'R_hypo_km', 'depth_e']
features_complex = list(X_all.columns)

feature_sets = {
    'Basic_GMPE_Features': features_basic,
    'Complex_Geology_Features': features_complex
}'''),

    nbf.v4.new_markdown_cell('## 2. Pembangkitan Arena Evaluasi (Models & Scalers)\n\n**A. Mengapa menggunakan Ablasi Model Skalabilitas (MinMaxScaler vs StandardScaler)?**\n1. **StandardScaler** meletakkan rata-rata nilai di 0 (distribusi Normal). Ini bagus untuk model regresi linier. Namun, dalam fisika GMPE, nilai jarak yang minus (standar deviasi negatif) kadang bisa membingungkan algoritma non-linier seperti *Support Vector Regressor* (SVR) dalam memetakan kernel RBF.\n2. **MinMaxScaler** meremas kuat seluruh satuan besaran (dari $10$ magnitudo hingga $500$ km jarak) menjadi proporsi kaku antara $0$ dan $1$. Tentu peremasan absolut ini menguji apakah model ML lebih menyukai sinyal batas tegas (0 vs 1) dibanding sinyal kelengkungan natural (Z-score).\n\n**B. Argumentasi Pemilihan Hyperparameter Bawaan:**\n- `n_estimators=100`: Ini adalah 100 pepohonan keputusan acak/iteratif. Jika terlalu kecil (misal 10), pola regresi tidak tertangkap penuh (*underfitting*). Jika 1000, komputasi meledak lambat dan rawan *overfitting* hafal mati.\n- `random_state=42`: Ini adalah rahasia ilmiah universal. Memasang "kunci bibit acak" angka 42 (atau angka absolut apapun) memaksa algoritma memproduksi formasi pohon yang **SAMA PERSIS** jika ditarik/di-Run ulang seribu kali. Tanpa ini, hasil riset akademis tidak bisa diandalkan karena *score* tebakan berubah tiap menit.\n- `C=1.0, epsilon=0.1` (SVR): Batas *error margin* toleransi SVR agar model peduli mengabaikan fluktuatif bising noise sensor mikro namun tetap menghukum pencilan gempa merusak.\n\n**C. Mengapa Hyperparameter Tuning (*GridSearch/RandomSearch*) Diperlukan Nantinya?**\nSecara murni, algoritma seperti *XGBoost* disetel secara asal-asalan dalam *default run*. Kita **HARUS** melakukan *hyperparameter tuning* (menyusun matriks pencocokan *learning_rate* dan *max_depth* pohon) nanti apabila kinerja bawaan ini mentok atau mengalami *Overfitting* akut.'),

    nbf.v4.new_code_cell('''# Instansiasi Algoritma Regresi Parameter Dasar
models = {
    'Linear_Regression': LinearRegression(),
    'Random_Forest': RandomForestRegressor(n_estimators=100, random_state=42),
    'XGBoost': XGBRegressor(n_estimators=100, random_state=42, objective='reg:squarederror'),
    'SVR': SVR(C=1.0, epsilon=0.1)
}

# Menyediakan Variasi Scaler Ablasi
scalers = {
    'StandardScale': None, # Data mentah dari proses output Data_Prep sebelumnya telah di-Standardisasi
    'MinMaxScale': MinMaxScaler() # Merepresi rentang fitur menjadi persis 0 hingga 1
}'''),

    nbf.v4.new_markdown_cell('## 3. Eksekusi Skenario Massal (*Ablation Loop*)\nMelatih **80%** porsi Train untuk memprediksi **20%** Uji (Test), disilangkan melewati matriks 4 algoritma $\\times$ 2 scaling $\\times$ 2 kelompok fitur (Total 16 Kombinasi).'),
    
    nbf.v4.new_code_cell('''results = []
trained_models_pack = {} # Menyimpan model dan X_test/y_test untuk plotting komparatif di akhir

print("Memulai Perang Algoritma GMPE (16 Kombinasi Skema)...")
for feat_name, feat_cols in feature_sets.items():
    X_subset = df[feat_cols]
    
    # Target and Splitting (Fixed Random State for Reproducibility/Academic Robustness)
    X_train, X_test, y_train, y_test = train_test_split(X_subset, y, test_size=0.2, random_state=42)
    
    for scale_name, scaler in scalers.items():
        X_tr = X_train.copy()
        X_te = X_test.copy()
        
        # Scaling Transformation Ablation
        if scaler is not None:
            X_tr = scaler.fit_transform(X_tr)
            X_te = scaler.transform(X_te)
            
        for model_name, model in models.items():
            # Pelatihan
            model.fit(X_tr, y_train)
            
            # Prediksi Regresi
            preds = model.predict(X_te)
            
            # Kalkulasi Evaluasi Matrik Metrik
            rmse = np.sqrt(mean_squared_error(y_test, preds))
            mae = mean_absolute_error(y_test, preds)
            r2 = r2_score(y_test, preds)
            
            # Repositori Catatan Hasil
            combo_name = f"{model_name}_{feat_name}_{scale_name}"
            results.append({
                'Feature_Set': feat_name,
                'Scaler': scale_name,
                'Model': model_name,
                'RMSE': rmse,
                'MAE': mae,
                'R2_Score': r2,
                'Combo_ID': combo_name
            })
            
            # Menyimpan artefak test untuk memfasilitasi Plotting Aktual VS Prediksi
            if model_name not in trained_models_pack or r2 > trained_models_pack.get(model_name, {}).get('r2', -999):
                trained_models_pack[model_name] = {
                    'y_test': y_test,
                    'y_pred': preds,
                    'r2': r2,
                    'detail': f"{feat_name} | {scale_name}"
                }

df_results = pd.DataFrame(results)
print("Eksperimen 16-Ablasi Selesai!")'''),

    nbf.v4.new_markdown_cell('## 4. Analitik Papan Juara (*Leaderboard*) & Uji Ablasi\nSiapa penguasa atenuasi kegempaan yang paling akurat memprediksi target PGA? Analisis performa berdasarkan metrik varians regresi murni ($R^2$).'),

    nbf.v4.new_code_cell('''# Peringkatkan berdasarkan Nilai R2 terbesar.
df_leaderboard = df_results.sort_values(by='R2_Score', ascending=False).reset_index(drop=True)
display(df_leaderboard.head(8)) # Hanya nampilklan top 8 performa teratas

# Visualisasi Ranking Performa R2
plt.figure(figsize=(14, 8))
sns.barplot(
    data=df_leaderboard,
    x='R2_Score',
    y='Model',
    hue='Feature_Set',
    palette='viridis'
)
plt.title('Ablation Study: Performa $R^2$ Algoritma Memprediksi GMPE PGA', fontsize=15)
plt.xlabel('R-Squared Score (Semakin Mendekati 1 Semakin Mumpuni Menerjemahkan Fisika Gempa)')
plt.ylabel('Machine Learning Models')
plt.grid(axis='x', linestyle='--', alpha=0.6)
plt.legend(title='Varian Fitur Ablasi')
plt.show()'''),

    nbf.v4.new_markdown_cell('## 5. Visualisasi Validasi Uji Hukum GMPE Komparatif\nMengekstrak dan membandingkan *Scatter Plot: Target Aktual VS Tebakan Model*. \\nUntuk memvalidasi ketahanan matematis masing-masing algoritma, kita menjajarkan performa 4 arsitektur utama secara sejajar.'),

    nbf.v4.new_code_cell('''# Plotting Komparatif Paralel untuk 4 Model Terbaik (Mewakili Masing-Masing Algoritma)
fig, axes = plt.subplots(2, 2, figsize=(16, 14))
axes = axes.flatten()

# Warna menarik pembedan estetika
colors = ['crimson', 'teal', 'darkorange', 'dodgerblue']

for idx, (model_name, artifacts) in enumerate(trained_models_pack.items()):
    ax = axes[idx]
    
    y_test_c = artifacts['y_test']
    y_pred_c = artifacts['y_pred']
    r2 = artifacts['r2']
    detail = artifacts['detail']
    
    # Scatter Curve
    ax.scatter(y_test_c, y_pred_c, alpha=0.25, color=colors[idx % len(colors)], s=25, edgecolor='black', linewidth=0.3)
    
    # Garis Lurus Sempurna (Y=X Line)
    p1 = max(max(y_test_c), max(y_pred_c))
    p2 = min(min(y_test_c), min(y_pred_c))
    ax.plot([p1, p2], [p1, p2], 'k--', lw=3, label='Garis Identik (Y=X)')
    
    ax.set_title(f"{model_name}\\n$R^2$: {r2:.3f} | {detail.split(' | ')[0]}\\n(Scale: {detail.split(' | ')[1]})", fontsize=12, fontweight='bold')
    ax.set_xlabel('Aktual $Log_{10}(PGA)$', fontsize=11)
    ax.set_ylabel('Prediksi $Log_{10}(PGA)$', fontsize=11)
    
    ax.grid(alpha=0.3, linestyle='-.')
    ax.legend(loc='upper left')

plt.suptitle('Diagnosis Komparatif Evaluasi Algoritma: Aktual vs Prediksi Puncak Percepatan GMPE', fontsize=18, fontweight='bold', y=1.02)
plt.tight_layout()
plt.show()''')
]

with open('notebooks/03_predictive_modeling.ipynb', 'w', encoding='utf-8') as f:
    nbf.write(nb, f)

print("Notebook 03_predictive_modeling.ipynb BERHASIL DIPERBARUI dengan penjabaran Tuning dan Plot 4 Grid!")
