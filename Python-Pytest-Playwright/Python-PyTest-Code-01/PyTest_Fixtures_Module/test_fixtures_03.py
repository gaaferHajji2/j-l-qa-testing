import pytest;

def test_fixtures_01(setup01):
    assert len(setup01) == 4;

def test_fixtures_02(setup02):
    assert len(setup02) == 3;

def test_fixtures_03(setup01):
    del setup01[0];

    assert pytest.weekdays1 == setup01;