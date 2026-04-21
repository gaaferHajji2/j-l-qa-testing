months = ["Jan", "Feb", "Mar"];

def test_request_fixture_01(setup04):
    assert len(setup04) == 4;

def test_months_from_fixtures(setup04):
    assert "April" in setup04;