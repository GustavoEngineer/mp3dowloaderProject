import tkinter as tk
from pathlib import Path

class ScrollableFrame(tk.Frame):
    """Contenedor scrollable premium y responsivo utilizando Canvas en Tkinter."""
    def __init__(self, parent, bg_color):
        super().__init__(parent, bg=bg_color)
        
        self.canvas = tk.Canvas(self, bg=bg_color, bd=0, highlightthickness=0)
        self.scrollbar = tk.Scrollbar(self, orient="vertical", command=self.canvas.yview)
        self.scrollable_frame = tk.Frame(self.canvas, bg=bg_color)
        
        self.scrollable_frame.bind(
            "<Configure>",
            lambda e: self.canvas.configure(
                scrollregion=self.canvas.bbox("all")
            )
        )
        
        self.canvas_window = self.canvas.create_window((0, 0), window=self.scrollable_frame, anchor="nw")
        self.canvas.bind("<Configure>", self._on_canvas_configure)
        self.canvas.configure(yscrollcommand=self.scrollbar.set)
        
        self.canvas.pack(side="left", fill="both", expand=True)
        self.scrollbar.pack(side="right", fill="y")
        
        # Enlace inteligente del mouse wheel para evitar conflictos de scroll
        self.canvas.bind("<Enter>", lambda e: self.canvas.bind_all("<MouseWheel>", self._on_mousewheel))
        self.canvas.bind("<Leave>", lambda e: self.canvas.unbind_all("<MouseWheel>"))

    def _on_canvas_configure(self, event):
        self.canvas.itemconfig(self.canvas_window, width=event.width)

    def _on_mousewheel(self, event):
        if self.winfo_exists():
            self.canvas.yview_scroll(int(-1 * (event.delta / 120)), "units")


