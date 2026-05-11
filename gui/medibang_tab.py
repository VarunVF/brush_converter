import os

import customtkinter as ctk
from platformdirs import user_data_dir

from gui.base_brush_tab import BaseBrushTab
from gui.components import ConvertWidget, ModeSwitcher, SelectDirectory, SelectFile
from medibang.load_mdp import load_mdp
from medibang.save_mdp import save_mdp


def get_config_dir():
    return user_data_dir(appname="CloudAlpaca", appauthor="Medibang")


class MedibangTabLoadFrame(BaseBrushTab):
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)

        self.label = ctk.CTkLabel(self, text="Medibang config folder (automatically selected for you):")
        self.label.grid(row=0, column=0, padx=10, pady=0, sticky="w")

        self.select_config_dir = SelectDirectory(self, "Config", get_config_dir(), fg_color="transparent")
        self.select_config_dir.grid(row=1, column=0, padx=10, pady=10, sticky="w")

        self.label = ctk.CTkLabel(self, text="Select which folder to write the output to:")
        self.label.grid(row=2, column=0, padx=10, pady=0, sticky="w")

        self.select_extract_dir = SelectDirectory(self, "Output", fg_color="transparent")
        self.select_extract_dir.grid(row=3, column=0, padx=10, pady=10, sticky="w")

        self.convert = ConvertWidget(self, "Load as JSON", self.convert_brush, fg_color="transparent")
        self.convert.grid(row=4, column=0, padx=10, pady=20, sticky="w")

    def convert_brush(self):
        config_dir = self.select_config_dir.get_dir()
        rules = [
            (config_dir, "No config folder is selected"),
            (os.path.join(config_dir, "Brush2.ini"), "Could not get path to Brush2.ini config file"),
            (self.select_extract_dir.get_dir(), "No extract folder is selected"),
        ]

        self.run_threaded_conversion(load_mdp, rules)


class MedibangTabSaveFrame(BaseBrushTab):
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)

        self.label = ctk.CTkLabel(self, text="Select the .json file (from your output directory):")
        self.label.grid(row=0, column=0, padx=10, pady=0, sticky="w")

        self.select_json_file = SelectFile(self, "json", fg_color="transparent")
        self.select_json_file.grid(row=1, column=0, padx=10, pady=10, sticky="w")

        self.label = ctk.CTkLabel(self, text="Medibang config folder (automatically selected for you):")
        self.label.grid(row=2, column=0, padx=10, pady=0, sticky="w")

        self.select_config_dir = SelectDirectory(self, "Config", get_config_dir(), fg_color="transparent")
        self.select_config_dir.grid(row=3, column=0, padx=10, pady=10, sticky="w")

        self.convert = ConvertWidget(self, "Convert & Save", self.convert_brush, fg_color="transparent")
        self.convert.grid(row=4, column=0, padx=10, pady=20, sticky="w")

    def convert_brush(self):
        config_dir = self.select_config_dir.get_dir()
        rules = [
            (self.select_json_file.get_file(), "No .json file is selected"),
            (os.path.join(config_dir, "Brush2.ini"), "Could not get path to Brush2.ini config file"),
            (os.path.join(config_dir, "brush_bitmap"), "Could not get path to bitmaps in config folder"),
        ]

        self.run_threaded_conversion(save_mdp, rules)


class MedibangTab(ctk.CTkFrame):
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)
        self.mode_switcher = ModeSwitcher(self, MedibangTabLoadFrame, MedibangTabSaveFrame)
        self.mode_switcher.pack(fill="both", expand=True)
