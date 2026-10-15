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
        data["status"] = ReleaseStatus(data["status"])
        return Release(**data)

    def list_all(self):
        result = []
        for p in sorted(self.folder.glob("*.json")):
            try:
                result.append(json.loads(p.read_text(encoding="utf-8")))
            except Exception:
                pass
        return result

    def latest(self):
        releases = self.list_all()
        if not releases:
            return None
        from src.version import Version
        releases.sort(key=lambda r: Version.parse(r["version"]).__dict__.__str__())
        return releases[-1]
