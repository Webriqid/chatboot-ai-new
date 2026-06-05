import streamlit as st
import json
from streamlit_gsheets import GSheetsConnection
import pandas as pd
from datetime import datetime

# 1. KONFIGURASI HALAMAN
st.set_page_config(page_title="Chatbot AI - Latihan", layout="wide")

# 2. INISIALISASI KONEKSI DATABASE
conn = st.connection("gsheets", type=GSheetsConnection)

# 3. CSS CUSTOM (UPGRADED VISUAL)
st.markdown("""
    <style>
    [data-testid="stSidebarNav"] {display: none !important;}
    @import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght=400;700&display=swap');
    html, body, [class*="css"] { font-family: 'Plus Jakarta Sans', sans-serif; }
    
    .chatbot-logo {
        font-weight: bold !important;
        font-size: 28px !important;
        text-decoration: none !important;
        color: inherit !important;
        display: block !important;
        margin: 20px 0 10px 0 !important;
    }

    /* UPGRADE: Membungkus setiap soal dengan kotak transparan yang estetik */
    .quiz-box {
        background-color: rgba(255, 255, 255, 0.03);
        padding: 20px;
        border-radius: 12px;
        border: 1px solid rgba(255, 255, 255, 0.08);
        margin-bottom: 15px;
    }
    </style>
""", unsafe_allow_html=True)

# 4. SIDEBAR CUSTOM
with st.sidebar:
    st.markdown('<a href="/" target="_self" class="chatbot-logo">Chatbot AI</a>', unsafe_allow_html=True)
    st.divider()
    st.page_link("app.py", label="🏠 Beranda")
    st.page_link("pages/Ruang_chat.py", label="💬 Ruang Chat")
    st.page_link("pages/Latihan.py", label="📝 Latihan AI")
    st.divider()

# 5. FUNGSI DATABASE & LOAD DATA
def load_kuis():
    try:
        with open("data/soal_latihan.json", "r", encoding="utf-8") as f:
            return json.load(f)
    except: 
        return []

def simpan_ke_database(nama, minggu, skor, total_soal):
    try:
        existing_data = conn.read(ttl=0)
        new_row = pd.DataFrame([{
            "Timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "Nama": nama,
            "Minggu": minggu,
            "Skor": skor,
            "Total_Soal": total_soal
        }])
        updated_df = pd.concat([existing_data, new_row], ignore_index=True)
        conn.update(data=updated_df)
        return True
    except Exception as e:
        st.error(f"Gagal menyimpan ke Database: {e}")
        return False

# 6. TAMPILAN UTAMA
st.title("📝 Latihan Mingguan")

nama_user = st.text_input("Masukkan Nama Lengkap kamu:", placeholder="Contoh: Kobe")

kuis_data = load_kuis()

if not kuis_data:
    st.warning("Belum ada soal kuis.")
else:
    opsi_kuis = [f"Kuis Minggu {k['minggu']}" for k in kuis_data]
    pilihan_minggu = st.selectbox("Pilih Kuis Minggu Ke:", opsi_kuis)
    
    idx_minggu = opsi_kuis.index(pilihan_minggu)
    minggu_ke = kuis_data[idx_minggu]['minggu']
    soal_list = kuis_data[idx_minggu]['soal']

    # UPGRADE UX: Menggunakan form agar aplikasi tidak melakukan refresh setiap kali opsi diklik
    with st.form(key=f"form_kuis_{idx_minggu}"):
        
        # List sementara untuk menampung input jawaban pengguna di dalam form
        jawaban_sementara = []
        
        for i, item in enumerate(soal_list):
            # Tampilan soal dibungkus div quiz-box agar rapi
            st.markdown('<div class="quiz-box">', unsafe_allow_html=True)
            st.write(f"**{i+1}. {item['pertanyaan']}**")
            
            ans = st.radio(
                f"Pilih:", 
                item['pilihan'], 
                index=None, 
                key=f"q_{idx_minggu}_{i}", 
                label_visibility="collapsed"
            )
            st.markdown('</div>', unsafe_allow_html=True)
            jawaban_sementara.append(ans)
        
        # Tombol submit khusus di dalam form
        tombol_kirim = st.form_submit_button("Kirim Jawaban", use_container_width=True, type="primary")

    # 7. LOGIKA VALIDASI SETELAH TOMBOL SUBMIT DIKLIK
    if tombol_kirim:
        if None in jawaban_sementara:
            st.warning("Harap jawab semua soal terlebih diante/dahulu!")
        elif nama_user.strip() == "":
            st.warning("Harap isi nama lengkap untuk keperluan database admin!")
        else:
            # Hitung skor jawaban benar
            skor_benar = sum(1 for i, s in enumerate(soal_list) if jawaban_sementara[i] == s['jawaban'])
            total_soal = len(soal_list)
            persentase = int((skor_benar / total_soal) * 100)
            
            with st.spinner("Sedang mengirim nilai ke database admin..."):
                berhasil = simpan_ke_database(nama_user, minggu_ke, skor_benar, total_soal)
            
            if berhasil:
                st.success(f"Skor Anda: {persentase}/100. Nilai berhasil disimpan!")
                if persentase >= 70:
                    st.balloons()