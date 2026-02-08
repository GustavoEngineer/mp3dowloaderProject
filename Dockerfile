# Usar imagen oficial de Python
FROM python:3.11-slim

# Instalar FFmpeg y dependencias del sistema
RUN apt-get update && apt-get install -y \
    ffmpeg \
    && rm -rf /var/lib/apt/lists/*

# Establecer directorio de trabajo
WORKDIR /app

# Copiar requirements.txt
COPY requirements.txt .

# Instalar dependencias de Python
RUN pip install --no-cache-dir -r requirements.txt

# Copiar el código de la aplicación
COPY backend/ /app/

# Exponer el puerto
EXPOSE 8080

# Variable de entorno para el puerto
ENV PORT=8080

# Comando para ejecutar la aplicación con gunicorn
CMD ["gunicorn", "--bind", "0.0.0.0:8080", "--workers", "2", "--timeout", "120", "app:app"]
