import numpy

from problem_solving_agent import SudokuProblem, SudokuAgent


class SudokuPuzzle:

    def __init__(self, board):
        self.board = board
        self.solution_node = None
        self.length = numpy.size(board, 0)
        self.step = 1

    def get_solution(self, algorithm=None):
        """Gets a valid board with all positions filled in, plus the end node, using the specified algorithm.
        The end node allows for tracing the steps of the solution. If there is no solution, return False."""
        self.step = 1  # reset the step-through
        problem = SudokuProblem(self)
        agent = SudokuAgent(problem)
        self.solution_node = agent.search(algorithm)
        if self.solution_node:
            return self.solution_node.state, self.solution_node
        else:
            return False

    def step_through(self, algorithm=None):
        """Returns the next step of the solution in the form of a board,
        as well as the position of the newly-added number. If there are
        no remaining steps, returns False."""
        if not self.solution_node:
            self.get_solution(algorithm)
        path = self.solution_node.path()

        if self.step < len(path):
            next_step = path[self.step]
            self.step += 1
            return next_step.state, self.find_blank_square(next_step.parent.state)

        return False

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
