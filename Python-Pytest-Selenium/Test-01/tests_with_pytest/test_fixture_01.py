import pytest

# yield_fixture Is Deprecated
# @pytest.yield_fixture()
# def fixture01():
#     print("This Will Run Before The Test That Used It")

@pytest.mark.run(order=2)
def test_02():
    print("The Test Is 02")
    
    assert True == True

@pytest.mark.run(order=3)
def test_03():
    print("The Test-03 Test")

    assert True

@pytest.mark.run(order=1)
def test_01():
    print("The Test-01 Test");
    assert 1 == 1