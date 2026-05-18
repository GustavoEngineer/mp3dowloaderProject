import socket
import subprocess

def check_internet_connection() -> bool:
    """Verifica si hay una conexión activa a internet.
    Intenta conectar a un DNS público confiable con un tiempo de espera de 2 segundos.
    """
    try:
        # Intentar conectar a Cloudflare DNS (1.1.1.1) en el puerto 53 (DNS)
        socket.setdefaulttimeout(2.0)
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.connect(("1.1.1.1", 53))
        s.close()
        return True
    except Exception:
        pass
    return False


def get_wifi_network_name() -> str | None:
    """Obtiene el nombre (SSID) de la conexión de red inalámbrica o cableada activa.
    Usa el cmdlet nativo de PowerShell Get-NetConnectionProfile.
    """
    try:
        # Usar CREATE_NO_WINDOW para evitar que destellen terminales PowerShell en segundo plano
        startupinfo = subprocess.STARTUPINFO()
        startupinfo.dwFlags |= subprocess.STARTF_USESHOWWINDOW
        
        result = subprocess.run(
            ["powershell", "-NoProfile", "-Command", "Get-NetConnectionProfile -ErrorAction SilentlyContinue | Select-Object -ExpandProperty Name"],
            capture_output=True,
            text=True,
            encoding="utf-8",
            errors="ignore",
            startupinfo=startupinfo,
            creationflags=subprocess.CREATE_NO_WINDOW
        )
        name = result.stdout.strip()
        if name:
            return name
    except Exception:
        pass
    return None


def open_wifi_settings() -> None:
    """Abre la pantalla de configuración de Wi-Fi de Windows nativa."""
    try:
        startupinfo = subprocess.STARTUPINFO()
        startupinfo.dwFlags |= subprocess.STARTF_USESHOWWINDOW
        
        # Abre la página de configuración de Wi-Fi de Windows nativa de forma asíncrona
        subprocess.Popen(
            ["cmd", "/c", "start ms-settings:network-wifi"],
            startupinfo=startupinfo,
            creationflags=subprocess.CREATE_NO_WINDOW
        )
    except Exception:
        pass
