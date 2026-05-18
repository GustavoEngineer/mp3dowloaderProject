from src.backend.api.core.utils import is_valid_youtube_url
from .commands import COMMAND_MAP

class CommandService:
    """Servicio de backend para validar URLs e interpretar comandos de consola modulares (RF-009, RF-010, RF-011)."""
    
    @staticmethod
    def parse_input(text: str) -> dict:
        """Analiza la entrada del usuario y determina si es un comando especial, un atajo o una URL.
        
        Retorna un diccionario con la estructura:
        - Para comandos: {"type": "command", "name": "...", "command": CommandObject, "args": [...]}
        - Para atajos: {"type": "shortcut", ...}
        - Para URLs: {"type": "url", "status": "valid|invalid", "url": "..."}
        """
        text_stripped = text.strip()
        text_lower = text_stripped.lower()
        
        parts = text_stripped.split()
        cmd_candidate = parts[0].lower() if parts else ""
        args = parts[1:] if len(parts) > 1 else []
        
        # Normalizar alias de ayuda
        if cmd_candidate == "?":
            cmd_candidate = "help"
            
        # Si el candidato está en COMMAND_MAP, es un comando
        if cmd_candidate in COMMAND_MAP:
            return {
                "type": "command",
                "name": cmd_candidate,
                "command": COMMAND_MAP[cmd_candidate],
                "args": args
            }
            
        # RF-036: Comprobar si es un acceso directo de navegación case-insensitive
        from pathlib import Path
        downloads_dir = Path("C:\\Users\\Gustavo\\Documents\\mp3dowloaderProject\\downloads")
        
        if text_lower == "sinalbum":
            return {
                "type": "shortcut",
                "target": "sin_album"
            }
            
        if downloads_dir.exists():
            albums = [p.name.lower() for p in downloads_dir.iterdir() if p.is_dir() and not p.name.startswith(".")]
            if text_lower in albums:
                actual_name = next(p.name for p in downloads_dir.iterdir() if p.name.lower() == text_lower)
                return {
                    "type": "shortcut",
                    "target": "album",
                    "album_name": actual_name
                }
                
        # RF-010: Todo lo demás se interpreta como URL
        # RF-011: Validar si la URL es válida o inválida
        is_valid = is_valid_youtube_url(text_stripped)
        return {
            "type": "url",
            "status": "valid" if is_valid else "invalid",
            "url": text_stripped
        }
