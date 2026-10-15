from src.version import Version, BumpType, classify_changes

def test_parse():
    v = Version.parse("1.2.3")
    assert (v.major, v.minor, v.patch) == (1, 2, 3)

def test_bump_major():
    assert str(Version.parse("1.2.3").bump(BumpType.MAJOR)) == "2.0.0.0"

def test_bump_minor():
    assert str(Version.parse("1.2.3").bump(BumpType.MINOR)) == "1.3.0.0"

def test_bump_patch():
    assert str(Version.parse("1.2.3").bump(BumpType.PATCH)) == "1.2.4.0"

def test_classify_breaking():
    commits = [{"type": "feat", "breaking": True, "message": "x"}]
    assert classify_changes(commits) == BumpType.MAJOR

def test_classify_feat():
    commits = [{"type": "feat", "message": "x"}]
    assert classify_changes(commits) == BumpType.MINOR

def test_classify_fix():
    commits = [{"type": "fix", "message": "x"}]
    assert classify_changes(commits) == BumpType.PATCH
