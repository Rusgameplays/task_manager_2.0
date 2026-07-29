import customtkinter as ctk


class ConfirmDialog(ctk.CTkToplevel):

    def __init__(self, master, title, message, on_confirm=None):
        super().__init__(master)

        self.on_confirm = on_confirm

        self.title(title)
        self.geometry("420x300")
        self.resizable(False, False)

        self.grab_set()
        self.focus_force()

        self.build_ui(message)

    def build_ui(self, message):

        self.grid_columnconfigure((0, 1), weight=1)

        self.label = ctk.CTkLabel(
            self,
            text=message,
            justify="left",
            wraplength=360,
            font=("Segoe UI", 14)
        )

        self.label.grid(
            row=0,
            column=0,
            columnspan=2,
            padx=20,
            pady=(25, 30),
            sticky="w"
        )

        self.cancel = ctk.CTkButton(
            self,
            text="Отмена",
            command=self.destroy
        )

        self.cancel.grid(
            row=1,
            column=0,
            padx=(20, 10),
            pady=20,
            sticky="ew"
        )

        self.delete = ctk.CTkButton(
            self,
            text="Удалить",
            fg_color="#C0392B",
            hover_color="#A93226",
            command=self.confirm
        )

        self.delete.grid(
            row=1,
            column=1,
            padx=(10, 20),
            pady=20,
            sticky="ew"
        )

    def confirm(self):

        if self.on_confirm:
            self.on_confirm()

        self.destroy()