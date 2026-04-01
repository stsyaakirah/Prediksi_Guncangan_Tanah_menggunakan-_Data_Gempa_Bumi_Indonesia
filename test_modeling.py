import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import MinMaxScaler
from sklearn.linear_model import LinearRegression
from sklearn.ensemble import RandomForestRegressor
from sklearn.svm import SVR
from xgboost import XGBRegressor
from sklearn.metrics import mean_squared_error, mean_absolute_error, r2_score
import warnings

warnings.filterwarnings("ignore")

# Load Data Matang
df = pd.read_csv("data/processed/model_ready_data.csv")
target_col = 'log_maxpga'
y = df[target_col]
X_all = df.drop(columns=[target_col])

# Skenario Ablasi: Seleksi Fitur
features_basic = ['mag', 'R_hypo_km', 'depth_e']
features_complex = list(X_all.columns)

feature_sets = {
    'Basic_GMPE_Features': features_basic,
    'Complex_Geology_Features': features_complex
}

models = {
    'Linear_Regression': LinearRegression(),
    'Random_Forest': RandomForestRegressor(n_estimators=10, random_state=42), # kurangi n_estimators untuk test
    'XGBoost': XGBRegressor(n_estimators=10, random_state=42, objective='reg:squarederror'),
    'SVR': SVR(C=1.0, epsilon=0.1)
}

scalers = {
    'StandardScale': None,
    'MinMaxScale': MinMaxScaler()
}

results = []

print("Mencoba loop...")
for feat_name, feat_cols in feature_sets.items():
    X_subset = df[feat_cols]
    X_train, X_test, y_train, y_test = train_test_split(X_subset, y, test_size=0.2, random_state=42)
    for scale_name, scaler in scalers.items():
        X_tr = X_train.copy()
        X_te = X_test.copy()
        if scaler is not None:
            X_tr = scaler.fit_transform(X_tr)
            X_te = scaler.transform(X_te)
        for model_name, model in models.items():
            model.fit(X_tr, y_train)
            preds = model.predict(X_te)
            rmse = np.sqrt(mean_squared_error(y_test, preds))
            mae = mean_absolute_error(y_test, preds)
            r2 = r2_score(y_test, preds)
            results.append({
                'Feature_Set': feat_name,
                'Scaler': scale_name,
                'Model': model_name,
                'RMSE': rmse,
                'MAE': mae,
                'R2_Score': r2
            })

df_results = pd.DataFrame(results)
print("Eksperimen Selesai! Hasil atas:")
print(df_results.sort_values(by='R2_Score', ascending=False).head(3))
