import numpy
import unittest

from sudoku_puzzle import SudokuPuzzle


class TestSudokuPuzzle(unittest.TestCase):
    def setUp(self):
        board1 = numpy.array([[0, 0, 0, 2, 6, 0, 7, 0, 1],
                             [6, 8, 0, 0, 7, 0, 0, 9, 0],
                             [1, 9, 0, 0, 0, 4, 5, 0, 0],
                             [8, 2, 0, 1, 0, 0, 0, 4, 0],
                             [0, 0, 4, 6, 0, 2, 9, 0, 0],
                             [0, 5, 0, 0, 0, 3, 0, 2, 8],
                             [0, 0, 9, 3, 0, 0, 0, 7, 4],
                             [0, 4, 0, 0, 5, 0, 0, 3, 6],
                             [7, 0, 3, 0, 1, 8, 0, 0, 0]])
        self.puzzle1 = SudokuPuzzle(board1)

        board2 = numpy.array([[4, 3, 5, 2, 6, 9, 7, 8, 1],
                              [6, 8, 2, 5, 7, 1, 4, 9, 3],
                              [1, 9, 7, 8, 3, 4, 5, 6, 2],
                              [8, 2, 6, 1, 9, 5, 3, 4, 7],
                              [3, 7, 4, 6, 8, 2, 9, 1, 5],
                              [9, 5, 1, 7, 4, 3, 6, 2, 8],
                              [5, 1, 9, 3, 2, 6, 8, 7, 4],
                              [2, 4, 8, 9, 5, 7, 1, 3, 6],
                              [7, 6, 3, 4, 1, 8, 2, 5, 9]])
        self.puzzle2 = SudokuPuzzle(board2)

    def test_find_blank_square(self):
        self.assertEqual((0, 0), self.puzzle1.find_blank_square())

        self.puzzle1.board[0][0] = 1
        self.assertEqual((0, 1), self.puzzle1.find_blank_square())

        self.assertFalse(self.puzzle2.find_blank_square())

    def test_get_valid_numbers(self):
        self.assertEqual([3, 4, 5], self.puzzle1.get_valid_numbers((0, 0)))
        self.assertEqual([6], self.puzzle1.get_valid_numbers((6, 5)))

        self.puzzle1.board[6][6] = 6
        self.assertEqual([], self.puzzle1.get_valid_numbers((6, 5)))

    def test_is_complete(self):
        self.assertFalse(self.puzzle1.is_complete())
        self.assertTrue(self.puzzle2.is_complete())

    def test_get_solution(self):
        algo_solution, final_node = self.puzzle1.get_solution()

        solution = numpy.array([[4, 3, 5, 2, 6, 9, 7, 8, 1],
                                [6, 8, 2, 5, 7, 1, 4, 9, 3],
                                [1, 9, 7, 8, 3, 4, 5, 6, 2],
                                [8, 2, 6, 1, 9, 5, 3, 4, 7],
                                [3, 7, 4, 6, 8, 2, 9, 1, 5],
                                [9, 5, 1, 7, 4, 3, 6, 2, 8],
                                [5, 1, 9, 3, 2, 6, 8, 7, 4],
                                [2, 4, 8, 9, 5, 7, 1, 3, 6],
                                [7, 6, 3, 4, 1, 8, 2, 5, 9]])
        self.assertTrue(final_node)

        for row in range(9):
            for col in range(9):
                self.assertEqual(solution[row][col], algo_solution[row][col])

    def test_step_through(self):
        # First step
        expected_step = numpy.array([[4, 0, 0, 2, 6, 0, 7, 0, 1],
                             [6, 8, 0, 0, 7, 0, 0, 9, 0],
                             [1, 9, 0, 0, 0, 4, 5, 0, 0],
                             [8, 2, 0, 1, 0, 0, 0, 4, 0],
                             [0, 0, 4, 6, 0, 2, 9, 0, 0],
                             [0, 5, 0, 0, 0, 3, 0, 2, 8],
                             [0, 0, 9, 3, 0, 0, 0, 7, 4],
                             [0, 4, 0, 0, 5, 0, 0, 3, 6],
                             [7, 0, 3, 0, 1, 8, 0, 0, 0]])

        actual_step, new_num = self.puzzle1.step_through()

        for row in range(9):
            for col in range(9):
                self.assertEqual(expected_step[row][col], actual_step[row][col])

        self.assertEqual((0, 0), new_num)

        # Second step
        expected_step = numpy.array([[4, 3, 0, 2, 6, 0, 7, 0, 1],
                                     [6, 8, 0, 0, 7, 0, 0, 9, 0],
                                     [1, 9, 0, 0, 0, 4, 5, 0, 0],
                                     [8, 2, 0, 1, 0, 0, 0, 4, 0],
                                     [0, 0, 4, 6, 0, 2, 9, 0, 0],
                                     [0, 5, 0, 0, 0, 3, 0, 2, 8],
                                     [0, 0, 9, 3, 0, 0, 0, 7, 4],
                                     [0, 4, 0, 0, 5, 0, 0, 3, 6],
                                     [7, 0, 3, 0, 1, 8, 0, 0, 0]])

        actual_step, new_num = self.puzzle1.step_through()

        for row in range(9):
            for col in range(9):
                self.assertEqual(expected_step[row][col], actual_step[row][col])

        self.assertEqual((0, 1), new_num)

        # Test if false when no steps left
        for i in range(81):
            self.puzzle1.step_through()

        self.assertFalse(self.puzzle1.step_through())


if __name__ == '__main__':
    unittest.main()
