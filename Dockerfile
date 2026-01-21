# Usa una imagen base de Python
FROM python:3.11-slim

# Instalar FFmpeg y Node.js (necesarios para yt-dlp)
RUN apt-get update && apt-get install -y \
    ffmpeg \
    curl \
    && curl -fsSL https://deb.nodesource.com/setup_18.x | bash - \
    && apt-get install -y nodejs \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Configurar el directorio de trabajo
WORKDIR /app

# Copiar archivos de requerimientos e instalar
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copiar el resto del código
COPY . .

# Comando para ejecutar la app (ajusta 'api.py' al nombre de tu archivo)
CMD ["python", "api.py"]
