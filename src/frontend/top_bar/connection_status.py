import customtkinter as ctk

class ConnectionStatusBadge(ctk.CTkFrame):
    """Badge para mostrar el estado de conexión del sistema (RF-001, RF-002)."""
    
    def __init__(self, parent, blue_color="#6BA3CC", red_color="#CC5555"):
        super().__init__(
            parent, 
            fg_color="transparent", 
            border_width=1, 
            border_color="#2A2A2A", 
            corner_radius=6,
            height=28
        )
        self.pack_propagate(True)
        self.blue_color = blue_color
        self.red_color = red_color

        self.label = ctk.CTkLabel(
            self, 
            text="● SYSTEM_ONLINE", 
            text_color=self.blue_color, 
            font=("Courier New", 13, "bold"),
            padx=12
        )
        self.label.pack(expand=True, fill="both")

    def update_status(self, is_connected: bool):
        """Actualiza visualmente el badge según el estado de conexión."""
        if is_connected:
            self.label.configure(
                text="● SYSTEM_ONLINE", 
                text_color=self.blue_color
            )
            self.configure(border_color="#2A3F5F")
        else:
            self.label.configure(
                text="● SYSTEM_OFFLINE", 
                text_color=self.red_color
            )
            self.configure(border_color="#5F2A2A")
