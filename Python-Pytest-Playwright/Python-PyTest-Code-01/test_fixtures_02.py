import pytest;

days1 = ["Sat", "Sun", "Mon"];
days2 = ["Tue", "Wed", "Thu"];

@pytest.fixture()
def setup_days1():
    wk1 = days1.copy();
    wk1.append('Fri');
    yield wk1;
    wk1.pop();

@pytest.fixture()
def setup_days2():
    wk2 = days2.copy();
    yield wk2;
    wk2.clear();

def test_wk1(setup_days1):
    assert len(setup_days1) == 4;

def test_wk1_wk2(setup_days1, setup_days2):
    assert len(setup_days1) + len(setup_days2) == 7;