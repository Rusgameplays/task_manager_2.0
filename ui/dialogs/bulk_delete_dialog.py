import customtkinter as ctk
from tkinter import messagebox


class BulkDeleteDialog(ctk.CTkToplevel):
    def __init__(self, master, tasks, on_delete):
        super().__init__(master)

        self.title("Массовое удаление заявок")
        self.geometry("760x650")
        self.minsize(600, 450)

        self.tasks = list(tasks)
        self.on_delete = on_delete
        self.checkboxes = []

        self.transient(master)
        self.grab_set()

        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=1)

        ctk.CTkLabel(
            self,
            text="Выберите заявки для удаления",
            font=("Segoe UI", 20, "bold")
        ).grid(
            row=0, column=0,
            padx=20, pady=(20, 10),
            sticky="w"
        )

        self.scroll = ctk.CTkScrollableFrame(self)
        self.scroll.grid(
            row=1, column=0,
            padx=15, pady=5,
            sticky="nsew"
        )
        self.scroll.grid_columnconfigure(0, weight=1)

        for task in self.tasks:
            var = ctk.BooleanVar(value=False)

            checkbox = ctk.CTkCheckBox(
                self.scroll,
                text=f"{task.rf} — {task.sd} — {task.name}",
                variable=var,
                command=self.update_count
            )
            checkbox.grid(
                sticky="ew",
                padx=10, pady=8
            )

            self.checkboxes.append((task, var))

        self.count_label = ctk.CTkLabel(
            self,
            text="Выбрано: 0"
        )
        self.count_label.grid(
            row=2, column=0,
            padx=20, pady=5,
            sticky="w"
        )

        buttons = ctk.CTkFrame(self, fg_color="transparent")
        buttons.grid(
            row=3, column=0,
            padx=15, pady=15,
            sticky="ew"
        )

        buttons.grid_columnconfigure(0, weight=1)

        ctk.CTkButton(
            buttons,
            text="Выбрать все",
            command=self.toggle_all
        ).grid(row=0, column=0, padx=5, sticky="w")

        ctk.CTkButton(
            buttons,
            text="Удалить выбранные",
            fg_color="#C0392B",
            hover_color="#922B21",
            command=self.delete_selected
        ).grid(row=0, column=1, padx=5)

        ctk.CTkButton(
            buttons,
            text="Отмена",
            fg_color="gray",
            command=self.destroy
        ).grid(row=0, column=2, padx=5)

    def update_count(self):
        count = sum(
            var.get() for _, var in self.checkboxes
        )
        self.count_label.configure(
            text=f"Выбрано: {count}"
        )

    def toggle_all(self):
        select_all = not all(
            var.get() for _, var in self.checkboxes
        )

        for _, var in self.checkboxes:
            var.set(select_all)

        self.update_count()

    def delete_selected(self):
        selected = [
            task
            for task, var in self.checkboxes
            if var.get()
        ]

        if not selected:
            messagebox.showwarning(
                "Нет выбора",
                "Отметьте хотя бы одну заявку.",
                parent=self
            )
            return

        confirmed = messagebox.askyesno(
            "Подтверждение удаления",
            f"Удалить выбранные заявки: {len(selected)}?\n\n"
            "Это действие нельзя отменить.",
            parent=self
        )

        if confirmed:
            self.on_delete(selected)
            self.destroy()