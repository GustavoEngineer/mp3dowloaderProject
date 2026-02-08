# 📚 Documentación Técnica - YouTube to MP3 Downloader

## 📋 Descripción del Proyecto

Aplicación web desarrollada en Python con Flask que permite descargar videos de YouTube y convertirlos automáticamente a formato MP3. Los archivos se descargan directamente a la carpeta de descargas del navegador del usuario.

---

## 🛠️ Tecnologías y Herramientas

### Lenguajes de Programación
- **Python 3.7+**: Lenguaje principal del backend
- **HTML5**: Estructura de la interfaz web
- **CSS3**: Estilos y animaciones
- **JavaScript (ES6+)**: Lógica del cliente y manejo de descargas

### Frameworks y Librerías

#### Backend (Python)
- **Flask 3.0.0+**: Framework web para crear el servidor HTTP
  - Manejo de rutas y endpoints
  - Renderizado de templates
  - Envío de archivos al navegador
  
- **yt-dlp 2026+**: Descargador de videos de YouTube
  - Extracción de audio de videos
  - Soporte para múltiples formatos
  - Bypass de restricciones HTTP 403
  
- **colorama 0.4.6+**: Salida colorida en consola
  - Logs visuales del servidor
  - Mensajes de estado

#### Frontend
- **Fetch API**: Comunicación asíncrona con el backend
- **Blob API**: Manejo de archivos binarios
- **URL API**: Creación de enlaces de descarga temporales

### Herramientas Externas

#### FFmpeg (REQUERIDO)
- **Versión**: Cualquier versión reciente
- **Propósito**: Conversión de audio a formato MP3
- **Instalación Windows**:
  ```bash
  winget install ffmpeg
  ```
- **Uso**: yt-dlp lo utiliza automáticamente para la conversión

---

## 📦 Dependencias de Python

### requirements.txt
```
yt-dlp>=2024.0.0
colorama>=0.4.6
flask>=3.0.0
```

### Instalación
```bash
pip install -r requirements.txt
```

---

## 🏗️ Estructura del Proyecto

```
mp3Project/
├── backend/                    # Directorio principal del servidor
│   ├── app.py                 # Servidor web Flask (PRINCIPAL)
│   ├── server.py              # Versión consola (alternativa)
│   ├── templates/             # Plantillas HTML
│   │   └── index.html        # Interfaz web principal
│   ├── static/                # Archivos estáticos
│   │   └── style.css         # Estilos CSS
│   └── downloads/             # Carpeta temporal (auto-limpieza)
└── requirements.txt           # Dependencias del proyecto
```

---

## 🔧 Arquitectura del Sistema

### Backend (app.py)

#### Clase Principal: `YouTubeMP3Downloader`
```python
class YouTubeMP3Downloader:
    def __init__(self):
        # Inicializa directorio temporal
        self.temp_dir = Path(tempfile.gettempdir()) / 'yt_mp3_downloads'
    
    def validate_youtube_url(self, url) -> bool:
        # Valida URLs de YouTube con regex
    
    def download_mp3(self, url) -> tuple:
        # Descarga y convierte video a MP3
        # Retorna: (success, file_path/error, video_title)
    
    def cleanup_old_files(self, max_age_minutes=30):
        # Elimina archivos temporales antiguos
```

#### Endpoints de Flask

1. **GET `/`**
   - Renderiza la página principal
   - Template: `templates/index.html`

2. **POST `/download`**
   - Recibe: JSON con `{"url": "youtube_url"}`
   - Proceso:
     1. Valida URL de YouTube
     2. Descarga video con yt-dlp
     3. Convierte a MP3 con FFmpeg
     4. Envía archivo al navegador
     5. Limpia archivo temporal
   - Retorna: Archivo MP3 o error JSON

3. **GET `/health`**
   - Endpoint de salud del servidor
   - Retorna: `{"status": "ok"}`

### Frontend (index.html + style.css)

