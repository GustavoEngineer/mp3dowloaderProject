@echo off

REM Ir a la carpeta del proyecto
cd /d "C:\Users\Gustavo\Documents\mp3dowloaderProject"

REM Activar entorno virtual
call venv\Scripts\activate

REM Ejecutar aplicación
python src\main.py

pause