import random
from typing import Any, Dict, List, Tuple, Union
from src.utils.logger import setup_logger
from src.utils.dice_options import OptionRegistry, load_option_handlers
import re

log = setup_logger(__name__)

class Roller:

    def __init__(self, seed: int = None):
        """
        Instantiate dice roller with a defined random seed, if specified.
        Args:
            seed (int):             Optional.  Seed for random module.
        """

        if seed is not None:
            random.seed(seed)


    def roll(self, dice: Dict[str, int], **kwargs) -> Tuple[str, Tuple[int, int], int]:
        """
        Manager function for dice rolling simulation.

        Args:
            dice (Dict[str, int]):              Dictionary representing number and sides of dice to be
                                                rolled and the modifier.
            kwargs (Dict[str, bool]):           Booleans indicating rolling mechanics.
        """
        
        # Valid (Implemented) keywords

        #   Advantage:              Roll twice and take highest value.
        #   Disadvantage:           Roll twice and take lowest value.
        
        #   Keywords to be implemented

        #   Drop_Low_n:             Roll as specified and drop lowest 'n' values
        #   Drop_High_n:            Roll as specified and drop highest 'n' values
        #   Maximum:                Roll as specified and keep maximum value
        #   Minimum:                Roll as specified and keep lowest value
        #   Reroll_n:               Roll as specified, rerolling values 'n' or lower
        #   Stat_Roll:              The same as '4d6' with 'Drop_Low_1'
        #   Critical:               Roll specified dice as critical (critical mechanic
        #                           depends on house rules.)



        # Check format and values in call
        empty_result = ("No result", (0,0),0)
        true_count = sum(value for value in kwargs.values())
        dice_string = f"{dice['count']}d{dice['sides']}{' + ' if dice['modifier'] >= 0 else ' - '}{str(abs(dice['modifier']))}"

        if dice["count"]<=0 or dice["sides"]<=0:
            log.warning(f"Cannot have negative or zero values for dice or sides: '{dice_string}'.  Ignoring roll.")
            return empty_result

        print(f"Simulating dice: {dice_string}.")
        valid_keywords = ("advantage", "disadvantage")
        used_keywords = kwargs.keys()
        unimplemented_keys = used_keywords - valid_keywords
        if unimplemented_keys:
            for key in unimplemented_keys:
                log.warning(f"Logic not implemented for '{key}'.  Ignoring roll '{dice_string}'.")
            return empty_result

        # Distribute control based on kwargs
        if true_count == 0:
            return self.roll_standard(dice) # Standard roll

        if (kwargs.get("advantage", False) or kwargs.get("disadvantage", False)) and dice["count"] != 1:
            log.warning(f"Advantage/disadvantage must apply to a single roll.  Ignoring roll.")
            return empty_result

        if (kwargs.get("advantage", False)) and true_count == 1:
            return self.roll_advantage(dice) # Advantage roll

        if (kwargs.get("disadvantage", False)) and true_count == 1:
            return self.roll_disadvantage(dice) # Disadvantage roll
        
        log.warning("Mechanics not all implemented.")
        return empty_result


    def roll_standard(self, dice: Dict[str, int]) -> Tuple[str, Tuple[int, int], int]:
        # print("Standard Roll.")
        rolls = [random.randint(1, dice["sides"]) for _ in range(dice["count"])]
        return (f'd{dice["sides"]}', rolls, sum(rolls) + dice["modifier"])

    def roll_advantage(self, dice: Dict[str, int]) -> Tuple[str, Tuple[int, int], int]:
        # print("Advantage Roll.")
        rolls = (random.randrange(1, dice["sides"]), random.randrange(1, dice["sides"]))
        # print(f"{rolls}")
        return (f'd{dice["sides"]} with advantage.', rolls, max(rolls) + dice["modifier"])

    def roll_disadvantage(self, dice: Dict[str, int]) -> Tuple[str, Tuple[int, int], int]:
        # print("Disadvantage Roll.")
        rolls = (random.randrange(1, dice["sides"]), random.randrange(1, dice["sides"]))
        return (f'd{dice["sides"]} with disadvantage.', rolls, min(rolls) + dice["modifier"])    



def validate_string(dice_string: str, registry: OptionRegistry = None) -> Tuple[bool, Dict[str, Union[int, bool, str, list]]]:
    """
    Validates a dice string in the format 'xdy + z (a,b,c...)'.
    Returns a tuple (is_valid, result_dict) for a roll simulator.

    Args:
        dice_string (str): Dice string, e.g., '4d6 + 2 (keep_3, label_Strength)'.
        registry (OptionRegistry, optional): Registry for option parsing.

    Returns:
        Tuple[bool, Dict]: (is_valid, result_dict) where:
            - is_valid: True if valid, False if invalid.
            - result_dict: {"count": int, "sides": int, "modifier": int, <option_key>: <value>, ...}
              or {"error": str} if invalid.
    """
    # Initialize registry if not provided
    if registry is None:
        registry = load_option_handlers()

    # Default values
    default_count = 1
    default_modifier = 0

    log.debug(f"Processing dice string: '{dice_string}'")

    try:
        # Regex pattern: (optional count)(\d+)?d(\d+)(optional modifier)( *[+-] *\d+)? *(\(.*\))?$
        pattern = r"^(\d+)?d(\d+)(?: *([+-]) *(\d+))?(?: *(\(.*\)))?$"
        match = re.match(pattern, dice_string.strip())
        if not match:
            log.error(f"Invalid format for '{dice_string}'. Expected 'xdy + z (a,b,c...)'.")
            return False, {"error": "Invalid format. Expected 'xdy + z (a,b,c...)'"}

        # Extract components
        count_str, sides_str, op, modifier_str, options_str = match.groups()

        # Parse count
        count = int(count_str) if count_str else default_count
        if count <= 0:
            log.error(f"Number of dice ({count}) must be greater than 0.")
            return False, {"error": "Number of dice must be greater than 0."}

        # Parse sides
        sides = int(sides_str)
        if sides <= 0:
            log.error(f"Number of sides ({sides}) must be greater than 0.")
            return False, {"error": "Number of sides must be greater than 0."}

        # Parse modifier
        modifier = default_modifier
        if modifier_str:
            modifier = int(modifier_str)
            if op == "-":
                modifier = -modifier

        # Initialize result dictionary
        result = {"count": count, "sides": sides, "modifier": modifier}

        # Parse options
        options = []
        if options_str:
            options_clean = options_str.strip("()")
            options = [opt.strip() for opt in options_clean.split(",") if opt.strip()]
            if not options:
                log.error("Options list cannot be empty if provided.")
                return False, {"error": "Options list cannot be empty if provided."}
        else:
            result["standard"] = True
            log.debug("No options provided, defaulting to 'standard'.")

        # Process options
        for opt in options:
            parsed = registry.parse_option(opt)
            if parsed is None:
                log.error(f"Invalid option '{opt}'. Supported prefixes: {list(registry.handlers.keys())}.")
                return False, {"error": f"Invalid option '{opt}'. Supported prefixes: {list(registry.handlers.keys())}."}
            result.update(parsed)

        # Validate result types
        if not registry.validate_result(result):
            log.error(f"Type mismatch in result dictionary: {result}")
            return False, {"error": "Type mismatch in result dictionary."}

        log.info(f"Successfully parsed dice string: {result}")
        return True, result

    except (ValueError, TypeError) as e:
        log.error(f"Parsing error for '{dice_string}': {str(e)}")
        return False, {"error": f"Invalid input: {str(e)}"}