import speech_recognition as sr
from moviepy import AudioFileClip
import tempfile
import os
from pathlib import Path
from PyQt6.QtCore import QThread, pyqtSignal
from PyQt6.QtWidgets import QMessageBox
import time
import sys

class AudioConverterThread(QThread):
    progress = pyqtSignal(int)
    status = pyqtSignal(str)
    finished = pyqtSignal(dict)  # Cambiar a dict para pasar más información
    error = pyqtSignal(str)

    def __init__(self, audio_file, recognizer, language='es-ES', temp_dir="temp"):
            super().__init__()
            self.audio_file = audio_file
            self.recognizer = recognizer
            self.is_cancelled = False
            self.temp_dir = temp_dir
            self.language = language
            self.start_time = None

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
            self.start_time = time.time()
            self.status.emit("Iniciando conversión...")
            self.progress.emit(0)

            # Obtener la duración del archivo de audio
            audio_duration = 0
            try:
                audio_clip = AudioFileClip(self.audio_file)
                audio_duration = audio_clip.duration
                audio_clip.close()
            except:
                audio_duration = 0

            # Obtener el directorio base del ejecutable o del script
            if getattr(sys, 'frozen', False):
                base_path = sys._MEIPASS  # Ruta temporal cuando es ejecutable
            else:
                base_path = os.path.abspath(".")

            # Crear carpeta temporal manualmente (junto al ejecutable)
            temp_dir = os.path.join(base_path, 'temp_audio')
            if not os.path.exists(temp_dir):
                os.makedirs(temp_dir)

            # Ruta del archivo WAV temporal
            temp_wav = os.path.join(temp_dir, 'temp.wav')

            # Convertir archivo comprimido a WAV si es necesario
            audio_path = self.audio_file
            if self.audio_file.lower().endswith(('.mp3', '.m4a')):
                try:
                    file_format = self.audio_file.lower().split('.')[-1].upper()
                    self.status.emit(f"Convirtiendo {file_format} a WAV...")

                    # Asegurar la conversión
                    if self.convert_mp3_to_wav(self.audio_file, temp_wav):
                        audio_path = temp_wav
                        self.status.emit(f"Conversión {file_format} a WAV completada")
                    else:
                        self.error.emit(f"Error en la conversión de {file_format} a WAV")
                        return
                except Exception as e:
                    self.error.emit(f"Error al convertir archivo: {str(e)}")
                    return
            else:
                self.progress.emit(30)
                self.status.emit("Archivo WAV detectado, procesando...")

            # Verificar que el archivo de audio existe antes de procesarlo
            if not os.path.exists(audio_path):
                self.error.emit("El archivo de audio no existe o no es válido.")
                return

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
                    text = self.recognizer.recognize_google(audio, language=self.language)
                    self.progress.emit(90)

                    if text:
                        self.status.emit("Transcripción completada")
                        self.progress.emit(100)
                        
                        # Calcular tiempo de procesamiento
                        processing_time = time.time() - self.start_time
                        
                        # Enviar resultado como diccionario con metadatos
                        result = {
                            'text': text,
                            'duration': audio_duration,
                            'language': self.language,
                            'confidence': 0.95,  # Google Speech Recognition no devuelve confianza
                            'processing_time': processing_time,
                            'word_count': len(text.split())
                        }
                        self.finished.emit(result)
                    else:
                        self.status.emit("No se pudo extraer texto")
                        result = {
                            'text': 'No se pudo extraer texto del audio',
                            'duration': audio_duration,
                            'language': self.language,
                            'confidence': 0,
                            'processing_time': time.time() - self.start_time,
                            'word_count': 0
                        }
                        self.finished.emit(result)

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
            # Limpieza manual del archivo temporal
            if os.path.exists(temp_wav):
                os.remove(temp_wav)
            if os.path.exists(temp_dir):
                os.rmdir(temp_dir)
            self.cleanup()

    def cleanup(self):
        try:
            QThread.msleep(100)

            # Eliminar archivos temporales
            for file in Path(self.temp_dir).glob('*'):
                try:
                    if file.exists():
                        file.unlink(missing_ok=True)
                except Exception as e:
                    print(f"Error al eliminar archivo {file}: {e}")

            # Eliminar directorio temporal
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