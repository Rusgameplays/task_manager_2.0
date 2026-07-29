import json
from pathlib import Path


class HostRepository:

    def __init__(self, root="tasks"):
        self.root = Path(root)

    def load(self, folder_id):

        path = self.root / folder_id / "hosts.json"

        if not path.exists():
            return []

        with open(path, "r", encoding="utf-8") as f:
            return json.load(f)

    def save(self, folder_id, hosts):

        folder = self.root / folder_id

        folder.mkdir(
            parents=True,
            exist_ok=True
        )

        path = folder / "hosts.json"

        with open(path, "w", encoding="utf-8") as f:
            json.dump(
                hosts,
                f,
                ensure_ascii=False,
                indent=4
            )