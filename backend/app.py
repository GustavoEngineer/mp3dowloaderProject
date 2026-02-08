#!/usr/bin/env python3
"""
YouTube to MP3 Downloader - Web Server
Servidor Flask para descargar videos de YouTube como MP3 desde el navegador
"""

import os
import re
import hashlib
import requests
from pathlib import Path
from datetime import datetime
from flask import Flask, render_template, request, send_file, jsonify, session, redirect, url_for
from werkzeug.utils import secure_filename
import yt_dlp
from colorama import init, Fore, Style
import tempfile
import time

# Inicializar colorama para logs en consola
init(autoreset=True)

# Inicializar Flask con rutas específicas para Vercel
app = Flask(__name__, 
            static_folder='static', 
            template_folder='templates')

# Configuración de sesión
app.secret_key = os.getenv('SECRET_KEY', os.urandom(24))

# Configuración de admin
ADMIN_PASSWORD_HASH = os.getenv('ADMIN_PASSWORD_HASH', '')

# Cookie storage - usar URL externa (GitHub Gist, Pastebin, etc.)
# Esto evita el límite de tamaño de variables de entorno
YOUTUBE_COOKIES_URL = os.getenv('YOUTUBE_COOKIES_URL', '')

# Cache de cookies en memoria
_cookies_cache = None
_cookies_last_update = None

# Crear archivo temporal de cookies descargándolas desde URL
def get_cookie_file():
    """Descarga cookies desde URL externa y las guarda en archivo temporal"""
    global _cookies_cache, _cookies_last_update
    
    if not YOUTUBE_COOKIES_URL:
        print(f"{Fore.YELLOW}⚠️  No hay URL de cookies configurada")
        return None
    
    try:
        # Verificar si ya tenemos cookies en cache (válidas por 1 hora)
        if _cookies_cache and _cookies_last_update:
            elapsed = time.time() - _cookies_last_update
            if elapsed < 3600:  # 1 hora
                return _cookies_cache
        
        print(f"{Fore.CYAN}📥 Descargando cookies desde URL...")
        
        # Descargar cookies desde URL
        response = requests.get(YOUTUBE_COOKIES_URL, timeout=10)
        response.raise_for_status()
        
        # Crear archivo temporal
        temp_cookie_file = Path(tempfile.gettempdir()) / 'youtube_cookies.txt'
        temp_cookie_file.write_text(response.text)
        
        _cookies_cache = str(temp_cookie_file)
        _cookies_last_update = time.time()
        
        print(f"{Fore.GREEN}✅ Cookies descargadas exitosamente ({len(response.text)} caracteres)")
        return _cookies_cache
        
    except requests.RequestException as e:
        print(f"{Fore.RED}⚠️  Error al descargar cookies desde URL: {e}")
        return None
    except Exception as e:
        print(f"{Fore.RED}⚠️  Error al crear archivo temporal de cookies: {e}")
        return None

