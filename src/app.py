import streamlit as st
import joblib
import pandas as pd
import numpy as np
from pathlib import Path

# --- PAGE CONFIGURATION ---
st.set_page_config(page_title="PGA Prediction Dashboard", page_icon="🌍", layout="wide")

st.title("🌍 Seismic PGA Predictor - AI Dashboard")
st.markdown("Dashboard ini merupakan antarmuka interaktif *(deployment)* dari model **eXtreme Gradient Boosting (XGBoost)** untuk memprediksi *Peak Ground Acceleration* (PGA) berdasarkan analisis sesar gempa.")

# --- LOAD MODEL ---
@st.cache_resource
def load_model():
    model_path = Path(__file__).parent.parent / 'data' / 'processed' / 'pga_xgboost_model.joblib'
    if not model_path.exists():
        st.error(f"Model file tidak ditemukan pada lokasi absolut: {model_path}. Fase Evaluasi (Fase 6-7) mungkin belum merender model tersebut.")
        return None
    model = joblib.load(model_path)
    return model

model = load_model()

# --- SIDEBAR INPUT ---
st.sidebar.header("⚙️ Konfigurasi Geofisika (Sensor Input)")

def user_input_features():
    # Menyamakan ke fitur `Complex Features` di projek
    mag = st.sidebar.slider("Magnitude (Mw)", min_value=1.5, max_value=8.5, value=5.5, step=0.1)
    depth_e = st.sidebar.slider("Kedalaman Fokal (km)", min_value=0.0, max_value=300.0, value=35.0, step=1.0)
    latitude_e = st.sidebar.slider("Latitude", min_value=-15.0, max_value=15.0, value=-7.5, step=0.1)
    longitude_e = st.sidebar.slider("Longitude", min_value=90.0, max_value=145.0, value=110.0, step=0.1)
    
    st.sidebar.subheader("📐 Aspek Jarak/Atenuasi Sensor")
    R_epi_km = st.sidebar.number_input("Jarak Epispesifik (R_epi, km)", min_value=0.1, max_value=800.0, value=50.0)
    R_hypo_km = st.sidebar.number_input("Jarak Hiposenter (R_hypo, km)", min_value=0.1, max_value=1000.0, value=65.0)
    closest_station_elevation = st.sidebar.number_input("Elevasi Stasiun Pengukur (m)", min_value=-50.0, max_value=3000.0, value=150.0)
    
    st.sidebar.subheader("🪨 Mekanika Sesar (Nodal Planes)")
    np1_str = st.sidebar.slider("Nodal Plane 1 Strike", 0, 360, 150)
    np1_dip = st.sidebar.slider("Nodal Plane 1 Dip", 0, 90, 45)
    np1_rake = st.sidebar.slider("Nodal Plane 1 Rake", -180, 180, 90)
    
    np2_str = st.sidebar.slider("Nodal Plane 2 Strike", 0, 360, 270)
    np2_dip = st.sidebar.slider("Nodal Plane 2 Dip", 0, 90, 45)
    np2_rake = st.sidebar.slider("Nodal Plane 2 Rake", -180, 180, 45)

    data = {
        'mag': mag,
        'depth_e': depth_e,
        'latitude_e': latitude_e,
        'longitude_e': longitude_e,
        'nodal_plane_1_strike': np1_str,
        'nodal_plane_1_dip': np1_dip,
        'nodal_plane_1_rake': np1_rake,
        'nodal_plane_2_strike': np2_str,
        'nodal_plane_2_dip': np2_dip,
        'nodal_plane_2_rake': np2_rake,
        'R_epi_km': R_epi_km,
        'R_hypo_km': R_hypo_km,
        'closest_station_elevation': closest_station_elevation
    }
    
    features = pd.DataFrame(data, index=[0])
    return features

df = user_input_features()

# --- MAIN DASHBOARD BODY ---
st.subheader("📊 Tabel Ringkasan Sensor Prediktif")
st.dataframe(df.style.highlight_max(axis=0))

if model is not None:
    try:
        # 1. Konversi Tipe Data karena XGBoost ketat terhadap float vs int mismatch
        df_pred = df.astype(float)
        
        # 2. Prediction execution
        pred_log_pga = model.predict(df_pred)[0]
        pred_actual_pga = np.exp(pred_log_pga) # Anti-log for engineering metric conversions
        
        st.markdown("---")
        st.subheader("💡 Prediksi Arsitektur Mesin XGBoost")
        
        col1, col2 = st.columns(2)
        with col1:
            st.metric(label="Prediksi Log-PGA (Model Asli)", value=f"{pred_log_pga:.4f}")
        with col2:
            st.metric(label="Estimasi Intensitas Kasar PGA", value=f"{pred_actual_pga:.3f} cm/s²", delta="Berpotensi Membahayakan" if pred_actual_pga > 50 else "Kategori Terkendali")
            
        st.info("💡 **Explainability Note:** Coba perhatikan bagaimana memainkan *Slider* Magnitudo ke atas, otomatis akan menaikkan metrik prediksi. Sebaliknya, modifikasi slider Hiposenter menjauh (*R_hypo* ke >> 200 km), secara ajaib akan menstabilitaskan skor PGA karena XGBoost kita **sudah menjiwai hukum Fisika *Wave Attenuation (Peredaman Jarak)*.**")

    except ValueError as ve:
        st.error(f"❌ Terjadi kesalahan validasi tipe fitur XGBoost: {str(ve)}")
    except Exception as e:
        st.error(f"❌ Terjadi kesalahan sistem prediksi yang tidak terduga: {str(e)}")
else:
    st.warning("Model belum dapat diinisialisasi. Silakan laporkan galat kompilasi Anda.")

st.markdown("""
<br/>
<hr style="height:2px;border-width:0;color:gray;background-color:#E0E0E0">
<p align="center" style="font-size:12px">Antigravity MLOps Data Science Framework © 2026 - OOD PGA Predictor</p>
""", unsafe_allow_html=True)
