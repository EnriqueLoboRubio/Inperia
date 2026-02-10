import sounddevice as sd
import keyboard
import queue
import json
from vosk import Model, KaldiRecognizer

#Cola que captura el audio
cola = queue.Queue()

#Texto completo
texto_completo = ""

def callback(indata, frames, time, status):
    cola.put(bytes(indata))

#Cargar modelo de Vosk
modelo = Model("vosk-es/small2")
grabar = KaldiRecognizer(modelo, 16000)

#Configuración del microfono
with sd.RawInputStream(samplerate=16000, 
                       blocksize=8000, 
                       dtype='int16',
                       channels=1, 
                       callback=callback):
    print("🎙️ Hablando... (Pulsa ESPACIO para finalizar)")
    while True:

        if keyboard.is_pressed('space'):
            print("\n🛑 Grabación finalizada.")
            break

        datos = cola.get()
        if grabar.AcceptWaveform(datos):
            resultado = json.loads(grabar.Result())
            texto = resultado.get("text", "")
            if texto:
                texto_completo += texto + " "
                print("👉", texto)
           
# Mostrar todo el texto final
print("\n📝 Texto completo transcrito:")
print(texto_completo)