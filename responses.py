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