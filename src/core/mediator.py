from typing import Callable, Dict
from src.core.config import ConfigLoader

class Mediator:
    def __init__(self, config_loader: ConfigLoader):
        self.config_loader = config_loader
        self._handlers: Dict[str, Callable] = {}

    def register_handler(self, event: str, handler: Callable):
        """Register a handler for a specific event."""
        self._handlers[event] = handler

    def notify(self, event: str, *args, **kwargs):
        """Notify the handler for the given event."""
        handler = self._handlers.get(event)
        if handler:
            handler(*args, **kwargs)
        else:
            raise ValueError(f"No handler registered for event: {event}")