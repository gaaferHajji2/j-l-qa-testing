import pytest;

@pytest.fixture(params=[(3, 4), [3, 5]], ids=['tuple', 'list'])
def fixture01(request):
    return request.param;

@pytest.fixture(params=['access'])
def fixture02(request):
    return request.param;

def test_fixtures_with_params_01(fixture01):
    print("\n The Fixture Param From 01 is: ", fixture01);
    assert len(fixture01) == 2;

def test_fixtures_with_params_02(fixture01):
    print("\n The Fixture Param From 02 is: ", fixture01);
    assert 3 in fixture01;

def test_fixtures_with_params_03(fixture01):
    print("\n The Fixture Param From 03 is: ", fixture01);

    assert 3 in fixture01;

def test_fixtures_with_params_04(fixture01):
    assert type(fixture01) in [list, tuple];

def test_fixtures_with_multiple_params_05(fixture01, fixture02):
    if(fixture02 == 'access'):
        assert fixture01[0];