import json
from pathlib import Path

REPORT_FILE = Path("report.json")


class ReportRepository:

    def load(self):

        if not REPORT_FILE.exists():
            return []

        with open(REPORT_FILE, "r", encoding="utf-8") as f:
            return json.load(f)

    def save(self, report):

        REPORT_FILE.parent.mkdir(exist_ok=True)

        with open(REPORT_FILE, "w", encoding="utf-8") as f:
            json.dump(
                report,
                f,
                indent=4,
                ensure_ascii=False
            )