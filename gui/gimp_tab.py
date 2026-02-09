import customtkinter as ctk
from tkinter import filedialog

from gui.mode_switcher import ModeSwitcher
from load_gbr import load_gbr
from save_gbr import save_gbr


class GimpTabLoadFrame(ctk.CTkFrame):
    def __init__(self, master):
        super().__init__(master)

        self.btn_select = ctk.CTkButton(self, text="Select .gbr File", command=self.select_file)
        self.btn_select.grid(row=0, column=0, padx=10, pady=10)

        self.gbr_file_path = "No file selected"
        self.brush_label = ctk.CTkLabel(self, text=f"Selected File: {self.gbr_file_path}")
        self.brush_label.grid(row=0, column=1, padx=10, pady=10)
        
        self.btn_select = ctk.CTkButton(self, text="Select Extract Folder", command=self.select_extract_dir)
        self.btn_select.grid(row=1, column=0, padx=10, pady=10)

        self.extract_dir = "No folder selected"
        self.extract_label = ctk.CTkLabel(self, text=f"Extract Folder: {self.extract_dir}")
        self.extract_label.grid(row=1, column=1, padx=10, pady=10)

        # Convert Button
        self.btn_convert = ctk.CTkButton(self, text="Load as JSON", fg_color="green", command=self.convert_brush)
        self.btn_convert.grid(row=2, column=0, pady=20)

        # Error/Status Label
        self.status_label = ctk.CTkLabel(self, text="")
        self.status_label.grid(row=2, column=1, padx=10, pady=10)

    def select_file(self):
        file_path = filedialog.askopenfilename(
            title="Select Brush File",
            filetypes=[("GIMP Brush", "*.gbr"), ("All Files", "*.*")]
        )
        if file_path:
            self.gbr_file_path = file_path
            self.brush_label.configure(text=f"Selected file: {self.gbr_file_path}")

    def select_extract_dir(self):
        dir_path = filedialog.askdirectory(title="Select Extract Folder")
        if dir_path:
            self.extract_dir = dir_path
            self.extract_label.configure(text=f"Selected folder: {self.extract_dir}")

    def convert_brush(self):
        print(f"Source file: {self.gbr_file_path}")
        print(f"Extract directory: {self.extract_dir}")
        try:
            load_gbr(self.gbr_file_path, self.extract_dir)
            self.status_label.configure(text="Conversion completed successfully!", text_color="green")
        except Exception as e:
            self.status_label.configure(text=f"Error: {str(e)}", text_color="red")


class GimpTabSaveFrame(ctk.CTkFrame):
    def __init__(self, master):
        super().__init__(master)

        # Procreate save-specific arguments
        self.json_filepath = "No JSON file selected"
        self.bitmap_dir = "No bitmap directory selected"
        self.output_dir = "No output directory selected"

        self.btn_select_json = ctk.CTkButton(self, text="Select JSON File", command=self.select_json_file)
        self.btn_select_json.grid(row=0, column=0, padx=10, pady=10)

        self.json_label = ctk.CTkLabel(self, text=f"Selected JSON: {self.json_filepath}")
        self.json_label.grid(row=0, column=1, padx=10, pady=10)

        self.btn_select_bitmap = ctk.CTkButton(self, text="Select Bitmap Directory", command=self.select_bitmap_dir)
        self.btn_select_bitmap.grid(row=1, column=0, padx=10, pady=10)

        self.bitmap_label = ctk.CTkLabel(self, text=f"Bitmap Directory: {self.bitmap_dir}")
        self.bitmap_label.grid(row=1, column=1, padx=10, pady=10)

        self.btn_select_output = ctk.CTkButton(self, text="Select Output Directory", command=self.select_output_dir)
        self.btn_select_output.grid(row=2, column=0, padx=10, pady=10)

        self.output_label = ctk.CTkLabel(self, text=f"Output Directory: {self.output_dir}")
        self.output_label.grid(row=2, column=1, padx=10, pady=10)

        # Convert Button and Status Label
        self.btn_convert = ctk.CTkButton(self, text="Convert & Save", fg_color="green", command=self.convert_brush)
        self.btn_convert.grid(row=3, column=0, pady=(20))

        self.status_label = ctk.CTkLabel(self, text="")
        self.status_label.grid(row=3, column=1, padx=10, pady=10)

    def select_json_file(self):
        file_path = filedialog.askopenfilename(
            title="Select JSON File",
            filetypes=[("JSON Files", "*.json"), ("All Files", "*.*")]
        )
        if file_path:
            self.json_filepath = file_path
            self.json_label.configure(text=f"Selected JSON: {self.json_filepath}")

    def select_bitmap_dir(self):
        dir_path = filedialog.askdirectory(title="Select Bitmap Directory")
        if dir_path:
            self.bitmap_dir = dir_path
            self.bitmap_label.configure(text=f"Bitmap Directory: {self.bitmap_dir}")

    def select_output_dir(self):
        dir_path = filedialog.askdirectory(title="Select Output Directory")
        if dir_path:
            self.output_dir = dir_path
            self.output_label.configure(text=f"Output Directory: {self.output_dir}")

    def convert_brush(self):
        print(f"JSON file: {self.json_filepath}")
        print(f"Bitmap directory: {self.bitmap_dir}")
        print(f"Output directory: {self.output_dir}")
        try:
            save_gbr(self.json_filepath, self.bitmap_dir, self.output_dir)
            self.status_label.configure(text="Conversion completed successfully!", text_color="green")
        except Exception as e:
            self.status_label.configure(text=f"Error: {str(e)}", text_color="red")


class GimpTab(ctk.CTkFrame):
    def __init__(self, master):
        super().__init__(master)
        self.mode_switcher = ModeSwitcher(self, GimpTabLoadFrame, GimpTabSaveFrame)
        self.mode_switcher.pack(fill="both", expand=True)
