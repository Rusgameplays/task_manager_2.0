import customtkinter as ctk

from ui.theme import *


class Toolbar(ctk.CTkFrame):

    def __init__(
            self,
            master,
            on_new=None,
            on_search=None,
            on_report=None
    ):
        super().__init__(
            master,
            height=60,
            fg_color=SIDEBAR
        )

        self.on_new = on_new
        self.on_search = on_search
        self.on_report = on_report

        self.build_ui()

    def build_ui(self):

        self.grid_columnconfigure(2, weight=1)

        self.new_button = ctk.CTkButton(
            self,
            text="➕ Новая система",
            width=170,
            command=self.new_clicked
        )

        self.new_button.grid(
            row=0,
            column=0,
            padx=(15, 8),
            pady=10
        )

        self.report_button = ctk.CTkButton(
            self,
            text="Отчет",
            width=110,
            fg_color="#3A3D45",
            hover_color="#4A4E57",
            command=self.report_clicked
        )

        self.report_button.grid(
            row=0,
            column=1,
            padx=(0, 15),
            pady=10
        )

        self.search = ctk.CTkEntry(
            self,
            placeholder_text="Поиск системы..."
        )

        self.search.grid(
            row=0,
            column=2,
            sticky="ew",
            padx=(0, 15)
        )

        self.search.bind(
            "<KeyRelease>",
            self.search_changed
        )

    def new_clicked(self):

        if self.on_new:
            self.on_new()

    def report_clicked(self):

        if self.on_report:
            self.on_report()

    def search_changed(self, event):

        if self.on_search:
            self.on_search(self.search.get())