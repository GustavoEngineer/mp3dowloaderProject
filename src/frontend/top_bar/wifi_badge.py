import customtkinter as ctk
from src.backend.top_bar.network_service import open_wifi_settings

class WifiBadge(ctk.CTkFrame):
    """Badge interactivo para mostrar el estado y nombre del Wi-Fi (RF-003, RF-004, RF-006)."""
    
    def __init__(self, parent, gray_color="#808080", red_color="#CC5555"):
        super().__init__(
            parent, 
            fg_color="transparent", 
            border_width=1, 
            border_color="#2A2A2A", 
            corner_radius=6,
            height=28,
            cursor="hand2"
        )
        self.pack_propagate(True)
        self.gray_color = gray_color
        self.red_color = red_color

        self.label = ctk.CTkLabel(
            self, 
            text="📶 WIFI: checking...", 
            text_color=self.gray_color, 
            font=("Courier New", 13, "bold"),
            padx=12,
            cursor="hand2"
        )
        self.label.pack(expand=True, fill="both")

        # Vincular clics de ratón para abrir configuración de red (RF-006)
        self.bind("<Button-1>", lambda e: self._on_click())
        self.label.bind("<Button-1>", lambda e: self._on_click())

    def update_wifi(self, is_connected: bool, wifi_name: str | None):
        """Actualiza el badge con el SSID actual o estado de desconexión."""
        if is_connected:
            if wifi_name:
                self.label.configure(
                    text=f"📶 WIFI: {wifi_name}", 
                    text_color=self.gray_color
                )
            else:
                self.label.configure(
                    text="📶 WIFI: CONECTADO", 
                    text_color=self.gray_color
                )
            self.configure(border_color="#2A3F5F")
        else:
            self.label.configure(
                text="📶 No hay conexión a internet", 
                text_color=self.red_color
            )
            self.configure(border_color="#5F2A2A")

    def _on_click(self):
        """Abre la pantalla de configuración de Wi-Fi de Windows nativa."""
        open_wifi_settings()
