from pydantic_settings import BaseSettings, SettingsConfigDict
from pathlib import Path

class Settings(BaseSettings):
    app_name: str = "mp3downloader"
    base_dir: Path = Path(__file__).resolve().parent.parent.parent.parent.parent
    download_dir: Path = base_dir / "downloads"
    temp_dir: Path = base_dir / "temp"

    model_config = SettingsConfigDict(env_file='.env', env_file_encoding='utf-8', extra='ignore')

settings = Settings()
