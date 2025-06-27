from abc import ABCMeta, abstractmethod
import json
from src.utils.logger import setup_logger
import os
from typing import Dict, List, Optional, Set
from content.item import Item
from effect import Effect
from src.core.session import dice_instance as dice

log = setup_logger("DMTools")

class Creature(metaclass=ABCMeta):
    """Base class for a D&D 5e creature, handling core attributes and mechanics."""

    _json_cache = {}

    def __new__(cls, species: str):
        data_file = "data/monsters/" + species.lower() + ".json"
        if not os.path.isfile(data_file):
            log.error(f"Species '{species.title()}' data file does not exist.  'FileNotFoundError' will be raised.")
            raise FileNotFoundError(f"Species '{species.title()}' data file does not exist.")
        instance = super().__new__(cls)
        return instance

    def __init__(self, species: str,
                 rules_file: str = "rules.json",
                 items_file: str = "items.json"):
    
        """
        Initialize a D&D 5e creature with species-specific data.
        
        Args:
            species (str):      Name of species of creature
            rules_file (str):   Path to file containing rules.  Defaults to 'rules.json'
            items_file (str):   Path to file containing item definitions.  Defaults to 'items.json'
            species_file(str):  Path to file containing species definitions.  Defaults to 'species.json'
        
        """

        self.species: str = species.title()
        log.Info(f"Start initializing Creature '{self.species}'.")
        self.warnings = 0
        species_file = "/data/monsters/" + species + ".json"
        species_data = self._load_json(species_file)
        rules = self._load_json("/data/rules.json")

        self.parent_species: str = species_data.get("parent_species", "")
        if not self.parent_species:
            log.warning(f"No parent species specified for species '{self.species}'.  Defaulting to 'None'.")
            self.warnings += 1
            self.parent_species = "None"
        self.content_creator: str = species_data.get("content_creator", "")
        if not self.content_creator:
            log.warning(f"No content creator specified for species '{self.species}")
            self.warnings += 1

        self.file_link: str = species_data.get("file_link", "")
        self.web_link: str = species_data.get("web_link", "")

        self.given_name: str = species_data.get("given_name", self.species)
        
        log.info("Validating creature size data.")
        valid_sizes = rules.get("sizes", ["Tiny", "Small", "Medium", "Large", "Huge", "Gargantuan"])
        size_data = species_data.get("size", "missing")
        if size_data == "missing":
            log.warning(f"Size data missing for species '{self.species}'.  Defaulting to medium.")
            self.warnings += 1
            size_data = "Medium"
        self.size: str = size_data if size_data in valid_sizes else "Medium"
        if self.size != size_data:
            log.warning(f"Invalid size '{size_data}' for {self.species}, defaulting to 'Medium'.")
            self.warnings += 1
        log.info("Creature size validation complete.")


        log.info("Validating creature type data.")
        valid_types = rules.get("creature_types", ["aberration", "beast", "celestial", "construct",
                                                  "dragon", "elemental", "fey", "fiend", "giant",
                                                  "humanoid", "monstrosity", "ooze", "plant", "undead"])
        type_data = species_data.get("creature_type", "missing")
        if type_data == "missing":
            log.warning(f"Type data missing for species '{self.species}'.  Defaulting to 'default'.")
            self.warnings += 1
            type_data = "default"
        self.creature_type: str = type_data if type_data in valid_types else "default"
        if self.creature_type != type_data:
            log.warning(f"Invalid creature type '{type_data}' for '{self.species}'.  Defaulting to 'default'.")
            self.warnings += 1
        log.info("Creature type validation complete.")


        log.info("Validating creature alignment data.")
        valid_alignments = rules.get("alignments", ["Lawful Good", "Lawful Neutral", "Lawful Evil",
                                                   "Neutral Good", "Neutral", "Neutral Evil",
                                                   "Chaotic Good", "Chaotic Neutral", "Chaotic Evil"])
        alignment_data = species_data.get("alignment", "missing")
        if alignment_data == "missing":
            log.warning(f"Alignment data missing for species '{self.species}'.  Defaulting to 'Neutral'.")
            self.warnings += 1
            type_data = "Neutral"
        self.alignment: str = alignment_data if alignment_data in valid_alignments else "Neutral"
        if self.alignment != alignment_data:
            log.warning(f"Invalid alignment '{alignment_data}' for {self.species}, defaulting to 'Neutral'.")
            self.warnings += 1
        log.info("Creature alignment validation complete.")


        log.info("Validating creature base armor class data.")
        ac_data = species_data.get("base_ac", -1)
        if ac_data == -1:
            log.warning(f"Base armor class data missing for species '{self.species}'.  Defaulting to 10.")
            self.warnings += 1
            ac_data = 10
        self.base_ac: int = ac_data if isinstance(ac_data, int) and ac_data >= 10 else 10
        if self.base_ac != ac_data:
            log.warning(f"Invalid base armor class '{ac_data}' for {self.species}, defaulting to 10.")
            self.warnings += 1
        log.info("Creature base armor class validation complete.")


        log.info("Validating creature hit dice and hit points.")
        hd_data = species_data.get("hit_dice", "")
        if not hd_data:
            log.warning(f"Hit dice data missing for species '{self.species}'.  Defaulting to 100d20.")
            self.warnings += 1
            hd_data = "100d20"
        
        hp_data = dice.roll(self.hit_dice)
        self.max_hp: int = hp_data[-1] if hp_data else 1
        if not hp_data:
            log.warning(f"Invalid hit dice for {species}, defaulting to 1.")
        self.current_hp: int = self.max_hp
        self.temp_hp: int = 0




    def _load_json(self, file_path: str) -> Dict:
        """Load JSON file into cache."""
        if file_path not in self._json_cache:
            try:
                with open(file_path, 'r') as f:
                    self._json_cache[file_path] = json.load(f)
            except FileNotFoundError:
                self._json_cache[file_path] = {}
                log.warning(f"JSON file '{file_path}' not found, returning empty dict.")
        return self._json_cache[file_path]

    @abstractmethod
    def _define_actions(self) -> Dict[str, any]:
        """Define creature's actions from species.json or default."""
        # Not the definition of how the action works, rather what actions are available to the creature.
        # Monster actions come from species.json
        # Character / NPC actions are complex
            # Dynamic for characters based on equipped items, feats, class features, etc.
        # Reactions don't become 'available' without a trigger.
        # Pass list of actions to mediator class
        pass

    @abstractmethod
    def apply_effect(self, effect_id: str) -> Dict[str, any]:
        pass

    @abstractmethod
    def remove_effect(self, effect_id: str) -> Dict[str, any]:
        pass

    def __eq__(self, other):
        if not isinstance(other, Creature):
            return NotImplemented
        return self.species == other.species and self.content_creator == other.content_creator

    def __repr__(self):
        return f"Creature: {self.species} by {self.content_creator}."

    def __str__(self):
        return f"Creature: {self.species} by {self.content_creator}."

