import tkinter as tk
from src.core.mediator import Mediator
from src.gui.theme import ThemeManager
from src.gui.widgets import WidgetFactory

class AppGUI:
    def __init__(self, mediator: Mediator, theme_manager: ThemeManager, widget_factory: WidgetFactory):
        self.mediator = mediator
        self.theme_manager = theme_manager
        self.widget_factory = widget_factory
        self.root = tk.Tk()
        self._setup_window()

    def _setup_window(self):
        """Configure the main window with theme and widgets."""
        self.theme_manager.apply_theme(self.root)
        menu_config = self.mediator.notify("get_menu_config")
        self.widget_factory.create_widgets(self.root, menu_config)

    def run(self):
        """Start the Tkinter main loop."""
        self.root.mainloop()