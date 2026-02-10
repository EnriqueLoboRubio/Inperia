import os
import json
import queue
import sounddevice as sd
from vosk import Model, KaldiRecognizer
from PyQt5.QtCore import QThread, pyqtSignal

class HiloTranscripcion(QThread):
    # Señales para comunicarse con la interfaz gráfica
    texto_transcrito_signal = pyqtSignal(str) 
    error_signal = pyqtSignal(str)

    def __init__(self, ruta_modelo):
        super().__init__()
        self.ruta_modelo = ruta_modelo
        self.corriendo = False
        self.cola = queue.Queue()

    def run(self):
        # existencia del modelo
        if not os.path.exists(self.ruta_modelo):
            self.error_signal.emit(f"Error: No se encuentra el modelo en {self.ruta_modelo}")
            return

        try:
            # modelo Vosk
            modelo = Model(self.ruta_modelo)
            reconocedor = KaldiRecognizer(modelo, 16000)
            
            # Iniciar micrófono
            self.corriendo = True
            with sd.RawInputStream(samplerate=16000, 
                                   blocksize=8000, 
                                   dtype='int16',
                                   channels=1, 
                                   callback=self.callback):
                
                self.ultimo_parcial = ""
                
                while self.corriendo:
                    try:
                        # Sacar datos de la cola
                        data = self.cola.get(timeout=0.5)
                        
                        if reconocedor.AcceptWaveform(data):
                            resultado = json.loads(reconocedor.Result())
                            texto = resultado.get("text", "")
                            if texto:
                                self.texto_transcrito_signal.emit(texto)
                        else:
                            parcial = json.loads(reconocedor.PartialResult())
                            texto_parcial = parcial.get("partial", "")
                            if texto_parcial and texto_parcial != self.ultimo_parcial:
                                self.ultimo_parcial = texto_parcial
                                self.texto_transcrito_signal.emit(texto_parcial)
      
                    except queue.Empty:
                        continue
                    except Exception as e:
                        self.error_signal.emit(str(e))
                        break

        except Exception as e:
            self.error_signal.emit(f"Error al iniciar micrófono o modelo: {str(e)}")

    def callback(self, indata, frames, time, status):
        """Función que llama sounddevice con audio crudo"""
        if self.corriendo:
            self.cola.put(bytes(indata))

    def detener(self):
        """Método seguro para detener el hilo"""
        self.corriendo = False
        self.wait()