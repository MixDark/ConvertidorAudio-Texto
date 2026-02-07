from cx_Freeze import setup, Executable
import sys

# Dependencias de tu proyecto
build_exe_options = {
    "packages": ["os", "sys", "speech_recognition", "moviepy", "PyQt6", "time", "pathlib","traceback","tempfile"],  # Añade las que uses
    "includes": [],
    "include_files": ["favicon.ico","converter.py"],  # Archivos adicionales (iconos, etc.)
    "excludes": [],
}

# Configuración de la aplicación
setup(
    name="ConvertidorAudioTexto",
    version="1.0",
    description="Aplicación para convertir audio a texto",
    options={"build_exe": build_exe_options},
    executables=[Executable(
        "gui.py",  # Archivo principal de tu GUI
        base="Win32GUI" if sys.platform == "win32" else None,  # GUI sin consola en Windows
        icon="favicon.ico"  # Icono del ejecutable
    )]
)
