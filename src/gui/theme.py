from src.core.config import ConfigLoader

class ThemeManager:
    def __init__(self, config_loader: ConfigLoader):
        self.config_loader = config_loader
        self.theme = self.config_loader.load_theme()
        self.app_theme = self.config_loader.load_app_theme()

    def apply_theme(self, widget):
        """Apply theme to a Tkinter widget."""
        widget.configure(**self.app_theme.get("window", {}))
        # Add logic to apply widget-specific styles