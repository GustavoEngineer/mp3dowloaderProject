
import tempfile
import shutil
import os
import re
import yt_dlp
from flask import Flask, request, jsonify, render_template, send_from_directory, Response, stream_with_context, send_file, after_this_request

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

# ... (rest of helper functions if needed, but I'll redefine the relevant endpoint below)

@app.route('/download', methods=['GET'])
def api_descargar_audio_get():
    """Endpoint para descargar MP3 directamente al navegador usando archivos temporales."""
    url = request.args.get('url')
    if not url:
        return jsonify({"message": "No se proporcionó URL."}), 400

    # Crear directorio temporal único para esta descarga
    temp_dir = tempfile.mkdtemp()

    try:
        opciones_ydl = {
            'format': 'bestaudio/best',
            'outtmpl': f'{temp_dir}/%(title)s.%(ext)s',
            'postprocessors': [{
                'key': 'FFmpegExtractAudio',
                'preferredcodec': 'mp3',
                'preferredquality': '192',
            }],
            'nocheckcertificate': True,
            'quiet': True,
        }

        with yt_dlp.YoutubeDL(opciones_ydl) as ydl:
            info = ydl.extract_info(url, download=True)
            titulo = limpiar_nombre(info['title'])
            # El archivo final tendrá extensión .mp3
            archivo_path = os.path.join(temp_dir, f"{titulo}.mp3")

        # Verificar si el archivo existe (a veces el título puede variar ligeramente)
        if not os.path.exists(archivo_path):
            # Intentar buscar cualquier archivo mp3 en el directorio temp
            archivos = [f for f in os.listdir(temp_dir) if f.endswith('.mp3')]
            if archivos:
                archivo_path = os.path.join(temp_dir, archivos[0])
                titulo = os.path.splitext(archivos[0])[0]
            else:
                raise Exception("No se pudo encontrar el archivo descargado.")

        @after_this_request
        def remove_temp_dir(response):
            try:
                shutil.rmtree(temp_dir)
            except Exception as e:
                app.logger.error(f"Error eliminando directorio temporal: {e}")
            return response

        return send_file(
            archivo_path, 
            as_attachment=True, 
            download_name=f"{titulo}.mp3", 
            mimetype='audio/mpeg'
        )

    except Exception as e:
        # Limpiar si falla antes de enviar respuesta
        shutil.rmtree(temp_dir, ignore_errors=True)
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
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port, debug=True)
