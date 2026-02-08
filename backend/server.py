#!/usr/bin/env python3
"""
YouTube to MP3 Downloader Server
Descarga videos de YouTube y los convierte a formato MP3
"""

import os
import sys
import re
from pathlib import Path
import yt_dlp
from colorama import init, Fore, Style

# Inicializar colorama para Windows
init(autoreset=True)

class YouTubeMP3Downloader:
    def __init__(self, download_path='downloads'):
        """
        Inicializa el descargador de YouTube a MP3
        
        Args:
            download_path: Ruta donde se guardarán los archivos MP3
        """
        self.download_path = Path(download_path).resolve()
        self.download_path.mkdir(exist_ok=True)
        
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
            bool: True si la descarga fue exitosa
        """
        if not self.validate_youtube_url(url):
            print(f"{Fore.RED}❌ Error: La URL no es válida de YouTube")
            return False
        
        # Configuración de yt-dlp para descargar como MP3
        ydl_opts = {
            'format': 'bestaudio[ext=m4a]/bestaudio[ext=webm]/bestaudio/best',
            'postprocessors': [{
                'key': 'FFmpegExtractAudio',
                'preferredcodec': 'mp3',
                'preferredquality': '192',
            }],
            'outtmpl': str(self.download_path / '%(title)s.%(ext)s'),
            'quiet': False,
            'no_warnings': False,
            'extract_flat': False,
            # Opciones para evitar errores 403
            'user_agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
            'extractor_args': {
                'youtube': {
                    'player_client': ['android', 'ios', 'web'],
                    'player_skip': ['webpage', 'configs'],
                }
            },
            'http_headers': {
                'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
                'Accept-Language': 'en-us,en;q=0.5',
                'Sec-Fetch-Mode': 'navigate',
            },
            # Opciones adicionales para mejorar compatibilidad
            'nocheckcertificate': True,
            'ignoreerrors': False,
            'no_color': False,
        }
        
        try:
            print(f"\n{Fore.CYAN}📥 Iniciando descarga...")
            print(f"{Fore.YELLOW}📂 Guardando en: {self.download_path}\n")
            
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                # Obtener información del video
                info = ydl.extract_info(url, download=False)
                video_title = info.get('title', 'Unknown')
                
                print(f"{Fore.GREEN}🎵 Título: {video_title}")
                print(f"{Fore.CYAN}⏳ Descargando y convirtiendo a MP3...\n")
                
                # Descargar y convertir
                ydl.download([url])
                
            print(f"\n{Fore.GREEN}✅ ¡Descarga completada exitosamente!")
            print(f"{Fore.GREEN}📁 Archivo guardado en: {self.download_path}")
            return True
            
        except yt_dlp.utils.DownloadError as e:
            print(f"\n{Fore.RED}❌ Error al descargar: {str(e)}")
            return False
        except Exception as e:
            print(f"\n{Fore.RED}❌ Error inesperado: {str(e)}")
            return False
    
    def run(self):
        """
        Ejecuta el servidor en modo consola
        """
        print(f"{Fore.MAGENTA}{Style.BRIGHT}")
        print("=" * 60)
        print("  🎵 YOUTUBE TO MP3 DOWNLOADER 🎵")
        print("=" * 60)
        print(f"{Style.RESET_ALL}")
        print(f"{Fore.CYAN}Directorio de descargas: {self.download_path}\n")
        
        while True:
            try:
                print(f"{Fore.YELLOW}{'─' * 60}")
                url = input(f"{Fore.WHITE}Ingresa la URL de YouTube (o 'salir' para terminar): {Style.RESET_ALL}").strip()
                
                if url.lower() in ['salir', 'exit', 'quit', 'q']:
                    print(f"\n{Fore.MAGENTA}👋 ¡Hasta pronto!")
                    break
                
                if not url:
                    print(f"{Fore.RED}⚠️  Por favor ingresa una URL válida\n")
                    continue
                
                self.download_mp3(url)
                print()
                
            except KeyboardInterrupt:
                print(f"\n\n{Fore.MAGENTA}👋 Proceso interrumpido. ¡Hasta pronto!")
                break
            except Exception as e:
                print(f"{Fore.RED}❌ Error: {str(e)}\n")


def main():
    """
    Función principal del servidor
    """
    # Crear el descargador con la carpeta 'downloads' dentro de backend
    script_dir = Path(__file__).parent
    downloads_dir = script_dir / 'downloads'
    
    downloader = YouTubeMP3Downloader(download_path=downloads_dir)
    downloader.run()


if __name__ == '__main__':
    main()
