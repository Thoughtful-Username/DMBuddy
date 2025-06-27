# src/core/observer.py
from typing import List, Optional
from src.utils.logger import setup_logger

log = setup_logger("DMBuddy.observer")

class Observer:
    
    def update(self, event: str, data: Optional[dict] = None) -> None:
        pass