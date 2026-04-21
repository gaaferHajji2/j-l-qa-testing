import unittest
class Test01(unittest.TestCase):
    
    def setUp(self):
        print("The SetUp Method Of Test01-Class TestCase")

    def tearDown(self):
        print("The TearDown Method Of Test01-Class TestCase")

    def test_method_01(self):
        print("Running From Method-01");

    def test_method_02(self):
        print("Running From Method-02");

if __name__ == '__main__':
    unittest.main(verbosity=3)