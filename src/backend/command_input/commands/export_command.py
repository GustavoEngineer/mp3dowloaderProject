from .base_command import BaseCommand

class ExportCommand(BaseCommand):
    """Comando export: Permite exportar canciones a una carpeta externa (RF-044)."""
    
    def __init__(self):
        super().__init__(
            name="export",
            description="Exporta una canción o todas a una carpeta elegida"
        )

    def execute(self, *args, **kwargs) -> None:
        # Se maneja en la UI dinámicamente
        pass
