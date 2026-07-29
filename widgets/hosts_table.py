import customtkinter as ctk
from collections import Counter

from ui.theme import CARD, BORDER, TEXT_SECONDARY
from widgets.host_row import HostRow

COLUMN_WEIGHTS = [
    1,  # OS
    1,  # DB
    2,  # Instance
    1,  # Window
    2,  # IP
    1   # Segment
]


class HostsTable(ctk.CTkFrame):

    def __init__(self, master):
        super().__init__(master, fg_color="transparent")

        self.all_hosts = []
        self.filtered_hosts = []

        self.build_ui()

    def build_ui(self):

        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=1)

        # ======================================================
        # Верхняя панель
        # ======================================================

        self.top = ctk.CTkFrame(
            self,
            fg_color="transparent"
        )

        self.top.grid(
            row=0,
            column=0,
            sticky="ew",
            pady=(0, 10)
        )

        self.top.grid_columnconfigure(1, weight=1)

        self.title = ctk.CTkLabel(
            self.top,
            text="Хосты",
            font=("Segoe UI", 18, "bold")
        )

        self.title.grid(
            row=0,
            column=0,
            sticky="w"
        )

        self.segment_filter = ctk.CTkComboBox(
            self.top,
            values=["Все"],
            width=170,
            command=self.segment_changed
        )

        self.segment_filter.grid(
            row=0,
            column=2,
            sticky="e"
        )

        self.stats_label = ctk.CTkLabel(
            self.top,
            text="",
            font=("Segoe UI", 12),
            text_color=TEXT_SECONDARY
        )

        self.stats_label.grid(
            row=1,
            column=0,
            columnspan=3,
            sticky="w",
            pady=(8, 0)
        )

        # ======================================================
        # Карточка таблицы
        # ======================================================

        self.table_frame = ctk.CTkFrame(
            self,
            fg_color=CARD,
            corner_radius=10,
            border_width=1,
            border_color=BORDER
        )

        self.table_frame.grid(
            row=1,
            column=0,
            sticky="nsew"
        )

        self.table_frame.grid_columnconfigure(0, weight=1)
        self.table_frame.grid_rowconfigure(2, weight=1)

        # ======================================================
        # Header
        # ======================================================

        self.header = ctk.CTkFrame(
            self.table_frame,
            fg_color="#36393F",
            corner_radius=8
        )

        self.header.grid(
            row=0,
            column=0,
            sticky="ew",
            padx=10,
            pady=(10, 0)
        )

        # ======================================================
        # Separator
        # ======================================================

        self.separator = ctk.CTkFrame(
            self.table_frame,
            height=1,
            fg_color=BORDER
        )

        self.separator.grid(
            row=1,
            column=0,
            sticky="ew",
            padx=10
        )

        # ======================================================
        # Body
        # ======================================================

        self.body = ctk.CTkScrollableFrame(
            self.table_frame,
            fg_color="transparent"
        )

        self.body.grid(
            row=2,
            column=0,
            sticky="nsew",
            padx=10,
            pady=(6, 10)
        )

    def load(self, rows):

        self.all_hosts = rows

        segments = sorted({
            h.get("Segment", "")
            for h in rows
            if h.get("Segment")
        })

        self.segment_filter.configure(
            values=["Все"] + segments
        )

        self.segment_filter.set("Все")

        self.filtered_hosts = rows

        self.refresh()

    # ==========================================================

    def refresh(self):

        for widget in self.header.winfo_children():
            widget.destroy()

        for widget in self.body.winfo_children():
            widget.destroy()

        if not self.filtered_hosts:
            self.update_stats([])
            return

        columns = list(self.filtered_hosts[0].keys())

        for i, column in enumerate(columns):
            weight = (
                COLUMN_WEIGHTS[i]
                if i < len(COLUMN_WEIGHTS)
                else 1
            )

            self.header.grid_columnconfigure(
                i,
                weight=weight,
                uniform="hosts"
            )

            ctk.CTkLabel(
                self.header,
                text=column,
                font=("Segoe UI", 13, "bold")
            ).grid(
                row=0,
                column=i,
                padx=8,
                sticky="ew"
            )

        for index, row in enumerate(self.filtered_hosts):

            HostRow(
                self.body,
                row,
                index
            ).pack(
                fill="x",
                padx=2,
                pady=2
            )

        self.update_stats(self.filtered_hosts)

    # ==========================================================

    def segment_changed(self, value):

        if value == "Все":
            self.filtered_hosts = self.all_hosts
        else:
            self.filtered_hosts = [
                host
                for host in self.all_hosts
                if host.get("Segment") == value
            ]

        self.refresh()

    # ==========================================================

    def update_stats(self, hosts):

        ips = [
            h["IP"]
            for h in hosts
            if h.get("IP")
        ]

        segments = {
            h["Segment"]
            for h in hosts
            if h.get("Segment")
        }

        duplicates = sum(
            c - 1
            for c in Counter(ips).values()
            if c > 1
        )

        self.stats_label.configure(
            text=(
                f"IP: {len(ips)}    •    "
                f"Сегментов: {len(segments)}    •    "
                f"Дубликатов: {duplicates}"
            )
        )

    # ==========================================================

    def get_visible_hosts(self):
        return self.filtered_hosts

    def get_visible_ips(self):
        return [
            host["IP"]
            for host in self.filtered_hosts
            if host.get("IP")
        ]