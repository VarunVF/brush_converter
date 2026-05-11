import customtkinter as ctk

from gui.base_brush_tab import BaseBrushTab
from gui.components import ConvertWidget, ModeSwitcher, SelectDirectory, SelectFile
from photoshop.load_photoshop import load_photoshop


class PhotoshopTabLoadFrame(BaseBrushTab):
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
        rules = [
            (self.select_brush_file.get_file(), "No .abr file is selected"),
            (self.select_extract_dir.get_dir(), "No extract folder is selected"),
        ]

        self.run_threaded_conversion(load_photoshop, rules)

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
