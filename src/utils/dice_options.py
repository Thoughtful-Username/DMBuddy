# src/utils/dice_options.py
import json
import os
from typing import Dict, List, Union, Callable, Optional
from src.utils.logger import setup_logger

log = setup_logger("DMTools")

_json_cache = {}


class OptionRegistry:
    """Manages option handlers for dice string validation."""
    def __init__(self):
        self.handlers: Dict[str, Callable[[List[str]], Optional[Dict[str, Union[int, str, List[int]]]]]] = {}
        self.schemas: Dict[str, type] = {}  # Expected type for each option key

    def register(self, prefix: str, handler: Callable[[List[str]], Optional[Dict[str, Union[int, str, List[int]]]]], schema: Dict[str, type]) -> None:
        """Register an option handler with its output schema."""
        self.handlers[prefix] = handler
        self.schemas.update(schema)

    def parse_option(self, option: str) -> Optional[Dict[str, Union[int, str, List[int]]]]:
        """Parse an option using the registered handler."""
        parts = option.split("_")
        if len(parts) < 2:
            return None
        prefix, params = parts[0], parts[1:]
        handler = self.handlers.get(prefix)
        if not handler:
            return None
        return handler(params)

    def validate_result(self, result: Dict) -> bool:
        """Validate dictionary against schemas."""
        for key, value in result.items():
            expected_type = self.schemas.get(key)
            if expected_type and not isinstance(value, expected_type):
                return False
        return True


def _load_json(file_name: str) -> Dict:
    """Load JSON file into cache."""
    if file_name not in _json_cache:
        project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', '..'))
        file_path = os.path.join(project_root, 'data/config', file_name)
        try:
            with open(file_path, 'r') as f:
                _json_cache[file_name] = json.load(f)
                log.debug(f"Loaded JSON from {file_path}")
        except FileNotFoundError:
            _json_cache[file_name] = {}
            log.warning(f"JSON file '{file_path}' not found, returning empty dict.")
    return _json_cache[file_name]


def load_option_handlers() -> OptionRegistry:
    """Load option handlers from configuration."""
    registry = OptionRegistry()

    OPTION_CONFIG = _load_json("dice_options.json")

    # Register simple options (not from config, but could be)
    for opt in OPTION_CONFIG["simple_options"]:
        registry.register(opt, lambda params: {opt: True} if not params else None, {opt: bool})

    # Register complex options from config
    for opt_config in OPTION_CONFIG["complex_options"]:
        prefix = opt_config["prefix"]
        param_count = opt_config["param_count"]
        param_types = opt_config["param_types"]
        schema = {list(opt_config["output"].keys())[0]: eval(opt_config["output"][list(opt_config["output"].keys())[0]])}

        def create_handler(p_count: int, p_types: List[str]) -> Callable:
            def handler(params: List[str]) -> Optional[Dict]:
                if len(params) != p_count:
                    return None
                try:
                    if p_types[0] == "int" and all(p.isdigit() for p in params):
                        if p_count == 1:
                            return {prefix: int(params[0])}
                        return {prefix: [int(p) for p in params]}
                    elif p_types[0] == "str" and p_count == 1:
                        return {prefix: params[0]}
                    return None
                except (ValueError, TypeError):
                    return None
            return handler

        registry.register(prefix, create_handler(param_count, param_types), schema)

    return registry
