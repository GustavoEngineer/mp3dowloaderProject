
import os
import re
import yt_dlp
from flask import Flask, request, jsonify, render_template, send_from_directory, Response, stream_with_context

app = Flask(__name__)

def limpiar_nombre(nombre):
    """Eliminar caracteres inválidos del nombre de archivo"""
    return re.sub(r'[\\/*?:\"<>|]', "", nombre)

def descargar_video(url, carpeta="descargas"):
    os.makedirs(carpeta, exist_ok=True)
    
    opciones = {
        'format': 'bestvideo+bestaudio/best',
        'outtmpl': f'{carpeta}/%(title)s.%(ext)s',
        'postprocessors': [],
        'nocheckcertificate': True,
    }

    try:
        with yt_dlp.YoutubeDL(opciones) as ydl:
            info = ydl.extract_info(url, download=False)
            info['title'] = limpiar_nombre(info['title'])
            ydl.download([url])
        return {"estado": "exito", "mensaje": f"Video descargado en '{carpeta}'"}
    except Exception as e:
        return {"estado": "error", "mensaje": str(e)}

def descargar_mp3(url, carpeta="descargas"):
    os.makedirs(carpeta, exist_ok=True)
    
    opciones = {
        'format': 'bestaudio/best',
        'outtmpl': f'{carpeta}/%(title)s.%(ext)s',
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '320',
        }],
        'ffmpeg_location': 'C:/ffmpeg/bin/ffmpeg.exe',
        'nocheckcertificate': True,
    }

    try:
        with yt_dlp.YoutubeDL(opciones) as ydl:
            info = ydl.extract_info(url, download=False)
            info['title'] = limpiar_nombre(info['title'])
            ydl.download([url])
        return {"estado": "exito", "mensaje": f"Audio MP3 descargado en '{carpeta}'"}
    except Exception as e:
        return {"estado": "error", "mensaje": str(e)}

@app.route('/download', methods=['GET'])
def api_descargar_audio_get():
    """Endpoint para la app móvil que usa GET."""
    url = request.args.get('url')
    if not url:
        return jsonify({"message": "No se proporcionó URL."}), 400

    try:
        opciones_ydl = {
            'format': 'bestaudio/best',
            'outtmpl': '-',  # Salida estándar (stdout)
            'postprocessors': [{
                'key': 'FFmpegExtractAudio',
                'preferredcodec': 'mp3',
                'preferredquality': '320',
            }],
            'ffmpeg_location': 'C:/ffmpeg/bin/ffmpeg.exe',
            'nocheckcertificate': True,
            'quiet': True,
        }

        with yt_dlp.YoutubeDL(opciones_ydl) as ydl:
            info = ydl.extract_info(url, download=False)
            titulo_limpio = limpiar_nombre(info['title'])

            @stream_with_context
            def generate():
                # Usamos un generador para transmitir la salida de yt-dlp directamente al cliente.
                # download() con outtmpl='-' escribirá en stdout, que capturamos aquí.
                with yt_dlp.YoutubeDL(opciones_ydl) as ydl_stream:
                    # No necesitamos un generador anidado, podemos ceder directamente
                    # desde el resultado de la descarga cuando se transmite.
                    yield ydl_stream.download([url])

            return Response(generate(), mimetype='audio/mpeg', headers={'Content-Disposition': f'attachment;filename="{titulo_limpio}.mp3"'})

    except Exception as e:
        return jsonify({"message": str(e)}), 500

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/descargas/<path:filename>')
def servir_archivo_descargado(filename):
    """Sirve los archivos desde la carpeta de descargas."""
    directorio_descargas = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'descargas')
    return send_from_directory(directorio_descargas, filename, as_attachment=True)

@app.route('/descargar-video', methods=['POST'])
def api_descargar_video():
    data = request.get_json()
    url = data.get('url')
    if not url:
        return jsonify({"estado": "error", "mensaje": "No se proporcionó URL"}), 400
    
    resultado = descargar_video(url)
    if resultado['estado'] == 'exito':
        return jsonify(resultado)
    else:
        return jsonify(resultado), 500

@app.route('/descargar-mp3', methods=['POST'])
def api_descargar_mp3():
    data = request.get_json()
    url = data.get('url')
    if not url:
        return jsonify({"estado": "error", "mensaje": "No se proporcionó URL"}), 400

    resultado = descargar_mp3(url)
    if resultado['estado'] == 'exito':
        return jsonify(resultado)
    else:
        return jsonify(resultado), 500

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000, debug=True)
