class BaseCommand:
    """Clase base de la cual deben heredar todos los comandos modulares."""
    
    def __init__(self, name: str, description: str):
        self.name = name
        self.description = description

    def execute(self, *args, **kwargs) -> None:
        """Método abstracto que implementará la lógica de ejecución del comando."""
        raise NotImplementedError("El comando debe implementar su propio método execute.")
