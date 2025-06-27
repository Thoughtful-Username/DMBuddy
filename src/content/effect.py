#src/content/effect.py
import json
from typing import List, Optional
from pathlib import Path
from src.utils.logger import setup_logger
from src.core.observer import Observer

log = setup_logger("DMBuddy.effect")

class Effect(Observer):
    """
    Effect resulting from an action in D&D 5e.
    """

    _rules_cache = None  # Class-level cache for effect_rules.json

    @classmethod
    def _load_rules(cls):
        """Load and cache effect_rules.json."""
        if cls._rules_cache is None:
            log.debug("Caching effect rules")
            rules_path = Path("data/config/effect_rules.json")
            try:
                with open(rules_path, 'r') as f:
                    cls._rules_cache = json.load(f)
            except FileNotFoundError:
                log.warning("Effects rules file not found.")
                raise FileNotFoundError("effect_rules.json not found in data/config/")
            except json.JSONDecodeError:
                log.warning("Effects rules not properly formatted.")
                raise ValueError("Invalid JSON in effect_rules.json")
        return cls._rules_cache


    def __init__(self, target: str, details: dict) -> None:
        log.debug("Defining new effect.")
        rules = Effect._load_rules
        self.effect_type: str = details.get("effect_type", "")

        # Effect duration.  More like 'duration_type'.  If not provided or not in the full list in the rules file, it is defaulted to 'instant'
        valid_duration: List[str] = rules.get("duration")
        self.duration: str = details.get("duration", "missing")
        if self.duration == "missing":
            log.warning(f"New effect for '{self.effect_type} is missing a duration.  Defaulting to instant.")
            self.duration = "instant"
        if not self.duration in valid_duration:
            log.warning(f"New effect for '{self.effect_type} has invalid duration '{self.duration}.  Defaulting to instant.")
            self.duration = "instant"
        
        # Attributes (all required) associated with a turn-based duration.
        if self.duration == "turn_based":
            log.debug("Turn-based effect.")

            # Number of turns effect lasts
            self.duration_value: int = details.get("duration_value", -1)
            if self.duration_value == -1:
                log.warning(f"New effect for '{self.effect_type} duration is turn-based, but is missing the number of turns.  Defaulting to 1.")
                self.duration_value = 1
            if self.duration_value < 0:
                log.warning(f"New effect for '{self.effect_type} duration is turn-based, but the number of turns specified is less than 0.  Defaulting to 1.")
                self.duration_value = 1

            # How/when the count of turns remaining is triggered.
            valid_trigger = rules.get("trigger", ["beginning_of_turn", "end_of_turn"])
            self.duration_trigger: str = details.get("duration_trigger", "missing")
            if self.duration_trigger == "missing":
                log.warning(f"New effect for '{self.effect_type} is duration-based but is missing a duration trigger.  Defaulting to 'end_of_turn'.")
                self.duration_trigger = "end_of_turn"
            if self.duration_trigger not in valid_trigger:
                log.warning(f"Invalid duration trigger '{self.duration_trigger}' for new turn-based effect '{self.effect_type}'.  Defaulting to 'end_of_turn'.")
                self.duration_trigger = "end_of_turn"
            
            # What entity triggers the count of remaining turns to increment.
            self.duration_trigger_source: str = details.get("duration_trigger_source", "missing")
            if self.duration_trigger_source == "missing":
                log.warning(f"New effect for '{self.effect_type} is duration-based but is missing a duration trigger source.  Defaulting to the target of the effect.")
                self.duration_trigger_source = "effect_target"
