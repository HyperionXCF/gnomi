import json
import os
from pathlib import Path


class Config:
    def __init__(self):
        self.config_file = Path.home() / ".ai_assistant_config.json"
        self.default_config = {
            "api_key": "",
            "selected_model": "llama-3.1-8b-instant",
            "window_position": [100, 100],
            "theme": "dark",
            "auto_start": False,
            "hotkey": "alt+a",
        }
        self.config = self.load_config()

    def load_config(self):
        if self.config_file.exists():
            try:
                with open(self.config_file, "r") as f:
                    config = json.load(f)
                    return {**self.default_config, **config}
            except (json.JSONDecodeError, IOError):
                return self.default_config.copy()
        return self.default_config.copy()

    def save_config(self):
        try:
            with open(self.config_file, "w") as f:
                json.dump(self.config, f, indent=2)
            return True
        except IOError:
            return False

    def get(self, key, default=None):
        return self.config.get(key, default)

    def set(self, key, value):
        self.config[key] = value
        self.save_config()

    def is_api_key_set(self):
        return bool(self.config.get("api_key", "").strip())
