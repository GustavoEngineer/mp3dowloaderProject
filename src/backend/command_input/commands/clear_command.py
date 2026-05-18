from .base_command import BaseCommand

class ClearCommand(BaseCommand):
    """Comando clear: Limpia el historial del terminal."""
    
    def __init__(self):
        super().__init__(
            name="clear",
            description="Limpia la pantalla de la terminal"
        )

    def execute(self, *args, **kwargs) -> None:
        # Se maneja en la UI dinámicamente
        pass
