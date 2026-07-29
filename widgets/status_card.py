import customtkinter as ctk

from ui.theme import *


class StatusCard(ctk.CTkFrame):

    def __init__(
            self,
            master,
            title,
            values,
            on_change=None
    ):
        super().__init__(
            master,
            fg_color=CARD,
            corner_radius=12,
            border_width=1,
            border_color=BORDER
        )

        self.on_change = on_change

        self.grid_columnconfigure(0, weight=1)

        self.title = ctk.CTkLabel(
            self,
            text=title,
            font=("Segoe UI", 12),
            text_color=TEXT_SECONDARY
        )

        self.title.grid(
            row=0,
            column=0,
            pady=(12, 6)
        )

        self.combo = ctk.CTkComboBox(
            self,
            values=values,
            command=self.changed
        )

        self.combo.grid(
            row=1,
            column=0,
            padx=12,
            pady=(0, 12),
            sticky="ew"
        )

    def changed(self, value):
        self.update_color()

        if self.on_change:
            self.on_change(value)

    def set(self, value):
        self.combo.set(value)

        self.update_color()

    def get(self):

        return self.combo.get()

    def update_color(self):
        color = CARD_COLORS.get(
            self.get(),
            CARD
        )

        self.configure(
            fg_color=color,
            border_color=color
        )