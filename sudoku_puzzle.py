import numpy

from problem_solving_agent import SudokuProblem, SudokuAgent


class SudokuPuzzle:

    def __init__(self, board):
        self.board = board
        self.solutions = [None, None, None]
        self.length = numpy.size(board, 0)
        self.step = 1

    def get_solution(self, algorithm=0, time_test=False):
        """Gets a valid board with all positions filled in, plus the end node, using the specified algorithm.
        The end node allows for tracing the steps of the solution. If there is no solution, return False.
        The time_test parameter indicates whether the function is being called to test how long it takes
        the given algorithm to solve the puzzle."""
        # If this is a time test, clear the "cache" so that the solution must be re-computed
        if time_test:
            self.solutions[algorithm] = None

        self.step = 1  # reset the step-through

        # If the solution has already been found, no need to re-compute it
        if self.solutions[algorithm]:
            return self.solutions[algorithm].state, self.solutions[algorithm]

        problem = SudokuProblem(self)
        agent = SudokuAgent(problem)
        self.solutions[algorithm] = agent.search(algorithm)
        if self.solutions[algorithm]:
            return self.solutions[algorithm].state, self.solutions[algorithm]
        else:
            return False

    def step_through(self, algorithm=0):
        """Returns the next step of the solution in the form of a board,
        as well as the position of the newly-added number. If there are
        no remaining steps, returns False."""
        if not self.solutions[algorithm]:
            self.get_solution(algorithm)
        path = self.solutions[algorithm].path()

        if self.step < len(path):
            next_step = path[self.step]
            self.step += 1
            if type(next_step.action) is int or next_step.action is None:
                new_num = self.find_blank_square(next_step.parent.state)
            else:
                new_num = next_step.action[0]

            return next_step.state, new_num
        self.step = 1
        return False, False

    def find_blank_square(self, bd=None):
        """Returns the position of the first blank square in the board as a tuple.
        If no squares are blank, returns False."""
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
            if self.length == 12:
                rows_per_sq = 3
                cols_per_sq = int(self.length / 3)
            else:
                rows_per_sq = int(self.length / 3)
                cols_per_sq = 3
            start_row = (square[0] // rows_per_sq) * rows_per_sq
            start_col = (square[1] // cols_per_sq) * cols_per_sq
            for j in range(rows_per_sq):
                for k in range(cols_per_sq):
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
