import unittest
class Test02(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        print('This Is From SetUp For Entire Class')

    @classmethod
    def tearDownClass(cls):
        print('This Is From TearDown For Entire Class')

    def test_method_01(self):
        print("Running From Method-01");

    def test_method_02(self):
        print("Running From Method-02");

if __name__ == '__main__':
    unittest.main(verbosity=3)