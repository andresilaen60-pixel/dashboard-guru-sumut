import streamlit as st
import pandas as pd
from st_gsheets_connection import GSheetsConnection

# Pengaturan dasar halaman
st.set_page_config(page_title="Dashboard Guru Sumut", layout="wide")

# --- SISTEM LOGIN ---
if "logged_in" not in st.session_state:
    st.session_state["logged_in"] = False

if not st.session_state["logged_in"]:
    # Tampilan Halaman Login
    st.title("🔐 Login Dashboard Disdik Sumut")
    with st.form("form_login"):
        user = st.text_input("Username")
        pasw = st.text_input("Password", type="password")
        if st.form_submit_button("Masuk"):
            if user == "admin" and pasw == "sumut2026":
                st.session_state["logged_in"] = True
                st.rerun()
            else:
                st.error("Username atau Password Salah!")
else:
    # --- TAMPILAN DASHBOARD (JIKA SUDAH LOGIN) ---
    if st.sidebar.button("Logout / Keluar"):
        st.session_state["logged_in"] = False
        st.rerun()

    st.title("📊 Dashboard Database Guru Dinas Pendidikan Sumut")
    st.markdown("---")

    # Bagian Menampilkan Data Google Sheets
    try:
        conn = st.connection("gsheets", type=GSheetsConnection)
        df = conn.read()
        
        # Tampilkan Tabel
        st.subheader("Data Usulan Masuk")
        st.dataframe(df, use_container_width=True)
        
    except Exception as e:
        st.error(f"Koneksi Google Sheets Bermasalah. Pastikan Secrets sudah diisi. Error: {e}")