#### Componentes HTML
- **Header**: Título con icono animado
- **Form**: Input de URL + botón de descarga
- **Progress**: Barra de progreso animada
- **Messages**: Notificaciones de éxito/error
- **Features**: Tarjetas de características

#### JavaScript
```javascript
// Manejo de formulario
form.addEventListener('submit', async (e) => {
    // 1. Validación de URL
    // 2. Petición POST a /download
    // 3. Recepción de blob
    // 4. Creación de enlace de descarga
    // 5. Trigger de descarga automática
});
```

---

## ⚙️ Configuración de yt-dlp

### Opciones Principales
```python
ydl_opts = {
    'format': 'bestaudio[ext=m4a]/bestaudio[ext=webm]/bestaudio/best',
    'postprocessors': [{
        'key': 'FFmpegExtractAudio',
        'preferredcodec': 'mp3',
        'preferredquality': '192',  # 192 kbps
    }],
    'outtmpl': 'ruta/temporal/%(title)s.%(ext)s',
    
    # Bypass HTTP 403
    'user_agent': 'Mozilla/5.0 ...',
    'extractor_args': {
        'youtube': {
            'player_client': ['android', 'ios', 'web'],
            'player_skip': ['webpage', 'configs'],
        }
    },
    'nocheckcertificate': True,
}
```

---

## 🎨 Diseño y Estilos

### Paleta de Colores
```css
:root {
    --primary: #6366f1;        /* Indigo */
    --primary-dark: #4f46e5;   /* Indigo oscuro */
    --secondary: #ec4899;      /* Rosa */
    --success: #10b981;        /* Verde */
    --error: #ef4444;          /* Rojo */
    --bg-dark: #0f172a;        /* Fondo oscuro */
    --bg-card: rgba(30, 41, 59, 0.8);  /* Card con transparencia */
}
```

### Efectos Visuales
- **Glassmorphism**: `backdrop-filter: blur(20px)`
- **Gradientes**: Fondos y textos con gradientes animados
- **Animaciones**:
  - `fadeInDown`: Entrada del header
  - `fadeInUp`: Entrada de cards
  - `float`: Flotación del icono
  - `progress`: Barra de carga

### Responsive Design
- Breakpoint: `640px`
- Grid adaptativo para features
- Padding y tamaños ajustables

---

## 🔄 Flujo de Trabajo

### Proceso de Descarga

```
1. Usuario ingresa URL
   ↓
2. Validación en cliente (JavaScript)
   ↓
3. POST a /download con URL
   ↓
4. Backend valida URL
   ↓
5. yt-dlp descarga video
   ↓
6. FFmpeg convierte a MP3
   ↓
7. Archivo guardado temporalmente
   ↓
8. Flask envía archivo al navegador
   ↓
9. Navegador descarga a carpeta Downloads
   ↓
10. Backend limpia archivo temporal
```

### Limpieza Automática
- Se ejecuta antes de cada descarga
- Elimina archivos > 30 minutos
- Ubicación: `tempfile.gettempdir()/yt_mp3_downloads/`

---

## 🚀 Ejecución del Servidor

### Comando de Inicio
```bash
cd backend
python app.py
```

### Configuración del Servidor
```python
app.run(
    host='0.0.0.0',    # Accesible desde red local
    port=5000,         # Puerto por defecto
    debug=True         # Modo debug (desarrollo)
)
```

### Acceso
- **Local**: `http://localhost:5000`
- **Red local**: `http://<IP-local>:5000`

---

## 🔒 Seguridad y Consideraciones

### Validaciones Implementadas
1. **URL de YouTube**: Regex pattern matching
2. **Formato de archivo**: Solo MP3
3. **Tamaño**: Limitado por yt-dlp
4. **Tiempo de vida**: Archivos temporales eliminados automáticamente

### Limitaciones
- No soporta videos con DRM
- Algunos videos con restricciones de edad pueden fallar
- Límite de descargas según políticas de YouTube
- Requiere conexión a internet

---

## 🐛 Manejo de Errores

### Errores Comunes

