---
name: data-audit
description: Panduan wajib untuk EDA, audit data, dan deteksi kebocoran (leakage).
---
# 📊 STANDAR AUDIT DATA & EDA (Q1 & INDUSTRY STANDARD)
1. **Rubin's Missing Data Framework:** Kategorikan missing value menjadi MCAR, MAR, atau MNAR. Imputasi berbasis MNAR memerlukan fitur indikator (is_missing).
2. **Leakage Taxonomy Audit:** - Hapus post-treatment features (Target Leakage).
   - Pastikan ID Column tidak berkorelasi dengan target.
   - Deteksi Temporal Leakage (jangan gunakan random split pada data waktu).
3. **Representativeness:** Cek survivorship bias atau class imbalance.
