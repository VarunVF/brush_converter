import customtkinter as ctk

from gui.procreate_tab import ProcreateTab


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
        self.gimp_tab = ctk.CTkFrame(self.tabview.tab("GIMP"))
        ctk.CTkLabel(self.gimp_tab, text="GIMP functionality coming soon!").pack(pady=20)
        self.gimp_tab.pack(fill="both", expand=True)

        self.medibang_tab = ctk.CTkFrame(self.tabview.tab("MediBang"))
        ctk.CTkLabel(self.medibang_tab, text="MediBang functionality coming soon!").pack(pady=20)
        self.medibang_tab.pack(fill="both", expand=True)
