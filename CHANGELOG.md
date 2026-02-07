# Changelog

Todos los cambios importantes en este proyecto se documentan en este archivo.

El formato se basa en [Keep a Changelog](https://keepachangelog.com/es-ES/1.0.0/),
y este proyecto se adhiere a la [Versionación Semántica](https://semver.org/lang/es/).

## [2.0] - 2026-02-06

### ✨ Agregado

#### Nuevas Características principales
- **Soporte multiidioma**: Agregado selector de 8 idiomas diferentes (español, inglés, francés, alemán, italiano, portugués, japonés, chino)
- **Editor de Texto Mejorado**: 
  - Modo edición activable/desactivable
  - Búsqueda y reemplazo de texto (Ctrl+H)
  - Contador de palabras y caracteres
  - Deshacer/Rehacer automático

- **Exportación a múltiples formatos**:
  - Documento Word (.docx)
  - Documento PDF (.pdf)
  - Markdown (.md)
  - Texto plano (.txt)

- **Historial de conversiones**:
  - Guarda las últimas 20 conversiones
  - Tabla con detalles: fecha, archivo, vista previa, cantidad de palabras
  - Restaurar conversiones previas
  - Limpiar historial completo

- **Sistema de configuración**:
  - Selector de idioma antes de convertir
  - Duración máxima configurable
  - Configuración persistente en `config.json`
  - Diálogo de configuración accesible

- **Información detallada de conversión**:
  - Duración del archivo de audio
  - Cantidad de palabras extraídas
  - Cantidad de caracteres
  - Idioma detectado
  - Confianza del reconocimiento
  - Tiempo de procesamiento

- **Interfaz mejorada**:
  - Ventana maximizada por defecto
  - Soporte para Drag & Drop
  - Menú completo con todas las opciones
  - Barra de estado mejorada

- **Atajos de teclado**:
  - Ctrl+O: Abrir audio
  - Ctrl+S: Guardar texto
  - Ctrl+C: Copiar
  - Ctrl+H: Buscar y reemplazar
  - Ctrl+Q: Salir

#### Módulos nuevos
- `styles.py`: Gestión centralizada de estilos CSS/PyQt6
- `history.py`: Gestión del historial de conversiones
- `config.py`: Gestión de configuración persistente

#### Dependencias nuevas
- `python-docx` (0.8.11): Exportación a Word
- `reportlab` (4.0.9): Exportación a PDF
- `markdown` (3.5.1): Exportación a Markdown

### 🎨 Cambiados

- **GUI completa rediseñada**:
  - Reorganización de botones y controles
  - Mejora de estilos y temas
  - Panel de información adicional

- **Estructura del código**:
  - Separación de estilos en archivo independiente
  - Mejor organización de diálogos
  - Clase `AudioConverterThread` mejorada para soportar metadatos

- **Textos de la aplicación**:
  - Capitalización consistente (primera palabra en mayúscula)
  - Mensajes más claros y descriptivos

- **Diálogos**:
  - Nuevo diálogo de configuración
  - Nuevo diálogo de historial con tabla
  - Nuevo diálogo de búsqueda y reemplazo

### 🔧 Corregido

- Error de inicialización: Removido `setDragDropMode` que no existe en `QTextEdit`
- Mejor manejo de errores en la conversión de audio
- Mejorada la limpieza de archivos temporales

### 📦 Dependencias

- Actualizado `requirements.txt` con nuevas dependencias
- Todas las dependencias son compatibles con Python 3.10+

### 🚀 Mejoras de rendimiento

- Interfaz más responsiva
- Mejor gestión de memoria temporal
- Optimización de la barra de progreso

---

## [1.0] - 2025-12-15

### ✨ Agregado

- Interfaz gráfica básica con PyQt6
- Conversión de audio MP3 y WAV a texto
- Reconocimiento de voz mediante Google Speech Recognition
- Barra de progreso
- Cargar y guardar archivos
- Botón cancelar conversión
- Gestión de mensajes de estado
- Tema oscuro profesional
- Icono de aplicación

### 🎨 Características de diseño

- Panel de botones con estilos personalizados
- Área de texto solo lectura
- Barra de estado informativa
- Ventana centrada en pantalla

### 🔧 Funcionalidad base

- Carga de archivos de audio
- Conversión a WAV si es necesario
- Transcripción automática
- Guardado en archivo de texto
- Manejo de errores básico

### ⚙️ Configuración

- Sistema de reconocedor centralizado
- Gestión de directorios temporales
- Manejo de rutas absolutas

---

## Legendas de cambios

- **✨ Agregado**: Nuevas características
- **🎨 Cambiado**: Cambios en funcionalidad existente
- **🔧 Corregido**: Corrección de bugs
- **🚀 Mejoras**: Mejoras de rendimiento
- **📦 Dependencias**: Cambios en dependencias
- **⚠️ Deprecado**: Funcionalidades que serán removidas
- **🗑️ Removido**: Funcionalidades removidas

---

## Planes futuros

### Versión 2.1
- [ ] Soporte para más formatos de audio (OGG, FLAC, AAC)
- [ ] Editor de audio integrado
- [ ] Corrección automática de ortografía
- [ ] Temas de colores personalizables
- [ ] Grabación de audio en tiempo real

### Versión 3.0
- [ ] API REST para integración externa
- [ ] Aplicación web
- [ ] Aplicación móvil (iOS/Android)
- [ ] Sincronización en la nube
- [ ] Reconocimiento de emociones
- [ ] Traducción automática de texto

### Largo plazo
- [ ] Plugin para Office
- [ ] Integración con Google Drive
- [ ] Subtítulos en tiempo real
- [ ] Análisis de sentimiento
- [ ] Transcripción de reuniones
- [ ] Base de datos de conversiones

---

**Mantenedor**: Tu Nombre
**Última Actualización**: Febrero 2026

¡Gracias por tu interés en Convertidor de audio a texto!
