import customtkinter as ctk

from ui.theme import *


class InfoRow(ctk.CTkFrame):

    def __init__(self, master, title, value=""):

        super().__init__(
            master,
            fg_color="transparent"
        )

        self.grid_columnconfigure(1, weight=1)

        self.title = ctk.CTkLabel(
            self,
            text=title,
            width=140,
            anchor="w",
            font=FONT_SMALL,
            text_color=TEXT_SECONDARY
        )

        self.title.grid(
            row=0,
            column=0,
            padx=(0, 20),
            pady=8,
            sticky="w"
        )

        self.value = ctk.CTkLabel(
            self,
            text=value,
            anchor="w",
            font=FONT
        )

        self.value.grid(
            row=0,
            column=1,
            pady=8,
            sticky="ew"
        )

    def set_value(self, value):

        self.value.configure(
            text=value
        )