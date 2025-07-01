# src/core/controller.py
from src.utils.json_cache import JSONCache
from src.utils.logger import setup_logger

class DMController:
    def __init__(self, jcache: JSONCache):
        self.jcache = jcache
        self.log = setup_logger(__name__, jcache)
        self.log.info("DMController initialized")

    def handle_button_click(self, button_name: str):
        self.log.debug(f"Processing click for button: {button_name}")
        # Add game logic here, e.g., load character data, roll dice, etc.
        return f"Action for {button_name} executed"