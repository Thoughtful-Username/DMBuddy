class Encounter:
    def __init__(self, dice_roller):
        self.dice_roller = dice_roller  # Injected dependency
        self.combatants = []

    def add_combatant(self, creature):
        initiative = self.dice_roller.roll("1d20") + creature.initiative_bonus
        self.combatants.append((initiative, creature))