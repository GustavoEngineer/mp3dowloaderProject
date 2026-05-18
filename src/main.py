import sys
from pathlib import Path

# Añadir el directorio raíz al path para que funcione como paquete
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from src.backend.api.core.config import settings
from src.backend.api.infrastructure.audio_adapter import YtDlpAdapter
from src.backend.api.services.download_service import DownloadService
from src.frontend.ui import TerminalUI


def main():
    audio_adapter = YtDlpAdapter()
    # Por defecto se descarga a la carpeta raíz "Sin album" del Vault (RF-022)
    download_service = DownloadService(audio_adapter, settings.download_dir / "Sin album")
    
    app = TerminalUI(download_service)
    app.mainloop()


if __name__ == "__main__":
    main()
