from .base_command import BaseCommand

class BackCommand(BaseCommand):
    """Comando back: Permite volver a la carpeta o nivel anterior en el Vault."""
    
    def __init__(self):
        super().__init__(
            name="back",
            description="Vuelve a la carpeta o nivel anterior en el Vault"
        )

    def execute(self, *args, **kwargs) -> None:
        # Se maneja en la UI dinámicamente
        pass
