import csv
import json
import re
from pathlib import Path


class RegistryRepository:

    def __init__(self):
        self.path = Path(__file__).resolve().parents[1] / "registry.json"

    @staticmethod
    def normalize(value):
        return str(value or "").strip().casefold()

    @staticmethod
    def extract_manager(value):
        matches = re.findall(r"\[\s*([^\]]+?)\s*\]", value or "")
        return matches[0].strip() if matches else ""

    def load(self):
        if not self.path.exists():
            return {}

        with open(self.path, "r", encoding="utf-8") as file:
            return json.load(file)

    def import_csv(self, filename):
        rows = None

        # Excel может сохранять CSV в разных кодировках
        for encoding in ("utf-8-sig", "cp1251", "utf-8"):
            try:
                with open(filename, "r", encoding=encoding, newline="") as file:
                    sample = file.read(4096)
                    file.seek(0)

                    try:
                        dialect = csv.Sniffer().sniff(
                            sample,
                            delimiters=";,\t"
                        )
                    except csv.Error:
                        dialect = csv.excel
                        dialect.delimiter = ";"

                    rows = list(csv.DictReader(file, dialect=dialect))
                break
            except UnicodeDecodeError:
                continue

        if rows is None:
            raise ValueError("Не удалось определить кодировку CSV.")

        registry = {}

        for row in rows:
            # Убираем пробелы и BOM из заголовков
            row = {
                str(key or "").replace("\ufeff", "").strip().casefold(): value
                for key, value in row.items()
            }

            code = str(row.get("код ас") or "").strip()
            full_name = str(
                row.get("наименование автоматизированной системы") or ""
            ).strip()
            short_name = str(
                row.get("сокращенное наименование ас") or
                row.get("сокращённое наименование ас") or ""
            ).strip()

            manager_raw = str(row.get("менеджер ас") or "").strip()
            compliance = str(
                row.get(
                    "принадлежность к контурам соответствия стандартам"
                ) or ""
            ).strip()

            if not short_name:
                continue

            secure = (
                "Нет"
                if not compliance or "нет" in compliance.casefold()
                else "Да"
            )

            registry[self.normalize(short_name)] = {
                "code": code,
                "full_name": f"{code}. {full_name}".strip(". "),
                "short_name": short_name,
                "manager": self.extract_manager(manager_raw),
                "secure": secure
            }

        if not registry:
            raise ValueError(
                "В CSV не найдено ни одной записи. Проверь названия колонок."
            )

        with open(self.path, "w", encoding="utf-8") as file:
            json.dump(registry, file, ensure_ascii=False, indent=4)

        return registry