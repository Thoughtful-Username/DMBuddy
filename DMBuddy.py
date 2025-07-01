# DMBuddy.py
from src.utils.json_cache import JSONCache
from src.utils.logger import setup_logger
from src.gui.main_window import MainWindow
import tkinter as tk
from typing import List, Optional


def main():
    jcache = JSONCache()
    config_file = "data/config/config.json"
    jcache.read(config_file)
    log = setup_logger(__name__, jcache)
    if not config_file in jcache.list_cached_files():
        log.error(f"Configuration file {config_file} not found in cache.")
    log.info("Starting DM Buddy application")

    data_path = "data/config/GUI/main_menu.json"

    root = tk.Tk() # Create the main application window
    app = MainWindow(root, jcache, data_path)
    root.mainloop()


if __name__ == "__main__":
    main()