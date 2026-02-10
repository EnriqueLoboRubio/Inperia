import os
import json
import queue
import sounddevice as sd
import numpy as np
from faster_whisper import WhisperModel
from PyQt5.QtCore import QThread, pyqtSignal

class HiloTranscripcion(QThread):
    # Señales para comunicarse con la interfaz gráfica
    texto_signal = pyqtSignal(str) 
    error_signal = pyqtSignal(str)

    def __init__(self):
        super().__init__()
        self.modelo = WhisperModel(
            "utils/whisper-small",
            device="cpu",
            compute_type="int8" 
        )
        self.corriendo = False
        self.cola = queue.Queue()

    def run(self):
        self.corriendo = True

        try:
            with sd.InputStream(
                samplerate=16000,
                channels=1,
                dtype="float32",
                callback=self.callback
            ):
                buffer = []

                while self.running:
                    data = self.audio_queue.get()
                    buffer.extend(data)

                    if len(buffer) > 16000 * 3:  # 3 segundos
                        audio_np = np.array(buffer, dtype=np.float32)
                        buffer.clear()

                        segments, _ = self.model.transcribe(
                            audio_np,
                            language="es",
                            vad_filter=True
                        )

                        for segment in segments:
                            if segment.text.strip():
                                self.texto_signal.emit(segment.text)

        except Exception as e:
            self.error_signal.emit(str(e))

    def callback(self, indata, frames, time, status):
        if self.corriendo:
            self.cola.put(indata[:, 0].copy())

    def detener(self):
        self.corriendo = False
        self.wait()