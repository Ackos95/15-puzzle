__author__ = 'Acko'

import unittest

from heap_test import HeapTest
from table_state_test import TableStateTest


class MainTest(unittest.TestCase):

    def runTests(self):
        table_state_test_suite = unittest.TestLoader().loadTestsFromTestCase(TableStateTest)
        heap_test_suite = unittest.TestLoader().loadTestsFromTestCase(HeapTest)

        test_suite = unittest.TestSuite([table_state_test_suite, heap_test_suite])
        unittest.TextTestRunner().run(test_suite)

if __name__ == '__main__':
    unittest.main()