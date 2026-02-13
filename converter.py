
import speech_recognition as sr
from moviepy import AudioFileClip
import tempfile
import os
from pathlib import Path
from PyQt6.QtCore import QThread, pyqtSignal
from PyQt6.QtWidgets import QMessageBox
import time
import sys

from langdetect import detect, DetectorFactory
DetectorFactory.seed = 0


class AudioConverterThread(QThread):

    progress = pyqtSignal(int)
    status = pyqtSignal(str)
    finished = pyqtSignal(dict)  # Cambiar a dict para pasar más información
    error = pyqtSignal(str)

    def cleanup(self):
        """Método de limpieza (placeholder)."""
        pass

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
        temp_wav = None
        temp_dir = None
        detected_languages = set()
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


            # Transcripción con speech_recognition y detección de idioma con langdetect
            try:
                self.status.emit("Procesando audio...")
                self.progress.emit(40)
                with sr.AudioFile(audio_path) as source:
                    audio = self.recognizer.record(source)
                self.status.emit("Transcribiendo audio con Google...")
                self.progress.emit(60)
                # Transcripción precisa en todos los idiomas
                lang_code = self.language if self.language else 'es-ES'
                try:
                    self.status.emit(f"Transcribiendo audio en idioma seleccionado: {lang_code}...")
                    full_text = self.recognizer.recognize_google(audio, language=lang_code)
                except Exception as e:
                    self.error.emit(f"Error en la transcripción: {str(e)}")
                    return
                self.progress.emit(80)
                # Detección de idioma en el texto completo
                try:
                    lang = detect(full_text)
                    detected_languages.add(lang)
                except Exception:
                    detected_languages = set()
                # Si el idioma detectado es diferente al seleccionado, retranscribir en el detectado
                idioma_detectado = next(iter(detected_languages), None)
                idioma_google = self._langdetect_to_google_code(idioma_detectado)
                if idioma_google and idioma_google != lang_code:
                    try:
                        self.status.emit(f"Idioma detectado: {idioma_detectado}. Retranscribiendo en {idioma_google} para máxima precisión...")
                        full_text = self.recognizer.recognize_google(audio, language=idioma_google)
                        detected_languages = {idioma_detectado}
                    except Exception as e:
                        self.status.emit(f"No se pudo retranscribir en {idioma_google}: " + str(e))
                idiomas_detectados = ', '.join(sorted(detected_languages)) if detected_languages else 'desconocido'
                self.status.emit(f"Idioma detectado: {idiomas_detectados}")
                self.progress.emit(100)
                processing_time = time.time() - self.start_time
                result = {
                    'text': full_text,
                    'duration': audio_duration,
                    'language': idiomas_detectados,
                    'confidence': 1.0,
                    'processing_time': processing_time,
                    'word_count': len(full_text.split())
                }
                self.finished.emit(result)
            except Exception as e:
                self.error.emit(f"Error durante la conversión: {str(e)}")
                self.progress.emit(0)
        finally:
            # Limpieza manual del archivo temporal (fuera de los bloques try/except)
            if temp_wav and os.path.exists(temp_wav):
                os.remove(temp_wav)
            if temp_dir and os.path.exists(temp_dir):
                try:
                    os.rmdir(temp_dir)
                except Exception:
                    pass
            self.cleanup()

    def _langdetect_to_google_code(self, langdetect_code):
        """Convierte el código de langdetect a un código de idioma Google Speech Recognition"""
        mapping = {
            'es': 'es-ES',
            'en': 'en-US',
            'fr': 'fr-FR',
            'de': 'de-DE',
            'it': 'it-IT',
            'pt': 'pt-BR',
            'ja': 'ja-JP',
            'zh': 'zh-CN',
            'ru': 'ru-RU',
        }
        return mapping.get(langdetect_code)

    def cancel(self):
        self.is_cancelled = True
        self.progress.emit(0)
        self.status.emit("Conversión cancelada")