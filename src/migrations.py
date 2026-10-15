from dataclasses import dataclass, field
from datetime import datetime

@dataclass
class Migration:
    id: str
    description: str
    up_script: str
    down_script: str
    applied: bool = False
    applied_at: str = ""
    duration_ms: int = 0

@dataclass
class MigrationPlan:
    release_version: str
    migrations: list = field(default_factory=list)

    def add(self, m: Migration):
        self.migrations.append(m)

    def validate(self):
        errors = []
        for m in self.migrations:
            if not m.up_script:
                errors.append(f"{m.id}: missing up_script")
            if not m.down_script:
                errors.append(f"{m.id}: missing down_script")
        return {"valid": len(errors) == 0, "errors": errors}

    def apply(self):
        plan = []
        for m in self.migrations:
            m.applied = True
            m.applied_at = datetime.utcnow().isoformat()
            plan.append({"id": m.id, "description": m.description,
                         "applied_at": m.applied_at})
        return plan

    def rollback(self):
        plan = []
        for m in reversed(self.migrations):
            m.applied = False
            plan.append({"id": m.id, "rolled_back_at":
                         datetime.utcnow().isoformat()})
        return plan

    def generate_sql(self):
        return "\n\n".join(
            f"-- Migration {m.id}: {m.description}\n{m.up_script}"
            for m in self.migrations)
