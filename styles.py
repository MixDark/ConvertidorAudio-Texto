"""
Módulo de estilos para la aplicación de Convertidor de Audio a Texto
Contiene todas las hojas de estilo CSS para PyQt6
"""

class StyleSheet:
    """Clase para manejar los estilos CSS de la aplicación"""
    
    @staticmethod
    def get_styles():
        """Retorna los estilos principales de la aplicación"""
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
        
        QComboBox {
            background-color: #2a2a2a;
            color: white;
            border: 1px solid #3d3d3d;
            border-radius: 4px;
            padding: 5px;
        }
        
        QComboBox::drop-down {
            subcontrol-origin: padding;
            subcontrol-position: top right;
            width: 15px;
            border: none;
        }
        
        QComboBox QAbstractItemView {
            background-color: #2a2a2a;
            color: white;
            selection-background-color: #2d5c8f;
        }
        
        QSpinBox, QDoubleSpinBox {
            background-color: #2a2a2a;
            color: white;
            border: 1px solid #3d3d3d;
            border-radius: 4px;
            padding: 5px;
        }
        
        QCheckBox {
            color: white;
            spacing: 5px;
        }
        
        QCheckBox::indicator {
            width: 18px;
            height: 18px;
        }
        
        QCheckBox::indicator:unchecked {
            background-color: #2a2a2a;
            border: 1px solid #3d3d3d;
            border-radius: 3px;
        }
        
        QCheckBox::indicator:checked {
            background-color: #2d5c8f;
            border: 1px solid #2d5c8f;
            border-radius: 3px;
        }
        
        QMenuBar {
            background-color: #252525;
            color: white;
            border-bottom: 1px solid #3d3d3d;
            padding: 5px;
        }
        
        QMenuBar::item:selected {
            background-color: #2d5c8f;
            border-radius: 4px;
        }
        
        QMenu {
            background-color: #252525;
            color: white;
            border: 1px solid #3d3d3d;
            border-radius: 4px;
        }
        
        QMenu::item:selected {
            background-color: #2d5c8f;
            padding: 5px;
        }
        
        QMenu::separator {
            background-color: #3d3d3d;
            height: 1px;
        }
        
        QTableWidget {
            background-color: #2a2a2a;
            color: white;
            border: 1px solid #3d3d3d;
            gridline-color: #3d3d3d;
        }
        
        QTableWidget::item {
            padding: 5px;
            border-bottom: 1px solid #3d3d3d;
        }
        
        QTableWidget::item:selected {
            background-color: #2d5c8f;
        }
        
        QHeaderView::section {
            background-color: #1f4d80;
            color: white;
            padding: 5px;
            border: none;
        }
        
        QScrollBar:vertical {
            background-color: #2a2a2a;
            width: 12px;
            border: none;
        }
        
        QScrollBar::handle:vertical {
            background-color: #3d3d3d;
            border-radius: 6px;
            min-height: 20px;
        }
        
        QScrollBar::handle:vertical:hover {
            background-color: #4d4d4d;
        }
        
        QScrollBar:horizontal {
            background-color: #2a2a2a;
            height: 12px;
            border: none;
        }
        
        QScrollBar::handle:horizontal {
            background-color: #3d3d3d;
            border-radius: 6px;
            min-width: 20px;
        }
        
        QScrollBar::handle:horizontal:hover {
            background-color: #4d4d4d;
        }
        
        QDialog {
            background-color: #1e1e1e;
            color: white;
        }
        
        QLineEdit {
            background-color: #2a2a2a;
            color: white;
            border: 1px solid #3d3d3d;
            border-radius: 4px;
            padding: 5px;
            selection-background-color: #2d5c8f;
        }
        """
    
    @staticmethod
    def get_button_container_style():
        """Retorna el estilo para contenedores de botones"""
        return """
            QWidget {
                background-color: rgba(45, 45, 45, 0.7);
                border-radius: 10px;
                padding: 10px;
            }
        """
    
    @staticmethod
    def get_text_container_style():
        """Retorna el estilo para contenedores de texto"""
        return """
            QWidget {
                background-color: rgba(45, 45, 45, 0.7);
                border-radius: 10px;
                padding: 10px;
            }
        """
    
    @staticmethod
    def get_error_box_style():
        """Retorna el estilo para cajas de error"""
        return """
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
        """
