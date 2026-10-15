from datetime import datetime
from pathlib import Path

SECTIONS = {
    "breaking": "Breaking Changes",
    "feat": "Features",
    "fix": "Bug Fixes",
    "perf": "Performance",
    "refactor": "Refactoring",
    "docs": "Documentation",
    "test": "Tests",
    "chore": "Chores",
}

def parse_commits(commits):
    grouped = {}
    for c in commits:
        ctype = c.get("type", "chore")
        if c.get("breaking"):
            grouped.setdefault("breaking", []).append(c)
        grouped.setdefault(ctype, []).append(c)
    return grouped

def render_changelog(version, commits, date=None):
    date = date or datetime.utcnow().date().isoformat()
    grouped = parse_commits(commits)
    lines = [f"## [{version}] - {date}", ""]
    for key in ["breaking", "feat", "fix", "perf", "refactor", "docs", "test", "chore"]:
        items = grouped.get(key, [])
        if not items:
            continue
        title = SECTIONS.get(key, key.capitalize())
        lines.append(f"### {title}")
        for c in items:
            scope = f"**{c['scope']}**: " if c.get("scope") else ""
            lines.append(f"- {scope}{c['message']} ({c.get('hash', '')[:7]})")
        lines.append("")
    return "\n".join(lines)

def append_changelog(path, content):
    p = Path(path)
    if not p.exists():
        p.write_text("# Changelog\n\n" + content, encoding="utf-8")
        return
    existing = p.read_text(encoding="utf-8")
    header, _, rest = existing.partition("\n\n")
    p.write_text(f"{header}\n\n{content}\n{rest}", encoding="utf-8")
