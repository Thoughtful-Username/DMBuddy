# src/gui/main_window.py
from src.utils.logger import setup_logger
from src.utils.json_cache import JSONCache
import tkinter as tk
from pathlib import Path
from typing import Callable, Optional

class MainWindow:
    def __init__(self, root: tk.Tk, jcache: JSONCache, data_path: str):
        """
        Initialize the main window with configuration loaded from a JSON file.
        
        Args:
            root (tk.Tk): The main application window.
            data_path (str): Path to the JSON file containing button configurations.
            jcache (JSONCache): Instance of JSONCache for reading configuration data.
        """

        self.log = setup_logger(__name__, jcache)
        self.root = root
        self.jcache = jcache
        self.jcache.read(data_path)
        if self.jcache.read(data_path):
            self.log.info(f"Loaded JSON data from {data_path}")
        else:
            self.log.error(f"Failed to load JSON data from {data_path}")
        self.root.title("DM Buddy")
        self.root.geometry("400x300")

        self.load_buttons(data_path)
        self.create_exit_button()

    def load_buttons(self, data_path):
        button_data = self.jcache.read(data_path)
        if button_data:
            buttons = button_data.get('buttons', {})
        else:
            self.log.error(f"Failed to load button data from {data_path}")
            buttons = {}
        
        for label in buttons:
            btn = tk.Button(self.root, text=label, command=lambda x=label: self.on_button_click(x))
            btn.pack(pady=5)

    def create_exit_button(self):
        exit_btn = tk.Button(self.root, text="Exit", command=self.root.quit)
        exit_btn.pack(side=tk.BOTTOM, anchor=tk.SE, padx=10, pady=10)

    def on_button_click(self, button_name: str):
        # Placeholder for controller callback
        print(f"{button_name} clicked!")