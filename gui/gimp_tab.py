import customtkinter as ctk

from gui.components import ConvertWidget, ModeSwitcher, SelectDirectory, SelectFile
from gimp.load_gbr import load_gbr
from gimp.save_gbr import save_gbr


class GimpTabLoadFrame(ctk.CTkFrame):
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)

        self.select_gbr_file = SelectFile(self, "gbr", fg_color="transparent")
        self.select_gbr_file.grid(row=0, column=0, padx=10, pady=10, sticky="w")

        self.select_extract_dir = SelectDirectory(self, "Extract", fg_color="transparent")
        self.select_extract_dir.grid(row=1, column=0, padx=10, pady=10, sticky="w")

        self.convert = ConvertWidget(self, "Load as JSON", self.convert_brush, fg_color="transparent")
        self.convert.grid(row=2, column=0, padx=10, pady=20, sticky="w")
    
    def convert_brush(self):
        gbr_file_path = self.select_gbr_file.get_file()
        extract_dir = self.select_extract_dir.get_dir()
        try:
            if not gbr_file_path:
                raise ValueError("No .gbr file is selected")
            if not extract_dir:
                raise ValueError("No extract folder is selected")
            load_gbr(gbr_file_path, extract_dir)
            self.convert.configure_label("Conversion completed successfully!", "green")
        except Exception as e:
            self.convert.configure_label(f"Error: {str(e)}", "red")


class GimpTabSaveFrame(ctk.CTkFrame):
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)

        self.select_json_file = SelectFile(self, "json", fg_color="transparent")
        self.select_json_file.grid(row=0, column=0, padx=10, pady=10, sticky="w")

        self.select_bitmap_dir = SelectDirectory(self, "Bitmap", fg_color="transparent")
        self.select_bitmap_dir.grid(row=1, column=0, padx=10, pady=10, sticky="w")

        self.select_output_dir = SelectDirectory(self, "Output", fg_color="transparent")
        self.select_output_dir.grid(row=2, column=0, padx=10, pady=10, sticky="w")

        self.convert = ConvertWidget(self, "Convert & Save", self.convert_brush, fg_color="transparent")
        self.convert.grid(row=3, column=0, padx=10, pady=20, sticky="w")

    def convert_brush(self):
        json_file_path = self.select_json_file.get_file()
        bitmap_dir = self.select_bitmap_dir.get_dir()
        output_dir = self.select_output_dir.get_dir()
        try:
            if not json_file_path:
                raise ValueError("No .json file is selected")
            if not bitmap_dir:
                raise ValueError("No bitmap folder is selected")
            if not output_dir:
                raise ValueError("No output folder is selected")
            save_gbr(json_file_path, bitmap_dir, output_dir)
            self.convert.configure_label("Conversion completed successfully!", "green")
        except Exception as e:
            self.convert.configure_label(f"Error: {str(e)}", "red")


class GimpTab(ctk.CTkFrame):
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)
        self.mode_switcher = ModeSwitcher(self, GimpTabLoadFrame, GimpTabSaveFrame)
        self.mode_switcher.pack(fill="both", expand=True)
