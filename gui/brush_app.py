import customtkinter as ctk

from gui.procreate_tab import ProcreateTab
from gui.gimp_tab import GimpTab
from gui.medibang_tab import MedibangTab


class BrushApp(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("Brush Converter")
        self.geometry("750x450")

        # Tabs for different backends
        self.tabview = ctk.CTkTabview(self)
        self.tabview.pack(padx=20, pady=20, fill="both", expand=True)
        
        self.tabview.add("Procreate")
        self.tabview.add("GIMP")
        self.tabview.add("MediBang")

        # Populate each tab
        self.procreate_tab = ProcreateTab(self.tabview.tab("Procreate"))
        self.procreate_tab.pack(fill="both", expand=True)

        # Placeholder frames for other tabs
        self.gimp_tab = GimpTab(self.tabview.tab("GIMP"))
        self.gimp_tab.pack(fill="both", expand=True)

        self.medibang_tab = MedibangTab(self.tabview.tab("MediBang"))
        self.medibang_tab.pack(fill="both", expand=True)
