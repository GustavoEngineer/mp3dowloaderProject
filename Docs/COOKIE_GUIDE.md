# 🍪 Guía para Exportar Cookies de YouTube

Esta guía te muestra cómo exportar cookies de YouTube para que la aplicación pueda descargar videos sin problemas de autenticación.

---

## ¿Por Qué Necesito Cookies?

YouTube bloquea descargas automatizadas desde servidores con el error:
> "Sign in to confirm you're not a bot"

Las cookies de una sesión autenticada de YouTube permiten que la aplicación funcione como si fueras tú descargando el video.

---

## 📋 Requisitos

- Un navegador (Chrome, Firefox, Edge, etc.)
- Una cuenta de YouTube (opcional pero recomendado)
- 2-3 minutos de tu tiempo

---

## 🔧 Método 1: Usando Extensión de Navegador (Recomendado)

### Para Google Chrome / Edge

1. **Instala la extensión "Get cookies.txt LOCALLY"**
   - Ve a Chrome Web Store
   - Busca "Get cookies.txt LOCALLY"
   - Haz clic en "Agregar a Chrome"
   - [Link directo](https://chrome.google.com/webstore/detail/get-cookiestxt-locally/cclelndahbckbenkjhflpdbgdldlbecc)

2. **Inicia sesión en YouTube**
   - Ve a [youtube.com](https://youtube.com)
   - Inicia sesión con tu cuenta (si no lo has hecho)

3. **Exporta las cookies**
   - Haz clic en el ícono de la extensión (en la barra de herramientas)
   - Selecciona "Export cookies for current site"
   - Se descargará un archivo `youtube.com_cookies.txt`

4. **Renombra el archivo** (opcional)
   - Puedes renombrarlo a `cookies.txt` para mayor claridad

### Para Firefox

1. **Instala la extensión "cookies.txt"**
   - Ve a Firefox Add-ons
   - Busca "cookies.txt"
   - Haz clic en "Agregar a Firefox"
   - [Link directo](https://addons.mozilla.org/en-US/firefox/addon/cookies-txt/)

2. **Inicia sesión en YouTube**
   - Ve a [youtube.com](https://youtube.com)
   - Inicia sesión con tu cuenta

3. **Exporta las cookies**
   - Haz clic en el ícono de la extensión
   - Selecciona "Current Site"
   - Se descargará un archivo `cookies.txt`

---

## 🔧 Método 2: Manualmente desde DevTools (Avanzado)

### Pasos

1. **Abre YouTube** en tu navegador
2. **Inicia sesión** en tu cuenta
3. **Abre DevTools**
   - Windows/Linux: `F12` o `Ctrl+Shift+I`
   - Mac: `Cmd+Option+I`
4. **Ve a la pestaña "Application"** (o "Almacenamiento" en Firefox)
5. **Expande "Cookies"** en el panel izquierdo
6. **Selecciona "https://www.youtube.com"**
7. **Exporta las cookies**:
   - Copia todas las cookies manualmente
   - Crea un archivo `.txt` en formato Netscape

**Formato Netscape:**
```
# Netscape HTTP Cookie File
.youtube.com	TRUE	/	TRUE	0	CONSENT	YES+
.youtube.com	TRUE	/	FALSE	1234567890	VISITOR_INFO1_LIVE	xxx
```

⚠️ **Este método es complicado y propenso a errores. Usa el Método 1 si es posible.**

---

## 📤 Subir Cookies a la Aplicación

Una vez que tengas el archivo `cookies.txt`:

1. **Accede al panel de admin**
   - Ve a `https://tu-app.leapcell.app/admin`
   - O `http://localhost:5000/admin` si estás en local

2. **Inicia sesión**
   - Contraseña por defecto (desarrollo): `admin123`
   - En producción: usa la contraseña configurada

3. **Sube el archivo**
   - Arrastra el archivo `cookies.txt` al área de carga
   - O haz clic para seleccionarlo
   - Haz clic en "Subir Cookies"

4. **Verifica el estado**
   - Deberías ver "✅ Cookies activas"
   - Con la fecha de subida

---

## ⏰ ¿Cada Cuánto Debo Actualizar las Cookies?

Las cookies de YouTube generalmente duran **1-2 semanas**.

**Señales de que necesitas actualizar:**
- Las descargas empiezan a fallar
- Ves el error "Sign in to confirm you're not a bot"
- El mensaje de estado en `/admin` indica que las cookies son antiguas

**Proceso de actualización:**
1. Exporta cookies nuevas (2 minutos)
2. Sube a `/admin`
3. ¡Listo! Las descargas funcionarán de nuevo

---

## 🔒 Seguridad y Privacidad

### ¿Es Seguro?

- ✅ Las cookies se almacenan **solo en tu servidor**
- ✅ No se comparten con terceros
- ✅ El panel admin está protegido con contraseña
- ✅ Las cookies **no se suben a GitHub** (están en `.gitignore`)

### Recomendaciones

1. **Usa una cuenta secundaria** de YouTube si te preocupa la seguridad
2. **No compartas** tu archivo de cookies con nadie
3. **Cambia la contraseña de admin** en producción (no uses `admin123`)
4. **Elimina las cookies** del panel admin si ya no las necesitas

---

## 🐛 Solución de Problemas

### "El archivo debe ser .txt"
- Asegúrate de que el archivo tenga extensión `.txt`
- Algunos navegadores pueden agregar `.txt.txt`, renómbralo a `.txt`

### "Cookies subidas pero las descargas siguen fallando"
- Verifica que iniciaste sesión en YouTube antes de exportar
- Intenta exportar cookies nuevamente
- Asegúrate de que las cookies sean de `youtube.com` (no otro dominio)

### "No puedo encontrar la extensión"
- Busca "cookies.txt" o "get cookies" en la tienda de extensiones
- Verifica que sea una extensión confiable (con buenas reseñas)
- Usa los links directos proporcionados arriba

### "Las cookies expiraron muy rápido"
- Esto puede pasar si YouTube detecta actividad inusual
- Intenta usar una cuenta diferente
- Reduce la frecuencia de descargas

---

## 📝 Formato del Archivo de Cookies

El archivo debe estar en **formato Netscape** (`.txt`):

```
# Netscape HTTP Cookie File
# This is a generated file! Do not edit.

.youtube.com	TRUE	/	TRUE	0	CONSENT	YES+cb.20210328-17-p0.en+FX+667
.youtube.com	TRUE	/	FALSE	1735689600	VISITOR_INFO1_LIVE	abcdefghijk
.youtube.com	TRUE	/	TRUE	1735689600	LOGIN_INFO	AFmmF2swRQIhAI...
# ... más cookies
```

**Características:**
- Empieza con `# Netscape HTTP Cookie File`
- Cada línea es una cookie con campos separados por TAB
- Campos: dominio, flag, path, secure, expiration, name, value

---

## ✅ Checklist

- [ ] Instalé la extensión de cookies
- [ ] Inicié sesión en YouTube
- [ ] Exporté las cookies a un archivo `.txt`
- [ ] Accedí al panel admin (`/admin`)
- [ ] Subí el archivo de cookies
- [ ] Verifiqué que el estado muestra "Cookies activas"
- [ ] Probé descargar un video
- [ ] ¡Funciona! 🎉

---

## 🔄 Mantenimiento

### Rutina Recomendada

**Cada 1-2 semanas:**
1. Exporta cookies nuevas (2 minutos)
2. Sube a `/admin`
3. Continúa usando la app

**Cuando las descargas fallen:**
1. Ve a `/admin`
2. Verifica el estado de las cookies
3. Si son antiguas, exporta y sube nuevas

---

## 📞 Soporte

Si tienes problemas:
1. Revisa la sección "Solución de Problemas" arriba
2. Verifica los logs del servidor en Leapcell
3. Asegúrate de que el archivo de cookies esté en formato correcto
4. Intenta con una cuenta de YouTube diferente

---

## 🎯 Resumen Rápido

1. **Instala extensión** → "Get cookies.txt LOCALLY" (Chrome) o "cookies.txt" (Firefox)
2. **Inicia sesión** → youtube.com
3. **Exporta** → Haz clic en la extensión
4. **Sube** → `/admin` → Arrastra el archivo
5. **Listo** → Las descargas funcionarán por 1-2 semanas

**Tiempo total: ~2 minutos** ⏱️
