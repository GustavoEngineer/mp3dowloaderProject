import customtkinter as ctk
from datetime import datetime

class DateLabel(ctk.CTkLabel):
    """Etiqueta dinámica que muestra la fecha actual (RF-005)."""
    
    def __init__(self, parent, blue_color="#6BA3CC"):
        super().__init__(
            parent, 
            text="", 
            text_color=blue_color, 
            font=("Courier New", 13, "bold")
        )
        self._update_time()

    def _update_time(self):
        """Actualiza la fecha cada segundo."""
        now = datetime.now()
        # Formato: Mes Día, Año (ej. May 16, 2026)
        date_str = now.strftime("🕒 %b %d, %Y").upper()
        self.configure(text=date_str)
        self.after(1000, self._update_time)
