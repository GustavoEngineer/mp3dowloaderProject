from .base_command import BaseCommand

class NavCommand(BaseCommand):
    """Comando nav: Permite navegar entre álbumes y carpeta raíz."""
    
    def __init__(self):
        super().__init__(
            name="nav",
            description="Navega a un álbum, sin-album o raíz. Opciones: --album <nombre>, --sin-album, --raiz"
        )

    def execute(self, *args, **kwargs) -> None:
        pass
