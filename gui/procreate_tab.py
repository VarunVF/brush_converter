import customtkinter as ctk

from gui.base_brush_tab import BaseBrushTab
from gui.components import ConvertWidget, ModeSwitcher, SelectDirectory, SelectFile
from procreate.load_procreate import load_procreate
from procreate.save_procreate import save_procreate


class ProcreateTabLoadFrame(BaseBrushTab):
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)

        self.label = ctk.CTkLabel(self, text="Select a Procreate .brush file to be converted:")
        self.label.grid(row=0, column=0, padx=10, pady=0, sticky="w")

        self.select_brush_file = SelectFile(self, "brush", fg_color="transparent")
        self.select_brush_file.grid(row=1, column=0, padx=10, pady=10, sticky="w")

        self.label = ctk.CTkLabel(self, text="Select which folder to write the output to:")
        self.label.grid(row=2, column=0, padx=10, pady=0, sticky="w")

        self.select_extract_dir = SelectDirectory(self, "Output", fg_color="transparent")
        self.select_extract_dir.grid(row=3, column=0, padx=10, pady=10, sticky="w")

        self.convert = ConvertWidget(self, "Load as JSON", self.convert_brush, fg_color="transparent")
        self.convert.grid(row=4, column=0, padx=10, pady=20, sticky="w")

    def convert_brush(self):
        rules = [
            (self.select_brush_file.get_file(), "No .brush file is selected"),
            (self.select_extract_dir.get_dir(), "No extract folder is selected"),
        ]

        self.run_threaded_conversion(load_procreate, rules)


class ProcreateTabSaveFrame(BaseBrushTab):
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)

        self.label = ctk.CTkLabel(self, text="Select the .json file (from your output directory):")
        self.label.grid(row=0, column=0, padx=10, pady=0, sticky="w")

        self.select_json_file = SelectFile(self, "json", fg_color="transparent")
        self.select_json_file.grid(row=1, column=0, padx=10, pady=10, sticky="w")

        self.label = ctk.CTkLabel(self, text="Select the folder containing the brush images (likely your output directory):")
        self.label.grid(row=2, column=0, padx=10, pady=0, sticky="w")

        self.select_bitmap_dir = SelectDirectory(self, "Bitmap", fg_color="transparent")
        self.select_bitmap_dir.grid(row=3, column=0, padx=10, pady=10, sticky="w")

        self.label = ctk.CTkLabel(self, text="Select which folder you want the converted results to be saved in:")
        self.label.grid(row=4, column=0, padx=10, pady=0, sticky="w")

        self.select_output_dir = SelectDirectory(self, "Output", fg_color="transparent")
        self.select_output_dir.grid(row=5, column=0, padx=10, pady=10, sticky="w")

        self.convert = ConvertWidget(self, "Convert & Save", self.convert_brush, fg_color="transparent")
        self.convert.grid(row=6, column=0, padx=10, pady=20, sticky="w")

    def convert_brush(self):
        rules = [
            (self.select_json_file.get_file(), "No .json file is selected"),
            (self.select_bitmap_dir.get_dir(), "No bitmap folder is selected"),
            (self.select_output_dir.get_dir(), "No output folder is selected"),
        ]
        
        self.run_threaded_conversion(save_procreate, rules)


class ProcreateTab(ctk.CTkFrame):
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)
        self.mode_switcher = ModeSwitcher(self, ProcreateTabLoadFrame, ProcreateTabSaveFrame)
        self.mode_switcher.pack(fill="both", expand=True)
