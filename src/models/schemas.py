THEME_SCHEMA = {
    "type": "object",
    "properties": {
        "button": {"type": "object", "properties": {"bg": {"type": "string"}, "fg": {"type": "string"}}},
        "label": {"type": "object", "properties": {"bg": {"type": "string"}, "fg": {"type": "string"}}}
    },
    "required": ["button", "label"]
}

APP_THEME_SCHEMA = {
    "type": "object",
    "properties": {
        "window": {"type": "object", "properties": {"bg": {"type": "string"}}}
    },
    "required": ["window"]
}

MENU_SCHEMA = {
    "type": "object",
    "properties": {
        "widgets": {
            "type": "array",
            "items": {
                "type": "object",
                "properties": {
                    "type": {"type": "string", "enum": ["button", "label"]},
                    "label": {"type": "string"}
                },
                "required": ["type", "label"]
            }
        }
    },
    "required": ["widgets"]
}