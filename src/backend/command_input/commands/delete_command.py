from .base_command import BaseCommand

class DeleteCommand(BaseCommand):
    """Comando delete: Permite eliminar álbumes y canciones (RF-042, RF-043)."""
    
    def __init__(self):
        super().__init__(
            name="delete",
            description="Eliminar un álbum o canción. Uso: delete --album <nombre> | --song <nombre>"
        )

    def execute(self, *args, **kwargs) -> None:
        pass
