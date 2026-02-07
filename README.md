# Convertidor de audio a texto

Una aplicación moderna y profesional para convertir archivos de audio a texto utilizando reconocimiento de voz mediante Google Speech Recognition API.

## 📋 Características principales

### Conversión de audio
- ✅ Soporte para archivos **MP3** y **WAV**
- ✅ Reconocimiento de voz automático
- ✅ Barra de progreso en tiempo real
- ✅ Cancelación de conversión en curso
- ✅ Interfaz amigable y responsiva

### Soporte multiidioma
- 🌍 8 idiomas soportados:
  - Español (es-ES)
  - Inglés (en-US)
  - Francés (fr-FR)
  - Alemán (de-DE)
  - Italiano (it-IT)
  - Portugués (pt-BR)
  - Japonés (ja-JP)
  - Chino Simplificado (zh-CN)
- ⚙️ Selector de idioma antes de convertir
- 💾 Configuración persistente

### Edición de texto
- ✏️ Modo edición activable/desactivable
- 🔍 Búsqueda y reemplazo de texto (Ctrl+H)
- 📊 Contador de palabras y caracteres
- 📋 Copiar al portapapeles (Ctrl+C)
- ↩️ Deshacer/Rehacer

### Exportación de archivos
- 📄 **Texto plano (.txt)**
- 📕 **Documento Word (.docx)**
- 📑 **PDF (.pdf)**
- 🔤 **Markdown (.md)**

### Historial de conversiones
- 📜 Guarda las últimas 20 conversiones
- 🔄 Restaurar conversiones previas
- 📊 Información detallada (fecha, archivo, vista previa, cantidad de palabras)
- 🗑️ Limpiar historial completo

### Información de conversión
- ⏱️ Duración del archivo de audio
- 📝 Cantidad de palabras extraídas
- 🔤 Cantidad de caracteres
- 🎯 Idioma detectado
- 📈 Confianza del reconocimiento
- ⚡ Tiempo de procesamiento

### Interfaz de usuario
- 🎨 Tema oscuro profesional
- 📱 Interfaz maximizada por defecto
- 🖱️ Soporte para Drag & Drop (arrastra archivos)
- ⌨️ Atajos de teclado
- 📋 Menú completo y intuitivo
- 🖼️ Icono personalizado

### Atajos de teclado
| Atajo | Función |
|-------|---------|
| Ctrl+O | Abrir audio |
| Ctrl+S | Guardar texto |
| Ctrl+C | Copiar texto |
| Ctrl+H | Buscar y reemplazar |
| Ctrl+Q | Salir |

## 🚀 Requisitos del sistema

- Python 3.10 o superior
- Windows, macOS o Linux
- Conexión a Internet (para reconocimiento de voz)
- Micrófono (opcional, para grabar audio en tiempo real)

## 📦 Dependencias

```
SpeechRecognition=3.14.0
moviepy=2.1.2
PyQt6=6.8.0
python-docx=0.8.11
reportlab=4.0.9
markdown=3.5.1
```

## 🔧 Instalación

### 1. Clonar o descargar el repositorio
```bash
git clone https://github.com/tu-usuario/ConvertidorAudio-Texto.git
cd ConvertidorAudio-Texto
```

### 2. Crear un entorno virtual (recomendado)
```bash
python -m venv venv
```

### 3. Activar el entorno virtual
**En Windows:**
```bash
venv\Scripts\activate
```

**En macOS/Linux:**
```bash
source venv/bin/activate
```

### 4. Instalar dependencias
```bash
pip install -r requirements.txt
```

## ▶️ Uso

### Iniciar la aplicación
```bash
python gui.py
```

### Convertir un archivo de audio
1. Haz clic en **"Cargar audio"** o arrastra un archivo a la ventana
2. Selecciona el idioma en el menú desplegable
3. Haz clic en **"Convertir"**
4. Espera a que se complete la conversión
5. El texto aparecerá en el área de texto

### Guardar el texto convertido
1. Haz clic en **"Guardar"** o usa Ctrl+S
2. Selecciona el formato y ubicación
3. El archivo se guardará en la ubicación especificada

### Usar el historial
1. Ve a **Ver → Historial de conversiones**
2. Selecciona una conversión anterior
3. Haz clic en **"Restaurar"** para cargar el texto

## 📁 Estructura del Proyecto

```
ConvertidorAudio-Texto/
│
├── gui.py                 # Interfaz gráfica principal
├── converter.py           # Lógica de conversión de audio
├── styles.py              # Estilos CSS/PyQt6
├── config.py              # Gestión de configuración
├── history.py             # Gestión del historial
├── requirements.txt       # Dependencias del proyecto
├── setup.py              # Script de instalación
├── README.md             # Este archivo
├── CHANGELOG.md          # Historial de versiones
├── favicon.ico           # Icono de la aplicación
└── config.json           # Configuración persistente (creado en ejecución)
```

## ⚙️ Configuración

La configuración se guarda automáticamente en `config.json`:

```json
{
  "language": "es-ES",
  "max_duration": 300,
  "auto_save": true,
  "window_geometry": null,
  "last_path": "C:\\Users\\Usuario\\Documents"
}
```

### Cambiar la configuración
1. Ve a **Herramientas → Configuración**
2. Modifica los parámetros deseados
3. Haz clic en **"Guardar"**

## 🐛 Solución de Problemas

### Error: "No se pudo reconocer el audio"
- Comprueba que la conexión a Internet esté activa
- Verifica que el audio sea claro y en el idioma configurado
- Intenta con otro archivo de audio

### Error: "No se puede cargar el archivo"
- Asegúrate de que el archivo es MP3 o WAV
- Verifica que el archivo no está corrupto
- Intenta renombrar el archivo sin caracteres especiales

### Error: Módulos no encontrados
```bash
pip install --upgrade -r requirements.txt
```

### La aplicación se ejecuta lentamente
- Cierra otras aplicaciones
- Intenta con un archivo de audio más pequeño
- Comprueba la velocidad de Internet

## 📝 Menciones Especiales

- **Google Speech Recognition**: Utilizado para el reconocimiento de voz
- **PyQt6**: Framework para la interfaz gráfica
- **MoviePy**: Para conversión de formatos de audio

## 📄 Licencia

Este proyecto está bajo la licencia MIT. Ver el archivo `LICENSE` para más detalles.

## 👤 Autor

Desarrollado por tu nombre/equipo

## 🤝 Contribuciones

Las contribuciones son bienvenidas. Por favor:
1. Fork el proyecto
2. Crea una rama para tu feature
3. Commit tus cambios
4. Push a la rama
5. Abre un Pull Request

## 📞 Soporte

Para reportar bugs o solicitar features, abre un issue en GitHub.


---

**Versión Actual**: 2.0
**Última Actualización**: Febrero 2026
