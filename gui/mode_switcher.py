import customtkinter as ctk


class ModeSwitcher(ctk.CTkTabview):
    def __init__(self, master, LoadWidget: type[ctk.CTkBaseClass], SaveWidget: type[ctk.CTkBaseClass]):
        super().__init__(master)

        self.load_frame = LoadWidget(self.add("Load"))
        self.load_frame.pack(fill="both", expand=True)
        self.save_frame = SaveWidget(self.add("Save"))
        self.save_frame.pack(fill="both", expand=True)
