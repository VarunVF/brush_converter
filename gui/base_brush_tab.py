import threading

import customtkinter as ctk

from gui.components import ConvertWidget


class BaseBrushTab(ctk.CTkFrame):
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)

        self.convert: ConvertWidget = None  # To be defined by subclasses

    def run_threaded_conversion(self, processing_func, rules_list: list[tuple[str, str]]):
        # Validation
        for param, failure_info in rules_list:
            if not param:
                self.convert.configure_label(f"Error: {failure_info}", "red")
                return

        # Update the UI to 'Loading'
        self.convert.configure_label("Loading...", "blue")
        self.update_idletasks()  # Force the UI to update the label NOW

        def task():
            try:
                processing_func(*[pair[0] for pair in rules_list])
                self.after(0, lambda: self.convert.configure_label("Conversion completed successfully!", "green"))
            except Exception as e:
                self.after(0, lambda msg=str(e): self.convert.configure_label(f"Error: {msg}", "red"))

        threading.Thread(target=task, daemon=True).start()
