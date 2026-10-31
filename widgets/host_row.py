
import tkinter as tk
import tkinter.font as tkfont
import customtkinter as ctk

from ui.theme import *


COLUMN_WEIGHTS = [
    1,  # OS
    1,  # DB
    2,  # Instances
    1,  # Window
    2,  # IP
    1,  # Segment
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
        self.labels = []
        self._last_widths = {}

        self.build_ui()

        # Пересчитываем перенос при изменении ширины таблицы
        self.bind(
            "<Configure>",
            self._on_resize
        )

        self.after_idle(self.update_wrapping)

    def build_ui(self):
        columns = list(self.values.values())

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

            font_tuple = (
                ("Consolas", 12)
                if i == 4
                else ("Segoe UI", 12)
            )

            label_font = tkfont.Font(
                root=self,
                font=font_tuple
            )

            label = ctk.CTkLabel(
                self,
                text=str(value or ""),
                anchor="w",
                justify="left",
                font=font_tuple,
                height=0
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

            self.labels.append({
                "widget": label,
                "font": label_font,
                "text": str(value or ""),
                "index": i,
            })

    def _on_resize(self, event):
        if event.width > 1:
            self.after_idle(self.update_wrapping)

    def _wrap_text(self, text, font, max_width):
        """Переносит текст по ширине, включая длинные слова и IP."""
        result = []

        for paragraph in text.split("\n"):
            if not paragraph:
                result.append("")
                continue

            current = ""

            for word in paragraph.split():
                candidate = (
                    f"{current} {word}".strip()
                )

                if font.measure(candidate) <= max_width:
                    current = candidate
                    continue

                if current:
                    result.append(current)
                    current = ""

                for char in word:
                    candidate = current + char

                    if (
                        current
                        and font.measure(candidate) > max_width
                    ):
                        result.append(current)
                        current = char
                    else:
                        current = candidate

            if current:
                result.append(current)

        return result or [""]


    def update_wrapping(self):
        if not self.winfo_exists():
            return


        no_wrap_columns = {0, 5}

        for item in self.labels:
            label = item["widget"]
            font = item["font"]
            original_text = item["text"]
            index = item["index"]

            width = label.winfo_width()

            if width <= 1:
                continue

            if self._last_widths.get(index) == width:
                continue

            self._last_widths[index] = width

            if index in no_wrap_columns:

                label.configure(
                    text=original_text,
                    height=font.metrics("linespace") + 4
                )
                continue

            available_width = max(30, width - 12)

            lines = self._wrap_text(
                original_text,
                font,
                available_width
            )

            line_height = font.metrics("linespace") + 3
            required_height = max(
                20,
                len(lines) * line_height + 4
            )

            label.configure(
                text="\n".join(lines),
                height=required_height
            )


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
