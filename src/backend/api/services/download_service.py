from pathlib import Path
from typing import Callable
from src.backend.api.core.utils import is_valid_youtube_url
from src.backend.api.core.exceptions import InvalidUrlError
from src.backend.api.infrastructure.audio_adapter import YtDlpAdapter


class DownloadService:
    def __init__(self, audio_adapter: YtDlpAdapter, download_dir: Path):
        self.audio_adapter = audio_adapter
        self.download_dir = download_dir
        self.download_dir.mkdir(parents=True, exist_ok=True)

    def process_download(
        self,
        url: str,
        album_dir: Path | None = None,
        progress_callback: Callable[[str, str], None] | None = None,
    ) -> Path:
        if not url:
            raise InvalidUrlError("La URL no puede estar vacía.")
        if not is_valid_youtube_url(url):
            raise InvalidUrlError("La URL no corresponde a YouTube.")
            
        target_dir = album_dir if album_dir is not None else self.download_dir
        target_dir.mkdir(parents=True, exist_ok=True)
        return self.audio_adapter.download_audio(url, target_dir, progress_callback)
