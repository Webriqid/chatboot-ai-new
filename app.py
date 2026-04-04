import streamlit as st
from responses import respon_ai


PERTANYAAN_CEPAT = [
    "Apa itu AI?",
    "Apa itu AI prediktif?",
    "Contoh AI generatif",
    "Perbedaan narrow AI dan general AI",
    "Apa fungsi AI preskriptif?",
    "Apa itu limited memory AI?"
]


st.set_page_config(
    page_title="Chatbot Materi AI",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded"
)


def load_css():
    st.markdown("""
    <style>
    .main {
        padding-top: 1rem;
    }

    .hero-box {
        background: linear-gradient(135deg, #0f172a, #1e293b);
        padding: 28px;
        border-radius: 20px;
        color: white;
        box-shadow: 0 8px 24px rgba(0,0,0,0.18);
        margin-bottom: 20px;
    }

    .hero-title {
        font-size: 42px;
        font-weight: 800;
        margin-bottom: 8px;
    }

    .hero-subtitle {
        font-size: 18px;
        opacity: 0.92;
    }

    .info-card {
        background: #111827;
        border: 1px solid #1f2937;
        border-radius: 18px;
        padding: 18px;
        margin-bottom: 14px;
        box-shadow: 0 4px 14px rgba(0,0,0,0.12);
    }

    .info-title {
        font-size: 20px;
        font-weight: 700;
        margin-bottom: 8px;
        color: #f9fafb;
    }

    .info-text {
        font-size: 15px;
        color: #e5e7eb;
        line-height: 1.7;
    }

    .section-title {
        font-size: 24px;
        font-weight: 700;
        margin-top: 6px;
        margin-bottom: 10px;
    }

    .small-note {
        font-size: 14px;
        color: #cbd5e1;
        margin-bottom: 12px;
    }

    .footer-note {
        text-align: center;
        font-size: 13px;
        color: #94a3b8;
        margin-top: 20px;
        margin-bottom: 10px;
    }

    div[data-testid="stChatMessage"] {
        border-radius: 18px;
        padding: 6px 4px;
    }

    div[data-testid="stChatInput"] {
        margin-top: 10px;
    }

    div.stButton > button {
        width: 100%;
        border-radius: 12px;
        border: 1px solid #334155;
        background: #0f172a;
        color: white;
        padding: 0.7rem 1rem;
        font-weight: 600;
        text-align: left;
        transition: 0.3s ease;
        margin-bottom: 8px;
    }

    div.stButton > button:hover {
        border: 1px solid #38bdf8;
        color: #38bdf8;
    }
    </style>
    """, unsafe_allow_html=True)


def inisialisasi_chat():
    if "messages" not in st.session_state:
        st.session_state.messages = [
            {
                "role": "assistant",
                "content": (
                    "Halo, saya siap membantu Anda mempelajari materi Artificial Intelligence. "
                    "Silakan ajukan pertanyaan terkait konsep, jenis, fungsi, contoh, atau perbedaan antar jenis AI."
                )
            }
        ]


def tampilkan_header():
    st.markdown("""
    <div class="hero-box">
        <div class="hero-title">🤖 Chatbot Materi AI</div>
        <div class="hero-subtitle">
            Aplikasi pembelajaran interaktif untuk membantu mahasiswa memahami konsep,
            jenis, fungsi, dan contoh penerapan Artificial Intelligence.
        </div>
    </div>
    """, unsafe_allow_html=True)


def tampilkan_kartu_info():
    col1, col2, col3 = st.columns(3)

    with col1:
        st.markdown("""
        <div class="info-card">
            <div class="info-title">📘 Fokus Materi</div>
            <div class="info-text">
                Konsep dasar AI, AI deskriptif, prediktif, preskriptif,
                generatif, reaktif, narrow AI, dan general AI.
            </div>
        </div>
        """, unsafe_allow_html=True)

    with col2:
        st.markdown("""
        <div class="info-card">
            <div class="info-title">🎯 Tujuan</div>
            <div class="info-text">
                Membantu mahasiswa belajar lebih mandiri, cepat memahami istilah,
                dan mudah mengeksplorasi materi melalui tanya jawab interaktif.
            </div>
        </div>
        """, unsafe_allow_html=True)

    with col3:
        st.markdown("""
        <div class="info-card">
            <div class="info-title">🧠 Mode Belajar</div>
            <div class="info-text">
                Mahasiswa dapat bertanya langsung tentang pengertian, fungsi,
                contoh, dan perbedaan konsep AI secara sederhana.
            </div>
        </div>
        """, unsafe_allow_html=True)


