import streamlit as st
import pandas as pd
from st_gsheets_connection import GSheetsConnection

# 1. CEK STATUS LOGIN
if "logged_in" not in st.session_state:
    st.session_state["logged_in"] = False

if not st.session_state["logged_in"]:
    # --- HALAMAN LOGIN ---
    st.title("🔐 Login Dashboard")
    with st.form("login_form"):
        username = st.text_input("Username")
        password = st.text_input("Password", type="password")
        submit = st.form_submit_button("Masuk")
        if submit:
            if username == "admin" and password == "sumut2026":
                st.session_state["logged_in"] = True
                st.rerun()
            else:
                st.error("Username/Password Salah")
else:
    # --- HALAMAN UTAMA (WAJIB MENJOROK KE DALAM / PAKAI TAB) ---
    if st.sidebar.button("Logout / Keluar"):
        st.session_state["logged_in"] = False
        st.rerun()

    # MASUKKAN SEMUA KODE DASHBOARD ANDA DI SINI
    # Contoh (Pastikan semua baris di bawah ini ada spasi di depannya):
    st.title("Dashboard Database Guru Dinas Pendidikan Sumut")
    
    # Hubungkan ke GSheets (Contoh kode koneksi Anda)
    conn = st.connection("gsheets", type=GSheetsConnection)
    df = conn.read()
    
    st.dataframe(df) # Tampilkan tabel
