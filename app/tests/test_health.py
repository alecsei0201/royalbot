from app.core.health import self_check

def test_self_check_has_python():
    data = self_check()
    assert "python_version" in data
    assert "feature_flags" in data
