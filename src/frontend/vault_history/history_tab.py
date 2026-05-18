import tkinter as tk
from src.frontend.vault_history.vault_tab import ScrollableFrame

class HistoryTab(tk.Frame):
    """Componente visual premium para la línea de tiempo del historial (RF-027 al RF-029)."""
    
    def __init__(self, parent, history_service, bg_color="#0D0D0D"):
        super().__init__(parent, bg=bg_color)
        self.history_service = history_service
        self.bg_color = bg_color
        
        # Etiqueta de Cabecera
        self.header_label = tk.Label(
            self,
            text="EXTRACTION TIMELINE",
            fg="#505050",
            bg=self.bg_color,
            font=("Courier New", 12, "bold"),
            anchor="w"
        )
        self.header_label.pack(fill="x", padx=15, pady=(10, 5))
        
        # Contenedor Scrollable
        self.scroll_container = ScrollableFrame(self, bg_color=bg_color)
        self.scroll_container.pack(fill="both", expand=True, padx=5, pady=5)
        
        self.refresh()

    def refresh(self):
        """Re-lee el historial de descargas y dibuja la línea de tiempo (RF-027, RF-028)."""
        # Limpiar
        for widget in self.scroll_container.scrollable_frame.winfo_children():
            widget.destroy()
            
        records = self.history_service.get_all_records()
        
        if not records:
            lbl_empty = tk.Label(
                self.scroll_container.scrollable_frame,
                text="Historial de descargas vacío.",
                fg="#454545",
                bg=self.bg_color,
                font=("Courier New", 11, "italic"),
                pady=20
            )
            lbl_empty.pack(fill="x")
            return
            
        for i, rec in enumerate(records):
            idx = len(records) - i  # Número correlativo (01, 02...)
            name = rec["name"]
            date_str = rec["date"]
            time_str = rec["time"]
            status = rec["status"].upper()
            
            # Determinar color según el estado (RF-029)
            color_status = "#00E5A3" if status == "SUCCESS" else "#FF4C4C"
            
            # Fila general
            row_frame = tk.Frame(self.scroll_container.scrollable_frame, bg=self.bg_color)
            row_frame.pack(fill="x", pady=4, padx=5)
            
            # 1. Canvas para el Nodo del Timeline a la Izquierda
            # Ancho de 40px, altura de 75px
            canvas = tk.Canvas(row_frame, width=40, height=75, bg=self.bg_color, bd=0, highlightthickness=0)
            canvas.pack(side="left", fill="y")
            
            # Dibujar línea vertical conectora
            # Dibujamos de arriba a abajo en el centro del canvas (x=20)
            canvas.create_line(20, 0, 20, 75, fill="#222222", width=2)
            
            # Dibujar círculo del nodo
            # Ovalo de 10px a 30px en X, y de 27px a 47px en Y (centrado a y=37)
            canvas.create_oval(10, 27, 30, 47, outline=color_status, fill=self.bg_color, width=2)
            
            # Número correlativo dentro del círculo
            canvas.create_text(20, 37, text=f"{idx:02d}", fill="#606060", font=("Courier New", 9, "bold"))
            
            # 2. Tarjeta del Registro a la Derecha
            card_border = tk.Frame(row_frame, bg="#222222", bd=1)
            card_border.pack(side="left", fill="both", expand=True, padx=(5, 10), pady=4)
            
            card = tk.Frame(card_border, bg="#121212", padx=10, pady=8)
            card.pack(fill="both", expand=True)
            
            # Contenedor para Texto
            text_frame = tk.Frame(card, bg="#121212")
            text_frame.pack(side="left", fill="both", expand=True)
            
            # Nombre de la Canción (en rojo si falló)
            lbl_title = tk.Label(
                text_frame,
                text=name.upper(),
                fg="#EDEDED" if status == "SUCCESS" else "#FF4C4C",
                bg="#121212",
                font=("Courier New", 11, "bold"),
                anchor="w",
                justify="left",
                wraplength=180
            )
            lbl_title.pack(fill="x", anchor="w")
            
            # Subtítulo (Fecha · Hora · Estado)
            details = f"{time_str}  ·  {date_str}  ·  {status}"
            lbl_sub = tk.Label(
                text_frame,
                text=details,
                fg="#606060",
                bg="#121212",
                font=("Courier New", 9)
                # anchor="w" (Removido para evitar error de Tkinter)
            )
            lbl_sub.pack(fill="x", anchor="w", pady=(3, 0))
            
            # Grip de textura a la Derecha (estilo sci-fi de la captura)
            lbl_grip = tk.Label(
                card,
                text="☰",
                fg="#2C2C2C",
                bg="#121212",
                font=("Courier New", 14),
                padx=5
            )
            lbl_grip.pack(side="right", fill="y")
