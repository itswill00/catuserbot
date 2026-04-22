import os
import ujson
import threading
from pathlib import Path

class JsonDB:
    _instances = {}
    _master_lock = threading.Lock()

    def __new__(cls, filename: str):
        with cls._master_lock:
            if filename not in cls._instances:
                cls._instances[filename] = super(JsonDB, cls).__new__(cls)
            return cls._instances[filename]

    def __init__(self, filename: str):
        if hasattr(self, 'initialized'):
            return
        self.path = Path(f"userbot/cache/{filename}.json")
        self.lock = threading.Lock()
        self._cache = self._load()
        self.initialized = True

    def _load(self):
        with self.lock:
            if not self.path.exists():
                self.path.parent.mkdir(parents=True, exist_ok=True)
                self._save_to_disk({})
                return {}
            try:
                with open(self.path, "r") as f:
                    return ujson.load(f)
            except (ValueError, ujson.JSONDecodeError):
                return {}

    def _save_to_disk(self, data):
        # Atomic write: write to .tmp then rename
        temp_path = self.path.with_suffix(".tmp")
        with open(temp_path, "w") as f:
            ujson.dump(data, f, indent=4)
        os.replace(temp_path, self.path)

    def _save(self):
        with self.lock:
            self._save_to_disk(self._cache)

    def get(self, key, default=None):
        return self._cache.get(str(key), default)

    def set(self, key, value):
        self._cache[str(key)] = value
        self._save()

    def delete(self, key):
        if str(key) in self._cache:
            del self._cache[str(key)]
            self._save()

    def get_all(self):
        return self._cache

    def clear(self):
        self._cache = {}
        self._save()

# Pre-defined databases
global_db = JsonDB("cat_globals")
blacklist_db = JsonDB("cat_blacklists")
pmpermit_db = JsonDB("cat_pmpermit")
gban_db = JsonDB("cat_gban")
sudo_db = JsonDB("cat_sudo")
filters_db = JsonDB("cat_filters")
notes_db = JsonDB("cat_notes")
welcome_db = JsonDB("cat_welcome")
warns_db = JsonDB("cat_warns")
locks_db = JsonDB("cat_locks")
