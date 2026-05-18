import customtkinter as ctk
from threading import Thread
from pathlib import Path
from src.backend.core.exceptions import AppError
from src.backend.services.download_service import DownloadService

ctk.set_appearance_mode("System")
ctk.set_default_color_theme("blue")

class App(ctk.CTk):
    """Ventana principal de la aplicación."""
    
    def __init__(self, download_service: DownloadService):
        super().__init__()
        self.download_service = download_service
        
        self.title("🎵 MP3 Downloader")
        self.geometry("600x300")
        self.resizable(False, False)
        
        self._build_ui()

    def _build_ui(self):
        # Título
        self.title_label = ctk.CTkLabel(
            self, 
            text="Descargador de YouTube a MP3", 
            font=ctk.CTkFont(size=20, weight="bold")
        )
        self.title_label.pack(pady=20)
        
        # Input URL
        self.url_entry = ctk.CTkEntry(
            self, 
            placeholder_text="Pega el enlace de YouTube aquí...", 
            width=400
        )
        self.url_entry.pack(pady=10)
        
        # Botón Descargar
        self.download_button = ctk.CTkButton(
            self, 
            text="Descargar Audio", 
            command=self.start_download
        )
        self.download_button.pack(pady=10)
        
        # Etiqueta de estado
        self.status_label = ctk.CTkLabel(self, text="", text_color="gray")
        self.status_label.pack(pady=10)

    def start_download(self):
        url = self.url_entry.get().strip()
        if not url:
            self.status_label.configure(text="Por favor ingresa una URL.", text_color="red")
            return
            
        self.status_label.configure(text="Descargando... Por favor espera.", text_color="orange")
        self.download_button.configure(state="disabled")
        
        # Ejecutar en hilo secundario para no bloquear la UI
        Thread(target=self._download_task, args=(url,), daemon=True).start()

    def _download_task(self, url: str):
        try:
            file_path = self.download_service.process_download(url)
            self.after(0, self._download_success, file_path)
        except AppError as e:
            self.after(0, self._download_error, str(e))
        except Exception as e:
            self.after(0, self._download_error, f"Error inesperado: {str(e)}")

    def _download_success(self, file_path: Path):
        self.status_label.configure(text=f"¡Éxito! Guardado en:\n{file_path.name}", text_color="green")
        self.download_button.configure(state="normal")
        self.url_entry.delete(0, 'end')

    def _download_error(self, message: str):
        self.status_label.configure(text=message, text_color="red")
        self.download_button.configure(state="normal")
