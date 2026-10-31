import customtkinter as ctk
from ui.comment_box import CommentBox
from ui.info_row import InfoRow
from widgets.hosts_table import HostsTable
from ui.theme import *
from widgets.labeled_field import LabeledField
from widgets.status_card import StatusCard
from widgets.action_bar import ActionBar
from tkinter import simpledialog


class DetailsPanel(ctk.CTkFrame):

    def __init__(
            self,
            master,
            on_task_changed=None,
            on_open_folder=None,
            on_delete_task=None,
            on_copy_scan=None,
            on_load_docx=None,
            on_copy_ips=None
    ):

        super().__init__(
            master,
            fg_color=BACKGROUND
        )
        self.on_copy_ips = on_copy_ips
        self.on_load_docx = on_load_docx
        self.on_copy_scan = on_copy_scan
        self.on_delete_task = on_delete_task
        self.on_open_folder = on_open_folder
        self.current_task = None
        self.on_task_changed = on_task_changed

        self.build_ui()

    def build_ui(self):
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=1)
        self.card = ctk.CTkFrame(
            self,
            fg_color=CARD,
            corner_radius=15
        )

        self.card.grid(
            row=0,
            column=0,
            padx=20,
            pady=20,
            sticky="nsew"
        )

        self.card.grid_columnconfigure(1, weight=1)

        self.build_header()
        self.build_actions()
        self.build_layout()

        self.build_dashboard()
        self.build_info()
        self.build_comment()
        self.build_hosts()

    def show_task(self, task, hosts=None):
        self.current_task = task
        self.rf_label.configure(text=task.rf)
        self.name_label.configure(text=task.name)
        self.full_name_label.configure(
            text=task.full_name
        )


        self.type_card.set(task.type)

        self.pentest_card.set(task.pentest_audit)

        self.compliance_card.set(task.compliance)


        self.mp8_field.set(task.mp8)
        self.sd_field.set(task.sd)
        self.secure_field.set(task.secure)
        self.status_field.set(task.status)
        self.comment.set(task.comment)

        self.hosts.load(hosts or [])

    def build_header(self):

        # RF

        self.rf_label = ctk.CTkLabel(
            self.card,
            text="Выберите систему",
            font=("Segoe UI", 28, "bold")
        )

        self.rf_label.grid(
            row=0,
            column=0,
            padx=25,
            pady=(20, 4),
            sticky="w"
        )

        self.copy_rf = ctk.CTkButton(
            self.card,
            text="📋",
            width=28,
            height=28,
            fg_color="transparent",
            hover_color="#3A3A3A",
            command=lambda: self.copy_to_clipboard(
                self.current_task.rf
            )
        )

        self.copy_rf.grid(
            row=0,
            column=1,
            padx=(0, 25),
            pady=(20, 5),
            sticky="w"
        )

        # Краткое название

        self.name_label = ctk.CTkLabel(
            self.card,
            text="",
            font=("Segoe UI", 18, "bold"),
            text_color=TEXT_SECONDARY
        )

        self.name_label.grid(
            row=1,
            column=0,
            padx=25,
            pady=(0, 6),
            sticky="w"
        )

        # Контейнер строки полного названия

        self.full_name_frame = ctk.CTkFrame(
            self.card,
            fg_color="transparent"
        )

        self.full_name_frame.grid(
            row=2,
            column=0,
            padx=25,
            pady=(0, 12),
            sticky="w"
        )

        # Полное название

        self.full_name_label = ctk.CTkLabel(
            self.full_name_frame,
            text="",
            font=("Segoe UI", 20),
            text_color=TEXT_SECONDARY,
            anchor="w",
            justify="left",
            wraplength=700
        )

        self.full_name_label.grid(
            row=0,
            column=0,
            sticky="w"
        )

        # Редактировать

        self.edit_full_name = ctk.CTkButton(
            self.full_name_frame,
            text="✏️",
            width=28,
            height=28,
            fg_color="transparent",
            hover_color="#3A3A3A",
            command=self.edit_full_name
        )

        self.edit_full_name.grid(
            row=0,
            column=1,
            padx=(8, 0)
        )

        # Копировать

        self.copy_full_name = ctk.CTkButton(
            self.full_name_frame,
            text="📋",
            width=28,
            height=28,
            fg_color="transparent",
            hover_color="#3A3A3A",
            command=lambda: self.copy_to_clipboard(
                self.current_task.full_name
            )
        )

        self.copy_full_name.grid(
            row=0,
            column=2,
            padx=(4, 0)
        )

    def build_dashboard(self):

        self.dashboard = ctk.CTkFrame(
            self.left,
            fg_color="transparent"
        )

        self.dashboard.grid(
            row=0,
            column=0,
            sticky="ew",
            pady=(0, 20)
        )

        self.dashboard.grid_columnconfigure((0, 1, 2), weight=1)

        self.type_card = StatusCard(
            self.dashboard,
            title="Тип",
            values=[
                "ПСИ",
                "Актуализация",
                "Подключение",
                "Другое"
            ],
            on_change=lambda value:
            self.update_field("type", value)
        )

        self.type_card.grid(
            row=0,
            column=0,
            padx=(0, 8),
            sticky="ew"
        )

        self.pentest_card = StatusCard(
            self.dashboard,
            title="Пентест/Аудит",
            values=[
                "Не запущен",
                "Запущен",
                "Завершен"
            ],
            on_change=lambda value:
            self.update_field("pentest_audit", value)
        )

        self.pentest_card.grid(
            row=0,
            column=1,
            padx=8,
            sticky="ew"
        )

        self.compliance_card = StatusCard(
            self.dashboard,
            title="СКИБ",
            values=[
                "Не запущен",
                "Запущен",
                "Завершен"
            ],
            on_change=lambda value:
            self.update_field("compliance", value)
        )

        self.compliance_card.grid(
            row=0,
            column=2,
            padx=(8, 0),
            sticky="ew"
        )

    def build_info(self):

        self.info = ctk.CTkFrame(
            self.left,
            fg_color="transparent"
        )

        self.info.grid(
            row=1,
            column=0,
            pady=(0, 20),
            sticky="ew"
        )

        self.info.grid_columnconfigure(0, weight=1)
        self.info.grid_columnconfigure(1, weight=1)
        self.info.grid_columnconfigure(2, weight=0)


        # ---------- MP8 ----------

        self.mp8_field = LabeledField(
            self.info,
            "MP8",
            on_change=lambda value: self.update_field("mp8", value)
        )

        self.mp8_field.grid(
            row=1,
            column=0,
            sticky="ew",
            padx=(0, 8),
            pady=4
        )

        # ---------- SD ----------

        self.sd_field = LabeledField(
            self.info,
            "SD",
            copyable=True,
            on_change=lambda value: ...
        )

        self.sd_field.grid(
            row=1,
            column=1,
            sticky="ew",
            pady=4
        )



        # ---------- PCI DSS ----------

        self.secure_field = LabeledField(
            self.info,
            "PCI DSS",
            field_type="combo",
            values=[
                "Да",
                "Нет",
                "Не задан"
            ],
            on_change=lambda value: self.update_field("secure", value)
        )

        self.secure_field.grid(
            row=2,
            column=0,
            sticky="ew",
            padx=(0, 8),
            pady=4
        )

        # ---------- Статус ----------

        self.status_field = LabeledField(
            self.info,
            "Статус",
            field_type="combo",
            values=[
                "В работе",
                "Закрыто",
                "Приостановлено"
            ],
            on_change=lambda value: self.update_field("status", value)
        )

        self.status_field.grid(
            row=2,
            column=1,
            sticky="ew",
            pady=4
        )



    def build_comment(self):

        self.comment = CommentBox(
            self.left,
            on_change=lambda value:
            self.update_field(
                "comment",
                value
            )
        )

        self.comment.grid(
            row=2,
            column=0,
            pady=(0, 20),
            sticky="nsew"
        )

    def update_field(self, field_name, value):

        if self.current_task is None:
            return

        setattr(
            self.current_task,
            field_name,
            value
        )

        if self.on_task_changed:
            self.on_task_changed(self.current_task)

    def build_actions(self):

        self.actions = ActionBar(
            self.card,
            on_open_folder=self.open_folder,
            on_copy_scan=self.copy_scan,
            on_load_docx=self.load_docx,
            on_copy_ips=self.copy_ips,
            on_delete=self.delete_task
        )

        self.actions.grid(
            row=3,
            column=0,
            columnspan=2,
            padx=25,
            pady=(0, 15),
            sticky="w"
        )

    def open_folder(self):

        if self.current_task and self.on_open_folder:
            self.on_open_folder(self.current_task)

    def delete_task(self):

        if self.current_task and self.on_delete_task:
            self.on_delete_task(self.current_task)

    def clear(self):

        self.current_task = None

        self.rf_label.configure(
            text="Выберите систему"
        )

        self.name_label.configure(
            text=""
        )
        self.full_name_label.configure(
            text=""
        )

        self.type_card.set("ПСИ")

        self.sd_field.set("")
        self.mp8_field.set("")

        self.secure_field.set("Не задан")

        self.status_field.set("В работе")

        self.pentest_card.set("Не запущен")
        self.compliance_card.set("Не запущен")

        self.comment.set("")

    def copy_to_clipboard(self, text):

        if not text:
            return

        self.clipboard_clear()
        self.clipboard_append(text)
        self.update()

    def copy_scan(self):

        if self.current_task is None:
            return

        if self.on_copy_scan:
            self.on_copy_scan(self.current_task)

    def load_docx(self):

        if self.current_task and self.on_load_docx:
            self.on_load_docx(self.current_task)

    def build_hosts(self):

        self.hosts = HostsTable(
            self.right
        )

        self.hosts.grid(
            row=0,
            column=0,
            sticky="nsew"
        )
        self.right.grid_rowconfigure(0, weight=1)

    def copy_ips(self, mode):

        if self.current_task and self.on_copy_ips:
            self.on_copy_ips(
                self.current_task,
                mode,
                self.hosts.get_visible_ips()
            )

    def build_layout(self):

        self.content = ctk.CTkFrame(
            self.card,
            fg_color="transparent"
        )

        self.content.grid(
            row=4,
            column=0,
            columnspan=2,
            padx=25,
            pady=(10, 20),
            sticky="nsew"
        )

        self.card.grid_rowconfigure(3, weight=0)
        self.card.grid_rowconfigure(4, weight=1)

        self.content.grid_columnconfigure(0, weight=0)
        self.content.grid_columnconfigure(1, weight=1)

        # Левая часть

        self.left = ctk.CTkFrame(
            self.content,
            fg_color="transparent"
        )

        self.left.grid(
            row=0,
            column=0,
            sticky="ns"
        )

        #self.left.grid_propagate(False)

        # Правая часть

        self.right = ctk.CTkFrame(
            self.content,
            fg_color="transparent"
        )

        self.right.grid(
            row=0,
            column=1,
            padx=(25, 0),
            sticky="nsew"
        )

        self.content.grid_rowconfigure(0, weight=1)
        self.right.grid_rowconfigure(0, weight=1)
        self.left.grid_rowconfigure(2, weight=1)
        self.right.grid_columnconfigure(0, weight=1)

    def edit_full_name(self):

        if not self.current_task:
            return

        value = simpledialog.askstring(
            "Полное название",
            "Введите полное название системы:",
            initialvalue=self.current_task.full_name
        )

        if value is None:
            return

        self.current_task.full_name = value

        self.full_name_label.configure(
            text=value
        )

        if self.on_task_changed:
            self.on_task_changed(self.current_task)