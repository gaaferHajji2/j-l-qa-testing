import pytest;
import sys;

pytestmark = pytest.mark.skipif(sys.platform == 'win32', reason="No Reason Here")

class TestClass:
    @pytest.mark.skipif(sys.version_info.major>=3, reason="No Reason Here")
    def test_t1(self):
        assert 1 == 1;

    def test_t2(self):
        with pytest.raises(Exception):
            assert (1/0);

    @pytest.mark.skip(reason="Skip Reason Will be Here")
    def test_skip_test(self):
        assert type(1) == int;