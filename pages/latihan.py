import streamlit as st
import json

st.set_page_config(page_title="Chatbot AI - Latihan", page_icon=None, layout="wide")

# CSS UNTUK MENYEMBUNYIKAN NAVIGASI ASLI & FIX WARNA
st.markdown("""
    <style>
    /* Sembunyikan navigasi bawaan streamlit */
    [data-testid="stSidebarNav"] {display: none !important;}
    
    @import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;700&display=swap');
    html, body, [class*="css"] { font-family: 'Plus Jakarta Sans', sans-serif; }

    /* Gaya Logo Chatbot AI di Sidebar */
    .chatbot-logo, .chatbot-logo:visited, .chatbot-logo:active {
        font-weight: bold !important;
        font-size: 28px !important;
        text-decoration: none !important;
        color: var(--text-color) !important;
        display: block !important;
        margin: 20px 0 10px 0 !important;
    }

    /* Memastikan link navigasi tidak berwarna biru/ungu */
    section[data-testid="stSidebar"] a {
        color: var(--text-color) !important;
        text-decoration: none !important;
    }
    </style>
""", unsafe_allow_html=True)

# SIDEBAR CUSTOM (Sesuai Gambar FCD38CD2)
with st.sidebar:
    st.markdown('<a href="/" target="_self" class="chatbot-logo">Chatbot AI</a>', unsafe_allow_html=True)
    st.divider()
    st.page_link("app.py", label="🏠 Beranda")
    st.page_link("pages/Ruang_chat.py", label="💬 Ruang Chat")
    st.page_link("pages/Latihan.py", label="📝 Latihan AI")
    st.page_link("pages/Materi.py", label="📖 Materi AI")
    st.divider()

# ... (lanjutkan dengan kode logika kuis kamu di bawah sini)

# (Masukkan CSS yang sama seperti di atas)

# FUNGSI LOAD DATA
def load_kuis():
    try:
        with open("data/soal_latihan.json", "r") as f:
            return json.load(f)
    except: return []

st.title("📝 Latihan Mingguan")
kuis_data = load_kuis()

if not kuis_data:
    st.warning("Belum ada soal kuis.")
else:
    # 1. Pilih Minggu
    opsi_kuis = [f"Kuis Minggu {k['minggu']}" for k in kuis_data]
    pilihan_minggu = st.selectbox("Pilih Kuis Minggu Ke:", opsi_kuis)
    
    idx_minggu = opsi_kuis.index(pilihan_minggu)
    soal_list = kuis_data[idx_minggu]['soal']

    # State untuk jawaban
    if f"jawab_{idx_minggu}" not in st.session_state:
        st.session_state[f"jawab_{idx_minggu}"] = [None] * len(soal_list)
    
    # Tampilkan Soal
    for i, item in enumerate(soal_list):
        st.write(f"**{i+1}. {item['pertanyaan']}**")
        ans = st.radio(f"Pilih:", item['pilihan'], index=None, key=f"q_{idx_minggu}_{i}", label_visibility="collapsed")
        st.session_state[f"jawab_{idx_minggu}"][i] = ans
        st.write("---")

    # Tombol Submit (Hanya muncul jika semua diisi)
    if None not in st.session_state[f"jawab_{idx_minggu}"]:
        if st.button("Kirim Jawaban", use_container_width=True, type="primary"):
            skor = sum(1 for i, s in enumerate(soal_list) if st.session_state[f"jawab_{idx_minggu}"][i] == s['jawaban'])
            total = (skor / len(soal_list)) * 100
            st.success(f"Skor Anda: {int(total)}/100")
            if total >= 70: st.balloons()