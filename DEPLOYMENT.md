# 🚀 Guía de Deployment en Fly.io

## 📋 Requisitos Previos

1. **Cuenta en Fly.io**
   - Regístrate en [fly.io](https://fly.io/app/sign-up)
   - Es gratis para empezar (incluye recursos gratuitos)

2. **Instalar Fly CLI**
   
   **Windows (PowerShell):**
   ```powershell
   pwsh -Command "iwr https://fly.io/install.ps1 -useb | iex"
   ```
   
   **macOS/Linux:**
   ```bash
   curl -L https://fly.io/install.sh | sh
   ```

3. **Verificar instalación:**
   ```bash
   flyctl version
   ```

---

## 🔐 Paso 1: Autenticación

```bash
flyctl auth login
```

Esto abrirá tu navegador para iniciar sesión.

---

## 🎯 Paso 2: Preparar el Proyecto

### Estructura Actual
```
mp3Project/
├── backend/
│   ├── app.py
│   ├── templates/
│   ├── static/
│   └── ...
├── Dockerfile
├── fly.toml
├── .dockerignore
└── requirements.txt
```

### Verificar archivos creados:
- ✅ `Dockerfile` - Configuración de Docker con FFmpeg
- ✅ `fly.toml` - Configuración de Fly.io
- ✅ `.dockerignore` - Archivos a ignorar en el build
- ✅ `requirements.txt` - Dependencias Python

---

## 🚀 Paso 3: Crear la Aplicación en Fly.io

Desde el directorio raíz del proyecto (`mp3Project/`):

```bash
flyctl launch
```

**Responde a las preguntas:**
- **App name**: Presiona Enter para usar el nombre del `fly.toml` o elige uno nuevo
- **Region**: Elige la región más cercana (ej: `mia` para Miami)
- **Would you like to set up a Postgresql database?**: `No`
- **Would you like to set up an Upstash Redis database?**: `No`
- **Would you like to deploy now?**: `No` (lo haremos manualmente)

---

## ⚙️ Paso 4: Configurar Variables de Entorno (Opcional)

Si necesitas configurar variables de entorno:

```bash
flyctl secrets set VARIABLE_NAME=value
```

Por ahora no es necesario.

---

## 📦 Paso 5: Deploy Inicial

```bash
flyctl deploy
```

Este comando:
1. Construye la imagen Docker
2. Instala FFmpeg y dependencias
3. Sube la imagen a Fly.io
4. Despliega la aplicación

**Tiempo estimado**: 2-5 minutos

---

## ✅ Paso 6: Verificar el Deployment

### Ver el estado:
```bash
flyctl status
```

### Ver logs en tiempo real:
```bash
flyctl logs
```

### Abrir la aplicación:
```bash
flyctl open
```

Esto abrirá tu aplicación en el navegador: `https://tu-app.fly.dev`

---

## 🔍 Paso 7: Verificar Funcionalidad

1. **Accede a tu app**: `https://tu-app.fly.dev`
2. **Prueba con un video de YouTube**
3. **Verifica que la descarga funcione**

---

## 📊 Comandos Útiles

### Ver información de la app:
```bash
flyctl info
```

### Ver logs:
```bash
flyctl logs
```

### Escalar recursos (si es necesario):
```bash
flyctl scale vm shared-cpu-1x --memory 1024
```

### Reiniciar la app:
```bash
flyctl apps restart
```

### Ver métricas:
```bash
flyctl dashboard
```

### SSH a la máquina:
```bash
flyctl ssh console
```

---

## 🔄 Actualizaciones Futuras

Cuando hagas cambios en el código:

```bash
# 1. Hacer cambios en el código
# 2. Desplegar nuevamente
flyctl deploy
```

---

## 💰 Costos y Límites

### Plan Gratuito (Hobby):
- **3 máquinas compartidas** (256MB RAM cada una)
- **160GB de transferencia** por mes
- **3GB de almacenamiento persistente**

### Tu configuración actual:
- **1 máquina**: 512MB RAM, 1 CPU compartida
- **Auto-scaling**: Se apaga cuando no hay tráfico (ahorra recursos)
- **Costo estimado**: Gratis dentro del plan Hobby

---

## 🐛 Solución de Problemas

### Error: "failed to fetch an image"
```bash
flyctl deploy --local-only
```

### Error: "health check failed"
Verifica que el endpoint `/health` esté funcionando:
```bash
flyctl logs
```

### La app no responde:
```bash
# Ver estado
flyctl status

# Reiniciar
flyctl apps restart
```

### FFmpeg no funciona:
El Dockerfile ya incluye FFmpeg. Si hay problemas:
```bash
# SSH a la máquina
flyctl ssh console

# Verificar FFmpeg
ffmpeg -version
```

---

## 🔒 Seguridad

### HTTPS automático:
Fly.io proporciona certificados SSL automáticos.

### Variables sensibles:
Usa `flyctl secrets` para variables de entorno sensibles:
```bash
flyctl secrets set API_KEY=tu_clave_secreta
```

---

## 📈 Monitoreo

### Dashboard web:
```bash
flyctl dashboard
```

### Métricas en tiempo real:
- CPU usage
- Memory usage
- Request count
- Response times

---

## 🌍 Dominios Personalizados (Opcional)

### Agregar dominio propio:
```bash
flyctl certs add tudominio.com
```

Luego configura los DNS según las instrucciones.

---

## 🎯 Resumen de Comandos Esenciales

```bash
# Autenticación
flyctl auth login

# Crear app (primera vez)
flyctl launch

# Desplegar
flyctl deploy

# Ver logs
flyctl logs

# Abrir app
flyctl open

# Ver estado
flyctl status

# Dashboard
flyctl dashboard
```

---

## ✅ Checklist de Deployment

- [ ] Instalar Fly CLI
- [ ] Autenticarse con `flyctl auth login`
- [ ] Ejecutar `flyctl launch` desde `mp3Project/`
- [ ] Configurar región
- [ ] Ejecutar `flyctl deploy`
- [ ] Verificar logs con `flyctl logs`
- [ ] Abrir app con `flyctl open`
- [ ] Probar descarga de YouTube
- [ ] Verificar que FFmpeg funciona

---

## 📚 Recursos Adicionales

- [Documentación de Fly.io](https://fly.io/docs/)
- [Fly.io Pricing](https://fly.io/docs/about/pricing/)
- [Fly.io Status](https://status.flyio.net/)

---

## 🎉 ¡Listo!

Tu aplicación YouTube to MP3 ahora está desplegada en Fly.io con:
- ✅ FFmpeg instalado
- ✅ HTTPS automático
- ✅ Auto-scaling
- ✅ Health checks
- ✅ Logs en tiempo real
