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
    # --- HALAMAN DASHBOARD UTAMA ---
    
    # Ambil Data dari Google Sheets
    sheet_url = "https://docs.google.com/spreadsheets/d/1ASCcp72gr0JD8ynsS7PpeTxzaAYMH2upgR0IL2YGLw0/export?format=csv"
    
    try:
        df = pd.read_csv(sheet_url)

        # --- SIDEBAR NAVIGASI & FILTER ---
        st.sidebar.header("⚙️ Navigasi & Filter")
        
        # 1. Pencarian Nama
        search_nama = st.sidebar.text_input("🔍 Cari Nama Guru")

        # 2. Filter Jabatan
        list_jabatan = ["Semua"] + sorted(df['Jabatan'].dropna().unique().tolist())
        filter_jabatan = st.sidebar.selectbox("👨‍🏫 Filter Jabatan", list_jabatan)

        # 3. Filter Golongan (Revisi Baru)
        # Mengambil kolom golongan/pangkat sesuai data di image_27e6c9.png
        kolom_gol = 'Golongan / Pangkat Saat Ini' if 'Golongan / Pangkat Saat Ini' in df.columns else df.columns[5]
        list_golongan = ["Semua"] + sorted(df[kolom_gol].dropna().unique().tolist())
        filter_golongan = st.sidebar.selectbox("📈 Filter Golongan", list_golongan)

        # 4. Filter Periode Usulan (Revisi Baru: Jan - Des 2026)
        list_periode = ["Semua", "Januari 2026", "Februari 2026", "Maret 2026", "April 2026", "Mei 2026", 
                        "Juni 2026", "Juli 2026", "Agustus 2026", "September 2026", "Oktober 2026", 
                        "November 2026", "Desember 2026"]
        filter_periode = st.sidebar.selectbox("📅 Periode Usulan 2026", list_periode)

        # 5. Filter Status Berkas (Sesuai Revisi: Ditampilkan Kembali)
        kolom_status = 'Status Berkas' # Pastikan nama kolom ini sesuai di GSheets Anda
        if kolom_status in df.columns:
            list_status = ["Semua"] + sorted(df[kolom_status].dropna().unique().tolist())
            filter_status = st.sidebar.selectbox("📁 Status Berkas", list_status)
        else:
            st.sidebar.info("Kolom 'Status Berkas' tidak ditemukan di GSheets")

        # --- LOGIKA PENYARINGAN DATA ---
        df_filtered = df.copy()
        
        if search_nama:
            df_filtered = df_filtered[df_filtered['Nama Lengkap (Sesuai SK Terakhir)'].str.contains(search_nama, case=False, na=False)]
        if filter_jabatan != "Semua":
            df_filtered = df_filtered[df_filtered['Jabatan'] == filter_jabatan]
        if filter_golongan != "Semua":
            df_filtered = df_filtered[df_filtered[kolom_gol] == filter_golongan]
        if filter_periode != "Semua":
            # Mencari kata bulan dalam kolom periode
            df_filtered = df_filtered[df_filtered.iloc[:, -1].astype(str).str.contains(filter_periode.split()[0], case=False, na=False)]
        if kolom_status in df.columns and filter_status != "Semua":
            df_filtered = df_filtered[df_filtered[kolom_status] == filter_status]

        # --- TAMPILAN UTAMA ---
        st.title("📊 Dashboard Database Guru Dinas Pendidikan Sumut")
        st.markdown("---")
        
        # Baris Informasi Singkat (Metrics)
        col1, col2, col3 = st.columns(3)
        col1.metric("Total Data", len(df))
        col2.metric("Hasil Filter", len(df_filtered))
        col3.metric("Status Server", "Online ✅")

        # Tabel Data
        st.subheader("📋 Rekapitulasi Data Usulan Masuk")
        st.dataframe(df_filtered, use_container_width=True)

        # --- TOMBOL LOGOUT (Revisi: Posisi Paling Bawah) ---
        st.sidebar.markdown("<br><br>" * 5, unsafe_allow_html=True) # Memberi jarak ke bawah
        if st.sidebar.button("🚪 Keluar / Logout", use_container_width=True):
            st.session_state["logged_in"] = False
            st.rerun()

    except Exception as e:
        st.error(f"Terjadi kesalahan data: {e}")
