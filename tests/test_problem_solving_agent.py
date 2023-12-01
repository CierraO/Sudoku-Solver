import numpy
import unittest

from sudoku_puzzle import SudokuPuzzle


class TestAlgorithms(unittest.TestCase):
    def test_something(self):
        board = numpy.array([[0, 0, 0, 2, 6, 0, 7, 0, 1],
                             [6, 8, 0, 0, 7, 0, 0, 9, 0],
                             [1, 9, 0, 0, 0, 4, 5, 0, 0],
                             [8, 2, 0, 1, 0, 0, 0, 4, 0],
                             [0, 0, 4, 6, 0, 2, 9, 0, 0],
                             [0, 5, 0, 0, 0, 3, 0, 2, 8],
                             [0, 0, 9, 3, 0, 0, 0, 7, 4],
                             [0, 4, 0, 0, 5, 0, 0, 3, 6],
                             [7, 0, 3, 0, 1, 8, 0, 0, 0]])
        puzzle = SudokuPuzzle(board)
        final_node = puzzle.get_solution()

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

        algo_solution = final_node.state
        for row in range(9):
            for col in range(9):
                self.assertEqual(solution[row][col], algo_solution[row][col])


if __name__ == '__main__':
    unittest.main()
