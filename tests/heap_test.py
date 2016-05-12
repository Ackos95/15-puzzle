__author__ = 'Acko'

import unittest
from application.Heap import *


class HeapTest(unittest.TestCase):

    def test_add(self):

        # preparation
        h = Heap()

        # do work and test
        h.add(5, '1')
        self.assertEqual(h.top(), (5, '1'))

        h.add(10, '2')
        self.assertEqual(h.top(), (5, '1'))

        h.add(2, '3')
        self.assertEqual(h.top(), (2, '3'))

        h.add(7, '4')
        self.assertEqual(h.top(), (2, '3'))

        h.add(1, '5')
        self.assertEqual(h.top(), (1, '5'))

    def test_pop(self):

        # preparation
        h = Heap()

        for element in ([(5, '1'), (10, '2'), (2, '3'), (7, '4'), (1, '5')]):
            h.add(element[0], element[1])

        # do work and test
        self.assertEqual(h.pop(), (1, '5'))
        self.assertEqual(h.pop(), (2, '3'))
        self.assertEqual(h.pop(), (5, '1'))
        self.assertEqual(h.pop(), (7, '4'))
        self.assertEqual(h.pop(), (10, '2'))

        with self.assertRaises(HeapError):
            h.pop()

    def test_direction_test(self):

        # preparation
        h_up = Heap(Heap.HEAP_UP)
        h_down = Heap(Heap.HEAP_DOWN)

        elements = [(1, 1), (4, 4), (2, 2), (3, 3)]

        # do work
        for element in elements:
            h_up.add(element[0], element[1])
            h_down.add(element[0], element[1])

        # test
        self.assertNotEqual(h_up.top(), h_down.top())

        for i in xrange(1, 5):
            self.assertEqual(h_up.pop(), (5 - i, 5 - i))
            self.assertEqual(h_down.pop(), (i, i))


if __name__ == '__main__':
    unittest.main()
