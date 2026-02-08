import customtkinter as ctk
from tkinter import filedialog

from gui.mode_switcher import ModeSwitcher
# from load_mdp import load_mdp
# from save_mdp import save_mdp


class MedibangTabLoadFrame(ctk.CTkFrame):
    def __init__(self, master):
        super().__init__(master)


class MedibangTabSaveFrame(ctk.CTkFrame):
    def __init__(self, master):
        super().__init__(master)


class MedibangTab(ctk.CTkFrame):
    def __init__(self, master):
        super().__init__(master)
        self.mode_switcher = ModeSwitcher(self, MedibangTabLoadFrame, MedibangTabSaveFrame)
        self.mode_switcher.pack(fill="both", expand=True)

        ctk.CTkLabel(self, text="MediBang functionality coming soon!").pack(pady=20)
