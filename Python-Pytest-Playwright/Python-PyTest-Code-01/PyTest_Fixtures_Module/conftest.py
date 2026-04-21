import pytest;

def pytest_configure():
    pytest.weekdays1 = ['sat', 'sun', 'mon'];
    pytest.weekdays2 = ['tue', 'wed', 'thu'];

@pytest.fixture(scope='module')
def setup01():
    wk1 = pytest.weekdays1.copy();
    wk1.insert(0, 'fri');
    yield wk1;
    wk1.clear();

@pytest.fixture()
def setup02():
    wk2 = pytest.weekdays2.copy();
    yield wk2;
    wk2.clear();

@pytest.fixture()
def setup04(request):
    months = getattr(request.module, "months");
    print("\n The Setup04 Fixture");
    print("\n Fixture Scope: ", str(request.scope));
    print("\n Calling Function: ", request.function.__name__);
    print("\n Calling Module: ", request.module.__name__);
    print("\n The Months Of Function Are: ", months);
    months.append("April");

    yield months;

    months.pop();

@pytest.fixture()
def setup05():
    def get_structure(name):
        if name == 'list':
            return [1, 2, 3];
        elif name == 'tuple':
            return (1, 3, 4);
    return get_structure;