import streamlit as st
import json
from streamlit_gsheets import GSheetsConnection
import pandas as pd
from datetime import datetime

# 1. KONFIGURASI HALAMAN
st.set_page_config(page_title="Chatbot AI - Latihan", layout="wide")

# 2. INISIALISASI KONEKSI DATABASE
conn = st.connection("gsheets", type=GSheetsConnection)

# 3. CSS CUSTOM (SIDEBAR & STYLE)
st.markdown("""
    <style>
    [data-testid="stSidebarNav"] {display: none !important;}
    @import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;700&display=swap');
    html, body, [class*="css"] { font-family: 'Plus Jakarta Sans', sans-serif; }
    .chatbot-logo {
        font-weight: bold !important;
        font-size: 28px !important;
        text-decoration: none !important;
        color: inherit !important;
        display: block !important;
        margin: 20px 0 10px 0 !important;
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
    st.page_link("pages/Materi.py", label="📖 Materi AI")
    st.divider()

# 5. FUNGSI DATABASE & LOAD DATA
def load_kuis():
    try:
        with open("data/soal_latihan.json", "r") as f:
            return json.load(f)
    except: return []

def simpan_ke_database(nama, minggu, skor, total_soal):
    try:
        # Ambil data lama (ttl=0 agar data selalu fresh dari Google Sheets)
        existing_data = conn.read(ttl=0)
        
        # Buat baris baru
        new_row = pd.DataFrame([{
            "Timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "Nama": nama,
            "Minggu": minggu,
            "Skor": skor,
            "Total_Soal": total_soal
        }])
        
        # Gabungkan dan Update
        updated_df = pd.concat([existing_data, new_row], ignore_index=True)
        conn.update(data=updated_df)
        return True
    except Exception as e:
        st.error(f"Gagal menyimpan ke Database: {e}")
        return False

# 6. TAMPILAN UTAMA
st.title("📝 Latihan Mingguan")

# Form Nama (Wajib diisi sebelum kirim)
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

    if f"jawab_{idx_minggu}" not in st.session_state:
        st.session_state[f"jawab_{idx_minggu}"] = [None] * len(soal_list)
    
    # Tampilkan Daftar Soal
    for i, item in enumerate(soal_list):
        st.write(f"**{i+1}. {item['pertanyaan']}**")
        ans = st.radio(f"Pilih:", item['pilihan'], index=None, key=f"q_{idx_minggu}_{i}", label_visibility="collapsed")
        st.session_state[f"jawab_{idx_minggu}"][i] = ans
        st.write("---")

    # Tombol Submit
    if st.button("Kirim Jawaban", use_container_width=True, type="primary"):
        if None in st.session_state[f"jawab_{idx_minggu}"]:
            st.warning("Harap jawab semua soal terlebih dahulu!")
        elif nama_user.strip() == "":
            st.warning("Harap isi nama lengkap untuk keperluan database admin!")
        else:
            # Hitung Skor
            skor_benar = sum(1 for i, s in enumerate(soal_list) if st.session_state[f"jawab_{idx_minggu}"][i] == s['jawaban'])
            total_soal = len(soal_list)
            persentase = int((skor_benar / total_soal) * 100)
            
            # Proses Simpan
            with st.spinner("Sedang mengirim nilai ke database admin..."):
                berhasil = simpan_ke_database(nama_user, minggu_ke, skor_benar, total_soal)
            
            if berhasil:
                st.success(f"Skor Anda: {persentase}/100. Nilai berhasil disimpan!")
                if persentase >= 70:
                    st.balloons()