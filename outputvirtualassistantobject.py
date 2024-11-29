import pygame
from elevenlabs import ElevenLabs

# Inisialisasi client dengan API key Anda
client = ElevenLabs(api_key="sk_c231ca6a49142d9380abba3d52bd5b0bf8b2079008989f52")

# Membaca teks dari file 'virtualassistantobject.txt'
with open('virtualassistantobject.txt', 'r') as file:
    text_to_convert = file.read().strip()

# Mengonversi teks menjadi suara
response = client.text_to_speech.convert(
    voice_id="21m00Tcm4TlvDq8ikWAM",  # Ganti dengan ID suara yang diinginkan
    model_id="eleven_multilingual_v2",  # Model yang mendukung bahasa multibahasa
    text=text_to_convert
)

# Menyimpan hasil suara ke file MP3 dan memutar suara secara otomatis
try:
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
