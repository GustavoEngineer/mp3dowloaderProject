from .base_command import BaseCommand

class HelpCommand(BaseCommand):
    """Comando help: Muestra el menú interactivo de ayuda de comandos."""
    
    def __init__(self):
        super().__init__(
            name="help",
            description="Muestra el menú de ayuda de MP3DL"
        )

    def execute(self, *args, **kwargs) -> None:
        # Se maneja en la UI dinámicamente o mediante hooks
        pass
