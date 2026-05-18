from .base_command import BaseCommand

class EditCommand(BaseCommand):
    """Comando edit: Permite editar álbumes y canciones (RF-040, RF-041)."""
    
    def __init__(self):
        super().__init__(
            name="edit",
            description="Editar un álbum o canción. Uso: edit --album-name <viejo> <nuevo> | edit --song-name <album> <num> <nuevo_nombre>"
        )

    def execute(self, *args, **kwargs) -> None:
        pass
