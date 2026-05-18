from .base_command import BaseCommand

class CreateCommand(BaseCommand):
    """Comando create: Permite crear nuevos álbumes (RF-040)."""
    
    def __init__(self):
        super().__init__(
            name="create",
            description="Crear un nuevo álbum. Uso: create --album <nombre>"
        )

    def execute(self, *args, **kwargs) -> None:
        pass
