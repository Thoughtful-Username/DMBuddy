# DMBuddy.py
from src.utils.json_cache import JSONCache
from src.utils.logger import setup_logger

import tkinter as tk
from typing import List, Optional
from pathlib import Path


jcache = JSONCache()
jcache.get("data/config/config.json")
logger = setup_logger("DMBuddy", jcache)


# Function to load button labels from JSON file
def load_buttons_from_json(file_path):
    buttons = jcache.get(file_path)
    return buttons.get('buttons', []) if buttons else []


# Function to handle button clicks (placeholder for now)
def button_click(button_name):
    print(f"{button_name} clicked!")

# Create the main Tkinter application
class App:
    def __init__(self, root, json_file):
        self.root = root
        self.root.title("My Tkinter App")  # Set window title
        self.root.geometry("400x300")  # Set window size (optional)

        # Load button labels from JSON
        button_labels = load_buttons_from_json(json_file)

        # Create and pack buttons from JSON
        for label in button_labels:
            btn = tk.Button(self.root, text=label, command=lambda x=label: button_click(x))
            btn.pack(pady=5)  # Add some vertical padding

        # Create Exit button in the bottom right
        exit_btn = tk.Button(self.root, text="Exit", command=self.root.quit)
        exit_btn.pack(side=tk.BOTTOM, anchor=tk.SE, padx=10, pady=10)  # Align to bottom-right

# Main execution
if __name__ == "__main__":
    # Path to your JSON file
    json_file_path = Path("data/config/main_menu.json")
    
    # Initialize Tkinter
    root = tk.Tk()
    app = App(root, json_file_path)
    root.mainloop()