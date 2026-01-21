# Guía de Configuración y Ejecución del Servidor

Este documento detalla los pasos para configurar y ejecutar el servidor de descarga de MP3/Video desde cero.

## Prerrequisitos

Asegúrate de tener instalados los siguientes componentes en tu sistema:

1.  **Python 3.8 o superior**: [Descargar Python](https://www.python.org/downloads/)
    *   *Nota*: Al instalar, asegúrate de marcar la casilla "Add Python to PATH".
2.  **FFmpeg**: Necesario para la conversión de audio.
    *   Descargar desde: [ffmpeg.org](https://ffmpeg.org/download.html)
    *   Extraer el archivo y agregar la carpeta `bin` a las variables de entorno (PATH) de tu sistema.
    *   Para verificar, abre una terminal y ejecuta: `ffmpeg -version`.

## Instalación de Dependencias

1.  Abre una terminal (PowerShell o CMD).
2.  Navega a la carpeta del proyecto:
    ```bash
    cd "ruta/a/tu/proyecto/mp3_downloader_pythonServer"
    ```
3.  Instala las librerías necesarias ejecutando:
    ```bash
    pip install flask yt-dlp
    ```

## Ejecución del Servidor

Para iniciar el servidor web (API):

1.  En la terminal, dentro de la carpeta del proyecto, ejecuta:
    ```bash
    python api.py
    ```
2.  Deberías ver un mensaje similar a:
    ```
    * Running on http://127.0.0.1:5000
    ```
3.  El servidor ahora está listo para recibir peticiones.

## Ejecución del Script Independiente

Si prefieres usar el descargador por consola sin el servidor web:

1.  Ejecuta:
    ```bash
    python Descargador.py
    ```
2.  Sigue las instrucciones en pantalla para introducir la URL y elegir el formato.

## Solución de Problemas Comunes

*   **Error "ffmpeg not found"**: Asegúrate de que FFmpeg esté correctamente agregado al PATH de tu sistema.
*   **Error de permisos**: Intenta ejecutar la terminal como administrador si tienes problemas ejecutando los scripts.
