import pytest;

@pytest.fixture()
def setup_names():
    return ["Jafar", "Loka", "Jafar-Loka-01"];

def test_len_of_names(setup_names):
    assert len(setup_names) == 3;

@pytest.mark.usefixtures("setup_names")
def test_use_fixtures():
    assert 1 == 1;