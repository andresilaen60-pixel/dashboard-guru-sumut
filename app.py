import streamlit as st
from streamlit_gsheets import GSheetsConnection
import pandas as pd
import io

# 1. Konfigurasi Halaman
st.set_page_config(page_title="Database Guru Disdik Sumut", layout="wide")

# CSS Kustom: Memastikan teks navigasi tajam dan header rapi
st.markdown("""
    <style>
    [data-testid="stSidebar"] h2, [data-testid="stSidebar"] label, [data-testid="stSidebar"] p {
        color: #1e293b !important;
        font-weight: bold !important;
    }
    .header-box {
        background-color: white;
        padding: 20px;
        border-radius: 15px;
        box-shadow: 0 4px 15px rgba(0,0,0,0.05);
        border-left: 10px solid #1e3a8a;
    }
    </style>
    """, unsafe_allow_html=True)

# 2. Koneksi Data
url = "https://docs.google.com/spreadsheets/d/1ASCcp72gr0JD8ynsS7PpeTxzaAYMH2upgR0IL2YGLw0/edit#gid=1416024160"
conn = st.connection("gsheets", type=GSheetsConnection)

@st.cache_data(ttl=5)
def load_data():
    return conn.read(spreadsheet=url)

df_raw = load_data()

# --- LOGIKA DETEKSI KOLOM OTOMATIS ---
# Kita cari kolom mana yang kira-kira berisi 'Selesai', 'Perbaikan', atau 'Proses'
def find_status_col(dataframe):
    keywords = ['selesai', 'perbaikan', 'proses', 'lengkap', 'belum']
    for i, col in enumerate(dataframe.columns):
        # Cek sampel data di kolom tersebut
        sample_data = dataframe.iloc[:, i].astype(str).str.lower()
        if any(sample_data.str.contains(k).any() for k in keywords):
            return i
    return 9 # Default ke kolom J jika tidak ketemu

idx_status = find_status_col(df_raw)

# 3. Sidebar (Navigasi)
with st.sidebar:
    st.markdown("<h2 style='text-align:center;'>⚙️ Navigasi</h2>", unsafe_allow_html=True)
    st.divider()
    
    search_name = st.text_input("🔍 Cari Nama Guru")
    
    # Filter Jabatan (Kolom index 3)
    jabatan_list = ["Semua"] + sorted(df_raw.iloc[:, 3].dropna().unique().astype(str).tolist())
    filter_jabatan = st.selectbox("👨‍🏫 Filter Jabatan", jabatan_list)
    
    # Filter Pengiriman (Kolom index 7)
    pengiriman_options = ["Semua"] + sorted(df_raw.iloc[:, 7].dropna().unique().astype(str).tolist())
    filter_pengiriman = st.selectbox("🚚 Filter Pengiriman", pengiriman_options)
    
    # Filter Status Berkas (Deteksi Otomatis)
    status_options = ["Semua"] + sorted(df_raw.iloc[:, idx_status].dropna().unique().astype(str).tolist())
    filter_status = st.selectbox("📂 Filter Status Berkas", status_options)
    
    st.divider()
    if st.button("🚪 Keluar"):
        st.stop()

# 4. Header
col_logo, col_text = st.columns([1, 5])
with col_logo:
    st.image("https://raw.githubusercontent.com/Ananda-Silaen/Asset/main/Logo_Sumut.png", width=100)
with col_text:
    st.markdown("""
        <div class="header-box">
            <h1 style='margin:0; color:#1e3a8a; font-size:2.1em;'>Dashboard Database Guru Dinas Pendidikan Sumut</h1>
            <p style='margin:0; color:#64748b;'>Portal Informasi Pendataan & Usulan Kenaikan Pangkat</p>
        </div>
    """, unsafe_allow_html=True)

# 5. Logika Filter Data
df = df_raw.copy()

if search_name:
    df = df[df.iloc[:, 2].astype(str).str.contains(search_name, case=False, na=False)]

if filter_jabatan != "Semua":
    df = df[df.iloc[:, 3].astype(str) == filter_jabatan]

if filter_pengiriman != "Semua":
    df = df[df.iloc[:, 7].astype(str) == filter_pengiriman]

if filter_status != "Semua":
    df = df[df.iloc[:, idx_status].astype(str) == filter_status]

# 6. Konten Utama
st.divider()
if not df.empty:
    m1, m2, m3 = st.columns(3)
    m1.metric("Total Guru", len(df_raw))
    m2.metric("Hasil Filter", len(df))
    m3.metric("Status Server", "Online ✅")

    st.subheader("📋 Rekapitulasi Data Usulan")
    st.dataframe(df, use_container_width=True)
else:
    st.warning("⚠️ Data tidak ditemukan. Pastikan isi kolom 'Status Berkas' di Google Sheets sudah benar.")

# 7. Tombol Aksi
col_b1, col_b2, _ = st.columns([1, 1, 2])
with col_b1:
    try:
        buffer = io.BytesIO()
        with pd.ExcelWriter(buffer, engine='xlsxwriter') as writer:
            df.to_excel(writer, index=False)
        st.download_button("📥 Export ke Excel", data=buffer.getvalue(), file_name="data_guru_sumut.xlsx", mime="application/vnd.ms-excel")
    except:
        st.error("Gagal export. Pastikan 'xlsxwriter' sudah terinstal.")

with col_b2:
    if st.button("🖨️ Cetak PDF"):
        st.info("Tekan **Ctrl + P** untuk menyimpan PDF.")

st.caption("© 2026 Dinas Pendidikan Provinsi Sumatera Utara")