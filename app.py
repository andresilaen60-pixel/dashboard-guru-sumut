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
    # --- TAMPILAN DASHBOARD ---
    if st.sidebar.button("Logout / Keluar"):
        st.session_state["logged_in"] = False
        st.rerun()

    st.title("📊 Dashboard Database Guru Dinas Pendidikan Sumut")
    st.markdown("---")

    # CARA BARU: Langsung ambil data dari Link Google Sheets (Tanpa Secrets)
    sheet_url = "https://docs.google.com/spreadsheets/d/1ASCcp72gr0JD8ynsS7PpeTxzaAYMH2upgR0IL2YGLw0/export?format=csv"
    
    try:
        df = pd.read_csv(sheet_url)
        st.subheader("Data Usulan Masuk")
        st.dataframe(df, use_container_width=True)
    except Exception as e:
        st.error(f"Gagal memuat data. Pastikan link Google Sheet benar. Error: {e}")
