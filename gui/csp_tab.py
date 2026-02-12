import customtkinter as ctk

from gui.components import ConvertWidget, ModeSwitcher, SelectDirectory, SelectFile
from csp.load_csp import load_csp


class CspTabLoadFrame(ctk.CTkFrame):
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)

        self.select_sut_file = SelectFile(self, "sut", fg_color="transparent")
        self.select_sut_file.grid(row=0, column=0, padx=10, pady=10, sticky="w")

        self.select_output_dir = SelectDirectory(self, "Output", fg_color="transparent")
        self.select_output_dir.grid(row=1, column=0, padx=10, pady=10, sticky="w")

        self.convert = ConvertWidget(self, "Load as JSON", self.convert_brush, fg_color="transparent")
        self.convert.grid(row=2, column=0, padx=10, pady=20, sticky="w")
    
    def convert_brush(self):
        sut_file_path = self.select_sut_file.get_file()
        output_dir = self.select_output_dir.get_dir()
        try:
            if not sut_file_path:
                raise ValueError("No .sut file is selected")
            if not output_dir:
                raise ValueError("No output folder is selected")
            load_csp(sut_file_path, output_dir)
            self.convert.configure_label("Conversion completed successfully!", "green")
        except Exception as e:
            self.convert.configure_label(f"Error: {str(e)}", "red")


class CspTabSaveFrame(ctk.CTkFrame):
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)

        self.label = ctk.CTkLabel(self, text="Support for saving CSP brushes not currently available")
        self.label.grid(row=0, column=0, padx=10, pady=10, sticky="w")


class CspTab(ctk.CTkFrame):
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)
        self.mode_switcher = ModeSwitcher(self, CspTabLoadFrame, CspTabSaveFrame)
        self.mode_switcher.pack(fill="both", expand=True)
