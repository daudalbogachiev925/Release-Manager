import json
from pathlib import Path
from src.release import Release, ReleaseStatus

class ReleaseStorage:
    def __init__(self, folder="releases"):
        self.folder = Path(folder)
        self.folder.mkdir(exist_ok=True)

    def save(self, release: Release):
        path = self.folder / f"{release.version}.json"
        path.write_text(
            json.dumps(release.to_dict(), ensure_ascii=False, indent=2),
            encoding="utf-8")
        return path

    def load(self, version):
        path = self.folder / f"{version}.json"
        if not path.exists():
            return None
        data = json.loads(path.read_text(encoding="utf-8"))
        data
