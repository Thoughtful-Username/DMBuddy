import tkinter as tk
from src.core.mediator import Mediator

class WidgetFactory:
    def __init__(self, mediator: Mediator):
        self.mediator = mediator

    def create_widgets(self, parent: tk.Tk, menu_config: dict):
        """Create widgets based on menu configuration."""
        for widget_data in menu_config.get("widgets", []):
            widget_type = widget_data.get("type")
            label = widget_data.get("label", "")
            if widget_type == "button":
                button = tk.Button(parent, text=label)
                button.bind("<Button-1>", lambda event: self.mediator.notify("button_click", label))
                button.pack()
            # Add support for other widget types