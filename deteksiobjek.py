import subprocess
import os
from ultralytics import YOLO
import cv2
import matplotlib.pyplot as plt
from deep_translator import GoogleTranslator  # Alternatif menggunakan deep-translator
from collections import Counter
import pygame
from elevenlabs import ElevenLabs


model = YOLO('yolov5s.pt')

# Inisialisasi penerjemah
translator = GoogleTranslator(source='en', target='id')

# File input teks untuk menentukan gambar
file_text = 'textinputuser.txt'

# Template hasil deteksi
template_output = {
    'fotodepan.jpg': "di depan anda terdapat {objects}",
    'fotobelakang.jpg': "di belakang anda terdapat {objects}",
    'fotokiri.jpg': "di kiri anda terdapat {objects}",
    'fotokanan.jpg': "di kanan anda terdapat {objects}"
}

output_file = 'virtualassistantobject.txt'

# Inisialisasi client dengan API key Anda untuk Eleven Labs
client = ElevenLabs(api_key="sk_6649bb52fefe8202b9b92184644ca703dd591d7191295931")

def play_warning_sound(warning_text):
    try:
        # Mengonversi teks menjadi suara
        response = client.text_to_speech.convert(
            voice_id="21m00Tcm4TlvDq8ikWAM",  # Ganti dengan ID suara yang diinginkan
            model_id="eleven_multilingual_v2",  # Model yang mendukung bahasa multibahasa
            text=warning_text
        )

        # Mengambil semua data dari generator response
        audio_data = b''.join(response)  # Gabungkan semua bagian generator menjadi bytes

        # Menyimpan audio dalam file MP3
        with open("outputvirtualassistant.mp3", "wb") as audio_file:
            audio_file.write(audio_data)  # Menulis data audio ke dalam file MP3
        print("Konversi berhasil! Suara disimpan di 'outputvirtualassistant.mp3'.")

        # Memutar suara secara otomatis menggunakan pygame
        pygame.mixer.init()  # Initialize the mixer module
        pygame.mixer.music.load("outputvirtualassistant.mp3")  # Load the mp3 file
        pygame.mixer.music.play()  # Play the audio

        # Menunggu sampai suara selesai diputar
        while pygame.mixer.music.get_busy():
            pygame.time.Clock().tick(10)

    except Exception as e:
        print(f"Gagal menyimpan atau memutar file: {e}")

# Membaca isi file untuk menentukan gambar yang diambil
if os.path.exists(file_text):
    with open(file_text, 'r') as file:
        perintah = file.read().strip().lower()

    # Tentukan perintah yang valid
    valid_commands = ['objek depan', 'objek kanan', 'objek belakang', 'objek kiri']

    if perintah not in valid_commands:
        warning_text = "Mohon untuk menggunakan kata kunci objek kanan, objek kiri, objek belakang, atau objek depan"
        play_warning_sound(warning_text)
        image_path = None
    else:
        # Menentukan nama file berdasarkan perintah yang dibaca
        if perintah == 'objek depan':
            image_path = 'fotodepan.jpg'
        elif perintah == 'objek kanan':
            image_path = 'fotokanan.jpg'
        elif perintah == 'objek belakang':
            image_path = 'fotobelakang.jpg'
        elif perintah == 'objek kiri':
            image_path = 'fotokiri.jpg'
else:
    print(f"File {file_text} tidak ditemukan.")
    image_path = None

# Proses deteksi jika image_path ditemukan
if image_path:
    print(f"Path foto yang diambil: {image_path}")

    # Membaca gambar
    image = cv2.imread(image_path)
    if image is None:
        print(f"Error: Tidak dapat membaca gambar dari path: {image_path}")
    else:
        # Konversi warna untuk deteksi
        image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

        # Melakukan prediksi menggunakan YOLO
        results = model.predict(source=image, save=False, conf=0.25)

        # Ekstrak hasil deteksi
        detected_objects = [results[0].names[int(cls)] for cls in results[0].boxes.cls]

        # Terjemahkan nama objek secara dinamis
        translated_objects = []
        for obj in detected_objects:
            try:
                translated = translator.translate(obj)
                translated_objects.append(translated)
            except Exception as e:
                print(f"Error dalam menerjemahkan '{obj}': {e}")
                translated_objects.append(obj)  # Gunakan nama asli jika terjadi kesalahan

        # Hitung jumlah setiap objek
        object_counts = Counter(translated_objects)

        # Format output berdasarkan jumlah
        formatted_objects = ", ".join(
            f"{count} {obj}" for obj, count in object_counts.items()
        )
        objects_text = formatted_objects if formatted_objects else "tidak ada objek terdeteksi"

        # Membuat output teks berdasarkan template
        output_text = template_output.get(image_path, "").format(objects=objects_text)
        print(output_text)

        # Menyimpan ke file
        with open(output_file, 'w') as file:
            file.write(output_text)

        print(f"Hasil deteksi disimpan di {output_file}")

        # Menampilkan hasil deteksi
        # annotated_image = results[0].plot()  # Plot hasil deteksi
        # plt.imshow(annotated_image)
        # plt.axis('off')
        # plt.show()
else:
    print("Tidak ada gambar yang diambil.")


try:
    result = subprocess.run(
        ["python3.11", "/Users/nabilamutiara/Downloads/sightnerfinal2/outputvirtualassistantobject.py"], 
        check=True,
        capture_output=True,  # Menangkap output dari proses
        text=True  # Mengambil output dalam format teks
    )
except subprocess.CalledProcessError as e:
    print(f"Gagal menjalankan file deteksiobjek.py: {e}")
    print(f"Error output: {e.stderr}")
    print(f"Return Code: {e.returncode}")
