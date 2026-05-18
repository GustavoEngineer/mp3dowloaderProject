import re
import yt_dlp
import imageio_ffmpeg
from pathlib import Path
from typing import Callable
from src.backend.api.core.exceptions import DownloadError

# Elimina secuencias ANSI de color que yt-dlp inyecta en sus strings
_ANSI = re.compile(r"\x1B(?:[@-Z\\-_]|\[[0-?]*[ -/]*[@-~])")

def _strip(text: str) -> str:
    return _ANSI.sub("", text).strip()


class YtDlpAdapter:
    def download_audio(
        self,
        url: str,
        output_path: Path,
        progress_callback: Callable[[str, str], None] | None = None,
    ) -> Path:
        ffmpeg_path = imageio_ffmpeg.get_ffmpeg_exe()

        def _hook(d: dict):
            if progress_callback is None:
                return
            if d["status"] == "downloading":
                percent_raw = _strip(d.get("_percent_str", "0%"))
                speed_raw   = _strip(d.get("_speed_str", "--"))
                eta_raw     = _strip(d.get("_eta_str", "--"))
                try:
                    pct = float(percent_raw.replace("%", ""))
                except ValueError:
                    pct = 0.0
                bar = _dot_bar(pct)
                msg = f"  {bar}  {percent_raw:<6}  {speed_raw:<12}  eta {eta_raw}"
                progress_callback(msg, "progress")
            elif d["status"] == "finished":
                progress_callback("  converting to mp3...", "muted")

        ydl_opts = {
            "ffmpeg_location": ffmpeg_path,
            "format": "bestaudio[ext=m4a]/bestaudio[ext=webm]/bestaudio/best",
            "postprocessors": [{"key": "FFmpegExtractAudio", "preferredcodec": "mp3", "preferredquality": "192"}],
            "outtmpl": str(output_path / "%(title)s.%(ext)s"),
            "quiet": True,
            "no_warnings": True,
            "progress_hooks": [_hook],
        }

        try:
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                info = ydl.extract_info(url, download=True)
                mp3_path = Path(ydl.prepare_filename(info)).with_suffix(".mp3")
                if mp3_path.exists():
                    return mp3_path
                raise DownloadError("Archivo MP3 no encontrado tras la descarga.")
        except DownloadError:
            raise
        except Exception as e:
            raise DownloadError(_strip(str(e)))


def _dot_bar(percent: float, width: int = 20) -> str:
    """Barra minimalista de puntos: ···············╸"""
    filled = int((percent / 100) * width)
    if filled >= width:
        return "·" * width
    bar = "·" * filled + "╸" + " " * (width - filled - 1)
    return bar
