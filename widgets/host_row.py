import tkinter as tk

import customtkinter as ctk

from ui.theme import *

COLUMN_WEIGHTS = [
    1,  # OS
    1,  # DB
    2,  # Instance
    1,  # Window
    2,  # IP
    1   # Segment
]


class HostRow(ctk.CTkFrame):

    HIGHLIGHT_COLOR = "#4A5568"

    def __init__(self, master, values, index):

        self.normal_color = CARD if index % 2 == 0 else "#34373D"

        super().__init__(
            master,
            fg_color=self.normal_color,
            corner_radius=6
        )

        self.values = values

        self.build_ui()

    def build_ui(self):

        columns = list(self.values.values())

        # ---------- Меню ----------

        self.menu = tk.Menu(
            self,
            tearoff=False
        )

        self.menu.add_command(
            label="📋 Копировать IP",
            command=self.copy_ip
        )

        self.menu.add_command(
            label="📋 Копировать Instance",
            command=self.copy_instance
        )

        # ---------- Ячейки ----------

        for i, value in enumerate(columns):
            weight = (
                COLUMN_WEIGHTS[i]
                if i < len(COLUMN_WEIGHTS)
                else 1
            )

            self.grid_columnconfigure(
                i,
                weight=weight,
                uniform="hosts"
            )

            # IP отображаем моноширинным шрифтом
            font = (
                ("Consolas", 12)
                if i == 4
                else ("Segoe UI", 12)
            )

            label = ctk.CTkLabel(
                self,
                text=value,
                anchor="w",
                font=font
            )

            label.grid(
                row=0,
                column=i,
                padx=(10, 8),
                pady=8,
                sticky="ew"
            )

            label.bind("<Button-2>", self.popup)
            label.bind("<Button-3>", self.popup)

    def highlight(self):

        self.configure(
            fg_color=self.HIGHLIGHT_COLOR
        )

        self.after(
            800,
            lambda: self.configure(
                fg_color=self.normal_color
            )
        )

    def popup(self, event):

        self.highlight()

        self.menu.tk_popup(
            event.x_root,
            event.y_root
        )

    def copy_ip(self):

        ip = self.values.get("IP", "")

        self.clipboard_clear()
        self.clipboard_append(ip)
        self.update()

    def copy_instance(self):

        instance = self.values.get("Instances", "")

        self.clipboard_clear()
        self.clipboard_append(instance)
        self.update()