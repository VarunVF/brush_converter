import os

import customtkinter as ctk
from platformdirs import user_data_dir

from gui.components import ConvertWidget, ModeSwitcher, SelectDirectory, SelectFile
from medibang.load_mdp import load_mdp
from medibang.save_mdp import save_mdp


def get_config_dir():
    return user_data_dir(appname="CloudAlpaca", appauthor="Medibang")


class MedibangTabLoadFrame(ctk.CTkFrame):
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)

        self.select_config_dir = SelectDirectory(self, "Config", get_config_dir(), fg_color="transparent")
        self.select_config_dir.grid(row=0, column=0, padx=10, pady=10, sticky="w")

        self.select_extract_dir = SelectDirectory(self, "Extract", fg_color="transparent")
        self.select_extract_dir.grid(row=1, column=0, padx=10, pady=10, sticky="w")

        self.convert = ConvertWidget(self, "Load as JSON", self.convert_brush, fg_color="transparent")
        self.convert.grid(row=2, column=0, padx=10, pady=20, sticky="w")

    def convert_brush(self):
        config_dir = self.select_config_dir.get_dir()
        brush2ini_file_path = os.path.join(config_dir, "Brush2.ini")
        extract_dir = self.select_extract_dir.get_dir()
        try:
            if not brush2ini_file_path:
                raise ValueError("No .ini file is selected")
            if not extract_dir:
                raise ValueError("No extract folder is selected")
            load_mdp(config_dir, brush2ini_file_path, extract_dir)
            self.convert.configure_label("Conversion completed successfully!", "green")
        except Exception as e:
            self.convert.configure_label(f"Error: {str(e)}", "red")


class MedibangTabSaveFrame(ctk.CTkFrame):
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)

        self.select_json_file = SelectFile(self, "json", fg_color="transparent")
        self.select_json_file.grid(row=0, column=0, padx=10, pady=10, sticky="w")

        self.select_config_dir = SelectDirectory(self, "Config", get_config_dir(), fg_color="transparent")
        self.select_config_dir.grid(row=1, column=0, padx=10, pady=10, sticky="w")

        self.convert = ConvertWidget(self, "Convert & Save", self.convert_brush, fg_color="transparent")
        self.convert.grid(row=2, column=0, padx=10, pady=20, sticky="w")

    def convert_brush(self):
        brush_json_file_path = self.select_json_file.get_file()
        config_dir = self.select_config_dir.get_dir()
        brush2ini_file_path = os.path.join(config_dir, "Brush2.ini")
        bitmap_dir = os.path.join(config_dir, "brush_bitmap")
        try:
            if not brush_json_file_path:
                raise ValueError("No .json file is selected")
            if not config_dir:
                raise ValueError("No .ini file is selected")
            save_mdp(brush_json_file_path, brush2ini_file_path, bitmap_dir)
            self.convert.configure_label("Conversion completed successfully!", "green")
        except Exception as e:
            self.convert.configure_label(f"Error: {str(e)}", "red")


class MedibangTab(ctk.CTkFrame):
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)
        self.mode_switcher = ModeSwitcher(self, MedibangTabLoadFrame, MedibangTabSaveFrame)
        self.mode_switcher.pack(fill="both", expand=True)
