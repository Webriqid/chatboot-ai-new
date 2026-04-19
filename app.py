import streamlit as st

# 1. KONFIGURASI HALAMAN
st.set_page_config(page_title="Chatbot AI", page_icon=None, layout="wide")

# 2. INISIALISASI STATE
if "threads" not in st.session_state:
    st.session_state.threads = {"Diskusi Umum": []}

# 3. CSS GLOBAL (DIBERSIHKAN & DIPERKUAT)
st.markdown("""
    <style>
    [data-testid="stSidebarNav"] {display: none;}
    @import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;700&display=swap');
    html, body, [class*="css"] { font-family: 'Plus Jakarta Sans', sans-serif; }

    /* CSS UNTUK LOGO (KEBAL MODE GELAP & ANTI-BIRU SETELAH DIKLIK) */
    .chatbot-logo, 
    .chatbot-logo:link, 
    .chatbot-logo:visited, 
    .chatbot-logo:hover, 
    .chatbot-logo:active {
        font-weight: bold !important;
        font-size: 26px !important;
        text-decoration: none !important;
        color: var(--text-color) !important; 
        transition: 0.2s !important;
        display: block !important;
        margin-bottom: 10px !important;
    }

    .chatbot-logo:hover {
        opacity: 0.8 !important;
        text-decoration: underline !important;
    }
    
    hr { border: 0; border-top: 1px solid #d1d5db; margin: 1rem 0; }

    /* Kotak Menu yang Adaptif Mode Terang/Gelap */
    .option-card {
        background-color: rgba(255, 255, 255, 0.05); 
        padding: 20px;
        border-radius: 15px;
        border: 1px solid var(--text-color) !important; 
        text-align: center;
        min-height: 150px;
        box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1);
        color: var(--text-color) !important;
        transition: 0.3s;
    }

    .option-card:hover {
        transform: translateY(-5px);
        box-shadow: 0 10px 15px -3px rgba(0, 0, 0, 0.2);
        border: 1px solid #3b82f6 !important;
    }
    
    .option-card h3 {
        color: var(--text-color) !important;
    }

    /* Paksa navigasi link di sidebar agar tidak biru */
    section[data-testid="stSidebar"] a {
        color: var(--text-color) !important;
        text-decoration: none !important;
    }
    </style>
""", unsafe_allow_html=True)

# 4. SIDEBAR (DITAMBAHKAN NAVIGASI LATIHAN)
with st.sidebar:
    st.markdown('<a href="/" target="_self" class="chatbot-logo">Chatbot AI</a>', unsafe_allow_html=True)
    st.divider()
    st.page_link("app.py", label="🏠 Beranda")
    st.page_link("pages/Ruang_chat.py", label="💬 Ruang Chat")
    st.page_link("pages/Latihan.py", label="📝 Latihan AI")
    st.page_link("pages/Materi.py", label="📖 Materi AI") # Tambahkan baris ini
    st.divider()

# 5. KONTEN UTAMA
st.markdown("""
    <div style="background: linear-gradient(135deg, #1e293b 0%, #0f172a 100%); padding: 80px 40px; border-radius: 24px; color: white; text-align: center;">
        <h1 style='font-size: 50px; margin-bottom: 10px;'>Selamat Datang di Chatbot AI</h1>
        <p style='font-size: 18px; opacity: 0.8;'>Pilih modul pembelajaran di bawah ini untuk memulai.</p>
    </div>
""", unsafe_allow_html=True)

st.write("##")

# 6. PILIHAN MENU
col1, col2, col3 = st.columns(3)

with col1:
    st.markdown('<div class="option-card"><h3>💬 Ruang Chat</h3><p>Diskusi interaktif dengan AI tentang materi kuliah.</p></div>', unsafe_allow_html=True)
    if st.button("Masuk Chat", use_container_width=True, key="btn_chat"):
        st.switch_page("pages/Ruang_chat.py")

with col2:
    st.markdown('<div class="option-card"><h3>📝 Latihan AI</h3><p>Uji pemahamanmu dengan kuis mingguan yang menantang.</p></div>', unsafe_allow_html=True)
    if st.button("Mulai Latihan", use_container_width=True, key="btn_quiz"):
        st.switch_page("pages/Latihan.py") 

with col3:
    st.markdown('<div class="option-card"><h3>📖 Materi AI</h3><p>Lihat ringkasan materi dan glosarium istilah AI.</p></div>', unsafe_allow_html=True)
    if st.button("Lihat Materi", use_container_width=True, key="btn_materi"):
        st.switch_page("pages/Materi.py")