class VaultTab(tk.Frame):
    """Componente visual de árbol de directorios y álbumes simplificado (RF-020 al RF-026)."""
    
    def __init__(self, parent, vault_service, on_route_changed, bg_color="#0D0D0D"):
        super().__init__(parent, bg=bg_color)
        self.vault_service = vault_service
        self.on_route_changed = on_route_changed
        self.bg_color = bg_color
        
        # Estados de expansión por defecto
        self.expanded_states = {
            "vault_storage": True,
            "sin_album": True
        }
        
        # Crear contenedor scrollable
        self.scroll_container = ScrollableFrame(self, bg_color=bg_color)
        self.scroll_container.pack(fill="both", expand=True, padx=10, pady=10)
        
        self.refresh()

    def refresh(self):
        """Escanea el Vault y renderiza dinámicamente el árbol visual (RF-023)."""
        # Limpiar elementos previos
        for widget in self.scroll_container.scrollable_frame.winfo_children():
            widget.destroy()
            
        # Cargar canciones exportadas para mostrarlas en gris
        import json
        exported_set = set()
        exported_json_path = self.vault_service.download_dir.parent / "exported_songs.json"
        if exported_json_path.exists():
            try:
                with open(exported_json_path, "r", encoding="utf-8") as f:
                    exported_list = json.load(f)
                    exported_set = set(exported_list)
            except Exception:
                pass

        # Obtener estructura del backend
        data = self.vault_service.get_vault_structure()
        
        # Clasificar álbumes
        sin_album_item = None
        other_albums = []
        for album in data["albums"]:
            if album["name"] == "Sin album":
                sin_album_item = album
            else:
                other_albums.append(album)
                
        # Asegurar estados iniciales
        if "vault_storage" not in self.expanded_states:
            self.expanded_states["vault_storage"] = True
        if "raiz" not in self.expanded_states:
            self.expanded_states["raiz"] = True

        # ─── NODO 1: VAULT_STORAGE (Contenedor de Álbumes) ───
        is_storage_expanded = self.expanded_states["vault_storage"]
        storage_arrow = "▼" if is_storage_expanded else "▶"
        
        storage_frame = tk.Frame(self.scroll_container.scrollable_frame, bg=self.bg_color)
        storage_frame.pack(fill="x", anchor="w", pady=(0, 4))
        
        lbl_storage = tk.Label(
            storage_frame,
            text=f"{storage_arrow} VAULT_STORAGE",
            fg="#5A8FA8",
            bg=self.bg_color,
            font=("Courier New", 12, "bold"),
            anchor="w",
            cursor="hand2"
        )
        lbl_storage.pack(fill="x", side="left", expand=True)
        lbl_storage.bind("<Enter>", lambda e, lbl=lbl_storage: lbl.configure(fg="#00E5A3"))
        lbl_storage.bind("<Leave>", lambda e, lbl=lbl_storage: lbl.configure(fg="#5A8FA8"))
        lbl_storage.bind("<Button-1>", lambda e: self._toggle_storage("vault_storage"))
        
        # Renderizar álbumes si VAULT_STORAGE está expandido
        if is_storage_expanded:
            for album in other_albums:
                name = album["name"]
                count = album["count"]
                path = album["path"]
                
                if name not in self.expanded_states:
                    self.expanded_states[name] = False
                    
                is_expanded = self.expanded_states[name]
                arrow = "▼" if is_expanded else "▶"
                album_text = f"  {arrow} {name.upper()} / {count} canciones"
                
                album_frame = tk.Frame(self.scroll_container.scrollable_frame, bg=self.bg_color)
                album_frame.pack(fill="x", anchor="w", pady=1)
                
                lbl_album = tk.Label(
                    album_frame,
                    text=album_text,
                    fg="#808080" if not is_expanded else "#00E5A3",
                    bg=self.bg_color,
                    font=("Courier New", 11, "bold"),
                    anchor="w",
                    cursor="hand2"
                )
                lbl_album.pack(fill="x", side="left", expand=True)
                
                lbl_album.bind("<Enter>", lambda e, lbl=lbl_album: lbl.configure(fg="#00E5A3"))
                lbl_album.bind(
                    "<Leave>", 
                    lambda e, lbl=lbl_album, n=name: lbl.configure(
                        fg="#00E5A3" if self.expanded_states[n] else "#808080"
                    )
                )
                lbl_album.bind(
                    "<Button-1>",
                    lambda e, n=name, p=path: self._toggle_album(n, p)
                )
                
                # Listar canciones de álbum
                if is_expanded:
                    if not album["songs"]:
                        lbl_empty = tk.Label(
                            self.scroll_container.scrollable_frame,
                            text="      (álbum vacío)",
                            fg="#505050",
                            bg=self.bg_color,
                            font=("Courier New", 10, "italic"),
                            anchor="w"
                        )
                        lbl_empty.pack(fill="x", anchor="w", pady=1)
                    else:
                        for idx, song in enumerate(album["songs"], 1):
                            song_frame = tk.Frame(self.scroll_container.scrollable_frame, bg=self.bg_color)
                            song_frame.pack(fill="x", anchor="w", pady=1)
                            
                            song_path = str(Path(path) / song)
                            
                            is_exported = str(Path(song_path).resolve()) in exported_set
                            song_fg = "#666666" if is_exported else "#EDEDED"

                            lbl_song = tk.Label(
                                song_frame,
                                text=f"      📄 {idx}. {song}",
                                fg=song_fg,
                                bg=self.bg_color,
                                font=("Courier New", 11),
                                anchor="w",
                                cursor="hand2"
                            )
                            lbl_song.pack(fill="x", side="left", expand=True)
                            
                            lbl_song.bind("<Enter>", lambda e, lbl=lbl_song: lbl.configure(fg="#6BA3CC"))
                            lbl_song.bind("<Leave>", lambda e, lbl=lbl_song, fg=song_fg: lbl.configure(fg=fg))
                            lbl_song.bind(
                                "<Button-1>",
                                lambda e, sp=song_path: self.on_route_changed(sp)
                            )

        # ─── NODO 2: SIN ALBUM (Canciones sin álbum en el mismo nivel) ───
        is_sin_album_expanded = self.expanded_states["sin_album"]
        sin_album_arrow = "▼" if is_sin_album_expanded else "▶"
        
        raiz_songs = sin_album_item["songs"] if sin_album_item else []
        raiz_path = str(self.vault_service.download_dir)
        
        raiz_frame = tk.Frame(self.scroll_container.scrollable_frame, bg=self.bg_color)
        raiz_frame.pack(fill="x", anchor="w", pady=(8, 4))
        
        lbl_raiz = tk.Label(
            raiz_frame,
            text=f"{sin_album_arrow} SIN ALBUM",
            fg="#5A8FA8",
            bg=self.bg_color,
            font=("Courier New", 12, "bold"),
            anchor="w",
            cursor="hand2"
        )
        lbl_raiz.pack(fill="x", side="left", expand=True)
        lbl_raiz.bind("<Enter>", lambda e, lbl=lbl_raiz: lbl.configure(fg="#00E5A3"))
        lbl_raiz.bind("<Leave>", lambda e, lbl=lbl_raiz: lbl.configure(fg="#5A8FA8"))
        lbl_raiz.bind("<Button-1>", lambda e: self._toggle_sin_album("sin_album", raiz_path))
        
        # Renderizar canciones de la raíz
        if is_sin_album_expanded:
            if not raiz_songs:
                lbl_empty = tk.Label(
                    self.scroll_container.scrollable_frame,
                    text="  (directorio vacío)",
                    fg="#505050",
                    bg=self.bg_color,
                    font=("Courier New", 10, "italic"),
                    anchor="w"
                )
                lbl_empty.pack(fill="x", anchor="w", pady=1)
            else:
                for idx, song in enumerate(raiz_songs, 1):
                    song_frame = tk.Frame(self.scroll_container.scrollable_frame, bg=self.bg_color)
                    song_frame.pack(fill="x", anchor="w", pady=1)
                    
                    song_path = str(self.vault_service.download_dir / "Sin album" / song)
                    
                    is_exported = str(Path(song_path).resolve()) in exported_set
                    song_fg = "#666666" if is_exported else "#EDEDED"

                    lbl_song = tk.Label(
                        song_frame,
                        text=f"  📄 {idx}. {song}",
                        fg=song_fg,
                        bg=self.bg_color,
                        font=("Courier New", 11),
                        anchor="w",
                        cursor="hand2"
                    )
                    lbl_song.pack(fill="x", side="left", expand=True)
                    
                    lbl_song.bind("<Enter>", lambda e, lbl=lbl_song: lbl.configure(fg="#6BA3CC"))
                    lbl_song.bind("<Leave>", lambda e, lbl=lbl_song, fg=song_fg: lbl.configure(fg=fg))
                    lbl_song.bind(
                        "<Button-1>",
                        lambda e, sp=song_path: self.on_route_changed(sp)
                    )

    def _toggle_storage(self, name: str):
        """Alterna el estado de expansión de VAULT_STORAGE."""
        self.expanded_states[name] = not self.expanded_states[name]
        self.refresh()

    def _toggle_sin_album(self, name: str, path: str):
        """Alterna el estado de expansión de SIN ALBUM y actualiza la ruta del sistema."""
        self.expanded_states[name] = not self.expanded_states[name]
        self.on_route_changed(path)
        self.refresh()

    def _toggle_album(self, album_name: str, path: str):
        """Alterna el estado de expansión del álbum y actualiza la ruta (RF-024, RF-026)."""
        self.expanded_states[album_name] = not self.expanded_states[album_name]
        self.on_route_changed(path)
        self.refresh()
