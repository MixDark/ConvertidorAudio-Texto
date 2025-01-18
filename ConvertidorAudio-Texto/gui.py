import sys
import speech_recognition as sr
import traceback
from pathlib import Path
from PyQt6.QtWidgets import (QApplication, QMainWindow, QPushButton, 
                            QVBoxLayout, QWidget, QFileDialog, QTextEdit,
                            QProgressBar, QMessageBox, QHBoxLayout, QLabel,
                            QStatusBar, QFrame)
from PyQt6.QtCore import Qt, QSize
from PyQt6.QtGui import QFont, QIcon
import os
from converter import AudioConverterThread

class StyleSheet:
    """Clase para manejar los estilos CSS de la aplicación"""
    @staticmethod
    def get_styles():
        return """
        QMainWindow {
            background-color: #1e1e1e;
        }
        
        QWidget {
            background-color: rgba(30, 30, 30, 0.95);
            color: #ffffff;
        }
        
        QPushButton {
            padding: 8px 15px;
            border-radius: 6px;
            background-color: #2d5c8f;
            color: white;
            font-weight: bold;
            min-width: 120px;
            border: none;
        }
        
        QPushButton:hover {
            background-color: #366daa;
        }
        
        QPushButton:pressed {
            background-color: #1f4d80;
        }
        
        QPushButton:disabled {
            background-color: #4a4a4a;
            color: #8f8f8f;
        }
        
        QProgressBar {
            border: 2px solid #2d5c8f;
            border-radius: 5px;
            text-align: center;
            color: white;
            background-color: #2a2a2a;
        }
        
        QProgressBar::chunk {
            background-color: #2d5c8f;
            border-radius: 3px;
        }
        
        QTextEdit {
            background-color: rgba(30, 30, 30, 0.7);
            border: 2px solid #3d3d3d;
            border-radius: 6px;
            padding: 5px;
            color: #ffffff;
            selection-background-color: #2d5c8f;
            selection-color: white;
        }
        
        QLabel {
            color: #ffffff;
            background-color: transparent;
        }
        
        QStatusBar {
            background-color: #252525;
            color: #ffffff;
            border-top: 1px solid #3d3d3d;
        }
        
        QStatusBar::item {
            border: None;
        }
        
        QFrame#separator {
            background-color: #3d3d3d;
            max-height: 1px;
            margin: 10px 0px;
        }
        
        QMessageBox {
            background-color: #1e1e1e;
            color: white;
        }
        
        QMessageBox QPushButton {
            min-width: 80px;
            min-height: 24px;
        }
        
        QFileDialog {
            background-color: #1e1e1e;
            color: white;
        }
        
        QFileDialog QListView {
            background-color: #2a2a2a;
            color: white;
        }
        
        QFileDialog QTreeView {
            background-color: #2a2a2a;
            color: white;
        }
        """

class AudioConverterApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowOpacity(0.98)
        self.initUI()
        self.audio_file = None
        self.converter_thread = None
        
        try:
            # Inicializar el reconocedor
            self.recognizer = sr.Recognizer()
            self.status_bar.showMessage('Sistema inicializado correctamente')
        except Exception as e:
            QMessageBox.critical(self, "Error de inicialización", str(e))
            sys.exit(1)

    def initUI(self):
        self.setWindowTitle('Convertidor de audio a texto')
        self.setGeometry(100, 100, 1000, 700)
        self.setStyleSheet(StyleSheet.get_styles())
        self.center_window()
        self.setWindowIcon(QIcon("favicon.ico"))

        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        main_layout = QVBoxLayout(central_widget)
        main_layout.setSpacing(10)
        main_layout.setContentsMargins(20, 20, 20, 20)

        separator = QFrame()
        separator.setObjectName("separator")
        separator.setFrameShape(QFrame.Shape.HLine)
        separator.setFrameShadow(QFrame.Shadow.Sunken)
        main_layout.addWidget(separator)

        button_container = QWidget()
        button_container.setStyleSheet("""
            QWidget {
                background-color: rgba(45, 45, 45, 0.7);
                border-radius: 10px;
                padding: 10px;
            }
        """)
        button_layout = QHBoxLayout(button_container)
        button_layout.setSpacing(15)
        
        self.load_button = QPushButton('Cargar audio')
        self.convert_button = QPushButton('Convertir')
        self.save_button = QPushButton('Guardar')
        self.cancel_button = QPushButton('Cancelar')

        for button in [self.load_button, self.convert_button, 
                    self.save_button, self.cancel_button]:
            button.setMinimumSize(QSize(130, 45))
            button.setFont(QFont('Segoe UI', 10))
            button_layout.addWidget(button)

        self.convert_button.setEnabled(False)
        self.save_button.setEnabled(False)
        self.cancel_button.setEnabled(False)

        self.load_button.clicked.connect(self.load_audio)
        self.convert_button.clicked.connect(self.convert_audio)
        self.save_button.clicked.connect(self.save_text)
        self.cancel_button.clicked.connect(self.cancel_conversion)

        main_layout.addWidget(button_container)

        self.progress_bar = QProgressBar()
        self.progress_bar.setVisible(False)
        self.progress_bar.setMinimumHeight(20)
        self.progress_bar.setFont(QFont('Segoe UI', 9))
        main_layout.addWidget(self.progress_bar)

        text_container = QWidget()
        text_container.setStyleSheet("""
            QWidget {
                background-color: rgba(45, 45, 45, 0.7);
                border-radius: 10px;
                padding: 10px;
            }
        """)
        text_layout = QVBoxLayout(text_container)
        
        self.text_area = QTextEdit()
        self.text_area.setReadOnly(True)
        self.text_area.setMinimumHeight(400)
        self.text_area.setFont(QFont('Segoe UI', 11))
        text_layout.addWidget(self.text_area)
        
        main_layout.addWidget(text_container)

        self.status_bar = QStatusBar()
        self.status_bar.setFont(QFont('Segoe UI', 9))
        self.setStatusBar(self.status_bar)
        self.status_bar.showMessage('Listo')

    def center_window(self):
        """Centra la ventana en la pantalla actual"""
        # Obtener la geometría de la pantalla que contiene el cursor
        cursor_pos = QApplication.primaryScreen().geometry().center()
        available_geometry = QApplication.primaryScreen().availableGeometry()

        # Calcular el centro
        center_point = available_geometry.center()

        # Obtener el tamaño de la ventana
        frame_geometry = self.frameGeometry()
        frame_geometry.moveCenter(center_point)

        # Mover la ventana
        self.move(frame_geometry.topLeft())        
        
    def load_audio(self):
        try:
            file_name, _ = QFileDialog.getOpenFileName(
                self,
                "Seleccionar archivo de audio",
                str(Path.home()),
                "Audio Files (*.mp3 *.wav)"
            )

            if file_name:
                self.audio_file = file_name
                self.convert_button.setEnabled(True)
                self.text_area.setText(f"Archivo cargado: {Path(file_name).name}")
                self.status_bar.showMessage('Archivo cargado correctamente')
        except Exception as e:
            self.show_error("Error al cargar el archivo", str(e))

    def convert_audio(self):
        if not self.audio_file:
            return

        self.progress_bar.setVisible(True)
        self.progress_bar.setValue(0)
        self.update_ui_state(is_converting=True)

        # Iniciar el hilo de conversión con el recognizer en lugar del modelo
        self.converter_thread = AudioConverterThread(self.audio_file, self.recognizer)
        self.converter_thread.progress.connect(self.update_progress)
        self.converter_thread.status.connect(self.update_status)
        self.converter_thread.finished.connect(self.conversion_finished)
        self.converter_thread.error.connect(self.show_error)
        self.converter_thread.start()

    def update_ui_state(self, is_converting=False):
            """Actualiza el estado de los botones según el estado de la conversión"""
            self.convert_button.setEnabled(not is_converting)
            self.load_button.setEnabled(not is_converting)
            self.cancel_button.setEnabled(is_converting)
            # Corregir la evaluación del texto
            has_text = bool(self.text_area.toPlainText().strip())
            self.save_button.setEnabled(not is_converting and has_text)

    def conversion_finished(self, results):
        try:
            if results:
                text = '\n'.join(results)
                self.text_area.setText(text)
                self.status_bar.showMessage('Conversión completada exitosamente')
            else:
                self.text_area.setText("No se pudo extraer texto del audio")
                self.status_bar.showMessage('Conversión completada sin resultados')
            
            self.reset_ui()
            # Actualizar el estado del botón de guardar basado en si hay texto
            has_text = bool(self.text_area.toPlainText().strip())
            self.save_button.setEnabled(has_text)
            
        except Exception as e:
            self.show_error("Error al finalizar la conversión", str(e))

    def reset_ui(self):
        """Resetea la interfaz de usuario"""
        try:
            self.progress_bar.setVisible(False)
            self.progress_bar.setValue(0)
            self.convert_button.setEnabled(True)
            self.load_button.setEnabled(True)
            self.cancel_button.setEnabled(False)
            # Actualizar el estado del botón de guardar
            has_text = bool(self.text_area.toPlainText().strip())
            self.save_button.setEnabled(has_text)
        except Exception as e:
            self.show_error("Error al resetear la interfaz", str(e))

    def cancel_conversion(self):
        if self.converter_thread and self.converter_thread.isRunning():
            self.converter_thread.cancel()
            self.converter_thread.wait()
            self.reset_ui()
            self.text_area.setText("Conversión cancelada")
            self.status_bar.showMessage('Conversión cancelada')

    def update_progress(self, value):
        self.progress_bar.setValue(value)

    def update_status(self, message):
        self.status_bar.showMessage(message)


    def save_text(self):
        try:
            file_name, _ = QFileDialog.getSaveFileName(
                self,
                "Guardar texto",
                str(Path.home() / "texto_convertido.txt"),
                "Archivo de texto (*.txt);;Todos los archivos (*.*)"
            )

            if file_name:
                with open(file_name, 'w', encoding='utf-8') as f:
                    f.write(self.text_area.toPlainText())
                self.status_bar.showMessage('Archivo guardado correctamente')
                QMessageBox.information(self, "Éxito", 
                                      "El texto se ha guardado correctamente")
        except Exception as e:
            self.show_error("Error al guardar el archivo", str(e))

    def show_error(self, title, message=None):
        """
        Muestra un mensaje de error.
        Si solo se proporciona title, se usa como mensaje y se usa un título genérico.
        """
        if message is None:
            message = title
            title = "Error"

        error_box = QMessageBox(self)
        error_box.setStyleSheet("""
            QMessageBox {
                background-color: #1e1e1e;
                color: white;
            }
            QLabel {
                color: white;
            }
            QPushButton {
                min-width: 80px;
                min-height: 24px;
            }
        """)
        error_box.setIcon(QMessageBox.Icon.Critical)
        error_box.setWindowTitle(title)
        error_box.setText(message)
        error_box.exec()
        self.status_bar.showMessage(f'Error: {title}')

    def closeEvent(self, event):
        """Maneja el evento de cierre de la ventana"""
        if self.converter_thread and self.converter_thread.isRunning():
            reply = QMessageBox.question(
                self, 'Confirmar salida',
                '¿Está seguro de que desea salir? La conversión en curso se cancelará.',
                QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
                QMessageBox.StandardButton.No
            )

            if reply == QMessageBox.StandardButton.Yes:
                try:
                    self.converter_thread.cancel()
                    self.converter_thread.wait()
                except Exception as e:
                    print(f"Error al cancelar la conversión: {e}")
                finally:
                    event.accept()
            else:
                event.ignore()
        else:
            event.accept()

def main():
    app = QApplication(sys.argv)
    try:
        app_path = Path(__file__).parent
        os.chdir(str(app_path))
        
        try:
            # Verificar que podemos inicializar el reconocedor
            recognizer = sr.Recognizer()
            
        except Exception as e:
            QMessageBox.warning(
                None, 
                "Error de inicialización",
                f"Error al inicializar el sistema:\n{str(e)}\n\n"
                "Verifica que todas las dependencias están correctamente instaladas."
            )
            return

        ex = AudioConverterApp()
        ex.show()
        sys.exit(app.exec())
    except Exception as e:
        QMessageBox.critical(
            None, 
            "Error Fatal", 
            f"Error al iniciar la aplicación:\n{str(e)}\n\n"
            f"Detalles técnicos:\n{traceback.format_exc()}"
        )
        sys.exit(1)

if __name__ == '__main__':
    main()