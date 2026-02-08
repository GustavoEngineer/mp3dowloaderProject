# 🚀 Guía de Deployment en Leapcell

## 📋 Descripción

Leapcell es una plataforma de deployment moderna que soporta aplicaciones Python/Flask directamente desde GitHub. **No requiere tarjeta de crédito** y ofrece un plan gratuito generoso.

---

## ✅ Ventajas de Leapcell

- ✅ **Sin tarjeta de crédito** requerida
- ✅ **Deployment automático** desde GitHub
- ✅ **Soporta Docker** (FFmpeg funcionará)
- ✅ **Plan gratuito** generoso
- ✅ **HTTPS automático**
- ✅ **Fácil configuración**

---

## 📦 Requisitos Previos

1. **Cuenta en GitHub**
   - Tu código debe estar en un repositorio de GitHub

2. **Cuenta en Leapcell**
   - Regístrate en [leapcell.io](https://leapcell.io)

---

## 🔧 Paso 1: Preparar el Repositorio de GitHub

### 1.1 Inicializar Git (si no lo has hecho)

```powershell
# Desde c:\Room\ItsMe\mp3dowloaderProject
git init
git add .
git commit -m "Initial commit - YouTube to MP3 Downloader"
```

### 1.2 Crear Repositorio en GitHub

1. Ve a [github.com](https://github.com) y crea un nuevo repositorio
2. Nómbralo: `youtube-mp3-downloader` (o el nombre que prefieras)
3. **NO inicialices** con README, .gitignore, o licencia

### 1.3 Conectar y Subir el Código

```powershell
# Reemplaza 'tu-usuario' con tu nombre de usuario de GitHub
git remote add origin https://github.com/tu-usuario/youtube-mp3-downloader.git
git branch -M main
git push -u origin main
```

---

## 🌐 Paso 2: Configurar Leapcell

### 2.1 Crear Cuenta en Leapcell

1. Ve a [leapcell.io](https://leapcell.io)
2. Haz clic en **"Sign Up"** o **"Get Started"**
3. Regístrate con GitHub (recomendado) o email

### 2.2 Conectar GitHub

1. En el dashboard de Leapcell, haz clic en **"New Project"**
2. Selecciona **"Import from GitHub"**
3. Autoriza a Leapcell para acceder a tus repositorios
4. Selecciona el repositorio `youtube-mp3-downloader`

### 2.3 Configurar el Proyecto

Leapcell detectará automáticamente que es una aplicación Python. Configura:

**Build Settings:**
- **Framework**: `Docker` (selecciona esta opción)
- **Dockerfile Path**: `Dockerfile` (ya lo tienes)
- **Build Command**: (déjalo vacío, Docker lo maneja)

**Environment Variables:**
- **PORT**: `8080` (ya está en el Dockerfile)

**Deploy Settings:**
- **Branch**: `main`
- **Auto Deploy**: ✅ Activado (para deployments automáticos)

---

## 📝 Paso 3: Verificar Archivos del Proyecto

Asegúrate de que tu repositorio tenga estos archivos:

```
mp3dowloaderProject/
├── backend/
│   ├── app.py
│   ├── templates/
│   │   └── index.html
│   └── static/
│       └── style.css
├── Dockerfile          ✅ Ya existe
├── requirements.txt    ✅ Ya existe
├── .dockerignore       ✅ Ya existe
└── .gitignore          ⚠️ Crear si no existe
```

### Crear `.gitignore` (si no existe)

```gitignore
# Python
__pycache__/
*.py[cod]
*$py.class
*.so
.Python
env/
venv/
ENV/
.venv

# Flask
instance/
.webassets-cache

# Archivos temporales
backend/downloads/
*.mp3
*.m4a
*.webm

# IDE
.vscode/
.idea/
*.swp
*.swo

# OS
.DS_Store
Thumbs.db

# Deployment
fly.toml
DEPLOYMENT.md
```

---

## 🚀 Paso 4: Deploy

### Opción A: Deploy desde Leapcell Dashboard

1. En Leapcell, haz clic en **"Deploy"**
2. Espera a que el build termine (2-5 minutos)
3. Verás logs en tiempo real del proceso

### Opción B: Deploy Automático (Push to Deploy)

Cada vez que hagas `git push` a la rama `main`, Leapcell desplegará automáticamente:

```powershell
# Hacer cambios en el código
git add .
git commit -m "Update: descripción de cambios"
git push
```

---

## ✅ Paso 5: Verificar el Deployment

### 5.1 Ver el Estado

En el dashboard de Leapcell verás:
- **Status**: Building → Running
- **URL**: `https://tu-app.leapcell.app`

### 5.2 Probar la Aplicación

1. Haz clic en la URL de tu app
2. Deberías ver la interfaz del YouTube MP3 Downloader
3. Prueba descargar un video de YouTube

### 5.3 Ver Logs

En Leapcell dashboard:
- Ve a la sección **"Logs"**
- Verás los logs en tiempo real de tu aplicación

---

## 🔧 Comandos Git Útiles

### Subir cambios:
```powershell
git add .
git commit -m "Descripción del cambio"
git push
```

### Ver estado:
```powershell
git status
```

### Ver historial:
```powershell
git log --oneline
```

### Crear rama para testing:
```powershell
git checkout -b testing
git push -u origin testing
```

---

## 🐛 Solución de Problemas

### Error: "Build Failed"
**Causa**: Problema con el Dockerfile o dependencias

**Solución**:
1. Revisa los logs de build en Leapcell
2. Verifica que `requirements.txt` esté correcto
3. Asegúrate de que el Dockerfile esté en la raíz del repo

### Error: "Application Crashed"
**Causa**: Error en el código o puerto incorrecto

**Solución**:
1. Revisa los logs de runtime
2. Verifica que el puerto sea `8080` en el Dockerfile
3. Asegúrate de que `app.py` no tenga errores

### FFmpeg no funciona
**Causa**: Dockerfile no instaló FFmpeg correctamente

**Solución**:
El Dockerfile actual ya incluye FFmpeg. Si hay problemas:
```dockerfile
# Verifica que esta línea esté en el Dockerfile
RUN apt-get update && apt-get install -y ffmpeg
```

### Git push rechazado
**Causa**: Cambios remotos no sincronizados

**Solución**:
```powershell
git pull --rebase
git push
```

---

## 🔄 Actualizaciones Futuras

### Workflow Normal:
1. Hacer cambios en el código localmente
2. Probar localmente: `python backend/app.py`
3. Commit y push:
   ```powershell
   git add .
   git commit -m "Descripción del cambio"
   git push
   ```
4. Leapcell desplegará automáticamente

---

## 💰 Plan Gratuito de Leapcell

### Incluye:
- **Deployments ilimitados**
- **HTTPS automático**
- **Custom domains** (opcional)
- **Auto-scaling básico**
- **Logs en tiempo real**

### Límites:
- Consulta la documentación de Leapcell para límites actuales
- Generalmente suficiente para proyectos personales

---

## 🌍 Dominio Personalizado (Opcional)

### En Leapcell Dashboard:
1. Ve a **"Settings"** → **"Domains"**
2. Agrega tu dominio personalizado
3. Configura los DNS según las instrucciones

---

## 📊 Monitoreo

### Dashboard de Leapcell:
- **Deployments**: Historial de deployments
- **Logs**: Logs en tiempo real
- **Metrics**: CPU, memoria, requests
- **Settings**: Configuración y variables de entorno

---

## ✅ Checklist de Deployment

- [ ] Crear repositorio en GitHub
- [ ] Subir código a GitHub
- [ ] Crear cuenta en Leapcell
- [ ] Conectar GitHub con Leapcell
- [ ] Importar repositorio
- [ ] Configurar como proyecto Docker
- [ ] Hacer deploy
- [ ] Verificar que la app funcione
- [ ] Probar descarga de YouTube
- [ ] Verificar que FFmpeg funcione

---

## 🎯 Resumen de Comandos

### Setup Inicial:
```powershell
# Inicializar Git
git init
git add .
git commit -m "Initial commit"

# Conectar con GitHub
git remote add origin https://github.com/tu-usuario/youtube-mp3-downloader.git
git branch -M main
git push -u origin main
```

### Actualizaciones:
```powershell
git add .
git commit -m "Update: descripción"
git push
```

---

## 📚 Recursos

- [Leapcell Documentation](https://docs.leapcell.io)
- [GitHub Docs](https://docs.github.com)
- [Git Cheat Sheet](https://education.github.com/git-cheat-sheet-education.pdf)

---

## 🎉 ¡Listo!

Tu aplicación YouTube to MP3 estará desplegada en Leapcell con:
- ✅ FFmpeg instalado (vía Docker)
- ✅ HTTPS automático
- ✅ Deploy automático con git push
- ✅ Sin tarjeta de crédito requerida
- ✅ Plan gratuito
