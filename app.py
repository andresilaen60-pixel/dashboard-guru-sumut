import streamlit as st
import pandas as pd

# Pengaturan halaman
st.set_page_config(page_title="Dashboard Guru Sumut", layout="wide")

# --- SISTEM LOGIN ---
if "logged_in" not in st.session_state:
    st.session_state["logged_in"] = False

if not st.session_state["logged_in"]:
    st.title("🔐 Login Dashboard Disdik Sumut")
    with st.form("login_form"):
        user = st.text_input("Username")
        pasw = st.text_input("Password", type="password")
        if st.form_submit_button("Masuk"):
            if user == "admin" and pasw == "sumut2026":
                st.session_state["logged_in"] = True
                st.rerun()
            else:
                st.error("Username atau Password Salah!")
else:
    # --- SEMUA KODE DI BAWAH INI HANYA TAMPIL JIKA SUDAH LOGIN ---
    
    # 1. SIDEBAR NAVIGASI & FILTER
    st.sidebar.header("⚙️ Navigasi")
    
    # Tombol Logout
    if st.sidebar.button("Logout / Keluar"):
        st.session_state["logged_in"] = False
        st.rerun()
    
    st.sidebar.markdown("---")
    
    # Ambil Data
    sheet_url = "https://docs.google.com/spreadsheets/d/1ASCcp72gr0JD8ynsS7PpeTxzaAYMH2upgR0IL2YGLw0/export?format=csv"
    try:
        df = pd.read_csv(sheet_url)
        
        # Fitur Pencarian Nama
        search_nama = st.sidebar.text_input("🔍 Cari Nama Guru")
        
        # Filter Jabatan
        list_jabatan = ["Semua"] + sorted(df['Jabatan'].unique().tolist())
        filter_jabatan = st.sidebar.selectbox("👨‍🏫 Filter Jabatan", list_jabatan)
        
        # --- LOGIKA FILTER DATA ---
        df_filtered = df.copy()
        
        if search_nama:
            df_filtered = df_filtered[df_filtered['Nama Lengkap (Sesuai SK Terakhir)'].str.contains(search_nama, case=False, na=False)]
        
        if filter_jabatan != "Semua":
            df_filtered = df_filtered[df_filtered['Jabatan'] == filter_jabatan]

        # 2. TAMPILAN UTAMA
        st.title("📊 Dashboard Database Guru Dinas Pendidikan Sumut")
        st.markdown("---")
        
        # Baris Informasi Singkat (Metrics)
        col1, col2, col3 = st.columns(3)
        col1.metric("Total Guru", len(df))
        col2.metric("Hasil Filter", len(df_filtered))
        col3.metric("Status Server", "Online ✅")

        # Tabel Data
        st.subheader("📋 Rekapitulasi Data Usulan")
        st.dataframe(df_filtered, use_container_width=True)

    except Exception as e:
        st.error(f"Gagal memuat data filter. Error: {e}")
