import streamlit as st
import pandas as pd
from src.release import create_release, mark_released, mark_rolled_back, ReleaseStatus
from src.storage import ReleaseStorage
from src.changelog import render_changelog
from src.version import Version, BumpType, classify_changes

st.set_page_config(page_title="Release Manager", layout="wide")
st.title("Release Manager — 1C")

storage = ReleaseStorage()

# seed
if not storage.list_all():
    r = create_release("1.0.0", "2025-01-15",
                       features=["Справочник Товары", "Отчёт Продажи"],
                       bugfixes=["Исправлен НДС"])
    mark_released(r)
    storage.save(r)
    r2 = create_release("1.1.0", "2025-02-20",
                        features=["Интеграция с WMS"])
    storage.save(r2)

tab1, tab2, tab3 = st.tabs(["Releases", "Changelog", "Versioning"])

with tab1:
    releases = storage.list_all()
    st.dataframe(pd.DataFrame(releases))
    version = st.text_input("Version")
    col1, col2 = st.columns(2)
    with col1:
        if st.button("Mark released"):
            r = storage.load(version)
            if r:
                mark_released(r)
                storage.save(r)
                st.success(f"Released {version}")
    with col2:
        if st.button("Rollback"):
            r = storage.load(version)
            if r:
                mark_rolled_back(r, "manual")
                storage.save(r)
                st.warning(f"Rolled back {version}")

with tab2:
    st.subheader("Generate changelog")
    commits_text = st.text_area("Commits (JSON)", '''[
{"type": "feat", "message": "add catalog", "hash": "abc1"},
{"type": "fix", "message": "fix NDS", "hash": "abc2"},
{"type": "feat", "message": "WMS integration", "hash": "abc3", "breaking": true}
]''')
    if st.button("Generate"):
        import json
        commits = json.loads(commits_text)
        bump = classify_changes(commits)
        st.info(f"Recommended bump: {bump.value}")
        st.code(render_changelog("1.2.0", commits))

with tab3:
    current = st.text_input("Current version", "1.2.3")
    if current:
        v = Version.parse(current)
        st.write(f"Major bump: {v.bump(BumpType.MAJOR)}")
        st.write(f"Minor bump: {v.bump(BumpType.MINOR)}")
        st.write(f"Patch bump: {v.bump(BumpType.PATCH)}")
