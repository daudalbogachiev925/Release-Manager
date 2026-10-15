from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum

class ReleaseStatus(str, Enum):
    PLANNED = "planned"
    IN_PROGRESS = "in_progress"
    RELEASED = "released"
    ROLLED_BACK = "rolled_back"

@dataclass
class Release:
    version: str
    status: ReleaseStatus
    planned_date: str
    actual_date: str = ""
    features: list = field(default_factory=list)
    bugfixes: list = field(default_factory=list)
    breaking_changes: list = field(default_factory=list)
    migrations: list = field(default_factory=list)
    rollback_plan: str = ""
    notes: str = ""

    def to_dict(self):
        d = self.__dict__.copy()
        d["status"] = self.status.value
        return d

def create_release(version, planned_date, features=None, bugfixes=None):
    return Release(
        version=version,
        status=ReleaseStatus.PLANNED,
        planned_date=planned_date,
        features=features or [],
        bugfixes=bugfixes or [],
    )

def mark_released(release, actual_date=None):
    release.status = ReleaseStatus.RELEASED
    release.actual_date = actual_date or datetime.utcnow().date().isoformat()
    return release

def mark_rolled_back(release, reason=""):
    release.status = ReleaseStatus.ROLLED_BACK
    release.notes = f"{release.notes}\nRollback: {reason}"
    return release
