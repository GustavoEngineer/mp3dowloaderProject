# 🎵 mp3DL Project — Downloader & Vault Premium

¡Bienvenido a **mp3DL Project**! Esta es una aplicación de escritorio híbrida e interactiva en Python diseñada para descargar audios de YouTube de forma ultra rápida en formato `.mp3` de alta fidelidad, organizarlos en álbumes físicos estructurados (Vault), editar sus metadatos ID3 en caliente (Título, Álbum, Artista), eliminarlos con seguridad contextual y exportarlos con indicadores visuales avanzados.

El proyecto está diseñado bajo una arquitectura limpia y desacoplada, utilizando una consola interactiva premium montada sobre una elegante interfaz oscura responsiva en **CustomTkinter** y **Tkinter**.

---

## 🛠️ Requisitos Previos y Herramientas Necesarias

Para que la aplicación funcione al 100% en cualquier dispositivo nuevo, debes asegurarte de tener instaladas las siguientes herramientas de sistema:

### 1. Python 3.10 o Superior
Asegúrate de tener instalado Python en tu sistema. Puedes verificarlo abriendo una terminal o PowerShell y escribiendo:
```powershell
python --version
```
> 💡 *Durante la instalación de Python en Windows, asegúrate de marcar la casilla **"Add Python to PATH"**.*

### 2. FFmpeg (Indispensable para yt-dlp)
`yt-dlp` requiere la herramienta de sistema **FFmpeg** para extraer, convertir y encapsular correctamente los audios descargados a formato `.mp3` sin pérdida de calidad.

#### **Instalación rápida en Windows (Recomendada):**
Abre una terminal de PowerShell como administrador y ejecuta el siguiente comando nativo de Windows:
```powershell
winget install Gyan.FFmpeg
```
*Una vez instalado, reinicia tu terminal para que se apliquen los cambios.*

#### **Instalación Manual en Windows:**
1. Descarga el build binario oficial de FFmpeg desde [FFmpeg Builds](https://www.gyan.dev/ffmpeg/builds/).
2. Extrae la carpeta en un lugar seguro (por ejemplo, `C:\ffmpeg`).
3. Añade la ruta de la carpeta `bin` (ej. `C:\ffmpeg\bin`) a las **Variables de Entorno del Sistema** dentro de la variable `PATH`.

#### **Verificación de FFmpeg:**
Verifica que el sistema reconozca FFmpeg ejecutando en tu terminal:
```powershell
ffmpeg -version
```

---

## 🚀 Instalación Paso a Paso (Instalación Limpia)

Dado que las carpetas de entornos virtuales y configuraciones personales están protegidas en el archivo `.gitignore`, sigue este orden riguroso para instalar el proyecto en tu nuevo dispositivo:

### Paso 1: Clonar el Repositorio
Clona el repositorio desde GitHub en tu nuevo dispositivo y entra a la carpeta del proyecto:
```powershell
git clone https://github.com/GustavoEngineer/mp3dowloaderProject.git
cd mp3dowloaderProject
```

### Paso 2: Crear el Entorno Virtual de Python
Crea un entorno virtual limpio aislado de las librerías globales del sistema:
```powershell
python -m venv venv
```

### Paso 3: Activar el Entorno Virtual

*   **En Windows (PowerShell):**
    ```powershell
    .\venv\Scripts\Activate.ps1
    ```
*   **En Windows (Símbolo del Sistema / CMD):**
    ```cmd
    .\venv\Scripts\activate.bat
    ```
*   **En macOS / Linux:**
    ```bash
    source venv/bin/activate
    ```

> 💡 *Sabrás que el entorno se activó porque verás `(venv)` al inicio de la línea de tu consola.*

### Paso 4: Instalar las Dependencias de Python
Con el entorno virtual activado, instala todas las librerías y dependencias requeridas ejecutando:
```powershell
pip install -r requirements.txt
```

---

## 🎵 Ejecución de la Aplicación

Para iniciar la aplicación, asegúrate de tener el entorno virtual activado y ejecuta:
```powershell
python src/main.py
```

*O si estás en Windows, puedes hacer doble clic directamente sobre el script acelerador de arranque:*
* **[mp3app.bat](file:///c:/Users/Gustavo/Documents/mp3dowloaderProject/mp3app.bat)**

---

## 📂 Estructura Principal del Proyecto

Una vez completada la instalación, tu espacio de trabajo se verá estructurado de la siguiente forma:

*   **`src/`**: Código fuente de la aplicación.
    *   `main.py`: Punto de entrada de la aplicación.
    *   `frontend/`: Interfaz gráfica oscura premium (Consola interactiva, Logs, Árbol del Vault).
    *   `backend/`: Lógica de negocio, base de datos de historial y descargas con `yt-dlp`.
*   **`downloads/`**: Carpeta física del Vault donde se descargan y organizan los álbumes y canciones.
*   **`docs/`**: Documentación de desarrollo e implementación técnica.
*   **`exported_songs.json`**: Registro dinámico de canciones exportadas para el formateo gris del árbol.
*   **`requirements.txt`**: Librerías de Python requeridas para la app.

---

## 📊 Guía Rápida de Comandos de Consola (Prefix-Free)

La consola interactiva integrada admite los siguientes comandos con navegación contextual inteligente:

| Comando | Parámetros / Variantes | Descripción |
| :--- | :--- | :--- |
| **`help`** | *(ninguno)* | Muestra la tabla premium de ayuda en pantalla. |
| **`wifi`** | *(ninguno)* | Abre el panel de conexiones Wi-Fi nativo de Windows. |
| **`clear`** | *(ninguno)* | Limpia la consola y los registros de pantalla. |
| **`exit`** | *(ninguno)* | Cierra la aplicación de forma segura. |
| **`nav`** | `--raiz` \| `--sin-album` \| `--album <nombre>` | Navega contextual al nivel raíz, Sin Álbum o álbum específico. |
| **`back`** | *(ninguno)* | Vuelve al directorio de nivel anterior (de álbum a raíz). |
| **`create`** | `--album <nombre>` | Crea un nuevo álbum físico en disco. |
| **`edit`** | `--album-name <nuevo_nombre>` | Renombra el álbum en el que estás posicionado. |
| | `--song-name <num> <nuevo_nombre>` | Edita el nombre del archivo y metadata ID3 de la canción. |
| | `--song-album <num> <nuevo_album>` | Mueve físicamente una canción a otro álbum existente. |
| | `--song-artist <num> <nuevo_artista>` | Edita la metadata ID3 del artista de la canción. |
| **`export`** | `--song <num>` \| `--song <num1,num2>` | Exporta una o varias canciones a una carpeta externa mediante interfaz visual. |
| | `--song-all` | Exporta todas las canciones del álbum actual a una carpeta externa. |
| **`rm`** | `--song <num>` \| `--song <num1,num2>` | Elimina una o varias canciones del álbum actual. |
| | `--song-all` | Elimina todas las canciones del álbum actual físicamente. |
| | `--album` | Elimina el álbum actual completo con sus canciones físicas. |

> ⚠️ *Los comandos de edición (`edit`), exportación (`export`) y eliminación (`rm`) marcados con navegación requieren que te encuentres posicionado en el álbum correspondiente previamente mediante el comando `nav`.*

---

Disfruta de una organización musical ultra rápida y premium con **mp3DL Project**. 🚀
