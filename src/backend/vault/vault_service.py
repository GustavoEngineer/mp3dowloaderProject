from pathlib import Path

class VaultService:
    """Servicio de backend para administrar los álbumes y canciones del Vault (RF-020 al RF-026)."""
    
    def __init__(self, download_dir: Path):
        self.download_dir = Path(download_dir)
        self.ensure_directories()

    def ensure_directories(self):
        """Asegura que el directorio downloads y la carpeta 'Sin album' existan (RF-022)."""
        self.download_dir.mkdir(parents=True, exist_ok=True)
        sin_album_dir = self.download_dir / "Sin album"
        sin_album_dir.mkdir(parents=True, exist_ok=True)

    def get_vault_structure(self) -> dict:
        """Escanea la carpeta de descargas para retornar la estructura en formato de árbol (RF-020, RF-021)."""
        self.ensure_directories()
        
        albums = []
        # Escanea subdirectorios de la carpeta de descargas
        for item in self.download_dir.iterdir():
            if item.is_dir() and not item.name.startswith("."):
                songs = []
                for file in item.iterdir():
                    if file.is_file() and file.suffix.lower() in (".mp3", ".wav", ".m4a", ".ogg"):
                        songs.append(file.name)
                
                albums.append({
                    "name": item.name,
                    "path": str(item),
                    "songs": sorted(songs),
                    "count": len(songs)
                })
        
        # Ordenar: "Sin album" primero, luego alfabéticamente
        albums.sort(key=lambda a: (0 if a["name"] == "Sin album" else 1, a["name"].lower()))
        
        return {
            "name": "VAULT_STORAGE",
            "albums": albums
        }
