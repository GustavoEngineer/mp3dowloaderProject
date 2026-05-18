import tkinter as tk
import customtkinter as ctk
import threading
from pathlib import Path
from src.backend.api.services.download_service import DownloadService
from src.frontend.top_bar import TopBar
from src.frontend.command_input import CommandInputWidget
from src.backend.command_input.command_service import CommandService
from src.frontend.log_system import LogAreaWidget

# ── Paleta (tonos fríos / neutros, sin verde dominante) ───────────────────────
BG       = "#0D0D0D"
BLUE     = "#6BA3CC"   # Prompt y encabezados
GRAY     = "#808080"   # Texto de sistema / mensajes
WHITE    = "#EDEDED"   # Rutas, nombres de archivo (énfasis)
MUTED    = "#3D3D3D"   # Texto muy secundario
PROGRESS = "#5A8FA8"   # Barra de progreso (azul apagado)
RED      = "#CC5555"   # Errores
AMBER    = "#C89060"   # Advertencias (ámbar suave)
FONT     = ("Courier New", 12)

ctk.set_appearance_mode("Dark")


class TerminalUI(ctk.CTk):
    """Terminal interactiva — descarga de audio de YouTube."""

    PROMPT = "requests@mp3DL ~ "
    BANNER = [
        ("  mp3DL Terminal  ·  local", "blue"),
        ("  Ingrese la URL de un video de YouTube para descargar su audio.", "muted"),
        ("  ─" * 45,                                        "muted"),
    ]

    def __init__(self, download_service: DownloadService):
        super().__init__()
        self.download_service = download_service
        self._is_busy = False
        self.current_route = "C:\\Users\\Gustavo\\Documents\\mp3dowloaderProject"
        
        # Atributos para máquina de estados interactiva de metadatos (RF-033)
        self._interactive_state = None
        self._pending_url = None
        self._collected_metadata = {}
        self._pending_edit_op = {}
        self._pending_delete_op = {}
        
        # Atributos para control de estado de reproducción y logs (RF-026)
        self._current_playing_song = None
        self._playback_timer = None

        # Inicializar servicios en el backend
        from src.backend.vault import VaultService
        from src.backend.history import HistoryService
        self.vault_service = VaultService(self.download_service.download_dir.parent)
        self.history_service = HistoryService(self.download_service.download_dir.parent / "history.json")

        self.title("mp3DL Terminal")
        self.geometry("1100x650")
        self.minsize(800, 500)
        self.configure(fg_color=BG)

        self._build_ui()
        self._focus_input()

    # ── Construcción de UI ────────────────────────────────────────────────────

    def _build_ui(self):
        # ── Barra Superior (Top Bar) Modular ──
        self.top_bar = TopBar(
            self, 
            bg_color="#1E1E1E", 
            text_color=WHITE, 
            gray_color=GRAY, 
            red_color=RED
        )
        self.top_bar.pack(fill="x", side="top")

        # Contenedor principal para organizar izquierda (70%) y derecha (30%)
        self.main_container = tk.Frame(self, bg=BG)
        self.main_container.pack(fill="both", expand=True)

        self.main_container.grid_columnconfigure(0, weight=70)
        self.main_container.grid_columnconfigure(1, weight=30)
        self.main_container.grid_rowconfigure(0, weight=1)

        # Panel Izquierdo (70% del ancho)
        self.left_panel = tk.Frame(self.main_container, bg=BG)
        self.left_panel.grid(row=0, column=0, sticky="nsew")

        # Panel Derecho (30% del ancho)
        self.right_panel = tk.Frame(self.main_container, bg=BG)
        self.right_panel.grid(row=0, column=1, sticky="nsew")

        # ── Escritor de Comandos (Command Writer) Modular ──
        self.command_writer = CommandInputWidget(
            self.left_panel,
            bg_color=BG,
            text_color=WHITE,
            blue_color=BLUE,
            muted_color=MUTED,
            font=FONT,
            prompt=self.PROMPT
        )
        self.command_writer.pack(fill="x", side="top")
        self.command_writer.entry.bind("<Return>", self._on_enter)

        # ── Área de Logs (ocupando todo el panel izquierdo) (RF-013) ──
        self.log_area = LogAreaWidget(self.left_panel, bg_color=BG)
        self.log_area.pack(fill="both", expand=True)

        # ── Vault History Widget Modular (RF-020 al RF-029) ──
        from src.frontend.vault_history import VaultHistoryWidget
        self.vault_history = VaultHistoryWidget(
            self.right_panel,
            vault_service=self.vault_service,
            history_service=self.history_service,
            on_route_changed=self._on_route_changed,
            bg_color="#0D0D0D"
        )
        self.vault_history.pack(fill="both", expand=True)

    def _cleanup_exported_songs(self, deleted_paths):
        """Elimina de exported_songs.json cualquier ruta que sea coincidente o descendiente
        de las rutas eliminadas (archivos o álbumes).
        """
        import json
        from pathlib import Path
        
        exported_json_path = self.vault_service.download_dir.parent / "exported_songs.json"
        if not exported_json_path.exists():
            return
            
        try:
            with open(exported_json_path, "r", encoding="utf-8") as f:
                exported_list = json.load(f)
                
            resolved_deleted = [Path(p).resolve() for p in deleted_paths]
            new_exported = []
            
            for exp_path_str in exported_list:
                exp_path = Path(exp_path_str).resolve()
                should_remove = False
                
                for del_path in resolved_deleted:
                    # Si el archivo eliminado es exactamente el mismo, o si el directorio eliminado es padre de este archivo
                    if exp_path == del_path or del_path in exp_path.parents:
                        should_remove = True
                        break
                        
                if not should_remove:
                    new_exported.append(exp_path_str)
                    
            with open(exported_json_path, "w", encoding="utf-8") as f:
                json.dump(new_exported, f, indent=4, ensure_ascii=False)
                
        except Exception:
            pass

    def _get_song_path_by_number(self, song_num_str: str) -> str:
        """Retorna la ruta completa del archivo de la canción según su índice (1-indexed)
        dentro del contexto/álbum actual (self.current_route).
        Retorna None si el índice no es válido o no es un álbum.
        """
        try:
            num = int(song_num_str)
        except ValueError:
            return None
            
        from pathlib import Path
        current_path = Path(self.current_route)
        downloads_path = self.vault_service.download_dir
        
        # Debe ser un subdirectorio directo de downloads, o ser "downloads / Sin album"
        if not current_path.exists() or not current_path.is_dir() or (current_path.parent != downloads_path and current_path != downloads_path / "Sin album"):
            return None
            
        # Escanear y ordenar canciones alfabéticamente
        songs = []
        for file in current_path.iterdir():
            if file.is_file() and file.suffix.lower() in (".mp3", ".wav", ".m4a", ".ogg"):
                songs.append(file.name)
        songs.sort()
        
        if 1 <= num <= len(songs):
            target_song = songs[num - 1]
            return str(current_path / target_song)
            
        return None

    # ── Output ────────────────────────────────────────────────────────────────

    def _print(self, text: str, tag: str = "gray"):
        if not text.strip():
            return
            
        # Mapear las etiquetas de colores antiguas a niveles de logs permitidos (RF-016, RF-017)
        level = "INFO"
        if tag in ("red", "failed"):
            level = "FAILED"
        elif tag in ("green", "success"):
            level = "SUCCESS"
        elif tag in ("amber", "warn"):
            level = "WARN"
            
        # Remover prefijos estéticos redundantes si existen
        clean_text = text.strip()
        for prefix in ("done   ", "saved  ", "error  ", "status   ", "command  "):
            if clean_text.startswith(prefix):
                clean_text = clean_text[len(prefix):].strip()
                
        self.log_area.append_log(level, clean_text, route=self.current_route)

    def _overwrite_last(self, text: str, tag: str):
        """Sobreescribe la última línea del log (barra de progreso dinámica) (RF-018)."""
        clean_text = text.strip()
        self.log_area.overwrite_last_message(clean_text)

    # ── Lógica de Eventos ─────────────────────────────────────────────────────

    def _on_enter(self, _event=None):
        if self._is_busy:
            return
            
        text = self.command_writer.get_text()
        
        # Si no hay texto y no estamos en estado interactivo, ignorar
        if not text and self._interactive_state is None:
            return

        # RF-012: Limpiar automáticamente el input después de ejecutar la acción
        self.command_writer.clear()

        # Interceptar si estamos capturando metadatos interactivos (RF-033)
        if self._interactive_state is not None:
            self._handle_metadata_input(text)
            return

        # Parsear con nuestro servicio de backend modular
        parsed = CommandService.parse_input(text)

        if parsed["type"] == "command":
            cmd_name = parsed["name"]
            cmd_obj = parsed["command"]
            
            if cmd_name == "help":
                # RF-009: Mostrar tabla de ayuda con estética moderna y limpia
                C = " │ "   # column separator
                SEP = " ─────────────────  ──────────────────────────────────────────  ───────────────────────────────────────"
                HEADER_SEP = " ═════════════════  ══════════════════════════════════════════  ═══════════════════════════════════════"
                
                help_lines = [
                    "",
                    "  ✦  COMANDOS DISPONIBLES — mp3DL Terminal",
                    "",
                    "  Comando            Parámetros / Variantes                      Descripción",
                    HEADER_SEP,
                    f"  help              {C}(ninguno)                                   {C}Muestra esta tabla de ayuda",
                    f"  wifi              {C}(ninguno)                                   {C}Abre configuración Wi-Fi de Windows",
                    f"  clear             {C}(ninguno)                                   {C}Limpia todos los logs de pantalla",
                    f"  exit              {C}(ninguno)                                   {C}Cierra la aplicación",
                    SEP,
                    f"  nav               {C}--raiz                                      {C}Navega a la carpeta raíz del Vault",
                    f"                    {C}--sin-album                                 {C}Navega al álbum Sin Álbum",
                    f"                    {C}--album <nombre>                            {C}Navega a un álbum específico",
                    f"  back              {C}(ninguno)                                   {C}Vuelve a la carpeta o nivel anterior",
                    SEP,
                    f"  create            {C}--album <nombre>                            {C}Crea un nuevo álbum físico",
                    SEP,
                    f"  edit              {C}--album-name <nuevo nombre>                 {C}Renombra el álbum actual *",
                    f"                    {C}--song-name  <num> <nuevo nombre>           {C}Edita el nombre de una canción *",
                    f"                    {C}--song-album <num> <nuevo album>            {C}Mueve una canción a otro álbum *",
                    f"                    {C}--song-artist <num> <nuevo artista>         {C}Edita el artista de una canción *",
                    SEP,
                    f"  export            {C}--song  <numero>                            {C}Exporta canción(es) a carpeta externa *",
                    f"                    {C}--song-all                                  {C}Exporta todas las canciones del álbum *",
                    SEP,
                    f"  rm                {C}--song  <numero>                            {C}Elimina canción(es) del álbum actual *",
                    f"                    {C}--song-all                                  {C}Elimina todas las canciones del álbum *",
                    f"                    {C}--album                                      {C}Elimina el álbum actual *",
                    HEADER_SEP,
                    "",
                    "  ⓘ  Cualquier otro texto se interpretará como URL de YouTube para descargar su audio.",
                    "  *  Requiere estar navegado en el álbum correspondiente (con 'nav --album <nombre>').",
                    "",
                ]
                help_text = "\n".join(help_lines)
                self.log_area.append_log("INFO", help_text)
                self._focus_input()
                
            elif cmd_name == "wifi":
                # RF-006: Permitir abrir la configuración de Wi-Fi de Windows
                self.log_area.append_log("INFO", "Iniciando apertura de configuración Wi-Fi de Windows...")
                cmd_obj.execute()
                self.log_area.append_log("SUCCESS", "Ventana de configuración Wi-Fi abierta con éxito.")
                self._focus_input()
                
            elif cmd_name == "clear":
                # RF-019: El comando clear debe limpiar todos los logs
                self.log_area.clear()
                self._focus_input()
                
            elif cmd_name == "exit":
                # Salir de la aplicación
                self.log_area.append_log("WARN", "Cerrando la terminal MP3DL. Saliendo de la aplicación...")
                self.after(500, cmd_obj.execute)
                
            elif cmd_name == "nav":
                # RF-036: Navegación por comando nav
                args = parsed["args"]
                if not args:
                    self.log_area.append_log(
                        "FAILED", 
                        "Uso: nav --album <nombre> | nav --sin-album | nav --raiz",
                        route=self.current_route
                    )
                    self._focus_input()
                else:
                    opt = args[0].lower()
                    if opt == "--raiz":
                        # Ir a la carpeta raíz del proyecto
                        target_path = "C:\\Users\\Gustavo\\Documents\\mp3dowloaderProject"
                        self._navigate_to("raiz", target_path)
                    elif opt == "--sin-album":
                        # Ir a la sección de Sin album
                        target_path = str(self.vault_service.download_dir / "Sin album")
                        self._navigate_to("sin_album", target_path)
                    elif opt == "--album":
                        if len(args) < 2:
                            self.log_area.append_log(
                                "FAILED", 
                                "Debe especificar el nombre del álbum. Uso: nav --album <nombre>",
                                route=self.current_route
                            )
                            self._focus_input()
                        else:
                            # Reconstruir el nombre del álbum que podría tener espacios
                            user_album = " ".join(args[1:])
                            user_album_lower = user_album.lower()
                            
                            # Buscar case-insensitively en la carpeta downloads para resolver el nombre exacto
                            actual_name = None
                            if self.vault_service.download_dir.exists():
                                for p in self.vault_service.download_dir.iterdir():
                                    if p.is_dir() and not p.name.startswith(".") and p.name.lower() == user_album_lower:
                                        actual_name = p.name
                                        break
                                        
                            if actual_name is not None:
                                album_path = self.vault_service.download_dir / actual_name
                                self._navigate_to("album", str(album_path), actual_name)
                            else:
                                self.log_area.append_log(
                                    "FAILED", 
                                    f"El álbum '{user_album}' no existe en {self.vault_service.download_dir.name}.",
                                    route=self.current_route
                                )
                                self._focus_input()
                    else:
                        self.log_area.append_log(
                            "FAILED", 
                            f"Opción de navegación '{opt}' no válida. Uso: nav --album <nombre> | --sin-album | --raiz",
                            route=self.current_route
                        )
                        self._focus_input()
                        
            elif cmd_name == "back":
                from pathlib import Path
                current_path = Path(self.current_route)
                downloads_path = self.vault_service.download_dir
                
                is_in_album = (
                    current_path.exists()
                    and current_path.is_dir()
                    and (current_path.parent == downloads_path or current_path == downloads_path / "Sin album")
                )
                
                if is_in_album:
                    target_raiz = "C:\\Users\\Gustavo\\Documents\\mp3dowloaderProject"
                    self._navigate_to("raiz", target_raiz)
                else:
                    self.log_area.append_log(
                        "FAILED",
                        "ERR: Ya se encuentra en el directorio raíz (no se puede volver más atrás).",
                        route=self.current_route
                    )
                    self._focus_input()
                    
            elif cmd_name == "export":
                # RF-044: Exportar canciones
                from pathlib import Path
                current_path = Path(self.current_route)
                downloads_path = self.vault_service.download_dir
                
                is_valid_album = (
                    current_path.exists()
                    and current_path.is_dir()
                    and (current_path.parent == downloads_path or current_path == downloads_path / "Sin album")
                )
                
                if not is_valid_album:
                    self.log_area.append_log(
                        "FAILED",
                        "ERR: Debe navegar primero al álbum que contiene las canciones a exportar.",
                        route=self.current_route
                    )
                    self._focus_input()
                else:
                    args = parsed["args"]
                    if not args:
                        self.log_area.append_log(
                            "FAILED",
                            "Uso: export --song <numero> o export --song-all",
                            route=self.current_route
                        )
                        self._focus_input()
                    else:
                        opt = args[0].lower()
                        
                        # Buscar canciones del álbum actual
                        data = self.vault_service.get_vault_structure()
                        current_album_name = current_path.name
                        target_album = None
                        for album in data["albums"]:
                            if album["name"] == current_album_name:
                                target_album = album
                                break
                                
                        if not target_album or not target_album["songs"]:
                            self.log_area.append_log(
                                "FAILED",
                                "ERR: El álbum actual no contiene canciones para exportar.",
                                route=self.current_route
                            )
                            self._focus_input()
                        else:
                            available_songs = target_album["songs"]
                            songs_to_export = []
                            is_valid = True
                            
                            if opt == "--song":
                                if len(args) < 2:
                                    self.log_area.append_log(
                                        "FAILED",
                                        "ERR: Especifique el número o números de canción (ej. export --song 1 o export --song 1,2).",
                                        route=self.current_route
                                    )
                                    self._focus_input()
                                    is_valid = False
                                else:
                                    numbers_str = "".join(args[1:])
                                    try:
                                        nums = [int(n.strip()) for n in numbers_str.split(",") if n.strip()]
                                        if not nums:
                                            raise ValueError()
                                    except ValueError:
                                        self.log_area.append_log(
                                            "FAILED",
                                            "ERR: Los números de canciones deben ser enteros válidos separados por comas.",
                                            route=self.current_route
                                        )
                                        self._focus_input()
                                        is_valid = False
                                        
                                    if is_valid:
                                        for num in nums:
                                            if num < 1 or num > len(available_songs):
                                                self.log_area.append_log(
                                                    "FAILED",
                                                    f"ERR: El número de canción {num} no existe (rango 1-{len(available_songs)}).",
                                                    route=self.current_route
                                                )
                                                self._focus_input()
                                                is_valid = False
                                                break
                                            songs_to_export.append(available_songs[num - 1])
                                            
                            elif opt == "--song-all":
                                songs_to_export = available_songs
                            else:
                                self.log_area.append_log(
                                    "FAILED",
                                    "ERR: Opción no válida. Uso: export --song <numero> o export --song-all",
                                    route=self.current_route
                                )
                                self._focus_input()
                                is_valid = False
                                
                            if is_valid and songs_to_export:
                                from tkinter import filedialog
                                import shutil
                                import json
                                
                                target_dir = filedialog.askdirectory(title="Seleccionar carpeta de destino para exportar")
                                if not target_dir:
                                    self.log_area.append_log(
                                        "FAILED",
                                        "Exportación cancelada por el usuario (no se seleccionó carpeta).",
                                        route=self.current_route
                                    )
                                    self._focus_input()
                                else:
                                    target_dir_path = Path(target_dir)
                                    
                                    # Cargar canciones exportadas
                                    exported_json_path = self.vault_service.download_dir.parent / "exported_songs.json"
                                    exported_list = []
                                    if exported_json_path.exists():
                                        try:
                                            with open(exported_json_path, "r", encoding="utf-8") as f:
                                                exported_list = json.load(f)
                                        except Exception:
                                            pass
                                            
                                    exported_set = set(exported_list)
                                    
                                    for song_name in songs_to_export:
                                        src_file = current_path / song_name
                                        dest_file = target_dir_path / song_name
                                        try:
                                            shutil.copy2(src_file, dest_file)
                                            exported_set.add(str(src_file.resolve()))
                                            self.log_area.append_log(
                                                "SUCCESS",
                                                f"Canción '{song_name}' exportada con éxito a: {target_dir}",
                                                route=self.current_route
                                            )
                                        except Exception as e:
                                            self.log_area.append_log(
                                                "FAILED",
                                                f"ERR al exportar '{song_name}': {e}",
                                                route=self.current_route
                                            )
                                            
                                    try:
                                        with open(exported_json_path, "w", encoding="utf-8") as f:
                                            json.dump(list(exported_set), f, indent=4, ensure_ascii=False)
                                    except Exception:
                                        pass
                                        
                                    self.vault_history.refresh_all()
                                    self._focus_input()
                                    
            elif cmd_name == "create":
                # RF-040: Crear un nuevo álbum
                args = parsed["args"]
                if not args or args[0].lower() != "--album" or len(args) < 2:
                    self.log_area.append_log(
                        "FAILED",
                        "Uso: create --album <nombre>",
                        route=self.current_route
                    )
                    self._focus_input()
                else:
                    # Unir el nombre del álbum que podría tener espacios
                    album_name = " ".join(args[1:])
                    # Validar si el nombre es igual a la carpeta raíz "downloads" o "Sin album" de forma case-insensitive
                    if album_name.lower() in ("sin album", "sin_album"):
                        self.log_area.append_log(
                            "FAILED",
                            "ERR: No se puede crear un álbum con ese nombre reservado.",
                            route=self.current_route
                        )
                        self._focus_input()
                    else:
                        new_path = self.vault_service.download_dir / album_name
                        if new_path.exists():
                            self.log_area.append_log(
                                "FAILED",
                                f"ERR: El álbum '{album_name}' ya existe.",
                                route=self.current_route
                            )
                            self._focus_input()
                        else:
                            try:
                                new_path.mkdir(parents=True, exist_ok=True)
                                self.log_area.append_log(
                                    "SUCCESS",
                                    f"Álbum '{album_name}' creado con éxito.",
                                    route=self.current_route
                                )
                                # Refrescar la vista del Vault
                                self.vault_history.refresh_all()
                                # Navegar automáticamente al nuevo álbum (auto-apertura RF-039)
                                self._navigate_to("album", str(new_path), album_name)
                            except Exception as e:
                                self.log_area.append_log(
                                    "FAILED",
                                    f"ERR al crear álbum: {e}",
                                    route=self.current_route
                                )
                                self._focus_input()

            elif cmd_name == "edit":
                args = parsed["args"]
                if not args:
                    self.log_area.append_log(
                        "FAILED",
                        "Uso: edit --album-name <nuevo nombre> | edit --song-name <num> <new> | edit --song-album <num> <new> | edit --song-artist <num> <new>",
                        route=self.current_route
                    )
                    self._focus_input()
                    return
                    
                sub_opt = args[0].lower()
                
                if sub_opt == "--album-name":
                    # RF-040: Editar (renombrar) álbum en el que se está navegado actualmente
                    if len(args) < 2:
                        self.log_area.append_log(
                            "FAILED",
                            "Uso: edit --album-name <nuevo nombre>",
                            route=self.current_route
                        )
                        self._focus_input()
                        return
                        
                    # Validar si estamos navegando en un álbum (contexto correcto)
                    from pathlib import Path
                    current_path = Path(self.current_route)
                    downloads_path = self.vault_service.download_dir
                    
                    is_valid_album = (
                        current_path.exists()
                        and current_path.is_dir()
                        and current_path.parent == downloads_path
                        and current_path.name != "Sin album"
                    )
                    
                    if not is_valid_album:
                        self.log_area.append_log(
                            "FAILED",
                            "ERR: Debe navegar primero al álbum que desea renombrar. (No se puede renombrar 'Sin album')",
                            route=self.current_route
                        )
                        self._focus_input()
                        return
                        
                    old_name = current_path.name
                    new_name = " ".join(args[1:])
                    old_path = current_path
                    
                    if not new_name:
                        self.log_area.append_log(
                            "FAILED",
                            "ERR: Debe especificar el nuevo nombre para el álbum.",
                            route=self.current_route
                        )
                        self._focus_input()
                        return
                    # Validar si el nuevo nombre es igual a "Sin album" de forma case-insensitive
                    elif new_name.lower() in ("sin album", "sin_album"):
                        self.log_area.append_log(
                            "FAILED",
                            "ERR: No se puede renombrar un álbum al nombre reservado 'Sin album'.",
                            route=self.current_route
                        )
                        self._focus_input()
                        return
                    else:
                        new_path = downloads_path / new_name
                        if new_path.exists():
                            self.log_area.append_log(
                                "FAILED",
                                f"ERR: El álbum '{new_name}' ya existe.",
                                route=self.current_route
                            )
                            self._focus_input()
                            return
                        else:
                            # Entrar a confirmación interactiva y/n (RF-040)
                            self._interactive_state = "CONFIRM_EDIT"
                            self._pending_edit_op = {
                                "type": "album_rename",
                                "params": {
                                    "old_path": str(old_path),
                                    "new_path": str(new_path),
                                    "old_name": old_name,
                                    "new_name": new_name
                                }
                            }
                            self.log_area.append_log(
                                "WARN",
                                f"ADVERTENCIA: ¿Está seguro que desea renombrar el álbum '{old_name}' a '{new_name}'? (y/n):",
                                route=self.current_route
                            )
                            self.command_writer.set_prompt("CONFIRMAR (y/n) > ")
                            self._focus_input()

                elif sub_opt in ("--song-name", "--song-album", "--song-artist"):
                    # RF-041: Editar metadata de canción seleccionada
                    # El usuario debe estar navegado en el álbum — formato: edit --song-name <num> <nuevo valor>
                    if len(args) < 3:
                        self.log_area.append_log(
                            "FAILED",
                            f"Uso: edit {sub_opt} <número de la canción> <nuevo valor>  (navegue primero al álbum con 'nav --album <nombre>')",
                            route=self.current_route
                        )
                        self._focus_input()
                        return
                        
                    song_num_str = args[1]
                    new_val = " ".join(args[2:])
                    
                    # Validar que estemos posicionados dentro de un álbum válido
                    from pathlib import Path
                    current_path = Path(self.current_route)
                    downloads_path = self.vault_service.download_dir
                    
                    is_valid_album = (
                        current_path.exists()
                        and current_path.is_dir()
                        and (current_path.parent == downloads_path or current_path == downloads_path / "Sin album")
                    )
                    
                    if not is_valid_album:
                        self.log_area.append_log(
                            "FAILED",
                            "ERR: Debe navegar primero al álbum que contiene la canción. Usa 'nav --album <nombre>' o 'nav --sin-album'.",
                            route=self.current_route
                        )
                        self._focus_input()
                        return
                    
                    # Resolver la canción por su número 1-indexed dentro del álbum actual
                    song_path_str = self._get_song_path_by_number(song_num_str)
                    if not song_path_str:
                        total = len([f for f in current_path.iterdir() if f.is_file() and f.suffix.lower() in (".mp3", ".wav", ".m4a", ".ogg")])
                        self.log_area.append_log(
                            "FAILED",
                            f"ERR: El número '{song_num_str}' no existe en '{current_path.name}' ({total} canciones).",
                            route=self.current_route
                        )
                        self._focus_input()
                        return
                        
                    song_path = Path(song_path_str)
                    
                    if sub_opt == "--song-name":
                        new_song_name = new_val + song_path.suffix
                        new_song_path = song_path.with_name(new_song_name)
                        
                        if new_song_path.exists() and new_song_path != song_path:
                            self.log_area.append_log(
                                "FAILED",
                                f"ERR: El archivo '{new_song_name}' ya existe.",
                                route=self.current_route
                            )
                            self._focus_input()
                            return
                            
                        self._interactive_state = "CONFIRM_EDIT"
                        self._pending_edit_op = {
                            "type": "song_name",
                            "params": {
                                "song_path": str(song_path),
                                "new_song_path": str(new_song_path),
                                "new_title": new_val
                            }
                        }
                        self.log_area.append_log(
                            "WARN",
                            f"ADVERTENCIA: ¿Está seguro de cambiar el nombre de la canción '{song_path.stem}' a '{new_val}'? (y/n):",
                            route=self.current_route
                        )
                        
                    elif sub_opt == "--song-album":
                        dest_album = new_val
                        new_song_path = downloads_path / dest_album / song_path.name
                        
                        if new_song_path.exists() and new_song_path != song_path:
                            self.log_area.append_log(
                                "FAILED",
                                f"ERR: La canción ya existe en el álbum '{dest_album}'.",
                                route=self.current_route
                            )
                            self._focus_input()
                            return
                            
                        self._interactive_state = "CONFIRM_EDIT"
                        self._pending_edit_op = {
                            "type": "song_album",
                            "params": {
                                "song_path": str(song_path),
                                "new_song_path": str(new_song_path),
                                "new_album": dest_album
                            }
                        }
                        self.log_area.append_log(
                            "WARN",
                            f"ADVERTENCIA: ¿Está seguro de mover la canción '{song_path.stem}' al álbum '{dest_album}'? (y/n):",
                            route=self.current_route
                        )
                        
                    elif sub_opt == "--song-artist":
                        self._interactive_state = "CONFIRM_EDIT"
                        self._pending_edit_op = {
                            "type": "song_artist",
                            "params": {
                                "song_path": str(song_path),
                                "new_artist": new_val
                            }
                        }
                        self.log_area.append_log(
                            "WARN",
                            f"ADVERTENCIA: ¿Está seguro de cambiar el artista de la canción '{song_path.stem}' a '{new_val}'? (y/n):",
                            route=self.current_route
                        )
                        
                    self.command_writer.set_prompt("CONFIRMAR (y/n) > ")
                    self._focus_input()
                    
                else:
                    self.log_area.append_log(
                        "FAILED",
                        f"Opción de edición no reconocida: {sub_opt}",
                        route=self.current_route
                    )
                    self._focus_input()
                                    
            elif cmd_name in ("delete", "rm"):
                args = parsed["args"]
                if not args:
                    self.log_area.append_log(
                        "FAILED",
                        "Uso: rm --song <numero> | rm --song-all | rm --album",
                        route=self.current_route
                    )
                    self._focus_input()
                    return
                    
                sub_opt = args[0].lower()
                
                # Validar contexto de navegación para canciones
                from pathlib import Path
                current_path = Path(self.current_route)
                downloads_path = self.vault_service.download_dir
                
                if sub_opt in ("--song", "--song-all"):
                    is_valid_album = (
                        current_path.exists()
                        and current_path.is_dir()
                        and (current_path.parent == downloads_path or current_path == downloads_path / "Sin album")
                    )
                    
                    if not is_valid_album:
                        self.log_area.append_log(
                            "FAILED",
                            "ERR: Debe navegar primero al álbum que contiene las canciones.",
                            route=self.current_route
                        )
                        self._focus_input()
                        return
                        
                    # Escanear y ordenar canciones alfabéticamente
                    songs = []
                    for file in current_path.iterdir():
                        if file.is_file() and file.suffix.lower() in (".mp3", ".wav", ".m4a", ".ogg"):
                            songs.append(file.name)
                    songs.sort()
                    
                    songs_to_delete = []
                    is_valid = True
                    
                    if sub_opt == "--song":
                        if len(args) < 2:
                            self.log_area.append_log(
                                "FAILED",
                                "ERR: Especifique el número o números de canción (ej. rm --song 1 o rm --song 1,2).",
                                route=self.current_route
                            )
                            self._focus_input()
                            return
                            
                        numbers_str = "".join(args[1:])
                        try:
                            nums = [int(n.strip()) for n in numbers_str.split(",") if n.strip()]
                            if not nums:
                                raise ValueError()
                        except ValueError:
                            self.log_area.append_log(
                                "FAILED",
                                "ERR: Los números de canciones deben ser enteros válidos separados por comas.",
                                route=self.current_route
                            )
                            self._focus_input()
                            return
                            
                        for num in nums:
                            if num < 1 or num > len(songs):
                                self.log_area.append_log(
                                    "FAILED",
                                    f"ERR: El número de canción {num} no existe (rango 1-{len(songs)}).",
                                    route=self.current_route
                                )
                                self._focus_input()
                                return
                            songs_to_delete.append(str(current_path / songs[num - 1]))
                            
                    elif sub_opt == "--song-all":
                        if not songs:
                            self.log_area.append_log(
                                "FAILED",
                                "ERR: El álbum actual no contiene canciones para eliminar.",
                                route=self.current_route
                            )
                            self._focus_input()
                            return
                        songs_to_delete = [str(current_path / s) for s in songs]
                        
                    if songs_to_delete:
                        if len(songs_to_delete) == 1:
                            song_name = Path(songs_to_delete[0]).name
                            warn_msg = f"ADVERTENCIA: ¿Está seguro que desea ELIMINAR permanentemente la canción '{song_name}'? (y/n):"
                        else:
                            warn_msg = f"ADVERTENCIA: ¿Está seguro que desea ELIMINAR permanentemente {len(songs_to_delete)} canciones de este álbum? (y/n):"
                            
                        self._interactive_state = "CONFIRM_DELETE"
                        self._pending_delete_op = {
                            "type": "songs_multiple",
                            "params": {
                                "song_paths": songs_to_delete
                            }
                        }
                        self.log_area.append_log("WARN", warn_msg, route=self.current_route)
                        self.command_writer.set_prompt("CONFIRMAR (y/n) > ")
                        self._focus_input()
                        
                elif sub_opt == "--album":
                    # Validar contexto de navegación (debe estar en un álbum personal)
                    is_valid_album = (
                        current_path.exists()
                        and current_path.is_dir()
                        and current_path.parent == downloads_path
                        and current_path.name != "Sin album"
                    )
                    
                    if not is_valid_album:
                        self.log_area.append_log(
                            "FAILED",
                            "ERR: Debe navegar primero al álbum que desea eliminar. (No se puede eliminar 'Sin album' ni la raíz)",
                            route=self.current_route
                        )
                        self._focus_input()
                        return
                        
                    # Iniciar confirmación interactiva y/n
                    self._interactive_state = "CONFIRM_DELETE"
                    self._pending_delete_op = {
                        "type": "album",
                        "params": {
                            "album_path": str(current_path),
                            "album_name": current_path.name
                        }
                    }
                    self.log_area.append_log(
                        "WARN",
                        f"ADVERTENCIA: ¿Está seguro que desea ELIMINAR permanentemente el álbum '{current_path.name}' y TODAS sus canciones? (y/n):",
                        route=self.current_route
                    )
                    self.command_writer.set_prompt("CONFIRMAR (y/n) > ")
                    self._focus_input()
                    
                else:
                    self.log_area.append_log(
                        "FAILED",
                        f"Opción de eliminación no reconocida: {sub_opt}. Uso: rm --song <numero> | rm --song-all | rm --album",
                        route=self.current_route
                    )
                    self._focus_input()
            else:
                # Si el comando está registrado en el backend pero no tiene flujo de UI aún (ej. stubs)
                if cmd_name != "unknown":
                    self.log_area.append_log(
                        "INFO", 
                        f"El comando '{cmd_name}' está registrado en el sistema, pero su implementación interactiva está PENDIENTE (sección 2.8/3.2).",
                        route=self.current_route
                    )
                else:
                    # Comando realmente no reconocido
                    arg_str = parsed["args"][0] if parsed["args"] else ""
                    self.log_area.append_log("FAILED", f"ERR: Command '{arg_str}' not recognized or missing parameters.")
                self._focus_input()
                
        elif parsed["type"] == "shortcut":
            # RF-036: Navegación directa mediante atajo de nombre
            target_type = parsed["target"]
            if target_type == "sin_album":
                target_path = str(self.vault_service.download_dir / "Sin album")
                self._navigate_to("sin_album", target_path)
            elif target_type == "album":
                album_name = parsed["album_name"]
                target_path = str(self.vault_service.download_dir / album_name)
                self._navigate_to("album", target_path, album_name)
                
        elif parsed["type"] == "url":
            # RF-010: Interpretado como URL
            # RF-011: Validar si la URL es válida o inválida
            if parsed["status"] == "invalid":
                self.log_area.append_log("FAILED", f"La URL ingresada no es válida: {parsed['url']}")
                self._focus_input()
            else:
                # URL Válida: entramos al flujo interactivo de metadatos (RF-033)
                self._pending_url = parsed["url"]
                self._collected_metadata = {}
                self._interactive_state = "ASK_ALBUM"
                
                self.log_area.append_log("SUCCESS", f"URL de YouTube aceptada (RF-030).")
                self.log_area.append_log("INFO", "PROPORCIONE LOS METADATOS DE LA CANCIÓN:")
                self.log_area.append_log("INFO", "  INGRESE ÁLBUM (Presione Enter para 'Sin album'):")
                self.command_writer.set_prompt("ALBUM > ")
                self._focus_input()

    def _handle_metadata_input(self, text: str):
        val = text.strip()
        
        if self._interactive_state == "CONFIRM_DELETE":
            confirm = val.lower()
            if confirm in ("y", "yes"):
                op = self._pending_delete_op
                op_type = op["type"]
                params = op["params"]
                
                try:
                    if op_type == "song":
                        from pathlib import Path
                        song_path = Path(params["song_path"])
                        if song_path.exists():
                            song_path.unlink()
                            self._cleanup_exported_songs([params["song_path"]])
                            self.log_area.append_log(
                                "SUCCESS",
                                f"Canción '{song_path.name}' eliminada con éxito.",
                                route=self.current_route
                            )
                        else:
                            self.log_area.append_log(
                                "FAILED",
                                f"ERR: La canción ya no existe.",
                                route=self.current_route
                            )
                            
                    elif op_type == "songs_multiple":
                        from pathlib import Path
                        song_paths = params["song_paths"]
                        deleted_count = 0
                        deleted_ok = []
                        for sp in song_paths:
                            song_path = Path(sp)
                            if song_path.exists():
                                song_path.unlink()
                                deleted_ok.append(sp)
                                deleted_count += 1
                                self.log_area.append_log(
                                    "SUCCESS",
                                    f"Canción '{song_path.name}' eliminada con éxito.",
                                    route=self.current_route
                                )
                        if deleted_ok:
                            self._cleanup_exported_songs(deleted_ok)
                        if deleted_count == 0:
                            self.log_area.append_log(
                                "FAILED",
                                "ERR: Ninguna canción pudo ser eliminada (ya no existen).",
                                route=self.current_route
                            )
                            
                    elif op_type == "album":
                        from pathlib import Path
                        import shutil
                        album_path = Path(params["album_path"])
                        album_name = params["album_name"]
                        if album_path.exists():
                            shutil.rmtree(album_path)
                            self._cleanup_exported_songs([params["album_path"]])
                            self.vault_history.vault_tab.expanded_states.pop(album_name, None)
                            
                            self.log_area.append_log(
                                "SUCCESS",
                                f"Álbum '{album_name}' y todas sus canciones fueron eliminados con éxito.",
                                route=self.current_route
                            )
                            
                            # Navegar automáticamente a la raíz porque el álbum actual fue borrado
                            target_raiz = "C:\\Users\\Gustavo\\Documents\\mp3dowloaderProject"
                            self._navigate_to("raiz", target_raiz)
                        else:
                            self.log_area.append_log(
                                "FAILED",
                                f"ERR: El álbum ya no existe.",
                                route=self.current_route
                            )
                            
                    self.vault_history.refresh_all()
                    
                except Exception as e:
                    self.log_area.append_log(
                        "FAILED",
                        f"ERR al eliminar: {e}",
                        route=self.current_route
                    )
            else:
                self.log_area.append_log(
                    "FAILED",
                    "Eliminación cancelada por el usuario.",
                    route=self.current_route
                )
                
            self._interactive_state = None
            self._pending_delete_op = {}
            self.command_writer.set_prompt(self.PROMPT)
            self._focus_input()
            return
            
        if self._interactive_state == "CONFIRM_EDIT":
            confirm = val.lower()
            if confirm in ("y", "yes"):
                op = self._pending_edit_op
                op_type = op["type"]
                params = op["params"]
                
                try:
                    if op_type == "album_rename":
                        from pathlib import Path
                        old_path = Path(params["old_path"])
                        new_path = Path(params["new_path"])
                        old_name = params["old_name"]
                        new_name = params["new_name"]
                        
                        old_path.rename(new_path)
                        
                        self.vault_history.vault_tab.expanded_states.pop(old_name, None)
                        self.vault_history.vault_tab.expanded_states[new_name] = True
                        
                        if self.current_route == str(old_path):
                            self.current_route = str(new_path)
                            
                        self.log_area.append_log(
                            "SUCCESS",
                            f"El álbum '{old_name}' ha sido renombrado a '{new_name}' con éxito.",
                            route=self.current_route
                        )
                        
                    elif op_type == "song_name":
                        from pathlib import Path
                        song_path = Path(params["song_path"])
                        new_song_path = Path(params["new_song_path"])
                        new_title = params["new_title"]
                        
                        song_path.rename(new_song_path)
                        
                        try:
                            from mutagen.easyid3 import EasyID3
                            audio = EasyID3(new_song_path)
                            audio['title'] = new_title
                            audio.save()
                        except Exception:
                            pass
                            
                        self.log_area.append_log(
                            "SUCCESS",
                            f"Canción renombrada a '{new_title}' con éxito.",
                            route=self.current_route
                        )
                        
                    elif op_type == "song_album":
                        from pathlib import Path
                        import shutil
                        song_path = Path(params["song_path"])
                        new_song_path = Path(params["new_song_path"])
                        new_album = params["new_album"]
                        
                        new_song_path.parent.mkdir(parents=True, exist_ok=True)
                        shutil.move(str(song_path), str(new_song_path))
                        
                        try:
                            from mutagen.easyid3 import EasyID3
                            audio = EasyID3(new_song_path)
                            audio['album'] = new_album
                            audio.save()
                        except Exception:
                            pass
                            
                        self.vault_history.vault_tab.expanded_states[new_album] = True
                        
                        self.log_area.append_log(
                            "SUCCESS",
                            f"Canción movida al álbum '{new_album}' con éxito.",
                            route=self.current_route
                        )
                        
                    elif op_type == "song_artist":
                        from pathlib import Path
                        song_path = Path(params["song_path"])
                        new_artist = params["new_artist"]
                        
                        try:
                            from mutagen.easyid3 import EasyID3
                            audio = EasyID3(song_path)
                            audio['artist'] = new_artist
                            audio.save()
                        except Exception:
                            pass
                            
                        self.log_area.append_log(
                            "SUCCESS",
                            f"Artista de la canción cambiado a '{new_artist}' con éxito.",
                            route=self.current_route
                        )
                        
                    self.vault_history.refresh_all()
                    
                except Exception as e:
                    self.log_area.append_log(
                        "FAILED",
                        f"ERR al realizar modificación: {e}",
                        route=self.current_route
                    )
            else:
                self.log_area.append_log(
                    "FAILED",
                    "Modificación cancelada por el usuario.",
                    route=self.current_route
                )
                
            self._interactive_state = None
            self._pending_edit_op = {}
            self.command_writer.set_prompt(" >_ ")
            self._focus_input()
            return
            
        elif self._interactive_state == "ASK_ALBUM":
            # Si el usuario no asigna álbum, se almacena en "Sin album" (RF-034)
            album = val if val else "Sin album"
            self._collected_metadata["album"] = album
            self.log_area.append_log("INFO", f"  Álbum asignado: {album}")
            
            # Pasar al siguiente estado
            self._interactive_state = "ASK_SONG"
            self.log_area.append_log("INFO", "  INGRESE NOMBRE DE LA CANCIÓN (Presione Enter para usar título de YouTube):")
            self.command_writer.set_prompt("CANCIÓN > ")
            self._focus_input()
            
        elif self._interactive_state == "ASK_SONG":
            self._collected_metadata["song"] = val
            self.log_area.append_log("INFO", f"  Canción asignada: {val if val else '(Título de YouTube)'}")
            
            # Pasar al siguiente estado
            self._interactive_state = "ASK_ARTIST"
            self.log_area.append_log("INFO", "  INGRESE ARTISTA (Presione Enter para 'Artista Desconocido'):")
            self.command_writer.set_prompt("ARTISTA > ")
            self._focus_input()
            
        elif self._interactive_state == "ASK_ARTIST":
            artist = val if val else "Artista Desconocido"
            self._collected_metadata["artist"] = artist
            self.log_area.append_log("INFO", f"  Artista asignado: {artist}")
            
            # Finalizar recolección directamente sin pedir metadatos del álbum
            self._interactive_state = None
            self.command_writer.set_prompt(" >_ ")
            
            # Mostrar tarjeta de confirmación premium
            album = self._collected_metadata["album"]
            song = self._collected_metadata["song"]
            artist = self._collected_metadata["artist"]
            
            confirm_lines = [
                " ╔" + "═" * 48 + "╗",
                " ║" + "             CONFIRMACIÓN DE METADATOS          " + " ║",
                " ╠" + "═" * 48 + "╣",
                f" ║  Álbum:     {album:<34}  ║",
                f" ║  Canción:   {song if song else '(Título de YouTube)':<34}  ║",
                f" ║  Artista:   {artist:<34}  ║",
                " ╚" + "═" * 48 + "╝"
            ]
            self.log_area.append_log("SUCCESS", "\n".join(confirm_lines))
            
            # Iniciar descarga asíncrona asumiendo estado ocupado
            self._lock_input()
            self.log_area.append_log("INFO", f"Iniciando descarga: {self._pending_url}")
            
            url = self._pending_url
            metadata = self._collected_metadata.copy()
            metadata["description"] = ""  # Dejamos vacío el campo description por compatibilidad
            
            self._pending_url = None
            self._collected_metadata = {}
            
            import threading
            threading.Thread(target=self._download_task, args=(url, metadata), daemon=True).start()

    def _download_task(self, url: str, metadata: dict):
        last_was_progress = False

        def on_progress(msg: str, tag: str = "gray"):
            nonlocal last_was_progress
            if tag == "progress":
                if last_was_progress:
                    self.after(0, lambda m=msg, t=tag: self._overwrite_last(m, t))
                else:
                    self.after(0, lambda m=msg, t=tag: self._print(m, t))
                last_was_progress = True
            else:
                last_was_progress = False
                self.after(0, lambda m=msg, t=tag: self._print(m, t))

        try:
            album_name = metadata["album"]
            album_dir = self.vault_service.download_dir / album_name

            on_progress("  connecting...", "muted")
            self.after(0, lambda: self._print("", "progress"))
            path = self.download_service.process_download(url, album_dir=album_dir, progress_callback=on_progress)
            self.after(0, lambda: self._print("", "muted"))

            # Renombrar y aplicar metadatos nativos usando Mutagen (RF-033)
            import re
            song_name = metadata["song"]
            clean_song_name = ""
            if song_name:
                clean_song_name = re.sub(r'[\\/*?:"<>|]', "", song_name).strip()
                new_path = path.with_name(f"{clean_song_name}.mp3")
                if path != new_path:
                    if new_path.exists():
                        new_path.unlink()
                    path.rename(new_path)
                    path = new_path

            # Escribir etiquetas ID3 nativas usando Mutagen (tolerante a fallos si no está instalado)
            try:
                from mutagen.easyid3 import EasyID3
                from mutagen.id3 import ID3, COMM
                
                try:
                    audio = EasyID3(path)
                except Exception:
                    from mutagen.mp3 import MP3
                    mp3_file = MP3(path)
                    if mp3_file.tags is None:
                        mp3_file.add_tags()
                        mp3_file.save()
                    audio = EasyID3(path)
                    
                audio['title'] = clean_song_name if clean_song_name else path.stem
                audio['artist'] = metadata["artist"]
                audio['album'] = album_name
                audio.save()
                
                # Escribir metadatos del álbum (comentarios)
                if metadata["description"]:
                    try:
                        id3_tags = ID3(path)
                        id3_tags["COMM"] = COMM(
                            encoding=3,  # UTF-8
                            lang="eng",
                            desc="Album Metadata",
                            text=[metadata["description"]]
                        )
                        id3_tags.save()
                    except Exception:
                        pass
            except ImportError:
                # Si mutagen no está en el interprete activo, degradar graciosamente sin fallar
                pass

            self.after(0, lambda: self._print(f"  done   {path.name}", "green"))
            self.after(0, lambda: self._print(f"  saved  {path.parent}", "gray"))

            # Registrar éxito en historial y refrescar interfaz (RF-023, RF-027, RF-035)
            self.history_service.add_record(path.name, "SUCCESS")
            self.after(0, self.vault_history.refresh_all)

        except Exception as e:
            err_msg = str(e)
            self.after(0, lambda msg=err_msg: self._print(f"  error  {msg}", "red"))

            # Registrar fallo en historial y refrescar interfaz (RF-023, RF-027, RF-035)
            clean_err = err_msg.split(":")[0].strip().upper()
            if not clean_err or len(clean_err) > 30 or "ERR" in clean_err:
                clean_err = "DOWNLOAD_ERROR"
            self.history_service.add_record(clean_err, "FAILED")
            self.after(0, self.vault_history.refresh_all)

        finally:
            self.after(0, self._unlock_input)

    def _on_route_changed(self, new_route: str):
        """Callback gatillado al interactuar con el Vault (RF-026, RF-037)."""
        from pathlib import Path
        p = Path(new_route)
        
        # RF-037: Mantener el contexto de carpeta actual al hacer clic
        if p.is_file():
            self.current_route = str(p.parent)
        else:
            self.current_route = new_route
            # Clics/toggles visuales en álbumes son silenciosos (no emiten logs)
            return
            
        # Si ya había una canción reproduciéndose, loguear que se detiene antes de iniciar la nueva
        if self._playback_timer is not None:
            try:
                self.after_cancel(self._playback_timer)
            except Exception:
                pass
            self._playback_timer = None
            
        if self._current_playing_song is not None:
            self.log_area.append_log(
                "INFO", 
                f"Se ha finalizado la reproducción de la canción: {self._current_playing_song}", 
                route=self.current_route
            )
            
        # Iniciar la reproducción de la nueva canción
        self._current_playing_song = p.name
        self.log_area.append_log(
            "INFO", 
            f"Se ha iniciado la reproducción de la canción: {p.name}", 
            route=self.current_route
        )
        
        # Abrir la canción en el reproductor de Windows
        import os
        try:
            os.startfile(new_route)
        except Exception as e:
            self.log_area.append_log(
                "FAILED", 
                f"No se pudo iniciar la reproducción: {e}", 
                route=self.current_route
            )
            self._current_playing_song = None
            return
            
        # Intentar obtener la duración exacta del MP3 usando Mutagen para programar el log de finalización
        duration = 180  # Valor por defecto de 3 minutos
        try:
            from mutagen.mp3 import MP3
            audio = MP3(new_route)
            duration = int(audio.info.length)
        except Exception:
            pass
            
        # Programar log de finalización cuando termine la canción de forma natural
        def on_playback_finished():
            if self._current_playing_song == p.name:
                self.log_area.append_log(
                    "INFO", 
                    f"Se ha finalizado la reproducción de la canción: {p.name}", 
                    route=self.current_route
                )
                self._current_playing_song = None
                self._playback_timer = None
                
        self._playback_timer = self.after(duration * 1000, on_playback_finished)

    def _navigate_to(self, target_type: str, path: str, name: str = ""):
        """Helper para navegar a una ruta física, actualizar contexto y abrir visualmente el contenido (RF-036 al RF-039)."""
        self.current_route = path
        
        # RF-039: Al navegar a un album o sin-album, abrir visualmente su contenido. Si es raíz, colapsar todos.
        if target_type == "raiz":
            for key in list(self.vault_history.vault_tab.expanded_states.keys()):
                self.vault_history.vault_tab.expanded_states[key] = False
            # Mantener visible el contenedor principal vault_storage
            self.vault_history.vault_tab.expanded_states["vault_storage"] = True
            self.vault_history.vault_tab.refresh()
        elif target_type == "sin_album":
            self.vault_history.vault_tab.expanded_states["sin_album"] = True
            self.vault_history.vault_tab.refresh()
        elif target_type == "album":
            self.vault_history.vault_tab.expanded_states[name] = True
            self.vault_history.vault_tab.refresh()
            
        # RF-038: La ruta actual debe mostrarse en los logs (usamos la nueva ruta como ruta activa)
        self.log_area.append_log("INFO", f"Navegando a: {path}", route=self.current_route)
        self._focus_input()

    # ── Control de Input ──────────────────────────────────────────────────────

    def _lock_input(self):
        self._is_busy = True
        self.command_writer.lock()

    def _unlock_input(self):
        self._is_busy = False
        self.command_writer.unlock()
        self._print("")
        self._focus_input()

    def _focus_input(self):
        self.command_writer.focus()
