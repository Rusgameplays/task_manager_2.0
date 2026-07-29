import json

from models.task import Task


class TaskRepository:

    def __init__(self, filename="tasks.json"):
        self.filename = filename

    def load(self):

        with open(self.filename, encoding="utf-8") as f:
            data = json.load(f)

        tasks = []

        for item in data:

            tasks.append(
                Task(
                    rf=item.get("id", ""),
                    sd=item.get("second_id", ""),

                    name=item.get("name", ""),
                    full_name=item.get("full_name", ""),

                    type=item.get("type", ""),
                    mp8=item.get("mp8", ""),
                    secure=item.get("secure", ""),

                    status=item.get("status", ""),
                    pentest_audit=item.get("pentest/audit", ""),
                    compliance=item.get("compliance", ""),

                    comment=item.get("comment", ""),

                    folder_id=item.get("folder_id", "")
                )
            )

        return tasks

    def save(self, tasks):

        data = []

        for task in tasks:
            data.append({

                "id": task.rf,
                "second_id": task.sd,

                "name": task.name,
                "full_name": task.full_name,

                "type": task.type,
                "mp8": task.mp8,
                "secure": task.secure,

                "status": task.status,
                "pentest/audit": task.pentest_audit,
                "compliance": task.compliance,

                "comment": task.comment,

                "folder_id": task.folder_id

            })

        with open(self.filename, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=4)