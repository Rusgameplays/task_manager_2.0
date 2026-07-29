import tkinter as tk
import customtkinter as ctk

from ui.theme import *


class ActionBar(ctk.CTkFrame):

    def __init__(
            self,
            master,
            on_open_folder=None,
            on_delete=None,
            on_copy_scan=None,
            on_load_docx=None,
            on_copy_ips=None
    ):
        super().__init__(
            master,
            fg_color="transparent"
        )

        self.on_open_folder = on_open_folder
        self.on_delete = on_delete
        self.on_copy_scan = on_copy_scan
        self.on_load_docx = on_load_docx
        self.on_copy_ips = on_copy_ips

        self.build_ui()

        self.ip_menu = tk.Menu(
            self,
            tearoff=False
        )

        self.ip_menu.add_command(
            label="По строкам",
            command=lambda: self.copy_ips("lines")
        )

        self.ip_menu.add_command(
            label="Через запятую",
            command=lambda: self.copy_ips("csv")
        )

    def build_ui(self):

        BUTTON_WIDTH = 42
        BUTTON_HEIGHT = 34

        self.scan_button = ctk.CTkButton(
            self,
            text="ForMail",
            width=BUTTON_WIDTH,
            height=BUTTON_HEIGHT,
            corner_radius=8,
            command=self.copy_scan
        )

        self.scan_button.grid(
            row=0,
            column=0,
            padx=4
        )

        self.folder_button = ctk.CTkButton(
            self,
            text="Folder",
            width=BUTTON_WIDTH,
            height=BUTTON_HEIGHT,
            corner_radius=8,
            command=self.open_folder
        )

        self.folder_button.grid(
            row=0,
            column=1,
            padx=4
        )

        self.docx_button = ctk.CTkButton(
            self,
            text="DOCX",
            width=BUTTON_WIDTH,
            height=BUTTON_HEIGHT,
            corner_radius=8,
            command=self.load_docx
        )

        self.docx_button.grid(
            row=0,
            column=2,
            padx=4
        )

        self.copy_ips_button = ctk.CTkButton(
            self,
            text="IP",
            width=BUTTON_WIDTH,
            height=BUTTON_HEIGHT,
            corner_radius=8,
            command=self.show_ip_menu
        )

        self.copy_ips_button.grid(
            row=0,
            column=3,
            padx=(4, 12)
        )

        self.delete_button = ctk.CTkButton(
            self,
            text="Del",
            width=BUTTON_WIDTH,
            height=BUTTON_HEIGHT,
            corner_radius=8,
            fg_color="#C0392B",
            hover_color="#A93226",
            command=self.delete_task
        )

        self.delete_button.grid(
            row=0,
            column=4,
            padx=4
        )

    def open_folder(self):

        if self.on_open_folder:
            self.on_open_folder()

    def delete_task(self):

        if self.on_delete:
            self.on_delete()

    def copy_scan(self):

        if self.on_copy_scan:
            self.on_copy_scan()

    def load_docx(self):

        if self.on_load_docx:
            self.on_load_docx()

    def show_ip_menu(self):

        x = self.copy_ips_button.winfo_rootx()

        y = (
            self.copy_ips_button.winfo_rooty()
            + self.copy_ips_button.winfo_height()
        )

        self.ip_menu.tk_popup(x, y)

    def copy_ips(self, mode):

        if self.on_copy_ips:
            self.on_copy_ips(mode)