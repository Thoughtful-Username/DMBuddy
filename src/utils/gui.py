import tkinter as tk
from src.utils.mediator import Mediator

class GUI:
    def __init__(self, mediator):
        self.root = tk.Tk()
        self.mediator = mediator  # Injected dependency
        tk.Button(self.root, text="Start Encounter", command=self.mediator.start_encounter).pack()

    def run(self):
        self.root.mainloop()