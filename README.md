# Release-Manager
Описание: управление релизами 1С: планирование, changelog, версионирование, миграции, откат, нотификации.
# Release Manager for 1C

Управление релизами: версионирование, changelog, миграции, откат, нотификации.

## Возможности
- Semantic versioning + auto-bump по коммитам
- Changelog generator (Conventional Commits)
- Migration plan с up/down скриптами
- Rollback plan
- Нотификации в Telegram/Slack

## Запуск
```bash
pip install -r requirements.txt
uvicorn api.main:app --reload
streamlit run app.py
```
