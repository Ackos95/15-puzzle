__author__ = 'Acko'

import unittest
from application.TableState import TableState


class TableStateTest(unittest.TestCase):

    def test_equal_operator(self):

        # preparation
        puzzle1 = TableState('1 2 3 4 5 6 7 8 9 10 11 12 13 14 15 x', None)
        puzzle2 = TableState('1 2 3 4 5 6 7 8 9 10 11 12 13 14 15 x', None)
        puzzle3 = TableState('2 1 3 4 5 6 7 8 9 10 11 12 13 14 15 x', None)

        # do work and test
        self.assertEqual(puzzle1, puzzle2)
        self.assertNotEqual(puzzle1, puzzle3)
        self.assertIsNot(puzzle1, puzzle2)
        self.assertIsNot(puzzle1, puzzle3)

    def test_parse_string(self):

        # preparation
        puzzle1 = TableState(['1', '2', '3', '4', '5', '6', '7', '8', '9', '10', '11', '12', 'x', '13', '14', '15'],
                             None)
        puzzle2 = TableState('1 2 3 4 5 6 7 8 9 10 11 12 x 13 14 15', None)
        puzzle3 = TableState('1s2s3 4 5 asdf 6\n7\n8s9 10asdf11\t12 x 13 14 15', None)
        puzzle4 = TableState('2 1 3 4 5 6 7 8 9 10 11 12 13 14 15 x', None)

        # do work and test
        self.assertEqual(puzzle1, puzzle2)
        self.assertEqual(puzzle1, puzzle3)
        self.assertNotEqual(puzzle1, puzzle4)

    def test_is_solvable(self):

        # preparation
        puzzle1 = TableState('1 2 3 4 5 6 7 8 9 10 11 12 x 13 14 15', None)
        puzzle2 = TableState('2 1 3 4 5 6 7 8 9 10 11 12 x 13 14 15', None)

        # do work and test
        self.assertEqual(puzzle1.is_solvable(), True)
        self.assertEqual(puzzle2.is_solvable(), False)

    def test_is_final(self):

        # preparation
        puzzle1 = TableState('1 2 3 4 5 6 7 8 9 10 11 12 x 13 14 15', None)
        puzzle2 = TableState('1 2 3 4 5 6 7 8 9 10 11 12 13 14 15 x', None)
        puzzle3 = TableState('1 5 3 4 2 6 7 8 9 10 11 12 13 14 15 x', None)

        # do work and test
        self.assertEqual(puzzle1.is_final(), False)
        self.assertEqual(puzzle2.is_final(), True)
        self.assertEqual(puzzle3.is_final(), False)

    def test_manhattan_distance(self):

        # preparation
        puzzle1 = TableState('1 2 3 4 5 6 7 8 9 10 11 12 x 13 14 15', None)
        puzzle2 = TableState('1 2 3 4 5 6 7 8 9 10 11 12 13 14 15 x', None)
        puzzle3 = TableState('5 1 14 3 11 10 6 15 2 8 4 7 9 x 13 12', None)

        # do work and test
        self.assertEqual(puzzle1.manhattan(), 3)
        self.assertEqual(puzzle2.manhattan(), 0)
        self.assertEqual(puzzle3.manhattan(), 30)

    def test_hamming(self):

        # preparation
        puzzle1 = TableState('1 2 3 4 5 6 7 8 9 10 11 12 x 13 14 15', None)
        puzzle2 = TableState('1 2 3 4 5 6 7 8 9 10 11 12 13 14 15 x', None)
        puzzle3 = TableState('5 1 14 3 11 10 6 15 2 8 4 7 9 x 13 12', None)

        # do work and test
        self.assertEqual(puzzle1.hamming(), 3)
        self.assertEqual(puzzle2.hamming(), 0)
        self.assertEqual(puzzle3.hamming(), 15)

    def test_generate_next_moves(self):

        # preparations
        puzzle1 = TableState('1 2 3 4 5 6 x 7 8 9 10 11 12 13 14 15', None)
        puzzle2 = TableState('x 1 2 3 4 5 6 7 8 9 10 11 12 13 14 15', None)
        puzzle3 = TableState('1 2 3 4 5 6 7 8 9 10 11 12 13 14 15 x', None)

        puzzle1_next_should_be = [
            TableState('1 2 3 4 5 x 6 7 8 9 10 11 12 13 14 15', puzzle1),
            TableState('1 2 x 4 5 6 3 7 8 9 10 11 12 13 14 15', puzzle1),
            TableState('1 2 3 4 5 6 7 x 8 9 10 11 12 13 14 15', puzzle1),
            TableState('1 2 3 4 5 6 10 7 8 9 x 11 12 13 14 15', puzzle1)
        ]
        puzzle2_next_should_be = [
            TableState('1 x 2 3 4 5 6 7 8 9 10 11 12 13 14 15', puzzle2),
            TableState('4 1 2 3 x 5 6 7 8 9 10 11 12 13 14 15', puzzle2)
        ]

        puzzle3_next_should_be = [
            TableState('1 2 3 4 5 6 7 8 9 10 11 12 13 14 x 15', puzzle3),
            TableState('1 2 3 4 5 6 7 8 9 10 11 x 13 14 15 12', puzzle3)
        ]

        # do work
        puzzle1_next = puzzle1.generate_next_moves()
        puzzle2_next = puzzle2.generate_next_moves()
        puzzle3_next = puzzle3.generate_next_moves()

        # test
        self.assertEqual(puzzle1_next, puzzle1_next_should_be)
        self.assertEqual(puzzle2_next, puzzle2_next_should_be)
        self.assertEqual(puzzle3_next, puzzle3_next_should_be)


if __name__ == '__main__':
    unittest.main()