class YouTubeMP3Downloader:
    def __init__(self):
        """Inicializa el descargador de YouTube a MP3"""
        self.temp_dir = Path(tempfile.gettempdir()) / 'yt_mp3_downloads'
        self.temp_dir.mkdir(exist_ok=True)
        
    def validate_youtube_url(self, url):
        """
        Valida si la URL es de YouTube
        
        Args:
            url: URL a validar
            
        Returns:
            bool: True si es una URL válida de YouTube
        """
        youtube_regex = (
            r'(https?://)?(www\.)?'
            r'(youtube|youtu|youtube-nocookie)\.(com|be)/'
            r'(watch\?v=|embed/|v/|.+\?v=)?([^&=%\?]{11})'
        )
        
        youtube_regex_match = re.match(youtube_regex, url)
        return youtube_regex_match is not None
    
    def download_mp3(self, url):
        """
        Descarga un video de YouTube y lo convierte a MP3
        
        Args:
            url: URL del video de YouTube
            
        Returns:
            tuple: (success: bool, file_path: str or error_message: str, video_title: str)
        """
        if not self.validate_youtube_url(url):
            return False, "La URL no es válida de YouTube", None
        
        # Generar nombre único para el archivo temporal
        timestamp = int(time.time())
        temp_filename = f'temp_{timestamp}'
        
        # Configuración de yt-dlp para descargar como MP3
        ydl_opts = {
            'format': 'bestaudio[ext=m4a]/bestaudio[ext=webm]/bestaudio/best',
            'postprocessors': [{
                'key': 'FFmpegExtractAudio',
                'preferredcodec': 'mp3',
                'preferredquality': '192',
            }],
            'outtmpl': str(self.temp_dir / f'{temp_filename}.%(ext)s'),
            'quiet': True,
            'no_warnings': True,
            'extract_flat': False,
            # Usar cookies desde variable de entorno
            'cookiefile': get_cookie_file(),
            # Opciones mejoradas para evitar errores 403 y bot detection
            'user_agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
            'extractor_args': {
                'youtube': {
                    'player_client': ['android', 'ios', 'web', 'tv_embedded'],
                    'player_skip': ['webpage', 'configs'],
                    'skip': ['dash', 'hls'],
                }
            },
            'http_headers': {
                'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
                'Accept-Language': 'en-us,en;q=0.5',
                'Accept-Encoding': 'gzip, deflate',
                'Sec-Fetch-Mode': 'navigate',
            },
            'nocheckcertificate': True,
            'ignoreerrors': False,
            'no_color': True,
            # Opciones adicionales para evitar bot detection
            'age_limit': None,
            'geo_bypass': True,
            'geo_bypass_country': 'US',
        }
        
        # Log si se están usando cookies
        if YOUTUBE_COOKIES_URL:
            print(f"{Fore.GREEN}🍪 Usando cookies de YouTube")
        
        try:
            print(f"{Fore.CYAN}📥 Descargando: {url}")
            
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                # Obtener información del video
                info = ydl.extract_info(url, download=False)
                video_title = info.get('title', 'Unknown')
                
                print(f"{Fore.GREEN}🎵 Título: {video_title}")
                
                # Descargar y convertir
                ydl.download([url])
                
            # Encontrar el archivo MP3 generado
            mp3_file = self.temp_dir / f'{temp_filename}.mp3'
            
            if not mp3_file.exists():
                return False, "Error al generar el archivo MP3", None
                
            print(f"{Fore.GREEN}✅ Descarga completada: {video_title}")
            return True, str(mp3_file), video_title
            
        except yt_dlp.utils.DownloadError as e:
            error_msg = str(e)
            print(f"{Fore.RED}❌ Error al descargar: {error_msg}")
            return False, f"Error al descargar: {error_msg}", None
        except Exception as e:
            error_msg = str(e)
            print(f"{Fore.RED}❌ Error inesperado: {error_msg}")
            return False, f"Error inesperado: {error_msg}", None
    
    def cleanup_old_files(self, max_age_minutes=30):
        """
        Limpia archivos temporales antiguos
        
        Args:
            max_age_minutes: Edad máxima de archivos en minutos
        """
        try:
            current_time = time.time()
            for file in self.temp_dir.glob('temp_*.mp3'):
                file_age = current_time - file.stat().st_mtime
                if file_age > (max_age_minutes * 60):
                    file.unlink()
                    print(f"{Fore.YELLOW}🗑️  Archivo temporal eliminado: {file.name}")
        except Exception as e:
            print(f"{Fore.RED}⚠️  Error al limpiar archivos: {e}")


# Instancia global del descargador
downloader = YouTubeMP3Downloader()


@app.route('/')
def index():
    """Página principal"""
    return render_template('index.html')


@app.route('/download', methods=['POST'])
def download():
    """Endpoint para descargar videos de YouTube como MP3"""
    try:
        data = request.get_json()
        url = data.get('url', '').strip()
        
        if not url:
            return jsonify({'success': False, 'error': 'Por favor ingresa una URL'}), 400
        
        # Limpiar archivos antiguos antes de descargar
        downloader.cleanup_old_files()
        
        # Descargar el video
        success, result, video_title = downloader.download_mp3(url)
        
        if not success:
            return jsonify({'success': False, 'error': result}), 400
        
        # result contiene la ruta del archivo MP3
        file_path = result
        
        # Generar nombre de archivo seguro
        safe_title = re.sub(r'[^\w\s-]', '', video_title)
        safe_title = re.sub(r'[-\s]+', '-', safe_title)
        download_name = f"{safe_title}.mp3"
        
        # Enviar el archivo al navegador
        return send_file(
            file_path,
            as_attachment=True,
            download_name=download_name,
            mimetype='audio/mpeg'
        )
        
    except Exception as e:
        print(f"{Fore.RED}❌ Error en endpoint /download: {e}")
        return jsonify({'success': False, 'error': str(e)}), 500


@app.route('/health', methods=['GET'])
def health():
    """Endpoint de salud del servidor"""
    return jsonify({'status': 'ok', 'message': 'Server is running'})


# ==================== ADMIN ENDPOINTS ====================

def check_admin_auth(password):
    """Verifica si la contraseña de admin es correcta"""
    if not ADMIN_PASSWORD_HASH:
        # Si no hay hash configurado, generar uno temporal para desarrollo
        # En producción, DEBE estar configurado en variables de entorno
        return password == 'admin123'  # Password por defecto solo para desarrollo
    
    password_hash = hashlib.sha256(password.encode()).hexdigest()
    return password_hash == ADMIN_PASSWORD_HASH


def require_admin():
    """Decorador para requerir autenticación de admin"""
    if not session.get('admin_authenticated'):
        return False
    return True


@app.route('/admin')
def admin():
    """Página de administración"""
    return render_template('admin.html')


@app.route('/admin/login', methods=['POST'])
def admin_login():
    """Endpoint para login de admin"""
    try:
        data = request.get_json()
        password = data.get('password', '')
        
        if check_admin_auth(password):
            session['admin_authenticated'] = True
            return jsonify({'success': True, 'message': 'Autenticación exitosa'})
        else:
            return jsonify({'success': False, 'error': 'Contraseña incorrecta'}), 401
            
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500


