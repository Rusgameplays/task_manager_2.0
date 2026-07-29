import shutil
import uuid

import customtkinter as ctk
from data.host_repository import HostRepository
from data.report_repository import ReportRepository

from data.task_repository import TaskRepository
from ui.details_panel import DetailsPanel
from ui.dialogs.confirm_dialog import ConfirmDialog
from ui.report_window import ReportWindow
from ui.sidebar import Sidebar
from ui.toolbar import Toolbar
from ui.theme import *
from ui.dialogs.new_task_dialog import NewTaskDialog
from models.task import Task
from pathlib import Path
import subprocess
from tkinter import filedialog
from pathlib import Path

from utils.parser import parse_hosts


class App(ctk.CTk):

    def __init__(self):
        super().__init__()

        self.title("Task Manager")
        self.geometry("1600x900")
        self.minsize(1300, 800)

        self.configure(fg_color=BACKGROUND)

        # Данные
        self.repository = TaskRepository("tasks.json")
        self.report_repository = ReportRepository()
        self.host_repository = HostRepository()
        self.tasks = self.repository.load()

        self.save_job = None

        # Интерфейс
        self.build_ui()

        # Загружаем список задач
        self.sidebar.load_tasks(self.tasks)
        self.current_filter = "Все"

    def build_ui(self):

        # Настройка сетки главного окна
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)

        # ---------------- Sidebar ----------------

        self.sidebar = Sidebar(
            self,
            on_task_selected=self.on_task_selected,
            on_filter_changed=self.filter_tasks
        )

        self.sidebar.grid(
            row=0,
            column=0,
            sticky="ns"
        )

        # ---------------- Правая часть ----------------

        self.main = ctk.CTkFrame(
            self,
            fg_color=BACKGROUND
        )

        self.main.grid(
            row=0,
            column=1,
            sticky="nsew"
        )

        self.main.grid_columnconfigure(0, weight=1)
        self.main.grid_rowconfigure(1, weight=1)

        # Toolbar

        self.toolbar = Toolbar(
            self.main,
            on_new=self.new_task,
            on_search=self.search_tasks,
            on_report=self.open_report
        )

        self.toolbar.grid(
            row=0,
            column=0,
            sticky="ew"
        )

        # Details

        self.details = DetailsPanel(
            self.main,
            on_task_changed=self.task_changed,
            on_open_folder=self.open_folder,
            on_delete_task=self.delete_task,
            on_copy_scan=self.copy_scan,
            on_load_docx=self.load_docx,
            on_copy_ips=self.copy_ips
        )

        self.details.grid(
            row=1,
            column=0,
            sticky="nsew"
        )

    # ==========================================================
    # Callbacks
    # ==========================================================

    def on_task_selected(self, task):

        hosts = self.host_repository.load(
            task.folder_id
        )

        self.details.show_task(
            task,
            hosts
        )

    def new_task(self):
        NewTaskDialog(
            self,
            on_create=self.create_task
        )

    def create_task(self, rf, sd, name):

        template = self.find_template(name)

        task = Task(
            rf=rf,
            sd=sd,

            name=name,

            full_name=template.full_name if template else "",

            type="",

            mp8="",

            secure=template.secure if template else "Не задан",

            status="В работе",

            pentest_audit="Не запущен",

            compliance="Не запущен",

            comment="",

            folder_id=str(uuid.uuid4())
        )

        self.tasks.append(task)

        self.repository.save(self.tasks)

        self.sidebar.load_tasks(self.tasks)

        self.details.show_task(task)

    def find_template(self, short_name):

        short_name = short_name.strip().lower()

        for task in self.tasks:

            if task.name.strip().lower() == short_name:
                return task

        return None

    def search_tasks(self, text):

        text = text.strip().lower()

        if not text:
            self.sidebar.load_tasks(self.tasks)
            return

        filtered = []

        for task in self.tasks:

            if (
                    text in task.rf.lower()
                    or text in task.sd.lower()
                    or text in task.name.lower()
                    or text in task.full_name.lower()
            ):
                filtered.append(task)

        self.sidebar.load_tasks(filtered)

    def task_changed(self, task):

        if self.save_job is not None:
            self.after_cancel(self.save_job)

        self.save_job = self.after(
            700,
            self.save_tasks
        )
        self.filter_tasks(self.current_filter)

        self.sidebar.update_card(task)

    def save_tasks(self):
        self.repository.save(self.tasks)

        self.save_job = None

    def filter_tasks(self, status):

        self.current_filter = status

        if status == "Все":
            filtered = self.tasks

        else:
            filtered = [
                task
                for task in self.tasks
                if task.status == status
            ]

        self.sidebar.load_tasks(filtered)

    def open_folder(self, task):

        folder = Path("tasks") / task.folder_id

        folder.mkdir(
            parents=True,
            exist_ok=True
        )

        subprocess.run([
            "open",
            str(folder)
        ])

    def delete_task(self, task):

        ConfirmDialog(
            self,
            title="Удаление системы",
            message=(
                f"Удалить систему?\n\n"
                f"{task.rf}\n"
                f"{task.name}\n\n"
                f"Это действие нельзя отменить."
            ),
            on_confirm=lambda:
            self.confirm_delete(task)
        )

    def confirm_delete(self, task):

        folder = Path("tasks") / task.folder_id

        if folder.exists():
            shutil.rmtree(folder)

        self.tasks.remove(task)

        self.repository.save(self.tasks)

        self.sidebar.load_tasks(self.tasks)

        self.details.clear()

    def copy_scan(self, task):

        text = f"Сканирование {task.name} ({task.rf}) - {task.sd}"

        self.clipboard_clear()
        self.clipboard_append(text)
        self.update()

    def load_docx(self, task):

        folder = Path("tasks") / task.folder_id

        folder.mkdir(
            parents=True,
            exist_ok=True
        )

        path = filedialog.askopenfilename(
            initialdir=str(folder),
            title="Выберите DOCX",
            filetypes=[
                ("Word document", "*.docx")
            ]
        )

        if not path:
            return

        hosts = parse_hosts(path)

        self.host_repository.save(
            task.folder_id,
            hosts
        )

        print(f"Импортировано {len(hosts)} записей")

    def copy_ips(self, task, mode):

        hosts = self.host_repository.load(task.folder_id)

        ips = [
            host["IP"]
            for host in hosts
            if host.get("IP")
        ]

        if mode == "lines":
            text = "\n".join(ips)
        else:
            text = ",".join(ips)

        self.clipboard_clear()
        self.clipboard_append(text)
        self.update()

    def open_report(self):

        ReportWindow(
            self,
            self.report_repository
        )