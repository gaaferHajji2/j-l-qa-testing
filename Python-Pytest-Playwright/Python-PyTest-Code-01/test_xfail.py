import pytest;
import sys;

@pytest.mark.xfail(raises=ValueError)
def test_t1():
    num = 1;
    string = 'Jafar-Loka-0';

    assert string + num == 'Jafar-Loka-01'

@pytest.mark.xfail(
    condition=sys.platform == 'linux', 
    reason='This Test For Linux Systems Only')
def test_t2():
    assert 1;

@pytest.mark.xfail
def test_t3():
    assert 3 < 2;