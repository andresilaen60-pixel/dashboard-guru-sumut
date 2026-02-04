import streamlit as st
import pandas as pd

# Pengaturan halaman
st.set_page_config(page_title="Dashboard Guru Sumut", layout="wide")

# --- SISTEM LOGIN ---
if "logged_in" not in st.session_state:
    st.session_state["logged_in"] = False

if not st.session_state["logged_in"]:
    st.title("🔐 Login Dashboard Monitoring Kenaikan Pangkat Disdik Sumut")
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
    # --- HALAMAN DASHBOARD UTAMA ---
    
    # Link menuju sheet 'Data_Usulan_KP' (GID: 1416024160)
    sheet_url = "https://docs.google.com/spreadsheets/d/1ASCcp72gr0JD8ynsS7PpeTxzaAYMH2upgR0IL2YGLw0/export?format=csv&gid=1416024160"
    
    try:
        df = pd.read_csv(sheet_url)

        # --- SIDEBAR NAVIGASI & FILTER ---
        st.sidebar.header("⚙️ Navigasi & Filter")
        
        search_nama = st.sidebar.text_input("🔍 Cari Nama Guru")

        # 1. Filter Jabatan
        list_jabatan = ["Semua"] + sorted(df['Jabatan'].dropna().unique().tolist()) if 'Jabatan' in df.columns else ["Semua"]
        filter_jabatan = st.sidebar.selectbox("👨‍🏫 Filter Jabatan", list_jabatan)

        # 2. Filter Golongan
        kolom_gol = 'Golongan / Pangkat Saat Ini' if 'Golongan / Pangkat Saat Ini' in df.columns else df.columns[5]
        list_golongan = ["Semua"] + sorted(df[kolom_gol].dropna().unique().tolist())
        filter_golongan = st.sidebar.selectbox("📈 Filter Golongan", list_golongan)

        # 3. Filter Periode Usulan
        list_periode = ["Semua", "Januari 2026", "Februari 2026", "Maret 2026", "April 2026", "Mei 2026", 
                        "Juni 2026", "Juli 2026", "Agustus 2026", "September 2026", "Oktober 2026", 
                        "November 2026", "Desember 2026"]
        filter_periode = st.sidebar.selectbox("📅 Periode Usulan 2026", list_periode)

        # 4. Filter Status Berkas
        kolom_status = 'Status Berkas'
        if kolom_status in df.columns:
            list_status = ["Semua"] + sorted(df[kolom_status].dropna().unique().tolist())
            filter_status = st.sidebar.selectbox("📁 Status Berkas", list_status)
        else:
            filter_status = "Semua"

        # --- LOGIKA PENYARINGAN DATA ---
        df_filtered = df.copy()
        
        if search_nama:
            kolom_nama = 'Nama Lengkap (Sesuai SK Terakhir)' if 'Nama Lengkap (Sesuai SK Terakhir)' in df.columns else df.columns[2]
            df_filtered = df_filtered[df_filtered[kolom_nama].astype(str).str.contains(search_nama, case=False, na=False)]
        
        if filter_jabatan != "Semua":
            df_filtered = df_filtered[df_filtered['Jabatan'] == filter_jabatan]
        
        if filter_golongan != "Semua":
            df_filtered = df_filtered[df_filtered[kolom_gol] == filter_golongan]
            
        if filter_periode != "Semua":
            kolom_periode = 'Periode Usulan' if 'Periode Usulan' in df.columns else df.columns[3]
            df_filtered = df_filtered[df_filtered[kolom_periode].astype(str).str.contains(filter_periode.split()[0], case=False, na=False)]
            
        if filter_status != "Semua" and kolom_status in df.columns:
            df_filtered = df_filtered[df_filtered[kolom_status] == filter_status]

        # --- TAMPILAN UTAMA ---
        st.title("📊 Dashboard Monitoring Kenaikan Pangkat Disdik Sumut")
        st.caption("Menampilkan Data dari Sheet: **Data_Usulan_KP**")
        st.markdown("---")
        
        col1, col2, col3 = st.columns(3)
        col1.metric("Total Data", len(df))
        col2.metric("Hasil Filter", len(df_filtered))
        col3.metric("Status Server", "Online ✅")

        st.subheader("📋 Rekapitulasi Data Usulan")
        st.dataframe(df_filtered, use_container_width=True)

        # --- TOMBOL LOGOUT (Posisi yang Sudah Dinaikkan Sedikit) ---
        st.sidebar.markdown("<br>" * 5, unsafe_allow_html=True) # Jarak dikurangi agar lebih naik
        if st.sidebar.button("🚪 Keluar / Logout", use_container_width=True):
            st.session_state["logged_in"] = False
            st.rerun()

    except Exception as e:
        st.error(f"Terjadi Kesalahan: {e}")



