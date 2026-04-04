import json
import os
import difflib
import re


BASE_DIR = os.path.dirname(os.path.abspath(__file__))
FILE_JSON = os.path.join(BASE_DIR, "data", "materi_ai.json")


def load_materi():
    try:
        with open(FILE_JSON, "r", encoding="utf-8") as file:
            data = json.load(file)

        if not isinstance(data, list):
            return []

        data_valid = []
        for item in data:
            if isinstance(item, dict) and "pertanyaan" in item and "jawaban" in item:
                data_valid.append(item)

        return data_valid

    except FileNotFoundError:
        return []

    except json.JSONDecodeError:
        return []

    except Exception:
        return []


def bersihkan_teks(teks):
    teks = teks.lower().strip()
    teks = re.sub(r"[^\w\s]", "", teks)
    teks = re.sub(r"\s+", " ", teks)
    return teks


def hitung_skor_kata(input_user, pertanyaan_data):
    kata_user = set(input_user.split())
    kata_data = set(pertanyaan_data.split())

    if not kata_user or not kata_data:
        return 0

    jumlah_cocok = len(kata_user.intersection(kata_data))
    return jumlah_cocok / len(kata_data)


def cari_jawaban(pertanyaan_user, data_materi):
    if not data_materi:
        return "Maaf, data materi belum tersedia."

    pertanyaan_user_bersih = bersihkan_teks(pertanyaan_user)

    daftar_pertanyaan = [bersihkan_teks(item["pertanyaan"]) for item in data_materi]

    # 1. Cek kecocokan persis
    for item in data_materi:
        if bersihkan_teks(item["pertanyaan"]) == pertanyaan_user_bersih:
            return item["jawaban"]

    # 2. Cek kemiripan teks
    hasil_cocok = difflib.get_close_matches(
        pertanyaan_user_bersih,
        daftar_pertanyaan,
        n=1,
        cutoff=0.4
    )

    if hasil_cocok:
        pertanyaan_terbaik = hasil_cocok[0]
        for item in data_materi:
            if bersihkan_teks(item["pertanyaan"]) == pertanyaan_terbaik:
                return item["jawaban"]

    # 3. Cek berdasarkan kata kunci
    skor_terbaik = 0
    jawaban_terbaik = None

    for item in data_materi:
        pertanyaan_data_bersih = bersihkan_teks(item["pertanyaan"])
        skor = hitung_skor_kata(pertanyaan_user_bersih, pertanyaan_data_bersih)

        if skor > skor_terbaik:
            skor_terbaik = skor
            jawaban_terbaik = item["jawaban"]

    if skor_terbaik >= 0.3:
        return jawaban_terbaik

    # 4. Respon default
    return "Maaf, saya belum menemukan jawaban yang sesuai di materi. Coba gunakan kata kunci yang lebih spesifik."


def respon_ai(pertanyaan_user):
    data_materi = load_materi()
    return cari_jawaban(pertanyaan_user, data_materi)