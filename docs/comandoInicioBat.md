# Configuración de Comando Personalizado para Ejecutar la Aplicación

## Objetivo

Automatizar la ejecución de la aplicación Python mediante un único comando personalizado en Windows utilizando un archivo `.bat`.

En lugar de ejecutar manualmente:

```powershell
.\venv\Scripts\activate
python src\main.py
```

se podrá iniciar la aplicación simplemente escribiendo:

```powershell
mp3app
```

desde cualquier terminal del sistema.

---

# Requisitos

- Windows 10 / Windows 11
- Python instalado
- Entorno virtual (`venv`) configurado
- Proyecto Python funcional

---

# Estructura del Proyecto

```plaintext
mp3app/
│
├── src/
│   └── main.py
│
├── venv/
│
├── launcher/
│   └── mp3app.bat
│
└── README.md
```

---

# Paso 1 — Crear el Archivo `.bat`

Crear una carpeta llamada:

```plaintext
launcher/
```

Dentro de la carpeta crear el archivo:

```plaintext
mp3app.bat
```

---

# Paso 2 — Configurar el Launcher

Agregar el siguiente contenido al archivo `mp3app.bat`:

```bat
@echo off

REM =========================
REM MP3APP LAUNCHER
REM =========================

REM Ir al directorio del proyecto
cd /d "C:\Ruta\Completa\mp3app"

REM Activar entorno virtual
call venv\Scripts\activate

REM Ejecutar aplicación
python src\main.py

REM Mantener consola abierta
pause
```

---

# Paso 3 — Configurar la Ruta del Proyecto

Modificar la línea:

```bat
cd /d "C:\Ruta\Completa\mp3app"
```

por la ruta real del proyecto.

## Ejemplo

```bat
cd /d "C:\Users\Gustavo\Desktop\mp3app"
```

---

# Explicación del Script

## `@echo off`

Oculta los comandos internos para mostrar una consola más limpia.

---

## `cd /d`

Permite cambiar al directorio del proyecto incluso si se encuentra en otro disco.

---

## `call venv\Scripts\activate`

Activa el entorno virtual del proyecto.

El uso de `call` es obligatorio para evitar que el script se detenga después de activar el entorno virtual.

---

## `python src\main.py`

Ejecuta el archivo principal de la aplicación.

---

## `pause`

Mantiene abierta la consola para visualizar errores o mensajes.

Puede eliminarse en producción.

---

# Paso 4 — Probar el Launcher

Ejecutar manualmente:

```plaintext
launcher/mp3app.bat
```

Si la configuración es correcta:

- El entorno virtual se activará automáticamente
- La aplicación iniciará
- La consola permanecerá abierta

---

# Paso 5 — Crear un Comando Global en Windows

## Crear Carpeta de Scripts

Crear una carpeta global para comandos personalizados.

Ejemplo:

```plaintext
C:\commands
```

---

## Mover el Archivo `.bat`

Mover:

```plaintext
launcher/mp3app.bat
```

a:

```plaintext
C:\commands\mp3app.bat
```

---

# Paso 6 — Agregar la Carpeta al PATH

## Abrir Variables de Entorno

1. Presionar:

```plaintext
WIN + S
```

2. Buscar:

```plaintext
Variables de entorno
```

3. Abrir:

```plaintext
Editar las variables de entorno del sistema
```

---

## Editar PATH

1. Seleccionar:

```plaintext
Variables de entorno
```

2. Buscar:

```plaintext
Path
```

3. Seleccionar:

```plaintext
Editar
```

4. Agregar:

```plaintext
C:\commands
```

5. Guardar cambios

---

# Paso 7 — Reiniciar Terminal

Cerrar todas las terminales abiertas y volver a abrir PowerShell o CMD.

---

# Paso 8 — Ejecutar la Aplicación

Ahora la aplicación puede ejecutarse desde cualquier ubicación utilizando:

```powershell
mp3app
```

---

# Ejemplo Completo del Archivo `.bat`

```bat
@echo off

REM =========================
REM MP3APP LAUNCHER
REM =========================

cd /d "C:\Users\Gustavo\Desktop\mp3app"

call venv\Scripts\activate

python src\main.py

pause
```

---

# Buenas Prácticas Recomendadas

## Mantener el launcher separado

Se recomienda mantener los launchers dentro de:

```plaintext
launcher/
```

para separar scripts operativos del código fuente.

---

## No subir el entorno virtual a Git

Agregar al archivo `.gitignore`:

```gitignore
venv/
```

---

## Documentar rutas importantes

Mantener documentación actualizada de:

- Ruta del proyecto
- Variables de entorno
- Dependencias
- Scripts personalizados

---

# Solución de Problemas

---

## Error: `'python' no se reconoce`

### Solución

Verificar que Python esté agregado al `PATH`.

Comprobar ejecutando:

```powershell
python --version
```

---

## Error: `No se puede encontrar la ruta`

### Solución

Verificar que la ruta configurada en:

```bat
cd /d "RUTA"
```

sea correcta.

---

## Error: El entorno virtual no existe

### Solución

Crear nuevamente el entorno virtual:

```powershell
python -m venv venv
```

---

# Ventajas de esta Implementación

- Automatización de ejecución
- Inicio rápido de la aplicación
- Mejor experiencia de desarrollo
- Compatible con cualquier terminal
- Escalable para futuros scripts
- Fácil mantenimiento

---

# Futuras Mejoras

Este launcher puede evolucionar posteriormente hacia:

- CLI profesional con `argparse`
- Comandos instalables con `pip`
- Ejecutables `.exe`
- Auto-updaters
- Instaladores de Windows
- Integración con Docker
- Servicios de sistema

---

# Resultado Final

La aplicación podrá iniciarse desde cualquier terminal mediante:

```powershell
mp3app
```

sin necesidad de ejecutar manualmente:

```powershell
.\venv\Scripts\activate
python src\main.py
```

---