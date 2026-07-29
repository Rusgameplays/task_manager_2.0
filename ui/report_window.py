import customtkinter as ctk

from datetime import datetime, timedelta

from ui.theme import CARD, BACKGROUND, BORDER


class ReportWindow(ctk.CTkToplevel):

    def __init__(self, master, repository):

        super().__init__(master)

        self.repository = repository
        self.report = self.repository.load()

        self.title("Отчет")
        self.geometry("700x500")
        self.resizable(False, False)

        self.configure(fg_color=BACKGROUND)

        self.grab_set()

        self.build_ui()

    # ==========================================================

    def build_ui(self):

        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=1)

        self.title_label = ctk.CTkLabel(
            self,
            text="📊 Отчет",
            font=("Segoe UI", 22, "bold")
        )

        self.title_label.grid(
            row=0,
            column=0,
            sticky="w",
            padx=20,
            pady=(20, 15)
        )

        self.table = ctk.CTkFrame(
            self,
            fg_color=CARD,
            corner_radius=10,
            border_width=1,
            border_color=BORDER
        )

        self.table.grid(
            row=1,
            column=0,
            padx=20,
            pady=(0, 15),
            sticky="nsew"
        )

        self.table.grid_columnconfigure((0, 1, 2), weight=1)

        headers = [
            "Неделя",
            "Сканы",
            "Закрыто"
        ]

        for i, text in enumerate(headers):

            ctk.CTkLabel(
                self.table,
                text=text,
                font=("Segoe UI", 13, "bold")
            ).grid(
                row=0,
                column=i,
                padx=10,
                pady=10,
                sticky="ew"
            )

        self.add_button = ctk.CTkButton(
            self,
            text="➕ Добавить неделю",
            command=self.add_week
        )

        self.add_button.grid(
            row=2,
            column=0,
            pady=(0, 20)
        )

        self.refresh()

    # ==========================================================

    def refresh(self):

        for widget in self.table.grid_slaves():

            if widget.grid_info()["row"] != 0:
                widget.destroy()

        for row, week in enumerate(self.report, start=1):

            ctk.CTkLabel(
                self.table,
                text=week["week"]
            ).grid(
                row=row,
                column=0,
                padx=10,
                pady=6,
                sticky="w"
            )

            self.create_counter(
                row,
                1,
                "scans",
                week["scans"]
            )

            self.create_counter(
                row,
                2,
                "closed",
                week["closed"]
            )

    # ==========================================================

    def create_counter(
            self,
            row,
            column,
            field,
            value
    ):

        frame = ctk.CTkFrame(
            self.table,
            fg_color="transparent"
        )

        frame.grid(
            row=row,
            column=column,
            pady=4
        )

        ctk.CTkButton(
            frame,
            text="−",
            width=28,
            height=28,
            command=lambda:
            self.change_value(
                row - 1,
                field,
                -1
            )
        ).pack(side="left")

        ctk.CTkLabel(
            frame,
            text=str(value),
            width=40,
            font=("Segoe UI", 13, "bold")
        ).pack(side="left")

        ctk.CTkButton(
            frame,
            text="+",
            width=28,
            height=28,
            command=lambda:
            self.change_value(
                row - 1,
                field,
                1
            )
        ).pack(side="left")

    # ==========================================================

    def change_value(
            self,
            index,
            field,
            delta
    ):

        self.report[index][field] += delta

        if self.report[index][field] < 0:
            self.report[index][field] = 0

        self.repository.save(self.report)

        self.refresh()

    # ==========================================================

    def get_week_range(self, offset=0):

        today = datetime.now()

        friday = today - timedelta(
            days=(today.weekday() - 4) % 7
        )

        friday += timedelta(days=offset * 7)

        thursday = friday + timedelta(days=6)

        return f"{friday:%d.%m} - {thursday:%d.%m}"

    # ==========================================================

    def add_week(self):

        current = self.get_week_range(0)
        next_week = self.get_week_range(1)

        weeks = {
            row["week"]
            for row in self.report
        }

        if current not in weeks:

            week = current

        elif next_week not in weeks:

            week = next_week

        else:
            return

        self.report.append(
            {
                "week": week,
                "scans": 0,
                "closed": 0
            }
        )

        self.report.sort(
            key=lambda x: datetime.strptime(
                x["week"].split(" - ")[0],
                "%d.%m"
            )
        )

        self.repository.save(self.report)

        self.refresh()