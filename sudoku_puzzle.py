import numpy

from problem_solving_agent import SudokuProblem, SudokuAgent


class SudokuPuzzle:

    def __init__(self, board):
        self.board = board
        self.length = numpy.size(board, 0)
        self.problem = SudokuProblem(self)
        self.agent = SudokuAgent(self.problem)

    def get_solution(self, algorithm=None):
        """Gets a valid board with all positions filled in, plus the end node, using the specified algorithm.
        The end node allows for tracing the steps of the solution."""
        return self.agent.search()

    def step_through(self, algorithm):
        """Displays the next step of the solution. Calls get_solution and uses the end node."""
        pass

    def find_blank_square(self, bd=None):
        """Returns the position of the first blank square in the board as a tuple.
        If no squares are blank, returns false."""
        if bd is None:
            bd = self.board

        for row in range(self.length):
            for col in range(self.length):
                if bd[row][col] == 0:
                    return row, col

        return False

    def get_valid_numbers(self, square, bd=None):
        """Gets the valid numbers that can be placed in this square.
        square is a tuple (row, col)."""
        if bd is None:
            bd = self.board

        valid_numbers = []
        for i in range(1, self.length+1):
            valid = True
            # Check if unique in column
            for row in range(self.length):
                if bd[row][square[1]] == i:
                    valid = False
                    break
            # Check if unique in row
            for col in range(self.length):
                if bd[square[0]][col] == i:
                    valid = False
                    break
            # Check if unique in square
            start_row = (square[0] // 3) * 3
            start_col = (square[1] // 3) * 3
            for j in range(3):
                for k in range(3):
                    if bd[start_row + j][start_col + k] == i:
                        valid = False
                        break

            if valid:
                valid_numbers.append(i)

        return valid_numbers

    def is_complete(self, bd=None):
        """Checks if there are no empty squares on the board."""
        if bd is None:
            bd = self.board

        for row in range(self.length):
            for col in range(self.length):
                if not bd[row][col]:
                    return False

        return True


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