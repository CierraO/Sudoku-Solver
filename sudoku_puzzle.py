class SudokuPuzzle:

    def __init__(self, board):
        self.board = board
        self.length = board.size

    def get_solution(self, algorithm):
        """Gets a valid board with all positions filled in, plus the end node, using the specified algorithm.
        The end node allows for tracing the steps of the solution."""
        pass

    def step_through(self, algorithm):
        """Displays the next step of the solution. Calls get_solution and uses the end node."""
        pass

    def find_blank_square(self):
        """Returns the position of the first blank square in the board.
        If no squares are blank, returns false."""
        square = False

        for row in range(self.length):
            for col in range(self.length):
                if self.board[row][col] == 0:
                    square = (row, col)
                    break

        return square

    def get_valid_numbers(self, square):
        """Gets the valid numbers that can be placed in this square.
        square is a tuple (row, col)."""
        valid_numbers = []
        for i in range(1, self.length+1):
            valid = True
            # Check if unique in column
            for row in range(self.length):
                if self.board[row][square[1]] == i:
                    valid = False
                    break
            # Check if unique in row
            for col in range(self.length):
                if self.board[square[0]][col] == i:
                    valid = False
                    break
            # Check if unique in square
            start_row = (square[0] // 3) * 3
            start_col = (square[1] // 3) * 3
            for j in range(3):
                for k in range(3):
                    if self.board[start_row + j][start_col + k] == i:
                        valid = False
                        break

            if valid:
                valid_numbers.append(i)

        return valid_numbers

    def is_complete(self):
        """Checks if there are no empty squares on the board."""
        for row in range(self.length):
            for col in range(self.length):
                if not self.board[row][col]:
                    return False

        return True
