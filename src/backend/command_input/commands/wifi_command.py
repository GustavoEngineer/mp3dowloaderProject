from .base_command import BaseCommand
from src.backend.top_bar.network_service import open_wifi_settings

class WifiCommand(BaseCommand):
    """Comando wifi: Abre la configuración nativa de Wi-Fi de Windows."""
    
    def __init__(self):
        super().__init__(
            name="wifi",
            description="Abre la configuración Wi-Fi de Windows"
        )

    def execute(self, *args, **kwargs) -> None:
        open_wifi_settings()
