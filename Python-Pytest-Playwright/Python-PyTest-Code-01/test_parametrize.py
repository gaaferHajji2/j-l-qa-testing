import pytest;
import math;

@pytest.mark.parametrize(['name', 'surname'], [['Jafar', 'Loka'], ['Test', '01']])
def test_parametrize(name, surname):
    assert name == 'Jafar';
    assert surname == 'Loka';

@pytest.mark.parametrize('number', [55, 45, 35, 75])
def test_numbers(number):
    assert number > 50;

@pytest.mark.parametrize(["name1", "name2"], [("Jafar", "Loka"), ("Test", "01")])
def test_names(name1, name2):
    assert name1 + ' ' + name2 == "Jafar Loka"

data=[([2, 3, 4], 'sum', 9), ([4, 5, 6], 'prod', 256)]

@pytest.mark.parametrize("a,b,c", data)
def test_data(a, b, c):
    if b == 'sum':
        assert sum(a) == c;
    elif b == 'prod':
        assert math.prod(a) == c;