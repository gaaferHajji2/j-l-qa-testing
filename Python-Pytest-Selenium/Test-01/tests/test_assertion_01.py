import unittest
class TestAssertion(unittest.TestCase):
    
    def test_assert_01(self):
        self.assertTrue(True)
        self.assertFalse(False)

    def test_assert_02(self):
        self.assertEqual(1, 1)
        self.assertNotEqual(1, 2)
    
    def test_assert_msg_01(self):
        self.assertTrue(True, "The Data Is False")

    def test_assert_msg_02(self):
        self.assertEqual(1, 1, "Data Not Equal")

if __name__ == '__main__':
    unittest.main(verbosity=3)