import customtkinter as ctk

from ui.theme import *


class LabeledField(ctk.CTkFrame):

    def __init__(
            self,
            master,
            title,
            field_type="entry",
            values=None,
            on_change=None,
            copyable=False
    ):

        super().__init__(
            master,
            fg_color="transparent"
        )

        self.on_change = on_change
        self.field_type = field_type
        self.copyable = copyable

        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=0)

        self.label = ctk.CTkLabel(
            self,
            text=title,
            anchor="w",
            font=FONT_SMALL,
            text_color=TEXT_SECONDARY
        )

        self.label.grid(
            row=0,
            column=0,
            columnspan=2,
            sticky="w",
            pady=(0, 4)
        )

        if field_type == "entry":

            self.widget = ctk.CTkEntry(self)

            self.widget.bind(
                "<FocusOut>",
                self.value_changed
            )

        elif field_type == "combo":

            self.widget = ctk.CTkComboBox(
                self,
                values=values or [],
                command=self.combo_changed
            )

        elif field_type == "textbox":

            self.widget = ctk.CTkTextbox(
                self,
                height=120
            )

        else:

            raise ValueError(
                f"Unknown field type: {field_type}"
            )

        self.widget.grid(
            row=1,
            column=0,
            sticky="ew"
        )

        if self.copyable:

            self.copy_button = ctk.CTkButton(
                self,
                text="📋",
                width=28,
                height=28,
                fg_color="transparent",
                hover_color="#3A3A3A",
                command=self.copy_value
            )

            self.copy_button.grid(
                row=1,
                column=1,
                padx=(6, 0)
            )

    def get(self):

        if self.field_type == "textbox":
            return self.widget.get("1.0", "end").strip()

        return self.widget.get()

    def set(self, value):

        value = value or ""

        if self.field_type == "textbox":

            self.widget.delete("1.0", "end")
            self.widget.insert("1.0", value)

        elif self.field_type == "combo":

            self.widget.set(value)

        else:

            self.widget.delete(0, "end")
            self.widget.insert(0, value)

    def copy_value(self):

        value = self.get()

        if not value:
            return

        self.clipboard_clear()
        self.clipboard_append(value)
        self.update()

    def value_changed(self, event):

        if self.on_change:
            self.on_change(self.get())

    def combo_changed(self, value):

        if self.on_change:
            self.on_change(value)