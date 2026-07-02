from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
STORAGE_DIR = BASE_DIR / "storage"
DATABASE_PATH = STORAGE_DIR / "filesync.db"

DATABASE_URL = f"sqlite:///{DATABASE_PATH}"