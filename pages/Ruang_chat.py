import streamlit as st
from responses import respon_ai
import time

# 1. KONFIGURASI HALAMAN
st.set_page_config(page_title="Chatbot AI - Chat", page_icon=None, layout="wide")

# 2. INISIALISASI STATE
if "threads" not in st.session_state:
    st.session_state.threads = {"Diskusi Umum": []}
if "current_thread" not in st.session_state:
    st.session_state.current_thread = "Diskusi Umum"

# 3. CSS MODERN (ANTI-BLUE & ADAPTIF)
st.markdown("""
    <style>
    [data-testid="stSidebarNav"] {display: none;}
    @import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;700&display=swap');
    html, body, [class*="css"] { font-family: 'Plus Jakarta Sans', sans-serif; }

    /* CSS UNTUK LOGO (KEBAL MODE GELAP & ANTI-BIRU) */
    .chatbot-logo, 
    .chatbot-logo:link, 
    .chatbot-logo:visited, 
    .chatbot-logo:hover, 
    .chatbot-logo:active {
        font-weight: bold !important;
        font-size: 26px !important;
        text-decoration: none !important;
        /* Menggunakan warna teks sistem (Putih di Gelap, Hitam di Terang) */
        color: var(--text-color) !important; 
        transition: 0.2s !important;
        display: block !important;
        margin-bottom: 10px !important;
    }

    .chatbot-logo:hover {
        opacity: 0.8 !important;
        text-decoration: underline !important;
    }

    /* Paksa navigasi link di sidebar agar tetap mengikuti warna tema */
    section[data-testid="stSidebar"] a {
        color: var(--text-color) !important;
        text-decoration: none !important;
    }

    hr { border: 0; border-top: 1px solid #d1d5db; margin: 1rem 0; }
    .main .block-container { max-width: 800px; padding-top: 2rem; }
    </style>
""", unsafe_allow_html=True)

# 4. SIDEBAR
with st.sidebar:
    st.markdown('<a href="/" target="_self" class="chatbot-logo">Chatbot AI</a>', unsafe_allow_html=True)
    st.divider()
    st.page_link("app.py", label="🏠 Beranda")
    st.page_link("pages/Ruang_chat.py", label="💬 Ruang Chat")
    st.page_link("pages/Latihan.py", label="📝 Latihan AI")
    st.page_link("pages/Materi.py", label="📖 Materi AI") # Tambahkan baris ini
    st.divider()
    
    # Kelola Ruangan Chat
    st.caption("RIWAYAT CHAT")
    selection = st.selectbox(
        "Pilih Ruangan", 
        options=list(st.session_state.threads.keys()), 
        index=list(st.session_state.threads.keys()).index(st.session_state.current_thread),
        key="nav_chat_fixed_v4",
        label_visibility="collapsed"
    )
    
    if selection != st.session_state.current_thread:
        st.session_state.current_thread = selection
        st.rerun()

    with st.expander("📝 Opsi"):
        new_topic = st.text_input("Topik Baru", key="nt_fixed_v4")
        if st.button("Buat", use_container_width=True):
            if new_topic:
                st.session_state.threads[new_topic] = []
                st.session_state.current_thread = new_topic
                st.rerun()

# 5. AREA CHAT
st.title(f"💬 {st.session_state.current_thread}")

current_messages = st.session_state.threads[st.session_state.current_thread]
for message in current_messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

if prompt := st.chat_input(f"Tanya sesuatu ke Chatbot AI..."):
    with st.chat_message("user"):
        st.markdown(prompt)
    current_messages.append({"role": "user", "content": prompt})

    jawaban_full = respon_ai(prompt)

    with st.chat_message("assistant"):
        placeholder = st.empty()
        full_response = ""
        for word in jawaban_full.split():
            full_response += word + " "
            time.sleep(0.04)
            placeholder.markdown(full_response + "▌")
        placeholder.markdown(full_response)
    
    current_messages.append({"role": "assistant", "content": full_response})
    st.session_state.threads[st.session_state.current_thread] = current_messages