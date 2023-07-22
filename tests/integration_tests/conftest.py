import pytest

@pytest.fixture(scope="session")
def test_container() -> str:
    return "hi"

def test_sample(test_container):
    pass