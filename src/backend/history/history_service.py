import json
import datetime
from pathlib import Path

class HistoryService:
    """Servicio de backend para registrar y persistir el historial de descargas (RF-027 al RF-029)."""
    
    def __init__(self, history_file_path: Path):
        self.history_file_path = Path(history_file_path)
        self.history_file_path.parent.mkdir(parents=True, exist_ok=True)
        self._records = []
        self._load_records()

    def _load_records(self):
        """Carga los registros desde el archivo JSON de historial (RF-027)."""
        if self.history_file_path.exists():
            try:
                with open(self.history_file_path, "r", encoding="utf-8") as f:
                    self._records = json.load(f)
            except Exception:
                self._records = []
        else:
            self._records = []
            
        # Limpiar registros con más de 24 horas de antigüedad
        self._clean_old_records()

    def _clean_old_records(self):
        """Elimina automáticamente todos los registros con más de 24 horas de antigüedad."""
        now = datetime.datetime.now()
        cleaned = []
        changed = False
        for rec in self._records:
            try:
                rec_dt = datetime.datetime.strptime(f"{rec['date']} {rec['time']}", "%d/%m/%Y %H:%M:%S")
                # Si tiene menos de 24 horas (86400 segundos), mantenerlo
                if (now - rec_dt).total_seconds() <= 24 * 3600:
                    cleaned.append(rec)
                else:
                    changed = True
            except Exception:
                # Si tiene un formato corrupto o inválido, se descarta para mantener la integridad
                changed = True
                
        if changed:
            self._records = cleaned
            self._save_records()

    def _save_records(self):
        """Persiste los registros en el archivo JSON (RF-027)."""
        try:
            with open(self.history_file_path, "w", encoding="utf-8") as f:
                json.dump(self._records, f, ensure_ascii=False, indent=4)
        except Exception:
            pass

    def add_record(self, name: str, status: str) -> dict:
        """Agrega un nuevo registro al historial en primer lugar (más reciente) (RF-028, RF-029)."""
        now = datetime.datetime.now()
        date_str = now.strftime("%d/%m/%Y")
        time_str = now.strftime("%H:%M:%S")
        
        record = {
            "name": name,
            "date": date_str,
            "time": time_str,
            "status": status.upper()
        }
        
        # Insertar al inicio de la lista para ordenar del más reciente al más antiguo (RF-028)
        self._records.insert(0, record)
        self._save_records()
        return record

    def get_all_records(self) -> list:
        """Retorna la lista de registros ordenados (RF-028)."""
        self._load_records()
        return self._records
