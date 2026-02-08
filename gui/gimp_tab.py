import customtkinter as ctk
from tkinter import filedialog

from gui.mode_switcher import ModeSwitcher
# from load_gbr import load_gbr
# from save_gbr import save_gbr


class GimpTabLoadFrame(ctk.CTkFrame):
    def __init__(self, master):
        super().__init__(master)


class GimpTabSaveFrame(ctk.CTkFrame):
    def __init__(self, master):
        super().__init__(master)


class GimpTab(ctk.CTkFrame):
    def __init__(self, master):
        super().__init__(master)
        self.mode_switcher = ModeSwitcher(self, GimpTabLoadFrame, GimpTabSaveFrame)
        self.mode_switcher.pack(fill="both", expand=True)

        ctk.CTkLabel(self, text="GIMP functionality coming soon!").pack(pady=20)
