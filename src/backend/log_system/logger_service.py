import datetime

class LoggerService:
    """Servicio de backend para registrar y centralizar acciones de la aplicación (RF-014, RF-016)."""
    
    def __init__(self, default_route: str = "C:\\Users\\Gustavo\\Documents\\mp3dowloaderProject"):
        self.default_route = default_route
        self.logs_history = []

    def log(self, level: str, message: str, route: str = None) -> dict:
        """Registra una acción en la terminal.
        
        Soporta niveles de logs permitidos (RF-016): INFO, SUCCESS, WARN, FAILED.
        Retorna el diccionario del registro formateado.
        """
        level_upper = level.upper()
        if level_upper not in ("INFO", "SUCCESS", "WARN", "FAILED"):
            level_upper = "INFO"

        active_route = route if route is not None else self.default_route
        time_str = datetime.datetime.now().strftime("%H:%M:%S")

        log_record = {
            "time": time_str,
            "route": active_route,
            "level": level_upper,
            "message": message
        }
        
        self.logs_history.append(log_record)
        return log_record

    def clear(self) -> None:
        """Limpia todo el historial de logs (RF-019)."""
        self.logs_history.clear()
