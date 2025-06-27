class Mediator:
    def __init__(self, gui, encounter_manager, session_manager):
        self.gui = gui
        self.encounter_manager = encounter_manager
        self.session_manager = session_manager

    def start_encounter(self):
        encounter_data = self.session_manager.get_current_encounter()
        self.encounter_manager.start(encounter_data)
        self.gui.show_encounter_screen()
    
    def set_encounter_manager(self, encounter_manager):
        self.encounter_manager = encounter_manager