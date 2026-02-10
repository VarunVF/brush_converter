from tkinter import filedialog

import customtkinter as ctk

from typing import Callable


class ConvertWidget(ctk.CTkFrame):
    def __init__(self, master, text: str, command: Callable, **kwargs):
        super().__init__(master, **kwargs)

        self.convert_button = ctk.CTkButton(self, text=text, fg_color="green", command=command)
        self.convert_button.grid(row=2, column=0)

        self.status_label = ctk.CTkLabel(self, text="")
        self.status_label.grid(row=2, column=1, padx=10)

    def configure_label(self, text: str, text_color: str):
        self.status_label.configure(text=text, text_color=text_color)


class ModeSwitcher(ctk.CTkTabview):
    def __init__(self, master, LoadWidget: type[ctk.CTkBaseClass], SaveWidget: type[ctk.CTkBaseClass], **kwargs):
        super().__init__(master, **kwargs)

        self.load_frame = LoadWidget(self.add("Load"), fg_color="transparent")
        self.load_frame.pack(fill="both", expand=True)
        self.save_frame = SaveWidget(self.add("Save"), fg_color="transparent")
        self.save_frame.pack(fill="both", expand=True)


class SelectDirectory(ctk.CTkFrame):
    def __init__(self, master, label_name: str, **kwargs):
        super().__init__(master, **kwargs)

        self.selected_dir = ""
        self.label_name = label_name

        self.button = ctk.CTkButton(self, text=f"Select {self.label_name} Folder", command=self.select_dir)
        self.button.grid(row=0, column=0)

        self.label = ctk.CTkLabel(self, text=f"Selected {self.label_name} Folder: {self.selected_dir}")
        self.label.grid(row=0, column=1, padx=10)
    
    def get_dir(self) -> str:
        return self.selected_dir

    def select_dir(self):
        dir_path = filedialog.askdirectory(title=f"Select {self.label_name} Directory")
        if dir_path:
            self.selected_dir = dir_path
            self.label.configure(text=f"Output {self.label_name} Directory: {self.selected_dir}")


class SelectFile(ctk.CTkFrame):
    def __init__(self, master, file_extension: str, **kwargs):
        super().__init__(master, **kwargs)

        self.file_extension = file_extension
        self.selected_file = ""

        self.button = ctk.CTkButton(self, text=f"Select .{self.file_extension} file", command=self.select_file)
        self.button.grid(row=0, column=0)

        self.label = ctk.CTkLabel(self, text=f"Selected .{self.file_extension}: {self.selected_file}")
        self.label.grid(row=0, column=1, padx=10)

    def get_file(self) -> str:
        return self.selected_file

    def select_file(self):
        file_path = filedialog.askopenfilename(
            title=f"Select .{self.file_extension} File",
            filetypes=[(f"{self.file_extension} Files", f"*.{self.file_extension}"), ("All Files", "*.*")]
        )
        if file_path:
            self.selected_file = file_path
            self.label.configure(text=f"Selected .{self.file_extension}: {self.selected_file}")
