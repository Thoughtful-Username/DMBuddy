class Creature:
    def __init__(self, name, stats, rules_engine):
        self.name = name
        self.stats = stats
        self.rules_engine = rules_engine  # Injected for rule validation

    def perform_action(self, action):
        if self.rules_engine.is_action_valid(self, action):
            # Execute action
            pass