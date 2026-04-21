import pytest

@pytest.fixture()
def simple_01():
    print("In The Fixture Simple_01")

@pytest.fixture(scope='module')
def simple_02():
    print("In The Fixture Simple_02 With Scope: Module")

@pytest.fixture(autouse=True, scope='session')
def fixture02():
    print("This Will Run Automatically Before Any Test");
    yield
    print("This Will Run Automatically After Any Test Because Of Scope Is: Session");