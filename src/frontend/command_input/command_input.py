import tkinter as tk
import customtkinter as ctk

class CommandInputWidget(tk.Frame):
    """Componente visual premium para el input de comandos (RF-007, RF-008).
    
    Presenta un borde de color azul, un icono de terminal `>_` de color azul a la izquierda
    y un placeholder interactivo y descriptivo que se limpia automáticamente.
    """
    
    def __init__(
        self, 
        parent, 
        bg_color="#0D0D0D", 
        text_color="#EDEDED", 
        blue_color="#6BA3CC",
        muted_color="#3D3D3D",
        font=("Courier New", 12, "bold"),
        prompt="requests@mp3DL ~ "
    ):
        super().__init__(parent, bg=bg_color, pady=12, padx=16)
        self.bg_color = bg_color
        self.text_color = text_color
        self.blue_color = blue_color
        self.muted_color = muted_color
        self.font = font
        self.prompt = prompt
        
        # Placeholder descriptivo (RF-008)
        self.placeholder = "Escriba una URL de YouTube o ingrese 'help' para obtener ayuda..."
        self.has_placeholder = True

        # RF-007: Borde exterior de color azul premium (1px de padding = borde)
        self.border_frame = tk.Frame(self, bg=self.blue_color, padx=1, pady=1)
        self.border_frame.pack(fill="x")

        # Interior oscuro del input
        self.inner_frame = tk.Frame(self.border_frame, bg=bg_color)
        self.inner_frame.pack(fill="x")

        # RF-007: Icono de terminal en la izquierda de color azul (>_)
        self.terminal_icon = tk.Label(
            self.inner_frame, 
            text=" >_ ",
            bg=bg_color, 
            fg=self.blue_color, 
            font=("Courier New", 12, "bold")
        )
        self.terminal_icon.pack(side="left", padx=(5, 2))

        # Campo de entrada
        self.entry = tk.Entry(
            self.inner_frame,
            bg=bg_color, 
            fg=self.muted_color,  # Inicialmente con color de placeholder
            insertbackground=text_color,
            disabledbackground=bg_color,
            disabledforeground=self.muted_color,
            relief="flat",
            font=font,
            highlightthickness=0,
            bd=0,
        )
        self.entry.insert(0, self.placeholder)
        self.entry.pack(side="left", fill="x", expand=True, ipady=8, padx=(0, 10))

        # Enlazar eventos para un comportamiento robusto del placeholder (RF-008)
        self.entry.bind("<FocusIn>", self._on_focus_in)
        self.entry.bind("<FocusOut>", self._on_focus_out)
        self.entry.bind("<KeyPress>", self._on_key_press)
        self.entry.bind("<Button-1>", self._on_click)

    def _clear_placeholder_if_present(self):
        """Limpia de forma segura el placeholder si está activo."""
        if self.has_placeholder:
            self.entry.delete(0, "end")
            self.entry.configure(fg=self.text_color)
            self.has_placeholder = False

    def _restore_placeholder(self):
        """Restaura de forma segura el placeholder."""
        self.entry.delete(0, "end")
        self.entry.insert(0, self.placeholder)
        self.entry.configure(fg=self.muted_color)
        self.has_placeholder = True

    def _on_focus_in(self, event=None):
        """Al recibir foco, limpiamos el placeholder."""
        self._clear_placeholder_if_present()

    def _on_focus_out(self, event=None):
        """Al perder el foco, si está vacío, restauramos el placeholder."""
        content = self.entry.get().strip()
        if not content:
            self._restore_placeholder()

    def _on_key_press(self, event=None):
        """Si el usuario presiona cualquier tecla de escritura estando el placeholder, lo limpiamos."""
        self._clear_placeholder_if_present()

    def _on_click(self, event=None):
        """Si hace clic en el campo estando el placeholder, lo limpiamos para escritura limpia."""
        self._clear_placeholder_if_present()

    def get_text(self) -> str:
        """Retorna el texto actual. Si tiene el placeholder, retorna vacío (RF-009, RF-010)."""
        if self.has_placeholder:
            return ""
        return self.entry.get().strip()

    def clear(self) -> None:
        """Limpia el texto. Si tiene foco activo, lo deja vacío listo para continuar escribiendo.
        Si no tiene foco, restaura el placeholder (RF-012).
        """
        self.entry.delete(0, "end")
        # Si sigue enfocado, lo dejamos limpio para que no obstruya la siguiente escritura
        if self.entry.focus_get() == self.entry:
            self.entry.configure(fg=self.text_color)
            self.has_placeholder = False
        else:
            self._restore_placeholder()

    def set_text(self, text: str) -> None:
        """Establece texto en el input, eliminando el placeholder si es necesario."""
        self.entry.delete(0, "end")
        if text:
            self.entry.configure(fg=self.text_color)
            self.entry.insert(0, text)
            self.has_placeholder = False
        else:
            self._restore_placeholder()

    def lock(self) -> None:
        """Deshabilita el input visualmente durante descargas o procesos."""
        self.entry.configure(state="disabled")
        self.terminal_icon.configure(fg=self.muted_color)
        self.border_frame.configure(bg=self.muted_color)

    def unlock(self) -> None:
        """Habilita el input visualmente al terminar un proceso."""
        self.entry.configure(state="normal")
        self.terminal_icon.configure(fg=self.blue_color)
        self.border_frame.configure(bg=self.blue_color)

    def focus(self) -> None:
        """Enfoca el cursor en el input."""
        self.entry.focus_set()

    def set_prompt(self, new_prompt: str) -> None:
        """Modifica dinámicamente el texto del prompt en el icono de terminal."""
        self.terminal_icon.configure(text=new_prompt)