def tampilkan_contoh_pertanyaan():
    st.markdown('<div class="section-title">💡 Contoh Pertanyaan</div>', unsafe_allow_html=True)
    st.markdown(
        '<div class="small-note">Klik salah satu pertanyaan berikut untuk mencoba chatbot secara cepat.</div>',
        unsafe_allow_html=True
    )

    col1, col2 = st.columns(2)

    setengah = (len(PERTANYAAN_CEPAT) + 1) // 2
    daftar_kiri = PERTANYAAN_CEPAT[:setengah]
    daftar_kanan = PERTANYAAN_CEPAT[setengah:]

    with col1:
        for i, pertanyaan in enumerate(daftar_kiri):
            if st.button(pertanyaan, key=f"kiri_{i}", use_container_width=True):
                proses_pertanyaan_cepat(pertanyaan)
                st.rerun()

    with col2:
        for i, pertanyaan in enumerate(daftar_kanan):
            if st.button(pertanyaan, key=f"kanan_{i}", use_container_width=True):
                proses_pertanyaan_cepat(pertanyaan)
                st.rerun()


def tampilkan_sidebar():
    with st.sidebar:
        st.markdown("## 📚 Tentang Aplikasi")
        st.write("""
        Chatbot ini dirancang sebagai media bantu pembelajaran untuk mahasiswa
        dalam memahami materi Artificial Intelligence secara lebih interaktif.
        """)

        st.markdown("## 📝 Cakupan Materi")
        st.write("""
        - Pengertian AI  
        - Jenis-jenis AI  
        - Fungsi tiap jenis AI  
        - Contoh penerapan AI  
        - Perbedaan antar konsep AI  
        """)

        st.markdown("## 🎓 Saran Penggunaan")
        st.write("""
        Gunakan pertanyaan yang jelas, misalnya:
        - apa itu ai
        - jelaskan ai prediktif
        - contoh ai generatif
        """)

        if st.button("🔄 Reset Percakapan", use_container_width=True):
            st.session_state.messages = [
                {
                    "role": "assistant",
                    "content": "Riwayat percakapan telah direset. Silakan mulai bertanya kembali."
                }
            ]
            st.rerun()


def tampilkan_riwayat():
    st.markdown('<div class="section-title">💬 Ruang Percakapan</div>', unsafe_allow_html=True)

    for msg in st.session_state.messages:
        with st.chat_message(msg["role"]):
            if msg["role"] == "user":
                st.markdown(f"**Mahasiswa:** {msg['content']}")
            else:
                st.markdown(f"**Chatbot:** {msg['content']}")


def proses_pertanyaan(prompt):
    st.session_state.messages.append({"role": "user", "content": prompt})

    with st.spinner("Chatbot sedang menyiapkan jawaban..."):
        jawaban = respon_ai(prompt)

    st.session_state.messages.append({"role": "assistant", "content": jawaban})


def proses_pertanyaan_cepat(pertanyaan):
    proses_pertanyaan(pertanyaan)


def main():
    load_css()
    inisialisasi_chat()
    tampilkan_sidebar()

    tampilkan_header()
    tampilkan_kartu_info()
    tampilkan_contoh_pertanyaan()
    tampilkan_riwayat()

    prompt = st.chat_input("Ketik pertanyaan Anda di sini...")

    if prompt:
        proses_pertanyaan(prompt)
        st.rerun()

    st.markdown(
        '<div class="footer-note">Dikembangkan sebagai media bantu pembelajaran materi Artificial Intelligence.</div>',
        unsafe_allow_html=True
    )


if __name__ == "__main__":
    main()