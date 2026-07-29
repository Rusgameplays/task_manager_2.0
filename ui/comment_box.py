import customtkinter as ctk

from ui.theme import *


class CommentBox(ctk.CTkFrame):

    def __init__(self, master, on_change=None):
        super().__init__(
            master,
            fg_color="transparent"
        )

        self.on_change = on_change

        self.build_ui()

    def build_ui(self):

        self.grid_columnconfigure(0, weight=1)

        self.label = ctk.CTkLabel(
            self,
            text="Комментарий",
            font=FONT_SMALL
        )

        self.label.grid(
            row=0,
            column=0,
            sticky="w",
            pady=(0, 8)
        )

        self.textbox = ctk.CTkTextbox(
            self,
            height=100,
            corner_radius=8
        )

        self.textbox.grid(
            row=1,
            column=0,
            sticky="nsew"
        )

        self.textbox.bind(
            "<KeyRelease>",
            self.text_changed
        )

    def text_changed(self, event):

        if self.on_change:
            self.on_change(self.get())

    def set(self, value):

        self.textbox.delete(
            "1.0",
            "end"
        )

        self.textbox.insert(
            "1.0",
            value
        )

    def get(self):

        return self.textbox.get(
            "1.0",
            "end-1c"
        )