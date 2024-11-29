#caramenjalankan main.py
#di bash, ketik : python3.11 /Users/nabilamutiara/Downloads/sightnerfinal2/main.py
import speech_recognition as sr
import aifc
import subprocess  # Import subprocess untuk menjalankan file lain

recognizer = sr.Recognizer()

def convert_speech_to_text():
    # Menggunakan mikrofon sebagai sumber input suara
    with sr.Microphone() as source:
        print("Silakan berbicara...")
        # Mengatur noise level
        recognizer.adjust_for_ambient_noise(source)
        # Merekam suara
        audio = recognizer.listen(source)
        
        try:
            # Menggunakan Google Web Speech API untuk mengonversi suara ke teks
            print("Mengenali suara...")
            text = recognizer.recognize_google(audio, language="id-ID")
            print("Teks yang dikenali:", text)
            
            # Menyimpan hasil teks ke file
            with open("textinputuser.txt", "w", encoding="utf-8") as file:
                file.write(text)
            print("Teks berhasil disimpan dalam 'textinputuser.txt'")
        
        except sr.UnknownValueError:
            print("Google Speech Recognition tidak dapat memahami suara")
        except sr.RequestError as e:
            print(f"Permintaan ke Google Speech API gagal; {e}")

# Memanggil fungsi untuk mulai mengenali suara
convert_speech_to_text()

# Menjalankan file 'inputfoto.py' setelah pengenalan suara selesai
try:
    subprocess.run(["python3.11", "/Users/nabilamutiara/Downloads/sightnerfinal2/inputfoto.py"], check=True)
    print("File inputfoto.py berhasil dijalankan.")
except subprocess.CalledProcessError as e:
    print(f"Gagal menjalankan file inputfoto.py: {e}")
