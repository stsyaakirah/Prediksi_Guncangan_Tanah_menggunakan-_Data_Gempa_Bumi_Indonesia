import streamlit as st

# ==========================================
# KONFIGURASI HALAMAN
# ==========================================
st.set_page_config(page_title="Antigravity DS Prompt Generator (Ultimate Edition)", layout="wide")
st.title("🚀 Antigravity Data Science Prompt Generator")
st.markdown("**Ultimate Edition:** Terintegrasi dengan Multi-Domain Intelligence, SLR/SOTA Mapping, & Q1 Academic Standards.")

tab1, tab2, tab3, tab4, tab5, tab6, tab7 = st.tabs([
    "Fase 2: Kickoff", 
    "Fase 3: Data Audit", 
    "Fase 3.5: SLR & SOTA", 
    "Fase 4: Prep & Arsitektur", 
    "Fase 5: Modeling", 
    "Fase 6-7: Eval & XAI", 
    "Fase 8: Publikasi"
])

# ==========================================
# TAB 1: FASE 2 - PROBLEM SCOPING
# ==========================================
with tab1:
    st.header("📝 Fase 2: Problem Scoping & Domain Intelligence")
    col1, col2 = st.columns(2)
    with col1:
        project_name = st.text_input("Nama Project", value="Prediksi Risiko Berbasis Machine Learning")
        domain = st.selectbox("Domain Industri", ["Healthcare", "Finance / Banking", "E-Commerce / Retail", "NLP / Text Processing", "General / Lainnya"])
        task_type = st.selectbox("Tipe Task", ["Klasifikasi", "Regresi", "Time-Series Forecasting", "Klasterisasi"])
    with col2:
        problem_desc = st.text_area("Deskripsi Masalah Bisnis", value="Mengidentifikasi anomali atau risiko tinggi berdasarkan data historis.")
        sensitive_data = st.radio("Apakah ada data sensitif (PII/Medis)?", ["Ya", "Tidak"])
    
    st.divider()
    prompt_2 = f"""Kita mulai project data science baru.
- Nama Project: **{project_name}**
- Domain: **{domain}**
- Masalah: **{problem_desc}**
- Tipe Task: **{task_type}**
- Data Sensitif: **{sensitive_data}**

TUGAS ANDA:
1. Ajukan maksimal 5 pertanyaan elicitasi mengenai tujuan bisnis, ketersediaan data, dan regulasi {domain}. Tunggu saya menjawab.
2. SETELAH saya menjawab, langsung buat dokumen CRISP-DM Project Charter.
3. Tulis hasilnya ke file `docs/01_project_charter.md`. Jangan cetak isi dokumennya di chat.
"""
    st.code(prompt_2, language="markdown")

# ... (Tab 2 sampai Tab 6 tetap sama, pastikan indentasi "with tabX:" benar) ...

# ==========================================
# TAB 7: FASE 8 - PUBLIKASI (BAGIAN YANG DIPERBAIKI)
# ==========================================
with tab7:
    st.header("🎓 Fase 8: Laporan Akademik Q1")
    paper_title = st.text_input("Judul Paper", value="SOTA Analysis for Predictive Modeling")
    st.divider()
    prompt_8 = f"""Fase 8 dimulai. Kumpulkan konteks proyek dari folder `docs/`.
TUGAS ANDA:
1. Sintesis informasi menjadi paper akademik berjudul **"{paper_title}"**.
2. Di bab **Tinjauan Pustaka**, integrasikan isi dari `docs/03_sota_literature_review.md` untuk memperkuat justifikasi pemilihan metode kita.
3. Di bab **Eksperimen & Hasil**, tampilkan CI 95% dan diskusikan komparasi metode SOTA melawan baseline.
4. Wajib sertakan bab "Robustness & Out-of-Distribution (OOD) Generalization Limits".
5. Tulis draf ke `docs/06_academic_report.md`. Kabari saya jika selesai!
"""
    st.code(prompt_8, language="markdown") # <-- SUDAH DITUTUP