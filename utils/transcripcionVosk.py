import os
import json
import queue
import sounddevice as sd
import wave
import pyaudio
from vosk import Model, KaldiRecognizer
from PyQt5.QtCore import QThread, pyqtSignal

class HiloTranscripcion(QThread):
    # Señales para comunicarse con la interfaz gráfica
    texto_signal = pyqtSignal(str) 
    error_signal = pyqtSignal(str)
    parcial_signal = pyqtSignal(str)

    def __init__(self, ruta_modelo, archivo_salida=None):
        super().__init__()
        self.ruta_modelo = ruta_modelo
        self.archivo_salida = archivo_salida
        self.corriendo = False       

    def run(self):
        # existencia del modelo
        if not os.path.exists(self.ruta_modelo):
            self.error_signal.emit(f"Error: No se encuentra el modelo en {self.ruta_modelo}")
            return
        
        wf = None
        p = None
        stream = None

        try:
            # modelo Vosk
            modelo = Model(self.ruta_modelo)
            reconocedor = KaldiRecognizer(modelo, 16000)

            p = pyaudio.PyAudio()
            stream = p.open(format=pyaudio.paInt16, 
                channels=1, 
                rate=16000, 
                input=True, 
                frames_per_buffer=8000)            

            #Archivo salida            
            if self.archivo_salida:
                try:
                    wf = wave.open(self.archivo_salida, "wb")
                    wf.setnchannels(1)
                    wf.setsampwidth(p.get_sample_size(pyaudio.paInt16))
                    wf.setframerate(16000)
                except Exception as e:
                    self.error_signal.emit(f"Error creando archivo de audio: {e}")
                    return

            self.corriendo = True

            while self.corriendo:
                data = stream.read(4000, exception_on_overflow=False)

                if len(data) == 0:
                    break

                # guardar audio si hay archivo
                if wf:
                    wf.writeframes(data)  

                # Procesar con vosk
                if reconocedor.AcceptWaveform(data):
                    resultado = json.loads(reconocedor.Result())
                    texto = resultado.get("text", "")
                    if texto:
                        self.texto_signal.emit(texto)
                else:
                    #Frase en construcción
                    parcial = json.loads(reconocedor.PartialResult())
                    texto_parcial = parcial.get("partial", "")
                    if texto_parcial:
                        self.parcial_signal.emit(texto_parcial)

        except Exception as e:
            self.error_signal.emit(f"Error crítico en el hilo: {str(e)}")

        finally:
            #Limpieza
            self.corriendo = False
            if wf:         
                wf.close()
            if stream:
                stream.stop_stream()    
                stream.close()
            if p:
                p.terminate()
    def detener(self):
        """Método seguro para detener el hilo"""
        self.corriendo = False
        self.wait()