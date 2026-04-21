import pytest;

@pytest.mark.jafar_loka_01
def test_t1():
    assert 1 == 1;

@pytest.mark.jafar_loka_01
@pytest.mark.fail
def test_t2():
    assert 1 > 2;

def test_t3(): 
    assert 2 > 1;

@pytest.mark.jafar_loka_01
def test_t4():
    assert 2 < 3;

def test_t5():
    assert 3 < 2;