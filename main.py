from responses import respon_ai


def tampil_judul():
    print("=" * 50)
    print("         CHATBOT MATERI AI MAHASISWA")
    print("=" * 50)
    print("Ketik pertanyaan Anda tentang materi AI.")
    print("Ketik 'keluar' untuk berhenti.")
    print("-" * 50)


def main():
    tampil_judul()

    while True:
        pertanyaan = input("\nMahasiswa: ").strip()

        if not pertanyaan:
            print("Chatbot : Silakan ketik pertanyaan terlebih dahulu.")
            continue

        if pertanyaan.lower() in ["keluar", "exit", "quit"]:
            print("Chatbot : Terima kasih. Sampai jumpa.")
            break

        jawaban = respon_ai(pertanyaan)
        print(f"Chatbot : {jawaban}")


if __name__ == "__main__":
    main()