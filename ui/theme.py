import customtkinter as ctk

# ---------- Colors ----------

STATUS_COLORS = {
    "В работе": "#34C759",         # Зеленый
    "Ожидание": "#FFCC00",         # Желтый
    "Закрыто": "#FF3B30",          # Красный
    "Приостановлено": "#FFCC00"
}

CARD_COLORS = {
    "ПСИ": "#1E3A5F",
    "Актуализация": "#5A2D82",
    "Подключение": "#0F5C4A",
    "Другое": "#444444",

    "Не запущен": "#3A3A3A",
    "Запущен": "#7A5A00",
    "Завершен": "#1E5F3A",
}

DEFAULT_STATUS_COLOR = "#34C759"

BACKGROUND = "#1E1F22"
SIDEBAR = "#25262B"
CARD = "#2B2D31"

BLUE = "#3B82F6"
GREEN = "#22C55E"
YELLOW = "#EAB308"
RED = "#EF4444"

TEXT = "#FFFFFF"
TEXT_SECONDARY = "#B5BAC1"

BORDER = "#3A3C43"

# ---------- Fonts ----------

FONT = ("Segoe UI", 13)
FONT_SMALL = ("Segoe UI", 11)
FONT_TITLE = ("Segoe UI", 22, "bold")
FONT_HEADER = ("Segoe UI", 16, "bold")


def init_theme():
    ctk.set_appearance_mode("dark")
    ctk.set_default_color_theme("blue")