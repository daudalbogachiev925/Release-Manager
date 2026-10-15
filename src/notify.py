import requests
import json
from dataclasses import dataclass

@dataclass
class NotifierConfig:
    telegram_token: str = ""
    telegram_chat_id: str = ""
    slack_webhook: str = ""
    email_api: str = ""

def send_telegram(text, config):
    if not config.telegram_token or not config.telegram_chat_id:
        return {"ok": False, "error": "telegram not configured"}
    url = f"https://api.telegram.org/bot{config.telegram_token}/sendMessage"
    r = requests.post(url, json={
        "chat_id": config.telegram_chat_id,
        "text": text,
        "parse_mode": "Markdown",
    })
    return {"ok": r.ok, "status": r.status_code}

def send_slack(text, config):
    if not config.slack_webhook:
        return {"ok": False, "error": "slack not configured"}
    r = requests.post(config.slack_webhook, json={"text": text})
    return {"ok": r.ok, "status": r.status_code}

def format_release_message(release):
    lines = [
        f"*Release {release.version}*",
        f"Status: {release.status.value}",
        f"Date: {release.actual_date or release.planned_date}",
    ]
    if release.features:
        lines.append("\n*Features:*")
        lines += [f"- {f}" for f in release.features]
    if release.bugfixes:
        lines.append("\n*Bugfixes:*")
        lines += [f"- {b}" for b in release.bugfixes]
    if release.breaking_changes:
        lines.append("\n*Breaking:*")
        lines += [f"- {b}" for b in release.breaking_changes]
    return "\n".join(lines)
