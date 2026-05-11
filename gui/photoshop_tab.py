import threading

import customtkinter as ctk

from gui.components import ConvertWidget, ModeSwitcher, SelectDirectory, SelectFile
from photoshop.load_photoshop import load_photoshop


class PhotoshopTabLoadFrame(ctk.CTkFrame):
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)

        self.file_label = ctk.CTkLabel(self, text="Select a Photoshop .abr file (version 10) to be converted:")
        self.file_label.grid(row=0, column=0, padx=10, pady=0, sticky="w")

        self.select_brush_file = SelectFile(self, "abr", fg_color="transparent")
        self.select_brush_file.grid(row=1, column=0, padx=10, pady=10, sticky="w")

        self.dir_label = ctk.CTkLabel(self, text="Select which folder to write the output to:")
        self.dir_label.grid(row=2, column=0, padx=10, pady=0, sticky="w")

        self.select_extract_dir = SelectDirectory(self, "Output", fg_color="transparent")
        self.select_extract_dir.grid(row=3, column=0, padx=10, pady=10, sticky="w")

        self.convert = ConvertWidget(self, "Load as JSON", self.convert_brush, fg_color="transparent")
        self.convert.grid(row=4, column=0, padx=10, pady=20, sticky="w")

    def convert_brush(self):
        brush_file_path = self.select_brush_file.get_file()
        extract_dir = self.select_extract_dir.get_dir()

        # Validation
        if not brush_file_path:
            self.convert.configure_label("Error: No .abr file is selected", "red")
            return
        if not extract_dir:
            self.convert.configure_label("Error: No extract folder is selected", "red")
            return        

        # Update UI to 'Loading'
        self.convert.configure_label("Loading...", "blue")
        self.update_idletasks()  # Force the UI to update the label NOW

        # The background task
        def run_conversion():
            try:
                load_photoshop(brush_file_path, extract_dir)
                self.after(0, lambda: self.convert.configure_label("Conversion completed successfully!", "green"))
            except Exception as e:
                self.after(0, lambda: self.convert.configure_label(f"Error: {str(e)}", "red"))
        
        # Loading takes some time.
        # Load on another thread to keep the GUI responsive.
        threading.Thread(target=run_conversion, daemon=True).start()


class PhotoshopTabSaveFrame(ctk.CTkFrame):
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)

        self.label = ctk.CTkLabel(self, text="Support for saving Photoshop brushes not currently available")
        self.label.grid(row=0, column=0, padx=10, pady=10, sticky="w")


class PhotoshopTab(ctk.CTkFrame):
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)
        self.mode_switcher = ModeSwitcher(self, PhotoshopTabLoadFrame, PhotoshopTabSaveFrame)
        self.mode_switcher.pack(fill="both", expand=True)
