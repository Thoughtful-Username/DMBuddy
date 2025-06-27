**Project Structure Outline (PSO)**:

# /data/config/DMBuddy.txt

```
DMBuddy/                                        # Python tool designed to assist Dungeon Masters running
│                                                 Dungeons and Dragons 5th Edition game.  First and
│                                                 foremost intended to assist with in-game information
│                                                 management, option selections, dice-rolling, etc.  My
│                                                 first idea was I need an 'initiative tracker' so that
│                                                 during complex encounters, turn management is controlled,
│                                                 valid actions are clearly defined, and temporary effects
│                                                 are administered.  The concept of this project grew from
│                                                 there, but that is my main priority for now.
│
│                                                 I know a little about Python and OOP and I don't expect
│                                                 this to be used by others, except maybe people in my friend
│                                                 group, but I want to develop it as a more formal/professional
│                                                 project would be done so that I can learn the concepts
│                                                 necessary for robust, maximally extensible code.
├── data/
│   ├── config/
│   │   ├── dice_config.json                    # Dice mechanics and options (e.g., advantage, explode, etc.).
│   │   ├── DMBuddy.txt                         # This file.
│   │   ├── rules.json                          # Lists, tables, etc., including things like official damage
│   │   │                                         types, skills, etc.  These lists are maintained for validation
│   │   │                                         of the json files in the various content folders.  Homebrew
│   │   │                                         changes would also be added here.  For example, I might add
│   │   │                                         'crushing' damage to the list of damage types.  Also includes
│   │   │                                         boolean for house rules and definitions for those house rules.
│   │   │                                         House rule examples include whether encumbrance is considered
│   │   │                                         or not, changes to the way damage is calculated on critical
│   │   │                                         hits, etc.
│   │   ├── options.json                        # User-selected options.  Includes app-related options and house
│   │   │                                         rule selection.
│   │   └── GUI/                                # Style and theme to be defined here.
│   │       ├── buttons.json                    # Button labels, sizes.
│   │       ├── styles.json                     # Widget styles (colors, fonts, etc.).
│   │       └── themes.json                     # Theme configuration.
│   ├── content/
│   │   ├── actions/                            # Complex / often used action definitions
│   │   ├── campaigns/                          # Campaign data.
│   │   │   └── my_campaign/                    # Example campaign
│   │   │       ├── resources/                  # Information and/or assets as needed.
│   │   │       ├── my_campaign.json            # Background, setting, objective, etc.
│   │   │       ├── random_encounters.json      # Scripted 'random' encounters and/or resources to generate
│   │   │       │                                 truly random encounters.  Could be as simple as preferred
│   │   │       │                                 monsters/NPC types.  Long-term goal.
│   │   │       └── session_01/                 # Example campaign session
│   │   │           ├── resources/              # Information and/or assets as needed.
│   │   │           ├── session_01.json         # Current character and NPC states, session goal, narrative,
│   │   │           │                             random encounter tables, etc.
│   │   │           └── encounter_01/           # Example encounter.  Could be scripted or random.
│   │   │               └── resources/          # Information and/or assets as needed.
│   │   │               └── encounter_01.json   # Encounter and combatant states, description, etc.
│   │   ├── characters/
│   │   │   ├── classes/                        # Definitions for character classes.
│   │   │   │   └── barbarian.json              # Example
│   │   │   ├── races/                          # Definitions for playable creature species.
│   │   │   │   └── goliath.json                # Example
│   │   ├── creatures/                          # Definitions for creature species.  Separate definitions
│   │   │   │                                     for generic creatures like 'Goblins' or more specific
│   │   │   │                                     like 'Goblin Doom Divers'.  TODO: Consider separating
│   │   │   │                                     or identifying definitions based on content creator since
│   │   │   │                                     some homebrew creators' content may be incompatible or at
│   │   │   │                                     least not properly balanced for use in conjunction with
│   │   │   │                                     official content or other content creators.
│   │   │   ├── goblin.json                     # Example
│   │   │   └── goblin_doom_diver.json          # Example
│   │   ├── conditions/                         # Definitions for conditions.
│   │   │   └── prone.json                      # Example
│   │   ├── design_resources/                   # Long-term goal.  For universal application or inclusion.
│   │   │   │                                     Subfolder list is *probably* incomplete.
│   │   │   ├── loot_tables/
│   │   │   └── narrative_embellishemet/
│   │   ├── items/                              # One item class with various types.  Or, perhaps separate
│   │   │   │                                     weapons and armor into their own subclasses, since they
│   │   │   │                                     have a large amount of additional unique attributes and
│   │   │   │                                     methods.
│   │   │   └── prone.json                      # Example
│   │   ├── spells/                             # Definitions for spells.
│   │   │   └── fireball.json                   # Example
│   │   ├── templates/                          # JSON templates for content validation.  Creature, action,
│   │   │   │                                     item, etc.
│   │   │   └── item_template.json              # Example
│   └── logs/                                   # Logging module logs.
├── docs/
│   ├── api/                                    # Suggested by Grok.  TODO: Learn proper format.
│   └── user_guide.md                           # Project documentation.  TODO: Keep up with documentation
│                                                 as project advances.
├── src/
│   ├── __init__.py                             # TODO: Learn about Python packages.
│   ├── content/                                # Logic for generating and maintaining game object resources only.
│   │   ├── __init__.py
│   │   ├── action.py                           # Class.  For characters and NPCs, available actions are
│   │   │                                         derived from: class and level; equipped and/or attuned items;
│   │   │                                         circumstance; other?.  For monsters, actions are defined
│   │   │                                         in statblock.
│   │   ├── armor.py                            # Armor subclass of Item.
│   │   ├── character.py                        # Player-character subclass of creature.
│   │   ├── creature.py                         # Base class. Attributes and methods universal to characters,
│   │   │                                         monsters, and NPCs.  In this project, characters, monsters,
│   │   │                                         and NPCs are collectively referred to as creatures (or
│   │   │                                         combatants in the context of a combat encounter.).
│   │   ├── effect.py                           # Class for potential outcome of an action.  An observer
│   │   │                                         class watching creature actions and turns.  This will
│   │   │                                         facilitate the proper incrementing of remaining time
│   │   │                                         effective for temporary effects and the monitoring of
│   │   │                                         specific conditions, if and as required, for all effects.
│   │   ├── item.py                             # Base class.  Attributes and methods universal to items.
│   │   ├── map.py                              # Long-term goal.  2D only.  Perhaps it would be easier to
│   │   │                                         start with ASCII representations?
│   │   ├── monster.py                          # Enemy subclass of creature
│   │   ├── npc.py                              # Non-player character subclass of creature.
│   │   └── sentient_item.py                    # TODO: Implement only the most basic requirements as a
│   │   │                                         placeholder.  Long-term goal.
│   │   └── weapon.py                           # Weapon subclass of Item.
│   ├── core/                                   # Logic for generating and maintaining app/game control.
│   │   ├── __init__.py
│   │   ├── campaign.py                         # Class.  Campaign management
│   │   ├── designer.py                         # Aid DM in preparing campaigns, sessions, and encounters,
│   │   │                                         and also new content.
│   │   ├── dice.py                             # Class.  Centralized dice roller.  Called by content
│   │   │                                         instances only at the direction of the app management code.
│   │   ├── encounter.py                        # Class.  Encounter management.  To include initiative tracker.
│   │   ├── session.py                          # Class.  Session management.
│   │   └── state.py                            # Application and game-play state management.  Suggested by Grok,
│   │                                             but I'm not sure yet how to implement/ what exactly it would do.
│   └── utils/                                  # Logic for helper code, reusable utilities, etc.
│       ├── __init__.py
│       ├── config.py                           # Handles loading/storing configurations.
│       ├── gui.py                              # GUI module, handles Tkinter code.
│       ├── jsonschema.py                       # Logic to validate json file formats.
│       ├── logger.py                           # Customized initialization of logger instance (using logging library).
│       ├── mediator.py                         # Suggested by Grok.  Mediator between core logic and GUI.
│       │                                         TODO: Learn about concept and how to implement.
│       └── string_render.py                    # Renders text strings with field codes into readable text.
├── tests/                                      # Test files for each new aspect implemented.  Implement *simple*
│       │                                         password in GUI for gate-keeping access.
│       └── __init__.py
├── main.py                                     # Entry point of the app.
├── README.md
├── requirements.txt                            # Dependencies (e.g., tkinter, if needed).  TODO: Learn how to format.
└── .gitignore                                  # Ignore pycache, etc.
```

**Coding requirements**:

- Maintain compliance with PEP8, with the exception of the 79-character-per-line limit. Code will
  be formatted at a later date to come into compliance with that particular requirement.
- Employ efficiency-, extensibility-, and robustness-ensuring coding concepts, including: class-level
  data caching, data file validation, dependency injections, type hinting, etc. TODO: identify other
  important concepts.
- Use preferred libraries: json, jsonschema, logging, pytest, re, tkinter, typing, etc. TODO: Define
  other preferred libraries.
