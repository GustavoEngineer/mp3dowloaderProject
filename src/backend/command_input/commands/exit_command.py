import sys
from .base_command import BaseCommand

class ExitCommand(BaseCommand):
    """Comando exit: Cierra y sale con éxito de la aplicación."""
    
    def __init__(self):
        super().__init__(
            name="exit",
            description="Sale con éxito de la aplicación"
        )

    def execute(self, *args, **kwargs) -> None:
        sys.exit(0)
