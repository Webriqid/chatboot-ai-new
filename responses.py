import json
from thefuzz import process, fuzz

def load_materi():
    try:
        with open("data/materi_ai.json", "r") as f:
            return json.load(f)
    except Exception as e:
        print(f"Error load JSON: {e}")
        return []

def respon_ai(user_input):
    dataset = load_materi()
    if not dataset:
        return "Database materi tidak ditemukan."

    # Ambil semua daftar pertanyaan dari file JSON
    daftar_pertanyaan = [item["pertanyaan"] for item in dataset]
    
    # Cari pertanyaan yang paling mirip dengan input user
    # scorer=fuzz.token_set_ratio membantu menangkap kata kunci penting
    hasil, skor = process.extractOne(user_input, daftar_pertanyaan, scorer=fuzz.token_set_ratio)

    # Jika kemiripan di atas 60%, berikan jawabannya
    if skor > 60:
        for item in dataset:
            if item["pertanyaan"] == hasil:
                return item["jawaban"]
    
    return "Maaf, saya tidak menemukan jawaban itu di materi. Coba tanya hal lain!"
def respon_ai(prompt):
    # Ubah input menjadi huruf kecil semua agar pencocokan lebih akurat
    prompt_lower = prompt.lower().strip()
    
    # 1. LOGIKA SAPAAN (GREETING) - TAMBAHKAN INI DI BARIS PALING ATAS
    sapaan_user = ["halo", "halo ai", "hai", "hi", "hello", "assalamualaikum", "p", "selamat pagi", "selamat siang"]
    if prompt_lower in sapaan_user:
        return "Halo juga! Ada yang bisa saya bantu untuk mendiskusikan materi AI kuliah kita hari ini?"
        
    # 2. LOGIKA MATERI KULIAH (Kode kamumu yang lama tetap di bawah sini)
    # Contoh isi kode lamamu:
    # if "etika" in prompt_lower:
    #     return ...
    
    # Fungsi fallback/default jika tidak ada kata kunci yang cocok
    return "Maaf, saya tidak menemukan jawaban itu di materi. Coba tanya hal lain!"