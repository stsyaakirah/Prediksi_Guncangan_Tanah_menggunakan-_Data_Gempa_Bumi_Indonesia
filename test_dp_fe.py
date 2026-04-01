import pandas as pd
import numpy as np
from sklearn.impute import KNNImputer
from sklearn.neighbors import BallTree
from sklearn.preprocessing import StandardScaler

import warnings
warnings.filterwarnings("ignore")

# 1. Load
df_gempa = pd.read_csv("data/raw/indonesia_earthquake_cleaned.csv")
df_sensor = pd.read_csv("data/raw/katalog_sensor.tsv", sep="\t")

# 2. Clean
df_clean = df_gempa[df_gempa['maxpga'] > 0].copy()
cols_to_drop = [
    'time', 'maxpsa03', 'maxpsa10', 'maxpsa30', 'maxmmi', 
    'dmin', 'horizontal_error', 'azimuthal_gap', 'num_stations_used', 
    'num_phases_used', 'minimum_distance', 'scalar_moment', 
    'gap', 'vertical_error', 'magnitude_error', 'standard_error', 'rms'
]
df_clean.drop(columns=cols_to_drop, inplace=True, errors='ignore')

# 3. KNN
nodal_cols = [
    'nodal_plane_1_strike', 'nodal_plane_1_dip', 'nodal_plane_1_rake',
    'nodal_plane_2_strike', 'nodal_plane_2_dip', 'nodal_plane_2_rake'
]
knn_imputer = KNNImputer(n_neighbors=5)
df_clean[nodal_cols] = knn_imputer.fit_transform(df_clean[nodal_cols])

# 4. Ball Tree
df_sensor['elevation'] = pd.to_numeric(df_sensor['elevation'], errors='coerce')
df_sensor['elevation'] = df_sensor['elevation'].fillna(df_sensor['elevation'].median())

st_coords_rad = np.radians(df_sensor[['latitude', 'longitude']])
tree = BallTree(st_coords_rad, metric='haversine')

eq_coords_rad = np.radians(df_clean[['latitude_e', 'longitude_e']])
dist_rad, indices = tree.query(eq_coords_rad, k=1)

R_EARTH_KM = 6371.0
df_clean['R_epi_km'] = dist_rad.flatten() * R_EARTH_KM
df_clean['R_hypo_km'] = np.sqrt(df_clean['R_epi_km']**2 + df_clean['depth_e']**2)
df_clean['closest_station_elevation'] = df_sensor.iloc[indices.flatten()]['elevation'].values

# 5. Transform
df_clean['log_maxpga'] = np.log10(df_clean['maxpga'])
df_clean = df_clean.drop(columns=['maxpga'])

# 6. Scaling
target_col = 'log_maxpga'
features = [c for c in df_clean.columns if c != target_col]
scaler = StandardScaler()
df_clean[features] = scaler.fit_transform(df_clean[features])

print("Test Completed Successfully! Shape:", df_clean.shape)
