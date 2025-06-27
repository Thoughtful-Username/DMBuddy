import json
from jsonschema import validate, ValidationError
from src.models.schemas import THEME_SCHEMA, APP_THEME_SCHEMA, MENU_SCHEMA

class ConfigLoader:
    def __init__(self, theme_file: str, app_theme_file: str, menu_file: str):
        self.theme_file = theme_file
        self.app_theme_file = app_theme_file
        self.menu_file = menu_file

    def load_theme(self) -> dict:
        """Load and validate theme configuration."""
        return self._load_and_validate(self.theme_file, THEME_SCHEMA)

    def load_app_theme(self) -> dict:
        """Load and validate app theme configuration."""
        return self._load_and_validate(self.app_theme_file, APP_THEME_SCHEMA)

    def load_menu_config(self) -> dict:
        """Load and validate menu configuration."""
        return self._load_and_validate(self.menu_file, MENU_SCHEMA)

    def _load_and_validate(self, file_path: str, schema: dict) -> dict:
        try:
            with open(file_path, 'r') as f:
                data = json.load(f)
            validate(instance=data, schema=schema)
            return data
        except (FileNotFoundError, ValidationError, json.JSONDecodeError) as e:
            raise ValueError(f"Configuration error in {file_path}: {e}")