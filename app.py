import streamlit as st

# --- FUNGSI LOGIN SEDERHANA ---
def login():
    st.title("🔐 Login Dashboard Disdik Sumut")
    
    # Buat form login
    with st.form("login_form"):
        username = st.text_input("Username")
        password = st.text_input("Password", type="password")
        submit = st.form_submit_button("Masuk")
        
        if submit:
            # GANTI USERNAME & PASSWORD DI SINI SESUAI KEINGINAN ANDA
            if username == "admin" and password == "sumut2026":
                st.session_state["logged_in"] = True
                st.success("Login Berhasil!")
                st.rerun()
            else:
                st.error("Username atau Password salah")

# --- CEK STATUS LOGIN ---
if "logged_in" not in st.session_state:
    st.session_state["logged_in"] = False

if not st.session_state["logged_in"]:
    login()
else:
    # --- JIKA SUDAH LOGIN, TAMPILKAN DASHBOARD ANDA ---
    
    # Tombol Keluar di Sidebar
    if st.sidebar.button("Logout / Keluar"):
        st.session_state["logged_in"] = False
        st.rerun()

    # --- MASUKKAN SEMUA KODE DASHBOARD LAMA ANDA DI BAWAH INI ---
    st.title("Dashboard Database Guru Dinas Pendidikan Sumut")
    # ... (lanjutkan dengan kode visualisasi data Anda yang lama)
