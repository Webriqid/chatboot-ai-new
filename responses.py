import json
import os
from thefuzz import process, fuzz

def load_data_materi():
    path = "data/materi_lengkap.json"
    if os.path.exists(path):
        try:
            with open(path, "r") as f:
                return json.load(f)
        except:
            return []
    return []

def respon_ai(prompt):
    prompt = prompt.lower().strip()
    materi_list = load_data_materi()
    
    # 1. Penanganan Percakapan Basa-Basi (Small Talk)
    small_talk = {
        "oke": "Siap! Kalau ada yang membingungkan lagi, tanya saja ya.",
        "siap": "Oke! Semangat belajarnya!",
        "terima kasih": "Sama-sama! Senang bisa membantu belajarmu hari ini.",
        "thanks": "You're welcome! Ada materi lain yang mau dibahas?",
        "itu saja": "Oke, ringkas sekali ya! Berarti kamu sudah paham bagian ini. Mau lanjut ke materi minggu berikutnya?",
        "sudah": "Mantap kalau sudah paham! Mau coba kerjakan Latihan AI untuk ngetes pemahamanmu?",
        "halo": "Halo juga! Saya asisten AI-mu. Hari ini kita mau bahas materi minggu ke-berapa nih?",
        "hai": "Hai! Yuk, mau nanya apa seputar materi AI kita?"
    }

    # Cek apakah input user ada di daftar small talk
    for key in small_talk:
        if key in prompt:
            return small_talk[key]

    # 2. Kumpulkan semua sub-materi
    semua_topik = {}
    for minggu in materi_list:
        for sub in minggu["sub_materi"]:
            semua_topik[sub["judul"]] = {
                "isi": sub["isi"],
                "minggu": minggu["judul_besar"]
            }

    # 3. Fuzzy Matching
    pilihan_judul = list(semua_topik.keys())
    hasil_terbaik, skor = process.extractOne(prompt, pilihan_judul, scorer=fuzz.token_set_ratio)

    # 4. Respon Dinamis (Tidak Kaku)
    if skor > 65:
        data = semua_topik[hasil_terbaik]
        # Membuat variasi awalan agar tidak bosan
        variasi_awalan = [
            f"Tentu, ini dia penjelasan tentang **{hasil_terbaik}**:",
            f"Mengenai **{hasil_terbaik}**, ini yang perlu kamu catat:",
            f"Berdasarkan materi {data['minggu']}, berikut adalah poin-poin penting **{hasil_terbaik}**:"
        ]
        import random
        awalan = random.choice(variasi_awalan)
        
        return f"{awalan}\n\n{data['isi']}\n\nAda bagian dari penjelasan ini yang kurang jelas?"

    # 5. Jika Bot Benar-benar Tidak Tahu
    return "Wah, sepertinya saya belum punya data spesifik soal itu. Tapi kalau mau bahas **" + ", ".join(pilihan_judul[:2]) + "**, saya siap bantu!"