@app.route('/admin/logout', methods=['POST'])
def admin_logout():
    """Endpoint para logout de admin"""
    session.pop('admin_authenticated', None)
    return jsonify({'success': True, 'message': 'Sesión cerrada'})


@app.route('/admin/check-auth', methods=['GET'])
def admin_check_auth():
    """Verifica si el usuario está autenticado"""
    is_auth = session.get('admin_authenticated', False)
    return jsonify({'authenticated': is_auth})


@app.route('/admin/upload-cookies', methods=['POST'])
def upload_cookies():
    """Endpoint para subir archivo de cookies"""
    if not require_admin():
        return jsonify({'success': False, 'error': 'No autenticado'}), 401
    
    try:
        if 'file' not in request.files:
            return jsonify({'success': False, 'error': 'No se envió ningún archivo'}), 400
        
        file = request.files['file']
        
        if file.filename == '':
            return jsonify({'success': False, 'error': 'Nombre de archivo vacío'}), 400
        
        if not file.filename.endswith('.txt'):
            return jsonify({'success': False, 'error': 'El archivo debe ser .txt'}), 400
        
        # Leer el contenido del archivo
        cookie_content = file.read().decode('utf-8')
        
        print(f"{Fore.GREEN}✅ Cookies recibidas ({len(cookie_content)} caracteres)")
        
        # Proporcionar instrucciones para crear GitHub Gist
        return jsonify({
            'success': True, 
            'message': 'Cookies procesadas. Ahora crea un GitHub Gist con este contenido',
            'cookie_content': cookie_content,
            'instructions': [
                '1. Ve a https://gist.github.com',
                '2. Pega el contenido de las cookies en el editor',
                '3. Nombre del archivo: youtube_cookies.txt',
                '4. Selecciona "Create secret gist" (privado)',
                '5. Click en "Create secret gist"',
                '6. Click en el botón "Raw" en tu Gist',
                '7. Copia la URL completa (debe empezar con https://gist.githubusercontent.com/...)',
                '8. Ve a Leapcell → Settings → Environment Variables',
                '9. Agrega: YOUTUBE_COOKIES_URL = <URL copiada>',
                '10. Guarda y Redeploy'
            ],
            'gist_url': 'https://gist.github.com'
        })
        
    except Exception as e:
        print(f"{Fore.RED}❌ Error al procesar cookies: {e}")
        return jsonify({'success': False, 'error': str(e)}), 500


@app.route('/admin/cookie-status', methods=['GET'])
def cookie_status():
    """Endpoint para verificar el estado de las cookies"""
    if not require_admin():
        return jsonify({'success': False, 'error': 'No autenticado'}), 401
    
    try:
        if YOUTUBE_COOKIES_URL:
            # Intentar descargar cookies para verificar que la URL funciona
            try:
                response = requests.get(YOUTUBE_COOKIES_URL, timeout=10)
                response.raise_for_status()
                
                return jsonify({
                    'success': True,
                    'exists': True,
                    'source': 'external_url',
                    'url': YOUTUBE_COOKIES_URL[:50] + '...' if len(YOUTUBE_COOKIES_URL) > 50 else YOUTUBE_COOKIES_URL,
                    'size_bytes': len(response.text),
                    'message': 'Cookies configuradas y accesibles desde URL externa'
                })
            except requests.RequestException as e:
                return jsonify({
                    'success': True,
                    'exists': True,
                    'source': 'external_url',
                    'url': YOUTUBE_COOKIES_URL[:50] + '...' if len(YOUTUBE_COOKIES_URL) > 50 else YOUTUBE_COOKIES_URL,
                    'error': f'URL configurada pero no accesible: {str(e)}',
                    'message': 'Verifica que la URL del Gist sea correcta y pública (raw)'
                })
        else:
            return jsonify({
                'success': True,
                'exists': False,
                'message': 'No hay cookies configuradas. Agrega YOUTUBE_COOKIES_URL como variable de entorno en Leapcell'
            })
            
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500


@app.route('/admin/delete-cookies', methods=['DELETE'])
def delete_cookies():
    """Endpoint para eliminar las cookies"""
    if not require_admin():
        return jsonify({'success': False, 'error': 'No autenticado'}), 401
    
    return jsonify({
        'success': False, 
        'error': 'Las cookies están en una URL externa (GitHub Gist). Para eliminarlas:\n1. Ve a Leapcell Dashboard → Settings → Environment Variables\n2. Elimina la variable YOUTUBE_COOKIES_URL\n3. Opcionalmente, elimina el Gist en GitHub'
    }), 400


def main():
    """Función principal para iniciar el servidor"""
    print(f"{Fore.MAGENTA}{Style.BRIGHT}")
    print("=" * 60)
    print("  🎵 YOUTUBE TO MP3 DOWNLOADER - WEB SERVER 🎵")
    print("=" * 60)
    print(f"{Style.RESET_ALL}")
    print(f"{Fore.CYAN}Servidor iniciando en: http://localhost:5000")
    print(f"{Fore.YELLOW}Presiona Ctrl+C para detener el servidor\n")
    
    # Iniciar servidor Flask
    app.run(host='0.0.0.0', port=5000, debug=True)


if __name__ == '__main__':
    main()
