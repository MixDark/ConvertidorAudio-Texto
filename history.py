"""
Módulo para gestionar el historial de conversiones
"""
import json
from pathlib import Path
from datetime import datetime
from typing import List, Dict

class ConversionHistory:
    """Gestiona el historial de conversiones"""
    
    def __init__(self, history_file: str = "history.json"):
        self.history_file = Path(history_file)
        self.conversions = self.load_history()
    
    def load_history(self) -> List[Dict]:
        """Carga el historial desde el archivo JSON"""
        try:
            if self.history_file.exists():
                with open(self.history_file, 'r', encoding='utf-8') as f:
                    return json.load(f)
        except Exception as e:
            print(f"Error al cargar historial: {e}")
        return []
    
    def save_history(self):
        """Guarda el historial en el archivo JSON"""
        try:
            with open(self.history_file, 'w', encoding='utf-8') as f:
                json.dump(self.conversions, f, ensure_ascii=False, indent=2)
        except Exception as e:
            print(f"Error al guardar historial: {e}")
    
    def add_conversion(self, filename: str, text: str, duration: float = 0, 
                      language: str = "es-ES", confidence: float = 0):
        """Agrega una nueva conversión al historial"""
        conversion = {
            'timestamp': datetime.now().isoformat(),
            'filename': Path(filename).name,
            'text_preview': text[:100] + '...' if len(text) > 100 else text,
            'full_text': text,
            'duration': duration,
            'language': language,
            'confidence': confidence
        }
        
        # Mantener solo las últimas 20 conversiones
        self.conversions.insert(0, conversion)
        if len(self.conversions) > 20:
            self.conversions = self.conversions[:20]
        
        self.save_history()
    
    def get_history(self) -> List[Dict]:
        """Retorna el historial completo"""
        return self.conversions
    
    def clear_history(self):
        """Limpia todo el historial"""
        self.conversions = []
        self.save_history()
    
    def get_conversion_by_index(self, index: int) -> Dict:
        """Obtiene una conversión específica por índice"""
        if 0 <= index < len(self.conversions):
            return self.conversions[index]
        return None
