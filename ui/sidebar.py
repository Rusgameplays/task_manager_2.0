import customtkinter as ctk
from ui.theme import *
from ui.system_card import SystemCard


class Sidebar(ctk.CTkFrame):

    def __init__(
            self,
            master,
            on_task_selected=None,
            on_filter_changed=None,
            on_bulk_delete=None
    ):
        super().__init__(
            master,
            width=350,
            corner_radius=0,
            fg_color=SIDEBAR
        )

        self.selected_card = None
        self.cards = []
        self.card_by_task = {}
        self.on_filter_changed = on_filter_changed
        self.on_task_selected = on_task_selected
        self.on_bulk_delete = on_bulk_delete
        self.build_ui()

    def build_ui(self):

        # Заголовок
        self.title = ctk.CTkLabel(
            self,
            text="Task Manager",
            font=FONT_TITLE
        )

        self.title.grid(
            row=0,
            column=0,
            padx=20,
            pady=(20, 15),
            sticky="w"
        )

        self.stats = ctk.CTkFrame(
            self,
            fg_color="transparent"
        )

        self.stats.grid(
            row=1,
            column=0,
            padx=15,
            pady=(0, 10),
            sticky="ew"
        )

        for i in range(4):
            self.stats.grid_columnconfigure(i, weight=1)

        self.total_label = self.make_stat(0, "0", "Все")
        self.work_label = self.make_stat(1, "0", "Раб.")
        self.wait_label = self.make_stat(2, "0", "Ожид.")
        self.close_label = self.make_stat(3, "0", "Закр.")

        self.filter = ctk.CTkSegmentedButton(
            self,
            values=[
                "Все",
                "В работе",
                "Приостановлено",
                "Закрыто"
            ],
            command=self.filter_changed
        )

        self.filter.set("В работе")

        self.after(
            100,
            lambda: self.filter_changed("В работе")
        )

        self.filter.grid(
            row=2,
            column=0,
            padx=15,
            pady=(0, 10),
            sticky="ew"
        )

        self.bulk_delete_button = ctk.CTkButton(
            self,
            text="Массовое удаление",
            fg_color="#C0392B",
            hover_color="#922B21",
            command=self.open_bulk_delete
        )

        self.bulk_delete_button.grid(
            row=3,
            column=0,
            padx=15,
            pady=(0, 10),
            sticky="ew"
        )

        # Скролл
        self.scroll = ctk.CTkScrollableFrame(
            self,
            fg_color="transparent"
        )

        self.scroll.grid(
            row=4,
            column=0,
            padx=10,
            pady=0,
            sticky="nsew"
        )

        self.grid_rowconfigure(4, weight=1)
        self.grid_columnconfigure(0, weight=1)

    def clear(self):
        for card in self.cards:
            card.destroy()

        self.cards.clear()
        self.card_by_task.clear()
        self.selected_card = None

    def card_clicked(self, task):


        for card in self.cards:
            card.deselect()


        for card in self.cards:

            if card.task == task:
                card.select()

                self.selected_card = card

                break

        if self.on_task_selected:
            self.on_task_selected(card.task)

    def load_tasks(self, tasks):
        visible_ids = set()

        for index, task in enumerate(tasks):
            task_id = id(task)
            visible_ids.add(task_id)

            card = self.card_by_task.get(task_id)

            # Создаём карточку только при первом появлении задачи
            if card is None:
                card = SystemCard(
                    self.scroll,
                    task,
                    command=self.card_clicked
                )

                self.card_by_task[task_id] = card
                self.cards.append(card)

            # Обновляем данные карточки
            card.task = task
            card.update_from_task()

            # Показываем карточку и задаём её позицию
            card.grid(
                row=index,
                column=0,
                sticky="ew",
                padx=5,
                pady=4
            )

        # Скрываем карточки, которые не подходят под фильтр
        for task_id, card in self.card_by_task.items():
            if task_id not in visible_ids:
                card.grid_remove()

        self.scroll.grid_columnconfigure(0, weight=1)


    def update_card(self, task):

        for card in self.cards:

            if card.task == task:
                card.update_status()
                break

    def filter_changed(self, value):

        if self.on_filter_changed:
            self.on_filter_changed(value)

    def make_stat(self, column, value, title):

        frame = ctk.CTkFrame(
            self.stats,
            corner_radius=8
        )

        frame.grid(
            row=0,
            column=column,
            padx=3,
            sticky="ew"
        )

        number = ctk.CTkLabel(
            frame,
            text=value,
            font=("Segoe UI", 18, "bold")
        )

        number.pack(pady=(6, 0))

        label = ctk.CTkLabel(
            frame,
            text=title,
            font=("Segoe UI", 10),
            text_color=TEXT_SECONDARY
        )

        label.pack(pady=(0, 6))

        return number


    def update_total_count(self, tasks):
        self.total_label.configure(text=str(len(tasks)))

    def update_status_counts(self, tasks):
        work = sum(t.status == "В работе" for t in tasks)
        wait = sum(t.status == "Приостановлено" for t in tasks)
        closed = sum(t.status == "Закрыто" for t in tasks)

        self.work_label.configure(text=str(work))
        self.wait_label.configure(text=str(wait))
        self.close_label.configure(text=str(closed))

    def update_stats(self, tasks):
        self.update_total_count(tasks)
        self.update_status_counts(tasks)


    def remove_task(self, task):
        task_id = id(task)
        card = self.card_by_task.pop(task_id, None)

        if card is None:
            return

        if card == self.selected_card:
            self.selected_card = None

        if card in self.cards:
            self.cards.remove(card)

        card.destroy()

    def open_bulk_delete(self):
        if self.on_bulk_delete:
            self.on_bulk_delete()