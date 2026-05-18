import customtkinter as ctk
import threading
from src.backend.top_bar.network_service import (
    check_internet_connection,
    get_wifi_network_name
)
from .connection_status import ConnectionStatusBadge
from .wifi_badge import WifiBadge
from .date_label import DateLabel

class TopBar(ctk.CTkFrame):
    """Contenedor de barra superior premium con fondo gris (default #1E1E1E)
    que coordina de forma modular los distintos componentes de red y fecha.
    """
    
    def __init__(
        self, 
        parent, 
        bg_color="#1E1E1E",  # Fondo gris premium por defecto
        text_color="#EDEDED", 
        gray_color="#808080", 
        red_color="#CC5555",
        blue_color="#6BA3CC"
    ):
        super().__init__(parent, fg_color=bg_color, corner_radius=0, height=44)
        self.pack_propagate(False)
        
        self.bg_color = bg_color
        self.text_color = text_color
        self.gray_color = gray_color
        self.red_color = red_color
        self.blue_color = blue_color

        # ── ESQUINA IZQUIERDA ─────────────────────────────────────────────────
        
        # Badge de Estado de Conexión (RF-001, RF-002)
        self.status_badge = ConnectionStatusBadge(
            self, 
            blue_color=self.blue_color, 
            red_color=self.red_color
        )
        self.status_badge.pack(side="left", padx=15, pady=8)

        # ── ESQUINA DERECHA ───────────────────────────────────────────────────

        # Fecha actual (RF-005) - Formato: Mes Día, Año
        self.date_label = DateLabel(self, blue_color=self.blue_color)
        self.date_label.pack(side="right", padx=(10, 15))

        # Badge de red Wi-Fi (RF-003, RF-004)
        self.wifi_badge = WifiBadge(
            self, 
            gray_color=self.gray_color, 
            red_color=self.red_color
        )
        self.wifi_badge.pack(side="right", padx=10, pady=8)

        # Iniciar bucle de verificación de red en segundo plano
        self._network_loop()

    def _network_loop(self):
        """Hilo asíncrono secundario para consultar el estado de la red sin trabar la UI."""
        def check():
            is_connected = check_internet_connection()
            wifi_name = get_wifi_network_name() if is_connected else None
            self.after(0, lambda: self._update_network_ui(is_connected, wifi_name))

        threading.Thread(target=check, daemon=True).start()
        # Repetir chequeo cada 5 segundos
        self.after(5000, self._network_loop)

    def _update_network_ui(self, is_connected: bool, wifi_name: str | None):
        """Notifica a los badges las actualizaciones de red."""
        self.status_badge.update_status(is_connected)
        self.wifi_badge.update_wifi(is_connected, wifi_name)
