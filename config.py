"""
Módulo para gestionar la configuración de la aplicación
"""
import json
from pathlib import Path
from typing import Any

class AppConfig:
    """Gestiona la configuración de la aplicación"""
    
    DEFAULT_CONFIG = {
        'language': 'es-ES',
        'max_duration': 300,  # segundos
        'auto_save': True,
        'window_geometry': None,
        'last_path': str(Path.home()),
    }
    
    SUPPORTED_LANGUAGES = {
        'es-ES': 'Español',
        'en-US': 'Inglés',
        'fr-FR': 'Francés',
        'de-DE': 'Alemán',
        'it-IT': 'Italiano',
        'pt-BR': 'Portugués (Brasil)',
        'ja-JP': 'Japonés',
        'zh-CN': 'Chino Simplificado',
    }
    
    def __init__(self, config_file: str = "config.json"):
        self.config_file = Path(config_file)
        self.config = self.load_config()
    
    def load_config(self) -> dict:
        """Carga la configuración desde el archivo JSON"""
        try:
            if self.config_file.exists():
                with open(self.config_file, 'r', encoding='utf-8') as f:
                    config = json.load(f)
                    # Mezclar con valores por defecto
                    return {**self.DEFAULT_CONFIG, **config}
        except Exception as e:
            print(f"Error al cargar configuración: {e}")
        return self.DEFAULT_CONFIG.copy()
    
    def save_config(self):
        """Guarda la configuración en el archivo JSON"""
        try:
            with open(self.config_file, 'w', encoding='utf-8') as f:
                json.dump(self.config, f, ensure_ascii=False, indent=2)
        except Exception as e:
            print(f"Error al guardar configuración: {e}")
    
    def get(self, key: str, default: Any = None) -> Any:
        """Obtiene un valor de configuración"""
        return self.config.get(key, default)
    
    def set(self, key: str, value: Any):
        """Establece un valor de configuración"""
        self.config[key] = value
        self.save_config()
    
    def get_language(self) -> str:
        """Obtiene el idioma configurado"""
        return self.config.get('language', 'es-ES')
    
    def set_language(self, language: str):
        """Establece el idioma"""
        if language in self.SUPPORTED_LANGUAGES:
            self.config['language'] = language
            self.save_config()
    
    def get_max_duration(self) -> int:
        """Obtiene la duración máxima en segundos"""
        return self.config.get('max_duration', 300)
    
    def set_max_duration(self, duration: int):
        """Establece la duración máxima"""
        self.config['max_duration'] = max(60, duration)  # Mínimo 60 segundos
        self.save_config()
