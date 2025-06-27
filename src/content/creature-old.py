from abc import ABCMeta, abstractmethod
import json
import logging
from typing import Dict, List, Optional, Set
from content.item import Item
from src.utils.dice import roll

class Creature(metaclass=ABCMeta):
    """Base class for a D&D 5e creature, handling core attributes and mechanics."""

    _json_cache = {}

    def __init__(self,
                 species: str,
                 rules_file: str = "rules.json",
                 items_file: str = "items.json",
                 species_file: str = "species.json"):
        """
        Initialize a D&D 5e creature with species-specific data.
        
        Args:
        species (str):      Name of species of creature
        rules_file (str):   Path to file containing rules.  Defaults to 'rules.json'
        items_file (str):   Path to file containing item definitions.  Defaults to 'items.json'
        species_file(str):  Path to file containing species definitions.  Defaults to 'species.json'
        
        """
        rules = self._load_json(rules_file)
        items_data = self._load_json(items_file)
        species_data = self._load_json(species_file).get(species, {})


        self.species: str = species
        self.parent_species: str = species_data.get("parent_species", "")
        self.content_creator: str = species_data.get("content_creator", "")
        self.file_link: Optional[str] = species_data.get("file_link", "")
        self.web_link: Optional[str] = species_data.get("web_link", "")

        self.given_name: str = species_data.get("given_name", species)

        valid_sizes = rules.get("sizes", ["Tiny", "Small", "Medium", "Large", "Huge", "Gargantuan"])
        size_data = species_data.get("size", "Medium")
        self.size: str = size_data if size_data in valid_sizes else "Medium"
        if self.size != size_data:
            logging.warning(f"Invalid size '{size_data}' for {species}, defaulting to 'Medium'.")

        valid_types = rules.get("creature_types", ["aberration", "beast", "celestial", "construct",
                                                  "dragon", "elemental", "fey", "fiend", "giant",
                                                  "humanoid", "monstrosity", "ooze", "plant", "undead"])
        type_data = species_data.get("creature_type", "Unknown Type")
        self.creature_type: str = type_data if type_data in valid_types else "Unknown Type"
        if self.creature_type != type_data:
            logging.warning(f"Invalid creature type '{type_data}' for {species}, defaulting to 'Unknown Type'.")

        valid_alignments = rules.get("alignments", ["Lawful Good", "Lawful Neutral", "Lawful Evil",
                                                   "Neutral Good", "Neutral", "Neutral Evil",
                                                   "Chaotic Good", "Chaotic Neutral", "Chaotic Evil"])
        alignment_data = species_data.get("alignment", "Unknown Alignment")
        self.alignment: str = alignment_data if alignment_data in valid_alignments else "Unknown Alignment"
        if self.alignment != alignment_data:
            logging.warning(f"Invalid alignment '{alignment_data}' for {species}, defaulting to 'Unknown Alignment'.")

        ac_data = species_data.get("base_ac", -1)
        self.base_ac: int = ac_data if isinstance(ac_data, int) and ac_data >= 10 else 10
        if self.base_ac != ac_data:
            logging.warning(f"Invalid base armor class for {species}, defaulting to 10.")

        self.hit_dice: str = species_data.get("hit_dice", "")
        hp_data = roll(self.hit_dice)
        self.max_hp: int = hp_data[-1] if hp_data else 1
        if not hp_data:
            logging.warning(f"Invalid hit dice for {species}, defaulting to 1.")
        self.current_hp: int = self.max_hp
        self.temp_hp: int = 0

        valid_movement_types = rules.get("movement_types", ["burrow", "climb", "fly", "swim", "walk"])
        movement_data = species_data.get("speed", {})
        self.speed: Dict[str, int] = {mode: movement_data.get(mode, 0) if
                                      isinstance(movement_data.get(mode, 0), int) else 0
                                      for mode in set(valid_movement_types) | set(movement_data.keys())}
        for mode in movement_data:
            if mode not in valid_movement_types:
                logging.warning(f"New movement type '{mode}' for {species}: added with value {self.speed[mode]}.")
            elif not isinstance(movement_data.get(mode, 0), int):
                logging.warning(f"Non-integer value for movement type '{mode}' for {species}, set to 0.")

        valid_abilities = rules.get("abilities", ["strength", "dexterity", "constitution",
                                                 "intelligence", "wisdom", "charisma"])
        stats_data = species_data.get("stats", {})
        self.stats: Dict[str, int] = {ability: stats_data.get(ability, 10) if
                                      isinstance(stats_data.get(ability, 0), int) else 10
                                      for ability in valid_abilities}
        for ability in stats_data:
            if ability not in valid_abilities:
                logging.warning(f"Invalid ability '{ability}' for {species}, ignored.")

        saves_data = species_data.get("saves", {})
        self.saves: Dict[str, int] = {ability: saves_data.get(ability, 0) if
                                      isinstance(saves_data.get(ability, 0), int) else 0
                                      for ability in valid_abilities}
        for ability in saves_data:
            if ability not in valid_abilities:
                logging.warning(f"Invalid save bonus '{ability}' for {species}, ignored.")

        valid_skills = rules.get("skills", ["acrobatics", "animal handling", "arcana", "athletics",
                                           "deception", "history", "insight", "intimidation",
                                           "investigation", "medicine", "nature", "perception",
                                           "performance", "persuasion", "religion", "sleight of hand",
                                           "stealth", "survival"])
        skills_data = species_data.get("skills", {})
        self.saves: Dict[str, int] = {skill: skills_data.get(skill, 0) if
                                      isinstance(skills_data.get(skill, 0), int) else 0
                                      for skill in valid_skills}
        for skill in skills_data:
            if skill not in valid_skills:
                logging.warning(f"Invalid skill '{skill}' for {species}, ignored.")

        valid_senses = rules.get("senses", ["blindsight", "darkvision", "passive perception",
                                           "tremorsense", "truesight"])
        senses_data = species_data.get("senses", {})
        self.senses: Dict[str, int] = {sense: senses_data.get(sense, 0) if
                                       isinstance(senses_data.get(sense, 0), int) else 0
                                       for sense in valid_senses}
        for sense in senses_data:
            if sense not in valid_senses:
                logging.warning(f"Invalid sense '{sense}' for {species}, ignored.")

        self.languages: List[str] = species_data.get("languages", [])
        self.language_note: str = species_data.get("language_note", "")

        valid_damage_types = rules.get("damage_types", ["acid", "bludgeoning", "cold", "fire", "force",
                                                       "lightning", "necrotic", "piercing", "poison",
                                                       "psychic", "radiant", "slashing", "thunder"])
        vul_data = species_data.get("damage_vulnerabilities", [])
        self.damage_vulnerabilities: Set[str] = {dtype for dtype in vul_data if dtype in valid_damage_types}
        for dtype in vul_data:
            if dtype not in valid_damage_types:
                logging.warning(f"Invalid damage vulnerability type '{dtype}' for {species}, ignored.")
        res_data = species_data.get("damage_resistances", [])
        self.damage_resistances: Set[str] = {dtype for dtype in res_data if dtype in valid_damage_types}
        for dtype in res_data:
            if dtype not in valid_damage_types:
                logging.warning(f"Invalid damage resistance type '{dtype}' for {species}, ignored.")
        imm_data = species_data.get("damage_immunities", [])
        self.damage_immunities: Set[str] = {dtype for dtype in imm_data if dtype in valid_damage_types}
        for dtype in imm_data:
            if dtype not in valid_damage_types:
                logging.warning(f"Invalid damage immunity type '{dtype}' for {species}, ignored.")

        valid_conditions = rules.get("conditions", ["blinded", "charmed", "deafened", "frightened",
                                                   "grappled", "incapacitated", "invisible", "paralyzed",
                                                   "petrified", "poisoned", "prone", "restrained",
                                                   "stunned", "unconscious"])
        cond_imm_data = species_data.get("condition_immunities", [])
        self.condition_immunities: Set[str] = {cond for cond in cond_imm_data if cond in valid_conditions}
        for cond in cond_imm_data:
            if cond not in valid_conditions:
                logging.warning(f"Invalid condition immunity '{cond}' for {species}, ignored.")

        # Dynamic state
        # TODO Implement creature level management methods for inventory, spells, actions and effects.  Actions in this sense are anything that a monster, npc, or character does.  From attacking with a weapon to drinking a potion or casting a spell.  For monsters that comes from the monster species definition.  For characters that comes from the items they have equippeed.  Effects in this sense are the outcomes of successful attack, spells or interactions.

        self.inventory_slots: Dict[str, int] = rules.get("inventory_slots")

        valid_items = items_data.items()
        inventory_data = species_data.get("inventory", [])
        self.inventory: List[Item] = []
        for item in items_data:
            if item in valid_items:
                self.inventory.append(Item(item))
            else:
                logging.warning(f"Invalid item '{item}' found in inventory.  Ignored")
        
        self.containers: List[str] = []
        for item in self.inventory:
            # If item is container, and item can be equipped, then add to self.containers
            
            pass

        for item in self.inventory:
            if item.item_ID not in self.containers:
                if item.container:
                    # Attempt Move to container
                    # If not then attempt inventory_slot
                    pass
                else:
                    # Move to inventory_slot
                    pass


        # TODO: Attempt to transfer items in inventory to noted containers

        # TODO: Attempt to equip inventory marked as such

        # TODO: Attempt to attune inventory marked as such



        self.containers: List[str] = []
        self.equipped: List[str] = []
        self.attuned: List[str] = []
        self.equipped_slots: Dict[str, List[str]] = {}
        self.spells_library: Dict[str, int] = {}
        self.spells_prepared: Dict[str, int] = {}
        self.spells_slots: Dict[int, int] = {}
        self.actions: Dict[str, Dict] = {}
        self.effects: Dict[str, Dict] = {}


    def _load_json(self, file_path: str) -> Dict:
        """Load JSON file into cache."""
        if file_path not in self._json_cache:
            try:
                with open(file_path, 'r') as f:
                    self._json_cache[file_path] = json.load(f)
            except FileNotFoundError:
                self._json_cache[file_path] = {}
                logging.warning(f"JSON file '{file_path}' not found, returning empty dict.")
        return self._json_cache[file_path]


    @abstractmethod
    def _define_actions(self) -> List[str]:
        """Define creature's actions from species.json or default."""
        # Not the definition of how the action works, rather what actions are available to the creature.
        # Monster actions come from species.json
        # Character / NPC actions are complex
            # Dynamic for characters based on equipped items, feats, class features, etc.
        # Reactions don't become 'available' without a trigger.
        # Pass list of actions to mediator class
        pass

    @abstractmethod
    def take_damage(self, damage_type: str, value: int) -> str:
        # Character specific considerations are not to be part of monster
        # Pass result narrative to mediator class
        pass

    def _can_take_item(self, item_id: str) -> bool:
        """Check if creature can carry the item."""
        # Creature has available inventory slot (i.e. hand or container, etc.)
        # Pass boolean indicating whether possible
        pass

    def _encumbrance(self) -> float:
        """Calculate total weight carried."""
        # Houserule defaults to false (don't use).
        # Implement system but pass 0 if not being used.
        pass

    def take_item(self, item: Item) -> str:
        """Add an item to inventory."""
        # Assign UUID to item to avoid conflicts from multiple copies of the same item
        # Add item to inventory and assign inventory slot / container
        # Check for effect updates
        # Pass result narrative to mediator class
        pass

    def drop_item(self, item_id: str) -> str:
        """Drop an item from inventory."""
        # Remove from inventory.
        # Check for effect updates
        pass

    def set_item_given_name(self, item_id: str, given_name: str) -> str:
        """Rename an item in inventory."""
        # My sword is Excalibur!
        # Pass result narrative to mediator class
        pass

    def add_container(self, container_id: str) -> str:
        """Register a container item."""
        # Register new item as container for other items
        # Pass result narrative to mediator class
        pass

    def remove_container(self, container_id: str) -> str:
        """Remove a container and its contents."""
        # Remove item from container register
        # Pass result narrative to mediator class
        pass

    def _can_put_in_container (self, item_ID: str, container_ID: str) -> bool:
        """Check for room in container"""
        # Uses weight capacity from container definition

    def transfer_item_to_container(self, item_id: str, container_id: str) -> str:
        """Move an item to a container."""
        # Update item for relevant container
        # update container available capacity
        # Pass result narrative to mediator class
        pass

    def remove_item_from_container(self, item_id: str, container_id: str) -> str:
        """Remove an item from a container."""
        # Update item for removal from container
        # Update item for inventory slot (e.g. hand)
        # Update container available capacity
        # Pass result narrative to mediator class
        pass

    def _can_equip_item(self, item_id: str) -> bool:
        """Check if an item can be equipped."""
        # Item is 'equippable'
        # Room to equip (e.g. cannot wear two sets of armor)
        # Requirements met
        pass

    def equip_item(self, item_id: str) -> str:
        """Equip an item."""
        # Mark item as equipped
        # Update effects
        # Update actions
        # Pass result narrative to mediator class
        pass

    def unequip_item(self, item_id: str) -> str:
        """Unequip an item."""
        # Mark item as unequipped
        # Update effects
        # Update actions
        # Pass result narrative to mediator class
        pass

    def _can_attune_item(self, item_id: str) -> bool:
        """Check if an item can be attuned."""
        # Does item require attunement
        # Requirements met?
        # No more than 3 attuned items
        pass

    def attune_item(self, item_id: str) -> str:
        """Attune to an item."""
        # Mark item as attuned
        # Update effects
        # Update actions
        # Pass result narrative to mediator class
        pass

    def unattune_item(self, item_id: str) -> str:
        """Unattune from an item."""
        # Mark item as unattuned
        # Update effects
        # Update actions
        # Pass result narrative to mediator class
        pass

    def heal(self, value: int) -> str:
        """Heal the creature."""
        # Restore hit points up to maximum
        # Remove certain condition(s)
        # Pass result narrative to mediator class
        pass

    def apply_effect(self, effect: str) -> str:
        """Apply an effect to the creature."""
        # Add effect to effect list
        # Pass result narrative to mediator class
        pass

    def resolve_effects(self) -> None:
        """Resolve active effects."""
        # Immediate, permanent or specific duration
        # Keep effects in list until ended or dispelled
        pass

    def prepare_spells(self, spells: List[str]) -> None:
        """Prepare spells for casting."""
        # TODO: Implement spell preparation
        pass

    def _available_spell_slots(self) -> Dict[int, int]:
        """Return available spell slots."""
        return self.spells_slots

    def cast_spell(self, spell: str, level: Optional[int] = 0) -> None:
        """Cast a spell."""
        # TODO: Implement spell casting
        pass

    def read_scroll(self, scroll: str) -> None:
        """Read a spell scroll."""
        # TODO: Implement scroll reading
        pass

    def calculate_skill_bonus(self) -> Dict[str, int]:
        """Calculate skill bonuses."""
        # TODO: Implement skill bonus calculation
        return self.skills

    def roll_initiative(self, mechanic: str = "default") -> int:
        """Roll initiative."""
        # TODO: implement initiative roll
        pass

    def roll_sense_check(self, sense: str) -> int:
        """Roll a sense check."""
        # TODO: implement sense check
        pass

    def take_action(self, action_name: str, target: List['Creature']):
        # Resolve hit roll
        # Resolve save rolls
        # Calculate damage
        # Send damage
        # Send effects
        # Update actions
        pass

    def end_turn(self) -> None:
        """End the creature's turn."""
        # Update effects
        # Pass turn control
        pass

    def begin_turn(self) -> None:
        """Begin the creature's turn."""
        # Accept turn control
        # Update effects
        pass

    def __str__(self) -> str:
        """String representation."""
        return f"{self.given_name} (HP: {self.current_hp}/{self.max_hp}, AC: {self.base_ac})"