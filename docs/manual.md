<h1 style="text-align:center;">DM Buddy - A Dungeon Master's Best Friend</h1>

DM Buddy is a comprehensive tool for Dungeon Masters that helps with everything from developing camgaigns to managing individual encounters and everything in between. With DM Buddy, gameplay flows more naturally, keeping players engaged and sessions exciting.

In real time, DM Buddy will keep track of combatants in an encounter, tracking turns, applying damage and spell effects, and keeping DMs informed on exactly what actions are available to the active combatant up-to-the-moment.

#### Table of Contents

- [Getting Started](#getting_started)
- [Building a Campaign](#campaign)
- [Preparing for a Game Session](#session_prep)
- [Managing a Game Session](#session_mgmt)
- [Adding Content](#adding_content)
- [Internals](#internals)

<h2 id="getting_started">Getting Started</h2>

#### In this section:

- [Preparing for the first use.](#first_use)
- [Starting DM Buddy](#start)
- [Navigating the application](#navigation)

<h2 id="campaign">Building a Campaign</h2>

<h2 id="session_prep">Preparing for a Game Session</h2>

<h2 id="session_mgmt">Managing a Game Session</h2>

<h2 id="adding_content">Adding Content</h2>

<h2 id="internals">Internals</h2>

#### In this section:

- [Coding principals](#coding_principals)
- [Main Directory](#main)
  - [DMBuddy.py](#dmbuddy_py)
- [Source Folder - 'src'](#src)
  - [Content Folder - 'src.content'](#src_content)
    - [action.py](#action_py)
    - [armor.py](#armor_py)
    - [character.py](#character_py)
    - [creature.py](creature_py)
    - [effect.py](#effect_py)

<h2 id="coding_principals">Coding principals</h2>

<h2 id="main">Main Directory</h2>

<h3 id="dmbuddy_py">DMBuddy.py</h3>

`DMBubby.py` acts as the entry point of the application. It initializes core components (e.g., logger, JSON cache) and launches the GUI.

<h4>Responsibilities</h4>

DMBudy's responsibilities include:

- Setting up global configurations.
- Instantiating the main application controller and starting the application.
- Handling command-line arguments or environment setup if needed.
