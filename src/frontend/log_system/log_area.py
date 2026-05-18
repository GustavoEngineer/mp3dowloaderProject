import tkinter as tk
import datetime

class LogAreaWidget(tk.Frame):
    """Componente visual premium para el área de logs (RF-013 al RF-019).
    
    Alineado al 70% del ancho de la aplicación, implementa cabeceras de logs
    formateadas, líneas finas divisorias, colores específicos para cada nivel
    de log (INFO, SUCCESS, WARN, FAILED) y scroll automático nativo.
    """
    
    def __init__(self, parent, bg_color="#0D0D0D"):
        super().__init__(parent, bg=bg_color)
        self.bg_color = bg_color
        
        # RF-013: Ocupar el 70% del ancho de la aplicación y pegado a la izquierda.
        # Lo logramos configurando una cuadrícula donde la columna izquierda
        # absorbe el 70% exacto y la de la derecha absorbe el 30% restante.
        self.grid_columnconfigure(0, weight=70)
        self.grid_columnconfigure(1, weight=30)
        self.grid_rowconfigure(0, weight=1)

        # Contenedor del log (pegado a la izquierda, 70% de ancho)
        self.center_frame = tk.Frame(self, bg=bg_color)
        self.center_frame.grid(row=0, column=0, sticky="nsew")

        # Campo de Texto para los Logs
        # Usamos tk.Text ya que permite etiquetas avanzadas y coloreado mixto en la misma línea
        self.output = tk.Text(
            self.center_frame,
            bg=bg_color,
            fg="#EDEDED",
            font=("Courier New", 12),
            insertbackground="#6BA3CC",
            selectbackground="#1A2A3A",
            relief="flat",
            bd=0,
            wrap="word",
            state="disabled",
            cursor="arrow",
            padx=10,
            pady=10,
            spacing1=2,
            spacing3=4,
        )
        self.output.pack(fill="both", expand=True)

        # Enlazar la rueda del ratón para scroll manual fluido
        self.output.bind(
            "<MouseWheel>",
            lambda e: self.output.yview_scroll(-1 * (e.delta // 120), "units")
        )

        # RF-017: Definir colores y estilos premium para las etiquetas de logs
        self.output.tag_configure("time",      foreground="#606060", font=("Courier New", 14, "bold"))
        self.output.tag_configure("route",     foreground="#5A8FA8", font=("Courier New", 14, "bold"))
        self.output.tag_configure("info",      foreground="#808080", font=("Courier New", 14, "bold"))
        self.output.tag_configure("success",   foreground="#00E5A3", font=("Courier New", 14, "bold"))
        self.output.tag_configure("warn",      foreground="#FFB800", font=("Courier New", 14, "bold"))
        self.output.tag_configure("failed",    foreground="#FF4C4C", font=("Courier New", 14, "bold"))
        
        self.output.tag_configure("message",   foreground="#EDEDED", font=("Courier New", 13))
        self.output.tag_configure("divider",   foreground="#333333")

    def append_log(self, level: str, message: str, route: str = "C:\\Users\\Gustavo\\Documents\\mp3dowloaderProject"):
        """Añade visualmente un log formateado en la terminal al estilo pixel-perfect (RF-014, RF-015)."""
        level_upper = level.upper()
        time_str = datetime.datetime.now().strftime("%H:%M:%S")
        
        self.output.configure(state="normal")
        
        # 1. Cabecera del log: [HH:MM:SS] ~/vault/root LEVEL (RF-014)
        self.output.insert("end", f"[{time_str}] ", "time")
        self.output.insert("end", f"{route} ", "route")
        
        # RF-016 y RF-017: Colores de logs permitidos
        if level_upper == "SUCCESS":
            self.output.insert("end", "SUCCESS\n", "success")
        elif level_upper == "WARN":
            self.output.insert("end", "WARN\n", "warn")
        elif level_upper == "FAILED":
            self.output.insert("end", "FAILED\n", "failed")
        else:
            self.output.insert("end", "INFO\n", "info")
            
        # 2. Mensaje de log / resultado acción en la siguiente línea
        self.output.insert("end", f"{message}\n", "message")
        
        # 3. Línea divisoria de separación visual más gruesa y visible (RF-015)
        self.output.insert("end", "═" * 80 + "\n\n", "divider")
        
        self.output.configure(state="disabled")
        
        # 4. Scroll automático hacia abajo (RF-018)
        self.output.see("end")

    def clear(self) -> None:
        """Limpia todos los logs del área de pantalla (RF-019)."""
        self.output.configure(state="normal")
        self.output.delete("1.0", "end")
        self.output.configure(state="disabled")

    def overwrite_last_message(self, message: str):
        """Sobreescribe la última línea del log (usado para barras de progreso) de forma limpia y fluida."""
        self.output.configure(state="normal")
        # Borrar el mensaje anterior y el divisor anterior
        self.output.delete("end-3l", "end-1c")
        self.output.insert("end", f"{message}\n", "message")
        self.output.insert("end", "═" * 80 + "\n\n", "divider")
        self.output.configure(state="disabled")
        self.output.see("end")
