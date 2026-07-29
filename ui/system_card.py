import customtkinter as ctk

from models.task import Task
from ui.theme import *


class SystemCard(ctk.CTkFrame):



    def __init__(self, master, task: Task, command=None):
        super().__init__(
            master,
            fg_color=CARD,
            corner_radius=10,
            border_width=1,
            border_color=BORDER,
            cursor="hand2"
        )



        self.task = task
        self.command = command
        self.selected = False

        self.grid_columnconfigure(1, weight=1)



        self.build_ui()
        self.bind_events()

    def build_ui(self):

        status_color = STATUS_COLORS.get(
            self.task.status,
            DEFAULT_STATUS_COLOR
        )

        self.indicator = ctk.CTkFrame(
            self,
            width=10,
            height=10,
            corner_radius=5,
            fg_color=status_color
        )

        self.indicator.grid(
            row=0,
            column=0,
            rowspan=3,
            padx=(15, 10),
            pady=20
        )

        self.rf_label = ctk.CTkLabel(
            self,
            text=self.task.rf,
            font=("Segoe UI", 13, "bold"),
            anchor="w"
        )

        self.rf_label.grid(
            row=0,
            column=1,
            sticky="w",
            pady=(10, 0)
        )

        self.name_label = ctk.CTkLabel(
            self,
            text=self.task.name,
            font=FONT_SMALL,
            text_color=TEXT_SECONDARY,
            anchor="w"
        )

        self.name_label.grid(
            row=1,
            column=1,
            sticky="w",
            pady=(2, 2)
        )

        self.type_badge = ctk.CTkLabel(
            self,
            text=self.task.type,
            fg_color=self.get_type_color(),
            text_color="white",
            corner_radius=6,
            padx=8,
            height=20,
            font=("Segoe UI", 10, "bold")
        )

        self.type_badge.grid(
            row=2,
            column=1,
            sticky="w",
            pady=(2, 10)
        )

    def bind_events(self):

        widgets = (
            self,
            self.indicator,
            self.rf_label,
            self.name_label,
            self.type_badge
        )

        for widget in widgets:
            widget.bind("<Button-1>", self.on_click)
            widget.bind("<Enter>", self.on_enter)
            widget.bind("<Leave>", self.on_leave)

    def on_click(self, event):

        if self.command:
            self.command(self.task)

    def on_enter(self, event):

        if not self.selected:
            self.configure(fg_color="#36393F")

    def on_leave(self, event):

        if not self.selected:
            self.configure(fg_color=CARD)

    def select(self):

        self.selected = True

        self.configure(
            fg_color=BLUE
        )

    def deselect(self):

        self.selected = False

        self.configure(
            fg_color=CARD
        )

    def update_status(self):

        color = STATUS_COLORS.get(
            self.task.status,
            DEFAULT_STATUS_COLOR
        )

        self.indicator.configure(
            fg_color=color
        )

    def get_type_color(self):

        colors = {
            "ПСИ": "#2E86DE",
            "Подключение": "#27AE60",
            "Актуализация": "#F39C12",
            "Другое": "#6C757D"
        }

        return colors.get(
            self.task.type,
            "#6C757D"
        )