def test_basic_math():
    """Простой тест который всегда проходит"""
    assert 1 + 1 == 2

def test_imports():
    """Проверяем что основные модули импортируются"""
    try:
        from app.main import app
        from app.database import engine
        print("✅ All imports work")
        assert True
    except ImportError as e:
        print(f"❌ Import error: {e}")
        assert False, f"Import failed: {e}"
