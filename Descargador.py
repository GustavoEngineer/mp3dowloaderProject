import yt_dlp
import os
import re

def limpiar_nombre(nombre):
    """Eliminar caracteres inválidos del nombre de archivo"""
    return re.sub(r'[\\/*?:"<>|]', "", nombre)

def descargar_video(url, carpeta="descargas"):
    os.makedirs(carpeta, exist_ok=True)
    
    opciones = {
        'format': 'bestvideo+bestaudio/best',
        'outtmpl': f'{carpeta}/%(title)s.%(ext)s',
        'progress_hooks': [lambda d: print(f"{d['_percent_str']} descargado...", end='\r')],
        'postprocessors': [],
    }

    with yt_dlp.YoutubeDL(opciones) as ydl:
        info = ydl.extract_info(url, download=False)
        info['title'] = limpiar_nombre(info['title'])
        ydl.download([url])
    print(f"\n✅ Video descargado en '{carpeta}'")

def descargar_mp3(url, carpeta="descargas"):
    os.makedirs(carpeta, exist_ok=True)
    
    opciones = {
        'format': 'bestaudio/best',
        'outtmpl': f'{carpeta}/%(title)s.%(ext)s',
        'progress_hooks': [lambda d: print(f"{d['_percent_str']} descargado...", end='\r')],
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '320',
        }],
    }

    with yt_dlp.YoutubeDL(opciones) as ydl:
        info = ydl.extract_info(url, download=False)
        info['title'] = limpiar_nombre(info['title'])
        ydl.download([url])
    print(f"\n✅ Audio MP3 descargado en '{carpeta}'")

if __name__ == "__main__":
    url = input("Introduce el enlace del video de YouTube: ").strip()
    print("Elige una opción:")
    print("1. Descargar Video")
    print("2. Descargar MP3 (alta calidad)")
    opcion = input("Opción: ").strip()

    if opcion == "1":
        descargar_video(url)
    elif opcion == "2":
        descargar_mp3(url)
    else:
        print("Opción inválida")
