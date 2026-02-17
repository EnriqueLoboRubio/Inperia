import os
import wave
import pyaudio
import whisper
import tempfile
import numpy as np
from PyQt5.QtCore import QThread, pyqtSignal

class HiloTranscripcion(QThread):
    """
    Hilo de transcripción usando Whisper (modelo mediano).
    Mantiene la misma interfaz que HiloTranscripcion de Vosk para facilitar la migración.
    """
    
    texto_signal = pyqtSignal(str)
    error_signal = pyqtSignal(str)
    parcial_signal = pyqtSignal(str)

    def __init__(self, modelo_nombre="medium", archivo_salida=None, idioma="es"):
        """
        Args:
            modelo_nombre: Tamaño del modelo Whisper ('tiny', 'base', 'small', 'medium', 'large')
            archivo_salida: Ruta donde guardar el audio grabado (opcional)
            idioma: Código del idioma para la transcripción (por defecto 'es' para español)
        """
        super().__init__()
        self.modelo_nombre = modelo_nombre
        self.archivo_salida = archivo_salida
        self.idioma = idioma
        self.corriendo = False
        self.stream = None
        self.p = None
        self.wf = None
        self.modelo = None
        self.frames = []
        
        # Configuración de audio
        self.RATE = 16000  # Whisper funciona bien con 16kHz
        self.CHUNK = 4000
        self.CHANNELS = 1
        self.FORMAT = pyaudio.paInt16
        
        # Configuración para transcripción parcial
        self.PARTIAL_DURATION = 3  # Segundos para transcripción parcial

    def run(self):
        """Ejecuta la grabación y transcripción en tiempo real"""
        try:
            # Cargar modelo Whisper
            self.texto_signal.emit(f"Cargando modelo Whisper {self.modelo_nombre}...")
            self.modelo = whisper.load_model(self.modelo_nombre)
            self.texto_signal.emit("Modelo cargado. Iniciando grabación...")
            
            self.p = pyaudio.PyAudio()

            # Configurar archivo de salida si se especifica
            if self.archivo_salida:
                try:
                    self.wf = wave.open(self.archivo_salida, "wb")
                    self.wf.setnchannels(self.CHANNELS)
                    self.wf.setsampwidth(self.p.get_sample_size(self.FORMAT))
                    self.wf.setframerate(self.RATE)
                except Exception as e:
                    self.error_signal.emit(f"Error al crear archivo de audio: {e}")
                    return

            self.corriendo = True
            self.frames = []

            def callback(in_data, frame_count, time_info, status):
                """Callback para capturar audio"""
                if not self.corriendo:
                    return (None, pyaudio.paComplete)

                # Guardar en archivo si se especifica
                if self.wf is not None:
                    try:
                        self.wf.writeframes(in_data)
                    except Exception:
                        pass

                # Almacenar frames para transcripción
                self.frames.append(in_data)
                
                # Transcripción parcial cada X segundos
                total_frames = len(self.frames)
                frames_por_segundo = self.RATE // self.CHUNK
                if total_frames > 0 and total_frames % (frames_por_segundo * self.PARTIAL_DURATION) == 0:
                    self.transcribir_parcial()

                return (None, pyaudio.paContinue)

            # Abrir stream de audio
            self.stream = self.p.open(
                format=self.FORMAT,
                channels=self.CHANNELS,
                rate=self.RATE,
                input=True,
                frames_per_buffer=self.CHUNK,
                stream_callback=callback
            )

            self.stream.start_stream()

            # Mantener el hilo activo mientras se graba
            while self.corriendo and self.stream.is_active():
                self.msleep(100)

            # Transcripción final
            if self.frames:
                self.transcribir_final()

        except Exception as e:
            self.error_signal.emit(f"Error crítico: {str(e)}")

        finally:
            self.limpiar()

    def transcribir_parcial(self):
        """Transcribe los últimos X segundos de audio para feedback parcial"""
        try:
            # Tomar solo los últimos frames (últimos segundos)
            frames_por_segundo = self.RATE // self.CHUNK
            frames_parciales = self.frames[-(frames_por_segundo * self.PARTIAL_DURATION):]
            
            if not frames_parciales:
                return
            
            # Convertir frames a numpy array
            audio_data = b''.join(frames_parciales)
            audio_np = np.frombuffer(audio_data, dtype=np.int16).astype(np.float32) / 32768.0
            
            # Transcribir con Whisper
            resultado = self.modelo.transcribe(
                audio_np,
                language=self.idioma,
                fp16=False,  # Usar False para compatibilidad con CPU
                verbose=False
            )
            
            texto_parcial = resultado.get("text", "").strip()
            if texto_parcial:
                self.parcial_signal.emit(texto_parcial)
                
        except Exception as e:
            # No emitir error para transcripciones parciales, solo continuar
            pass

    def transcribir_final(self):
        """Transcribe todo el audio grabado al finalizar"""
        try:
            # Guardar audio temporal para Whisper
            with tempfile.NamedTemporaryFile(suffix=".wav", delete=False) as temp_file:
                temp_path = temp_file.name
                
                # Escribir frames a archivo temporal
                with wave.open(temp_path, "wb") as wf_temp:
                    wf_temp.setnchannels(self.CHANNELS)
                    wf_temp.setsampwidth(self.p.get_sample_size(self.FORMAT))
                    wf_temp.setframerate(self.RATE)
                    wf_temp.writeframes(b''.join(self.frames))
            
            # Transcribir con Whisper
            resultado = self.modelo.transcribe(
                temp_path,
                language=self.idioma,
                fp16=False,
                verbose=False
            )
            
            texto_final = resultado.get("text", "").strip()
            if texto_final:
                self.texto_signal.emit(texto_final)
            
            # Limpiar archivo temporal
            try:
                os.unlink(temp_path)
            except:
                pass
                
        except Exception as e:
            self.error_signal.emit(f"Error en transcripción final: {str(e)}")

    def detener(self):
        """Detiene la grabación y transcripción"""
        self.corriendo = False

    def limpiar(self):
        """Libera recursos de audio"""
        if self.stream:
            try:
                if self.stream.is_active():
                    self.stream.stop_stream()
                self.stream.close()
            except Exception:
                pass
            self.stream = None

        if self.wf:
            try:
                self.wf.close()
            except Exception:
                pass
            self.wf = None

        if self.p:
            try:
                self.p.terminate()
            except Exception:
                pass
            self.p = None
