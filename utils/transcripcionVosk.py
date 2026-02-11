import os
import json
import sounddevice as sd
import wave
import pyaudio
from vosk import Model, KaldiRecognizer
from PyQt5.QtCore import QThread, pyqtSignal

class HiloTranscripcion(QThread):

    texto_signal = pyqtSignal(str)
    error_signal = pyqtSignal(str)
    parcial_signal = pyqtSignal(str)

    def __init__(self, ruta_modelo, archivo_salida=None):
        super().__init__()
        self.ruta_modelo = ruta_modelo
        self.archivo_salida = archivo_salida
        self.corriendo = False
        self.stream = None
        self.p = None
        self.wf = None

    def run(self):

        if not os.path.exists(self.ruta_modelo):
            self.error_signal.emit(f"No se encuentra el modelo en {self.ruta_modelo}")
            return

        try:
            modelo = Model(self.ruta_modelo)
            self.reconocedor = KaldiRecognizer(modelo, 16000)

            self.p = pyaudio.PyAudio()

            if self.archivo_salida:
                self.wf = wave.open(self.archivo_salida, "wb")
                self.wf.setnchannels(1)
                self.wf.setsampwidth(self.p.get_sample_size(pyaudio.paInt16))
                self.wf.setframerate(16000)

            self.corriendo = True

            def callback(in_data, frame_count, time_info, status):

                if not self.corriendo:
                    return (None, pyaudio.paComplete)

                if self.wf:
                    self.wf.writeframes(in_data)

                if self.reconocedor.AcceptWaveform(in_data):
                    resultado = json.loads(self.reconocedor.Result())
                    texto = resultado.get("text", "")
                    if texto:
                        self.texto_signal.emit(texto)
                else:
                    parcial = json.loads(self.reconocedor.PartialResult())
                    texto_parcial = parcial.get("partial", "")
                    if texto_parcial:
                        self.parcial_signal.emit(texto_parcial)

                return (None, pyaudio.paContinue)

            self.stream = self.p.open(
                format=pyaudio.paInt16,
                channels=1,
                rate=16000,
                input=True,
                frames_per_buffer=4000,
                stream_callback=callback
            )

            self.stream.start_stream()

            while self.stream.is_active():
                self.msleep(100)

        except Exception as e:
            self.error_signal.emit(f"Error crítico: {str(e)}")

        finally:
            self.limpiar()

    def detener(self):
        self.corriendo = False

    def limpiar(self):

        if self.stream:
            self.stream.stop_stream()
            self.stream.close()

        if self.wf:
            self.wf.close()

        if self.p:
            self.p.terminate()
