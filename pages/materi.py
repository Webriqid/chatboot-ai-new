import streamlit as st
import json
import os

st.set_page_config(page_title="Chatbot AI - Materi", page_icon=None, layout="wide")

# CSS (Tetap menggunakan yang anti-blue dan adaptif)
st.markdown("""
    <style>
    [data-testid="stSidebarNav"] {display: none;}
    .chatbot-logo, .chatbot-logo:visited {
        font-weight: bold !important; font-size: 26px !important;
        text-decoration: none !important; color: var(--text-color) !important;
        display: block !important; margin-bottom: 10px !important;
    }
    section[data-testid="stSidebar"] a {
        color: var(--text-color) !important; text-decoration: none !important;
    }
    </style>
""", unsafe_allow_html=True)

# SIDEBAR
with st.sidebar:
    st.markdown('<a href="/" target="_self" class="chatbot-logo">Chatbot AI</a>', unsafe_allow_html=True)
    st.divider()
    st.page_link("app.py", label="🏠 Beranda")
    st.page_link("pages/Ruang_chat.py", label="💬 Ruang Chat")
    st.page_link("pages/Latihan.py", label="📝 Latihan AI")
    st.page_link("pages/Materi.py", label="📖 Materi AI")

# FUNGSI LOAD DATA
def load_materi():
    try:
        with open("data/materi_lengkap.json", "r") as f:
            return json.load(f)
    except: return []

st.title("📖 Modul Pembelajaran Mingguan")
materi_data = load_materi()

if not materi_data:
    st.warning("Data materi belum tersedia di data/materi_lengkap.json")
else:
    # 1. Pilihan Minggu (Dropdown)
    opsi_minggu = [f"Minggu {m['minggu']}: {m['judul_besar']}" for m in materi_data]
    pilihan = st.selectbox("Pilih Pertemuan:", opsi_minggu)
    
    # 2. Ambil data sesuai pilihan
    idx = opsi_minggu.index(pilihan)
    data_pilihan = materi_data[idx]
    
    st.divider()
    st.header(data_pilihan['judul_besar'])
    
    # 3. Tampilkan Sub-Materi dalam Expander
    for sub in data_pilihan['sub_materi']:
        with st.expander(sub['judul']):
            st.write(sub['isi'])