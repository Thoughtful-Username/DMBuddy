from src.core.mediator import Mediator
from src.core.config import ConfigLoader
from src.gui.app_gui import AppGUI
from src.gui.theme import ThemeManager
from src.gui.widgets import WidgetFactory

class Injector:
    def __init__(self):
        self._instances = {}

    def get(self, cls):
        if cls not in self._instances:
            if cls == ConfigLoader:
                self._instances[cls] = ConfigLoader(
                    "config/themes.json",
                    "config/app_theme.json",
                    "config/menu_config.json"
                )
            elif cls == Mediator:
                self._instances[cls] = Mediator(self.get(ConfigLoader))
            elif cls == ThemeManager:
                self._instances[cls] = ThemeManager(self.get(ConfigLoader))
            elif cls == WidgetFactory:
                self._instances[cls] = WidgetFactory(self.get(Mediator))
            elif cls == AppGUI:
                self._instances[cls] = AppGUI(
                    self.get(Mediator),
                    self.get(ThemeManager),
                    self.get(WidgetFactory)
                )
        return self._instances[cls]