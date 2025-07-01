import json
import os
from typing import Dict, Optional

class JSONCache:
    def __init__(self, initial_file: str = "data/config/config.json"):
        """Initialize the JSON cache with an optional initial file.

        Args:
            initial_file (str): Path to the initial JSON file to load (default: 'data/config/config.json').
        """
        self._cache: Dict[str, dict] = {}  # In-memory cache for JSON data
        # Ensure the initial file's directory exists
        self._ensure_directory(os.path.dirname(initial_file))
        # Load the initial file if it exists
        if os.path.isfile(initial_file):
            self.read(initial_file)

    def _ensure_directory(self, directory: str) -> None:
        """Create the directory if it doesn't exist."""
        if directory and not os.path.exists(directory):
            os.makedirs(directory)

    def read(self, file_path: str, force_reload: bool = False) -> Optional[dict]:
        """Retrieve data from a JSON file, loading it into the cache if not already present.

        Args:
            file_path (str): Path to the JSON file (e.g., 'data/config/config.json').
            force_reload (bool): If True, reload the file even if it's cached.

        Returns:
            dict: The JSON data, or None if the file doesn't exist or is invalid.
        """
        # Normalize file path to handle different separators
        file_path = os.path.normpath(file_path)
        
        if file_path in self._cache and not force_reload:
            return self._cache[file_path]

        try:
            with open(file_path, 'r') as f:
                data = json.load(f)
                self._cache[file_path] = data
                return data
        except (FileNotFoundError, json.JSONDecodeError) as e:
            print(f"Error loading {file_path}: {e}")
            return None

    def set(self, file_path: str, data: dict, save_to_disk: bool = True) -> None:
        """Store data in the cache and optionally save to disk.

        Args:
            file_path (str): Path to the JSON file (e.g., 'data/config/config.json').
            data (dict): Data to store.
            save_to_disk (bool): If True, save the data to the JSON file.
        """
        # Normalize file path
        file_path = os.path.normpath(file_path)
        self._cache[file_path] = data
        
        if save_to_disk:
            # Ensure the directory exists before saving
            self._ensure_directory(os.path.dirname(file_path))
            try:
                with open(file_path, 'w') as f:
                    json.dump(data, f, indent=4)
            except OSError as e:
                print(f"Error saving {file_path}: {e}")

    def clear(self, file_path: Optional[str] = None) -> None:
        """Clear the cache for a specific file or all files.

        Args:
            file_path (str, optional): Path to the JSON file to clear. If None, clear all.
        """
        if file_path:
            file_path = os.path.normpath(file_path)
            self._cache.pop(file_path, None)
        else:
            self._cache.clear()

    def list_cached_files(self) -> list:
        """List all file paths currently in the cache."""
        return list(self._cache.keys())