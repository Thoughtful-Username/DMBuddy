# DMBuddy/main.py
from src.core.mediator import Mediator
from src.gui.app_gui import AppGUI
from src.utils.injector import Injector
from src.utils.logger import setup_logger
from src.core.config import ConfigLoader

def main():
    # Setup logging
    logger = setup_logger()

    try:
        # Initialize dependency injector
        injector = Injector()
        
        # Load and validate configurations
        config_loader = injector.get(ConfigLoader)
        
        # Initialize mediator and GUI
        mediator = injector.get(Mediator)
        gui = injector.get(AppGUI)
        
        # Start the application
        gui.run()
    except Exception as e:
        logger.error(f"Application failed: {e}")
        raise

if __name__ == "__main__":
    main()