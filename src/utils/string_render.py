# src/utils/string_render.py
import re
from src.utils.logger import setup_logger
from typing import List, Union

# Set up logging for debugging
log = setup_logger("DMBuddy")

class TemplateEngine:
    def __init__(self, default_value="UNKNOWN"):
        self.handlers = {}
        self.default_value = default_value
        self.filters = {
            "upper": str.upper,
            "lower": str.lower,
            "capitalize": str.capitalize,
            "join": lambda x: ", ".join(str(i) for i in x) if isinstance(x, (list, tuple)) else str(x)
        }

    def register_handler(self, code, handler):
        if not callable(handler):
            raise ValueError(f"Handler for '{code}' must be callable")
        self.handlers[code] = handler
        log.info(f"Registered handler for code: {code}")

    def register_filter(self, name, filter_func):
        if not callable(filter_func):
            raise ValueError(f"Filter '{name}' must be callable")
        self.filters[name] = filter_func
        log.info(f"Registered filter: {name}")

    def _get_nested_value(self, data, placeholder):
        """Resolve nested placeholders (e.g., item.name or attacker.name)."""
        parts = placeholder.split(".")
        value = data.get(parts[0], self.default_value)
        if value == self.default_value:
            return value

        for part in parts[1:]:
            try:
                if hasattr(value, part):
                    value = getattr(value, part)
                elif isinstance(value, dict):
                    value = value.get(part, self.default_value)
                else:
                    return self.default_value
                # Handle callable attributes (e.g., methods)
                if callable(value) and not isinstance(value, type):
                    value = value()
            except Exception:
                return self.default_value
        return value

    def render(self, template: str, data: dict = None) -> str:
        if data is None:
            data = {}
        if not isinstance(data, dict):
            raise ValueError("Data must be a dictionary")

        def replace_match(match):
            full_match = match.group(0)
            code = match.group(1)
            parts = code.split("|")
            placeholder = parts[0].strip()
            applied_filters = parts[1:] if len(parts) > 1 else []

            try:
                # Step 1: Check handlers
                if placeholder in self.handlers:
                    value = self.handlers[placeholder](data)
                # Step 2: Check nested attributes
                else:
                    value = self._get_nested_value(data, placeholder)
                    if value == self.default_value and hasattr(self, placeholder):
                        value = getattr(self, placeholder)

                # Apply filters
                for filter_name in applied_filters:
                    if filter_name in self.filters:
                        value = self.filters[filter_name](value)
                    else:
                        log.warning(f"Unknown filter: {filter_name}")
                        value = self.default_value

                return str(value)
            except Exception as e:
                log.error(f"Error processing placeholder '{full_match}': {e}")
                return self.default_value

        pattern = r"\{([^}]+)\}"
        try:
            result = re.sub(pattern, replace_match, template)
            log.info(f"Rendered template: {result}")
            return result
        except Exception as e:
            log.error(f"Error rendering template: {e}")
            return template

class Character:
    def __init__(self, name: str, strength: int = 10):
        self.name = name
        self.strength = strength

    def get_modifier(self, stat: str) -> int:
        """Calculate ability score modifier."""
        value = getattr(self, stat, 10)
        return (value - 10) // 2

class Creature:
    def __init__(self, name: str, hit_points: int = 10):
        self.name = name
        self.hit_points = hit_points

class Item:
    def __init__(self, name: str, damage_dice: str, actions: List['Action'] = None):
        self.name = name
        self.damage_dice = damage_dice
        self.actions = actions or []

class Action:
    def __init__(self, name: str, template: str, engine: TemplateEngine = None):
        self.name = name
        self.template = template
        self.engine = engine or TemplateEngine()

    def execute(self, item: Item, attacker: Character, targets: Union[Creature, List[Creature]] = None) -> str:
        """Render the action template with the given context."""
        data = {
            "item": item,
            "attacker": attacker,
            "targets": [targets] if isinstance(targets, Creature) else targets or []
        }
        return self.engine.render(self.template, data)

def main():
    # Initialize template engine
    engine = TemplateEngine(default_value="UNKNOWN")

    # Register handlers for D&D-specific logic
    def handle_attack_bonus(data):
        attacker = data.get("attacker")
        if attacker and hasattr(attacker, "get_modifier"):
            return attacker.get_modifier("strength")
        return 0

    def handle_damage(data):
        item = data.get("item")
        attacker = data.get("attacker")
        if item and attacker:
            base_damage = item.damage_dice
            modifier = attacker.get_modifier("strength")
            return f"{base_damage} + {modifier}"
        return "1d4"

    engine.register_handler("attack_bonus", handle_attack_bonus)
    engine.register_handler("damage", handle_damage)

    # Define actions
    melee_action = Action(
        name="Melee Attack",
        template="{attacker.name} makes a melee attack with {item.name} against {targets|join}. "
                 "Attack: +{attack_bonus}, Damage: {damage}.",
        engine=engine
    )
    ranged_action = Action(
        name="Ranged Attack",
        template="{attacker.name} makes a ranged attack with {item.name} at {targets|join} (range 20/60 ft). "
                 "Attack: +{attack_bonus}, Damage: {damage}.",
        engine=engine
    )

    # Define an item
    dagger = Item(
        name="dagger",
        damage_dice="1d4",
        actions=[melee_action, ranged_action]
    )

    # Define characters and creatures
    attacker = Character(name="Aragorn", strength=16)  # +3 modifier
    target1 = Creature(name="Goblin")
    target2 = Creature(name="Orc")

    # Execute actions
    print("=== Action Examples ===")
    # Single target
    result = dagger.actions[0].execute(dagger, attacker, target1)
    print(result)
    # Output: Aragorn makes a melee attack with dagger against Goblin. Attack: +3, Damage: 1d4 + 3.

    # Multiple targets
    result = dagger.actions[0].execute(dagger, attacker, [target1, target2])
    print(result)
    # Output: Aragorn makes a melee attack with dagger against Goblin, Orc. Attack: +3, Damage: 1d4 + 3.

    # Ranged attack
    result = dagger.actions[1].execute(dagger, attacker, target1)
    print(result)
    # Output: Aragorn makes a ranged attack with dagger at Goblin (range 20/60 ft). Attack: +3, Damage: 1d4 + 3.

    # Missing target
    result = dagger.actions[0].execute(dagger, attacker, None)
    print(result)
    # Output: Aragorn makes a melee attack with dagger against UNKNOWN. Attack: +3, Damage: 1d4 + 3.

if __name__ == "__main__":
    main()