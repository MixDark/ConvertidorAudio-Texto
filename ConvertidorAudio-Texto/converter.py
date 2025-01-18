import speech_recognition as sr
from moviepy import AudioFileClip
import tempfile
import os
from pathlib import Path
from PyQt6.QtCore import QThread, pyqtSignal
from PyQt6.QtWidgets import QMessageBox
import time

class AudioConverterThread(QThread):
    progress = pyqtSignal(int)
    status = pyqtSignal(str)
    finished = pyqtSignal(list)
    error = pyqtSignal(str)

    def __init__(self, audio_file, recognizer):
        super().__init__()
        self.audio_file = audio_file
        self.recognizer = recognizer
        self.is_cancelled = False
        self.temp_dir = tempfile.mkdtemp()

    def convert_mp3_to_wav(self, input_path, output_path):
        """Método separado para manejar la conversión de MP3 a WAV"""
        try:
            self.progress.emit(10)
            audio_clip = AudioFileClip(input_path)
            self.progress.emit(20)
            # Usar la forma más básica del método write_audiofile
            audio_clip.write_audiofile(output_path)
            self.progress.emit(30)
            audio_clip.close()
            return True
        except Exception as e:
            self.error.emit(f"Error en la conversión: {str(e)}")
            return False

    def run(self):
        try:
            self.status.emit("Iniciando conversión...")
            self.progress.emit(0)
            
            # Convertir audio a WAV si es necesario
            audio_path = self.audio_file
            if self.audio_file.lower().endswith('.mp3'):
                try:
                    self.status.emit("Convirtiendo MP3 a WAV...")
                    temp_wav = os.path.join(self.temp_dir, 'temp.wav')
                    if self.convert_mp3_to_wav(self.audio_file, temp_wav):
                        audio_path = temp_wav
                        self.status.emit("Conversión MP3 a WAV completada")
                    else:
                        return
                except Exception as e:
                    self.error.emit(f"Error al convertir MP3: {str(e)}")
                    return
            else:
                self.progress.emit(30)
                self.status.emit("Archivo WAV detectado, procesando...")

            # Procesar el audio
            self.status.emit("Procesando audio...")
            self.progress.emit(40)
            
            try:
                with sr.AudioFile(audio_path) as source:
                    self.status.emit("Leyendo archivo de audio...")
                    self.progress.emit(50)
                    audio = self.recognizer.record(source)
                    
                    self.status.emit("Transcribiendo audio...")
                    self.progress.emit(70)
                    
                    # Dividir la transcripción en pasos para mostrar progreso
                    self.status.emit("Iniciando transcripción con Google...")
                    text = self.recognizer.recognize_google(audio, language='es-ES')
                    self.progress.emit(90)
                    
                    if text:
                        self.status.emit("Transcripción completada")
                        self.progress.emit(100)
                        self.finished.emit([text])
                    else:
                        self.status.emit("No se pudo extraer texto")
                        self.finished.emit(["No se pudo extraer texto del audio"])

            except sr.UnknownValueError:
                self.error.emit("No se pudo reconocer el audio")
                self.progress.emit(0)
            except sr.RequestError as e:
                self.error.emit(f"Error en el servicio de reconocimiento: {str(e)}")
                self.progress.emit(0)
            except Exception as e:
                self.error.emit(f"Error durante la transcripción: {str(e)}")
                self.progress.emit(0)

        except Exception as e:
            self.error.emit(f"Error durante la conversión: {str(e)}")
            self.progress.emit(0)
        finally:
            self.cleanup()

    def cleanup(self):
        try:
            QThread.msleep(100)
            
            for file in Path(self.temp_dir).glob('*'):
                try:
                    if file.exists():
                        file.unlink(missing_ok=True)
                except Exception as e:
                    print(f"Error al eliminar archivo {file}: {e}")

            try:
                if Path(self.temp_dir).exists():
                    os.rmdir(self.temp_dir)
            except Exception as e:
                print(f"Error al eliminar directorio temporal: {e}")

        except Exception as e:
            print(f"Error en cleanup: {e}")

    def cancel(self):
        self.is_cancelled = True
        self.progress.emit(0)
        self.status.emit("Conversión cancelada")