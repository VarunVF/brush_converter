import customtkinter as ctk

from gui.procreate_tab import ProcreateTab


class BrushApp(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("Brush Converter")
        self.geometry("750x450")

        # 2. Tabs for different Backends
        self.tabview = ctk.CTkTabview(self)
        self.tabview.pack(padx=20, pady=20, fill="both", expand=True)
        
        self.tabview.add("Procreate")
        self.tabview.add("GIMP")
        self.tabview.add("MediBang")

        # 3. Populate Procreate Tab
        self.procreate_tab = ProcreateTab(self.tabview.tab("Procreate"))
        self.procreate_tab.pack(fill="both", expand=True)
