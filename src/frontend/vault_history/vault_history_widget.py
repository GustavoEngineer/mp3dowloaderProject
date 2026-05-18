import tkinter as tk
from src.frontend.vault_history.vault_tab import VaultTab
from src.frontend.vault_history.history_tab import HistoryTab

class VaultHistoryWidget(tk.Frame):
    """Componente visual contenedor que agrupa y conmuta las pestañas VAULT e HISTORY (RF-020 al RF-029)."""
    
    def __init__(self, parent, vault_service, history_service, on_route_changed, bg_color="#0D0D0D"):
        super().__init__(parent, bg=bg_color)
        self.vault_service = vault_service
        self.history_service = history_service
        self.on_route_changed = on_route_changed
        self.bg_color = bg_color
        
        # 1. Cabecera de Pestañas (Tab Header Frame)
        self.header_frame = tk.Frame(self, bg="#080808", height=65)
        self.header_frame.pack(fill="x", side="top")
        self.header_frame.pack_propagate(False)
        
        # Grid para dividir la cabecera en dos partes iguales (50% cada una)
        self.header_frame.grid_columnconfigure(0, weight=1)
        self.header_frame.grid_columnconfigure(1, weight=1)
        self.header_frame.grid_rowconfigure(0, weight=1)
        
        # Pestaña VAULT (Columna 0)
        self.vault_tab_btn = tk.Frame(self.header_frame, bg="#0D0D0D", cursor="hand2")
        self.vault_tab_btn.grid(row=0, column=0, sticky="nsew")
        
        self.vault_indicator = tk.Frame(self.vault_tab_btn, bg="#6BA3CC", height=3)
        self.vault_indicator.pack(fill="x", side="top")
        
        self.vault_label = tk.Label(
            self.vault_tab_btn,
            text="|\\ \\\nVAULT",
            fg="#EDEDED",
            bg="#0D0D0D",
            font=("Courier New", 10, "bold"),
            justify="center",
            pady=8
        )
        self.vault_label.pack(fill="both", expand=True)
        
        # Pestaña HISTORY (Columna 1)
        self.history_tab_btn = tk.Frame(self.header_frame, bg="#070707", cursor="hand2")
        self.history_tab_btn.grid(row=0, column=1, sticky="nsew")
        
        self.history_indicator = tk.Frame(self.history_tab_btn, bg="#070707", height=3)
        self.history_indicator.pack(fill="x", side="top")
        
        self.history_label = tk.Label(
            self.history_tab_btn,
            text="🕒\nHISTORY",
            fg="#404040",
            bg="#070707",
            font=("Courier New", 10, "bold"),
            justify="center",
            pady=8
        )
        self.history_label.pack(fill="both", expand=True)
        
        # 2. Contenedor de Contenido (Content Frame)
        self.content_frame = tk.Frame(self, bg=self.bg_color)
        self.content_frame.pack(fill="both", expand=True)
        
        # Instanciar las pestañas internas
        self.vault_tab = VaultTab(self.content_frame, self.vault_service, self.on_route_changed, bg_color)
        self.history_tab = HistoryTab(self.content_frame, self.history_service, bg_color)
        
        # Mostrar VAULT por defecto
        self.active_tab = "vault"
        self.vault_tab.pack(fill="both", expand=True)
        
        # Enlazar clics para conmutar pestañas
        self.vault_label.bind("<Button-1>", lambda e: self.switch_tab("vault"))
        self.vault_tab_btn.bind("<Button-1>", lambda e: self.switch_tab("vault"))
        
        self.history_label.bind("<Button-1>", lambda e: self.switch_tab("history"))
        self.history_tab_btn.bind("<Button-1>", lambda e: self.switch_tab("history"))
        
    def switch_tab(self, tab_name: str):
        """Conmuta visualmente entre la pestaña VAULT e HISTORY, refrescando sus contenidos."""
        if tab_name == self.active_tab:
            return
            
        self.active_tab = tab_name
        
        if tab_name == "vault":
            # Cambiar estilos de cabecera activa
            self.vault_tab_btn.configure(bg="#0D0D0D")
            self.vault_label.configure(fg="#EDEDED", bg="#0D0D0D")
            self.vault_indicator.configure(bg="#6BA3CC")
            
            # Cambiar estilos de cabecera inactiva
            self.history_tab_btn.configure(bg="#070707")
            self.history_label.configure(fg="#404040", bg="#070707")
            self.history_indicator.configure(bg="#070707")
            
            # Conmutar contenido
            self.history_tab.pack_forget()
            self.vault_tab.pack(fill="both", expand=True)
            self.vault_tab.refresh()
            
        else:
            # Cambiar estilos de cabecera activa
            self.history_tab_btn.configure(bg="#0D0D0D")
            self.history_label.configure(fg="#EDEDED", bg="#0D0D0D")
            self.history_indicator.configure(bg="#6BA3CC")
            
            # Cambiar estilos de cabecera inactiva
            self.vault_tab_btn.configure(bg="#070707")
            self.vault_label.configure(fg="#404040", bg="#070707")
            self.vault_indicator.configure(bg="#070707")
            
            # Conmutar contenido
            self.vault_tab.pack_forget()
            self.history_tab.pack(fill="both", expand=True)
            self.history_tab.refresh()
            
    def refresh_all(self):
        """Refresca ambas pestañas al completarse o fallar una descarga (RF-023)."""
        self.vault_tab.refresh()
        self.history_tab.refresh()
