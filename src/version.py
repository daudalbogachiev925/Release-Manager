import re
from dataclasses import dataclass
from enum import Enum

class BumpType(str, Enum):
    MAJOR = "major"
    MINOR = "minor"
    PATCH = "patch"

@dataclass
class Version:
    major: int
    minor: int
    patch: int
    build: int = 0

    @classmethod
    def parse(cls, s):
        m = re.match(r"(\d+)\.(\d+)\.(\d+)(?:\.(\d+))?", s)
        if not m:
            raise ValueError(f"Invalid version: {s}")
        return cls(int(m.group(1)), int(m.group(2)),
                   int(m.group(3)), int(m.group(4) or 0))

    def __str__(self):
        return f"{self.major}.{self.minor}.{self.patch}.{self.build}"

    def bump(self, kind):
        if kind == BumpType.MAJOR:
            return Version(self.major + 1, 0, 0, 0)
        if kind == BumpType.MINOR:
            return Version(self.major, self.minor + 1, 0, 0)
        return Version(self.major, self.minor, self.patch + 1, 0)

def classify_changes(commits):
    """commits: [{"type": "feat|fix|breaking|...", ...}]"""
    has_breaking = any(c.get("breaking") or "BREAKING" in c.get("message", "")
                       for c in commits)
    has_feat = any(c.get("type") == "feat" for c in commits)
    if has_breaking:
        return BumpType.MAJOR
    if has_feat:
        return BumpType.MINOR
    return BumpType.PATCH
