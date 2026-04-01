import os
import nbformat as nbf

# Buat folder notebooks bila belum ada
os.makedirs('notebooks', exist_ok=True)

nb = nbf.v4.new_notebook()
nb['cells'] = [
    nbf.v4.new_markdown_cell('# Exploratory Data Analysis (EDA) - PGA Prediction\nNotebook ini bertugas untuk mengeksplorasi dataset `indonesia_earthquake_cleaned.csv` guna keperluan Data Analysis & Understanding.'),
    nbf.v4.new_code_cell('import pandas as pd\nimport numpy as np\nimport matplotlib.pyplot as plt\nimport seaborn as sns\nimport warnings\n\nwarnings.filterwarnings("ignore")\n%matplotlib inline\n\n# Atur style visual\nsns.set_theme(style="whitegrid")'),
    nbf.v4.new_markdown_cell('## 1. Load Data & Inspection'),
    nbf.v4.new_code_cell('data_path = "../data/raw/indonesia_earthquake_cleaned.csv"\ndf = pd.read_csv(data_path)\n\nprint(f"Dataset shape: {df.shape}")\ndisplay(df.head())'),
    nbf.v4.new_code_cell('df.info()'),
    nbf.v4.new_markdown_cell('## 2. Missing Value Diagnostics'),
    nbf.v4.new_code_cell('missing_vals = df.isnull().sum()\nmissing_percentages = (missing_vals / len(df)) * 100\nmissing_df = pd.DataFrame({\n    \'Missing_Count\': missing_vals,\n    \'Missing_Percentage\': missing_percentages\n})\nmissing_df = missing_df[missing_df[\'Missing_Count\'] > 0].sort_values(by=\'Missing_Percentage\', ascending=False)\n\nplt.figure(figsize=(10, 6))\nsns.barplot(x=\'Missing_Percentage\', y=missing_df.index, data=missing_df)\nplt.title("Persentase Missing Values per Kolom")\nplt.xlabel("Percentage (%)")\nplt.ylabel("Features")\nplt.show()'),
    nbf.v4.new_markdown_cell('## 3. Univariate Analysis\nTarget variabel utama kita: `maxpga`. Fitur prediktor kunci utamanya adalah `mag`, `depth_e`. \nCatatan: Fitur rekam kejadian seperti `maxmmi`, `maxpsa03`, `maxpsa10`, `maxpsa30` adalah *secondary targets* yang sebaiknya **dihapus (dropped)** dalam pemodelan prediktor agar tidak membocorkan informasi (*data leakage*).'),
    nbf.v4.new_code_cell('plt.figure(figsize=(12, 5))\nplt.subplot(1, 2, 1)\nsns.histplot(df[\'maxpga\'], kde=True, bins=50, color=\'firebrick\')\nplt.title("Distribusi Peak Ground Acceleration (PGA)")\n\nplt.subplot(1, 2, 2)\nsns.boxplot(x=df[\'maxpga\'], color=\'salmon\')\nplt.title("Boxplot PGA")\n\nplt.tight_layout()\nplt.show()'),
    nbf.v4.new_code_cell('fig, axes = plt.subplots(1, 2, figsize=(12, 5))\nsns.histplot(df[\'mag\'], kde=True, bins=30, ax=axes[0], color=\'teal\')\naxes[0].set_title("Distribusi Magnitude (Mw)")\n\nsns.histplot(df[\'depth_e\'], kde=True, bins=30, ax=axes[1], color=\'navy\')\naxes[1].set_title("Distribusi Kedalaman (km)")\n\nplt.tight_layout()\nplt.show()'),
    nbf.v4.new_markdown_cell('## 4. Bivariate Analysis & Correlation\nHubungan kedalaman dan besaran magnetudo terhadap maxpga.'),
    nbf.v4.new_code_cell('fig, axes = plt.subplots(1, 2, figsize=(14, 5))\nsns.scatterplot(data=df, x=\'mag\', y=\'maxpga\', alpha=0.5, ax=axes[0], color=\'darkorange\')\naxes[0].set_title("Magnitude vs PGA")\n\nsns.scatterplot(data=df, x=\'depth_e\', y=\'maxpga\', alpha=0.5, ax=axes[1], color=\'darkcyan\')\naxes[1].set_title("Depth vs PGA")\n\nplt.tight_layout()\nplt.show()'),
    nbf.v4.new_code_cell('# Memilih fitur utama untuk menghitung matriks korelasi\nfeatures_to_check = [\'maxpga\', \'mag\', \'depth_e\', \'latitude_e\', \'longitude_e\', \'dmin\', \'rms\', \'gap\']\ncorr_matrix = df[features_to_check].corr()\n\nplt.figure(figsize=(8, 6))\nsns.heatmap(corr_matrix, annot=True, cmap=\'coolwarm\', fmt=".2f", linewidths=0.5)\nplt.title("Correlation Matrix of Key Features")\nplt.show()'),
    nbf.v4.new_markdown_cell('## 5. Spatial Diagnostics (Distribusi Spasial Geografis)\nMemetakan koordinat (`latitude_e`, `longitude_e`) dan melihat secara visual tingkat sebaran `maxpga`.'),
    nbf.v4.new_code_cell('plt.figure(figsize=(12, 6))\nscatter = plt.scatter(x=df[\'longitude_e\'], y=df[\'latitude_e\'], \n                      c=df[\'maxpga\'], cmap=\'Reds\', alpha=0.7, s=df[\'mag\']*2)\nplt.colorbar(scatter, label=\'Peak Ground Acceleration (maxpga)\')\nplt.title("Peta Persebaran Gempa berdasarkan maxpga di Indonesia")\nplt.xlabel("Longitude")\nplt.ylabel("Latitude")\nplt.grid(True, linestyle=\'--\', alpha=0.6)\nplt.show()')
]

with open('notebooks/01_exploratory_data_analysis.ipynb', 'w') as f:
    nbf.write(nb, f)

print("Notebook EDA berhasil di-generate!")
