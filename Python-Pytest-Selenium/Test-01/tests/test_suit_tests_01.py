import unittest

from test_01 import Test01
from test_02 import Test02
from test_assertion_01 import TestAssertion

# Getting All Tests From The Classes That Inherit From Test01, Test02, TestAssertion
t1 = unittest.TestLoader().loadTestsFromTestCase(Test01)
t2 = unittest.TestLoader().loadTestsFromTestCase(Test02)
t3 = unittest.TestLoader().loadTestsFromTestCase(TestAssertion)

# Create The Test Suite That Contains All Tests Cases
t4 = unittest.TestSuite([t1, t2, t3])

# Run The Tests With Verbosity Of 2
t5 = unittest.TextTestRunner(verbosity=3).run(t4)