def test_fixtures_list_05(setup05):
    list = setup05('list');
    assert 'list' in str(type(list));

def test_fixtures_tuple_05(setup05):
    tuple = setup05('tuple');
    assert 'tuple' in str(type(tuple))