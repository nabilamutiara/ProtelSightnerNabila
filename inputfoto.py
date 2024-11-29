import cv2
import time
import os
import subprocess  # Tambahkan import subprocess di sini

def baca_file(file_path):
    with open(file_path, 'r') as file:
        return file.read().strip()

def ambil_gambar(nama_file):
    # Mencoba beberapa indeks untuk menemukan kamera yang terhubung melalui USB converter
    for i in range(5):
        cap = cv2.VideoCapture(i)
        
        if cap.isOpened():
            print(f"Mengakses kamera pada indeks {i}")
            break
    else:
        print("Tidak dapat mengakses kamera.")
        return

    print("Menunggu kamera untuk stabil...")
    time.sleep(2)  # Memberikan waktu agar kamera siap

    # Membaca beberapa frame pertama untuk memastikan kamera siap
    for _ in range(10):
        cap.read()

    print("Mengambil gambar...")
    ret, frame = cap.read()

    if ret:
        cv2.imwrite(nama_file, frame)  # Menyimpan gambar
        print(f"Gambar disimpan di {nama_file}")
    else:
        print("Gagal mengambil gambar, frame tidak valid.")

    cap.release()  # Menut

# Path file teks input
file_text = 'textinputuser.txt'

if os.path.exists(file_text):
    isi_file = baca_file(file_text)

    # Mengecek nilai isi file dan menyimpan foto sesuai perintah
    if isi_file.lower() == 'objek depan':
        ambil_gambar('fotodepan.jpg')
    elif isi_file.lower() == 'objek kanan':
        ambil_gambar('fotokanan.jpg')
    elif isi_file.lower() == 'objek belakang':
        ambil_gambar('fotobelakang.jpg')
    elif isi_file.lower() == 'objek kiri':
        ambil_gambar('fotokiri.jpg')
    else:
        print("Isi file tidak sesuai dengan perintah yang dikenal.")
else:
    print(f"File {file_text} tidak ditemukan.")

try:
    subprocess.run(["python3.11", "/Users/nabilamutiara/Downloads/sightnerfinal2/deteksiobjek.py"], check=True)
    print("File deteksiobjek.py berhasil dijalankan.")
except subprocess.CalledProcessError as e:
    print(f"Gagal menjalankan file deteksiobjek.py: {e}")