1. **HTTP 403: Forbidden**
   - Causa: YouTube bloqueando descarga
   - Solución: Actualizar yt-dlp, usar múltiples player clients

2. **FFmpeg not found**
   - Causa: FFmpeg no instalado o no en PATH
   - Solución: Instalar FFmpeg y reiniciar terminal

3. **Invalid URL**
   - Causa: URL no es de YouTube
   - Solución: Validación en cliente y servidor

4. **Download Error**
   - Causa: Video privado, eliminado o restringido
   - Solución: Mensaje de error al usuario

---

## 📊 Requisitos del Sistema

### Mínimos
- **OS**: Windows 10+, macOS 10.14+, Linux (cualquier distro moderna)
- **Python**: 3.7 o superior
- **RAM**: 512 MB disponible
- **Disco**: 100 MB para dependencias + espacio para descargas
- **Internet**: Conexión estable

### Recomendados
- **Python**: 3.11+
- **RAM**: 2 GB disponible
- **Disco**: 1 GB libre
- **Internet**: Banda ancha (5+ Mbps)

---

## 🔄 Versiones Disponibles

### 1. Versión Web (app.py) - PRINCIPAL
- Interfaz gráfica en navegador
- Descargas directas a carpeta del navegador
- Limpieza automática
- Mejor UX

### 2. Versión Consola (server.py) - ALTERNATIVA
- Interfaz de línea de comandos
- Descargas a `backend/downloads/`
- Salida colorida
- Uso técnico

---

## 📝 Notas Técnicas

### Archivos Temporales
- **Ubicación**: `%TEMP%\yt_mp3_downloads\` (Windows)
- **Formato**: `temp_<timestamp>.mp3`
- **Limpieza**: Automática cada 30 minutos

### Formato de Salida
- **Codec**: MP3
- **Bitrate**: 192 kbps
- **Sample Rate**: Según fuente original
- **Canales**: Estéreo (si disponible)

### Compatibilidad de Navegadores
- ✅ Chrome 90+
- ✅ Firefox 88+
- ✅ Edge 90+
- ✅ Safari 14+
- ✅ Opera 76+

---

## 🎯 Características Técnicas Destacadas

1. **Streaming de Archivos**: Uso de `send_file()` de Flask
2. **Async Downloads**: Fetch API con async/await
3. **Blob Handling**: Manejo eficiente de archivos binarios
4. **Responsive Design**: Mobile-first approach
5. **Error Boundaries**: Try-catch en cliente y servidor
6. **Auto-cleanup**: Gestión automática de memoria
7. **Progress Feedback**: UX mejorada con indicadores visuales

---

## 📚 Referencias y Recursos

### Documentación Oficial
- [Flask Documentation](https://flask.palletsprojects.com/)
- [yt-dlp GitHub](https://github.com/yt-dlp/yt-dlp)
- [FFmpeg Documentation](https://ffmpeg.org/documentation.html)

### APIs Utilizadas
- [Fetch API (MDN)](https://developer.mozilla.org/en-US/docs/Web/API/Fetch_API)
- [Blob API (MDN)](https://developer.mozilla.org/en-US/docs/Web/API/Blob)
- [File API (MDN)](https://developer.mozilla.org/en-US/docs/Web/API/File)

---

## 🔧 Mantenimiento

### Actualización de Dependencias
```bash
pip install --upgrade yt-dlp flask colorama
```

### Verificación de FFmpeg
```bash
ffmpeg -version
```

### Logs del Servidor
- Modo debug habilitado por defecto
- Logs en consola con colorama
- Errores detallados en respuestas JSON

---

## ⚖️ Licencia y Uso

- **Uso**: Personal y educativo
- **Restricciones**: Respetar derechos de autor
- **Disclaimer**: Solo descargar contenido con permiso o de dominio público

---

## 📧 Información del Proyecto

- **Versión**: 2.0 (Web Server)
- **Fecha**: Febrero 2026
- **Stack**: Python + Flask + HTML/CSS/JS
- **Estado**: Producción
