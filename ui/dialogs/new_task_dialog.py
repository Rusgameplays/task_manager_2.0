import customtkinter as ctk


class NewTaskDialog(ctk.CTkToplevel):

    def __init__(self, master, on_create=None):
        super().__init__(master)

        self.on_create = on_create

        self.title("Новая система")
        self.geometry("420x260")
        self.resizable(False, False)

        self.grab_set()          # делает окно модальным
        self.focus_force()

        self.build_ui()

    def build_ui(self):
        self.grid_columnconfigure(1, weight=1)

        ctk.CTkLabel(self, text="RF").grid(
            row=0, column=0, padx=20, pady=(20, 10), sticky="w"
        )

        self.rf = ctk.CTkEntry(self)

        self.rf.grid(
            row=0,
            column=1,
            padx=20,
            pady=(20, 10),
            sticky="ew"
        )

        ctk.CTkLabel(self, text="SD").grid(
            row=1,
            column=0,
            padx=20,
            pady=10,
            sticky="w"
        )

        self.sd = ctk.CTkEntry(self)

        self.sd.grid(
            row=1,
            column=1,
            padx=20,
            pady=10,
            sticky="ew"
        )

        ctk.CTkLabel(self, text="Краткое название").grid(
            row=2,
            column=0,
            padx=20,
            pady=10,
            sticky="w"
        )

        self.name = ctk.CTkEntry(self)

        self.name.grid(
            row=2,
            column=1,
            padx=20,
            pady=10,
            sticky="ew"
        )

        self.create_button = ctk.CTkButton(
            self,
            text="Создать",
            command=self.create
        )

        self.create_button.grid(
            row=3,
            column=1,
            padx=20,
            pady=25,
            sticky="e"
        )

    def create(self):
        if self.on_create:
            self.on_create(

                self.rf.get(),

                self.sd.get(),

                self.name.get()

            )

        self.destroy()