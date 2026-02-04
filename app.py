import streamlit as st
import pandas as pd
from st_gsheets_connection import GSheetsConnection

# Atur Judul Tab Browser
st.set_page_config(page_title="Dashboard Guru Sumut", layout="wide")

# --- LOGIKA LOGIN ---
if "logged_in" not in st.session_state:
    st.session_state["logged_in"] = False

if not st.session_state["logged_in"]:
    st.title("🔐 Login Dashboard Disdik Sumut")
    with st.form("login_form"):
        user = st.text_input("Username")
        pw = st.text_input("Password", type="password")
        submit = st.form_submit_button("Masuk")
        if submit:
            if user == "admin" and pw == "sumut2026":
                st.session_state["logged_in"] = True
                st.rerun()
            else:
                st.error("Username atau Password Salah!")
else:
    # --- HALAMAN DASHBOARD (SEMUA HARUS MENJOROK KE DALAM) ---
    
    # Tombol Logout di Sidebar
    if st.sidebar.button("Logout / Keluar"):
        st.session_state["logged_in"] = False
        st.rerun()

    st.title("📊 Dashboard Database Guru Dinas Pendidikan Sumut")
    st.markdown("---")

    # Koneksi ke Google Sheets
    try:
        conn = st.connection("gsheets", type=GSheetsConnection)
        df = conn.read()
        
        # Tampilkan Data
        st.subheader("Rekapitulasi Data Usulan")
        st.dataframe(df, use_container_width=True)
        
    except Exception as e:
        st.error(f"Gagal memuat data dari Google Sheets. Pastikan Secrets sudah benar. Error: {e}")
