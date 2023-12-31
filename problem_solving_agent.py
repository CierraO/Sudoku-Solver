"""The MIT License (MIT)

Copyright (c) 2016 aima-python contributors

Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE."""
from enum import Enum

from utils import *

import numpy as np

import scipy as sp

import copy


class Problem:
    """The abstract class for a formal problem. You should subclass
    this and implement the methods actions and result, and possibly
    __init__, goal_test, and path_cost. Then you will create instances
    of your subclass and solve them with the various search functions."""

    def __init__(self, initial, goal=None):
        """The constructor specifies the initial state, and possibly a goal
        state, if there is a unique goal. Your subclass's constructor can add
        other arguments."""
        self.initial = initial
        self.goal = goal

    def actions(self, state):
        """Return the actions that can be executed in the given
        state. The result would typically be a list, but if there are
        many actions, consider yielding them one at a time in an
        iterator, rather than building them all at once."""
        raise NotImplementedError

    def result(self, state, action):
        """Return the state that results from executing the given
        action in the given state. The action must be one of
        self.actions(state)."""
        raise NotImplementedError

    def goal_test(self, state):
        """Return True if the state is a goal. The default method compares the
        state to self.goal or checks for state in self.goal if it is a
        list, as specified in the constructor. Override this method if
        checking against a single self.goal is not enough."""
        if isinstance(self.goal, list):
            return is_in(state, self.goal)
        else:
            return state == self.goal

    def path_cost(self, c, state1, action, state2):
        """Return the cost of a solution path that arrives at state2 from
        state1 via action, assuming cost c to get up to state1. If the problem
        is such that the path doesn't matter, this function will only look at
        state2. If the path does matter, it will consider c and maybe state1
        and action. The default method costs 1 for every step in the path."""
        return c + 1

    def value(self, state):
        """For optimization problems, each state has a value. Hill Climbing
        and related algorithms try to maximize this value."""
        raise NotImplementedError


class SudokuProblem(Problem):
    """The problem of searching for a valid sudoku board."""

    def __init__(self, puzzle):
        super().__init__(puzzle.board)
        self.puzzle = puzzle

    def actions(self, board):
        """The actions at a board configuration are the valid numbers
        that can be placed in the next empty square."""
        square = self.puzzle.find_blank_square(board)
        if not square:
            return []

        return self.puzzle.get_valid_numbers(square, board)

    def result(self, board, number):
        """The result of entering a number is the board with that number
        in the first empty spot."""
        square = self.puzzle.find_blank_square(board)
        new_board = [[board[x][y] for y in range(len(board[0]))] for x in range(len(board))]
        new_board[square[0]][square[1]] = number
        return new_board

    def goal_test(self, board):
        """The goal is to have a board with no empty spots."""
        return self.puzzle.is_complete(board)

    def h(self, node):
        return 1


class SudokuSinglesProblem(SudokuProblem):
    """The problem of searching for a valid sudoku board using singles techniques."""

    def actions(self, board):
        """An action is a (square, number) pair.
        The actions at a board configuration are the valid numbers
        that can be placed in the next empty square OR in a full house,
        hidden single, or naked single; as well as the coords of the square
        represented as a tuple (row, col)."""
        def create_actions_list(coords, numbers):
            actions_list = []
            for number in numbers:
                actions_list.append((coords, number))
            return actions_list

        # Check for full house
        board_len = self.puzzle.length
        if board_len == 12:
            rows_per_sq = 3
            cols_per_sq = int(board_len / 3)
        else:
            rows_per_sq = int(board_len / 3)
            cols_per_sq = 3
        sq_rows = int(board_len / rows_per_sq)  # number of rows of subsquares
        sq_cols = int(board_len / cols_per_sq)  # number of cols of subsquares

        for row_of_sq in range(sq_rows):  # for every row of subsquares
            for col_of_sq in range(sq_cols):  # for every subsquare in that row
                empty_cells = []
                # If there is only one empty square in this subsquare, it's a full house
                for i in range(row_of_sq * rows_per_sq, row_of_sq * rows_per_sq + row_of_sq):
                    for j in range(col_of_sq * cols_per_sq, col_of_sq * cols_per_sq + col_of_sq):
                        if board[i][j] == 0:
                            empty_cells.append((i, j))
                            if len(empty_cells) > 1:
                                break
                    if len(empty_cells) > 1:
                        break

                if len(empty_cells) == 1:
                    return create_actions_list(empty_cells[0], self.puzzle.get_valid_numbers(empty_cells[0], board))

        # Check for naked singles
        for row in range(board_len):
            for col in range(board_len):
                # If there is only one possible action in a square, use that
                if board[row][col] == 0:
                    valid_nums = self.puzzle.get_valid_numbers((row, col), board)
                    if len(valid_nums) == 1:
                        return create_actions_list((row, col), valid_nums)

        # If all else fails, move to next blank square and find all valid numbers
        return create_actions_list(self.puzzle.find_blank_square(board), super().actions(board))

    def result(self, board, action):
        """The result of entering a number in the given square
         is the board with that number inserted into that square."""
        square = action[0]
        number = action[1]
        new_board = [[board[x][y] for y in range(len(board[0]))] for x in range(len(board))]
        new_board[square[0]][square[1]] = number
        return new_board


# ______________________________________________________________________________


class Node:
    """A node in a search tree. Contains a pointer to the parent (the node
    that this is a successor of) and to the actual state for this node. Note
    that if a state is arrived at by two paths, then there are two nodes with
    the same state. Also includes the action that got us to this state, and
    the total path_cost (also known as g) to reach the node. Other functions
    may add an f and h value; see best_first_graph_search and astar_search for
    an explanation of how the f and h values are handled. You will not need to
    subclass this class."""

    def __init__(self, state, parent=None, action=None, path_cost=0):
        """Create a search tree Node, derived from a parent by an action."""
        self.state = state
        self.parent = parent
        self.action = action
        self.path_cost = path_cost
        self.depth = 0
        if parent:
            self.depth = parent.depth + 1

    def __repr__(self):
        return "<Node {}>".format(self.state)

    def __lt__(self, node):
        return self.state < node.state

    def expand(self, problem):
        """List the nodes reachable in one step from this node."""
        return [self.child_node(problem, action)
                for action in problem.actions(self.state)]

    def child_node(self, problem, action):
        """[Figure 3.10]"""
        next_state = problem.result(self.state, action)
        next_node = Node(next_state, self, action, problem.path_cost(self.path_cost, self.state, action, next_state))
        return next_node

    def solution(self):
        """Return the sequence of actions to go from the root to this node."""
        return [node.action for node in self.path()[1:]]

    def path(self):
        """Return a list of nodes forming the path from the root to this node."""
        node, path_back = self, []
        while node:
            path_back.append(node)
            node = node.parent
        return list(reversed(path_back))

    # We want for a queue of nodes in breadth_first_graph_search or
    # astar_search to have no duplicated states, so we treat nodes
    # with the same state as equal. [Problem: this may not be what you
    # want in other contexts.]

    def __eq__(self, other):
        return isinstance(other, Node) and self.state == other.state

    def __hash__(self):
        # We use the hash value of the state
        # stored in the node instead of the node
        # object itself to quickly search a node
        # with the same state in a Hash Table
        return hash(self.state)


# ______________________________________________________________________________


class SimpleProblemSolvingAgent:
    """
    [Figure 3.1]
    Abstract framework for a problem-solving agent.
    """

    def __init__(self, problem):
        """State is an abstract representation of the state
        of the world, and seq is the list of actions required
        to get to a particular state from the initial state(root)."""
        self.problem = problem
        self.state = problem.initial
        self.seq = []

    def __call__(self, percept):
        """[Figure 3.1] Formulate a goal and problem, then
        search for a sequence of actions to solve it."""
        self.state = self.update_state(self.state, percept)
        if not self.seq:
            goal = self.formulate_goal(self.state)
            problem = self.formulate_problem(self.state, goal)
            self.seq = self.search(problem)
            if not self.seq:
                return None
        return self.seq.pop(0)

    def update_state(self, state, percept):
        raise NotImplementedError

    def formulate_goal(self, state):
        raise NotImplementedError

    def formulate_problem(self, state, goal):
        raise NotImplementedError

    def search(self, algorithm):
        raise NotImplementedError


class SudokuAgent(SimpleProblemSolvingAgent):
    """A problem-solving agent to find solutions to sudoku puzzles.
        It is assumed that the given problem is a SudokuProblem."""

    def update_state(self, state, percept):
        return percept

    def formulate_goal(self, state):
        goal = self.problem.goal
        return goal

    def formulate_problem(self, state, goal):
        problem = self.problem.initial
        return problem

    def search(self, algorithm):
        match algorithm:
            case Algorithms.DEPTH_FIRST.value:
                goal_node = depth_first_tree_search(self.problem)
            case Algorithms.SIMPLEX.value:
                goal_node = simplex_search(self.problem)
            case Algorithms.NAKED_SINGLES.value:
                if type(self.problem) is not SudokuSinglesProblem:
                    singles_problem = SudokuSinglesProblem(self.problem.puzzle)
                    self.problem = singles_problem
                goal_node = depth_first_tree_search(self.problem)
            case _:
                goal_node = depth_first_tree_search(self.problem)

        return goal_node


# ______________________________________________________________________________
# Search Algorithms

class Algorithms(Enum):
    DEPTH_FIRST = 0
    SIMPLEX = 1
    NAKED_SINGLES = 2


def depth_first_tree_search(problem):
    """
    [Figure 3.7]
    Search the deepest nodes in the search tree first.
    Search through the successors of a problem to find a goal.
    The argument frontier should be an empty queue.
    Repeats infinitely in case of loops.
    """

    frontier = [Node(problem.initial)]  # Stack

    while frontier:
        node = frontier.pop()
        if problem.goal_test(node.state):
            return node
        frontier.extend(node.expand(problem))
    return None


def simplex_search(problem):
    """
    Uses linear programming to find solution to the Sudoku puzzle
    """
    if len(problem.initial) == 9:
        matrix = np.zeros((324, 729))
        for i in range(9):  # Inequalities for rows
            for j in range(9):
                for k in range(9):
                    matrix[9 * i + j][k + 9 * j + 81 * i] = 1
        for i in range(9):  # Inequalities for columns
            for k in range(9):
                for j in range(9):
                    matrix[9 * i + k + 81][k + 9 * j + 81 * i] = 1
        for j in range(9):  # Inequalities for 3d rows (z-axis)
            for k in range(9):
                for i in range(9):
                    matrix[9 * j + k + 162][k + 9 * j + 81 * i] = 1
        for n in range(9):
            for k in range(9):
                for x in [0, 9, 18, 81, 90, 99, 162, 171, 180]:
                    matrix[9 * n + k + 243][x + k + 27 * (n % 3) + 243 * (n // 3)] = 1
        b = np.full(324, 1).transpose()
        bound_list = [(0, 1) for _ in range(729)]
        for x in range(9):
            for y in range(9):
                if problem.initial[x][y] != 0:
                    bound_list[9*(9*x + y) + problem.initial[x][y] - 1] = (1, 1)
        result = sp.optimize.linprog(c=np.ones(729), A_eq=matrix, b_eq=b, bounds=bound_list, integrality=1, method='highs')
        result.x = np.round(result.x)
        output = np.reshape([np.where(row == 1)[0] + 1 for row in np.reshape(result.x, (81, 9))], (9, 9))
    elif len(problem.initial) == 6:  # board is 6x6
        matrix = np.zeros((144, 216))
        for i in range(6):  # Inequalities for rows
            for j in range(6):
                for k in range(6):
                    matrix[6 * i + j][k + 6 * j + 36 * i] = 1
        for i in range(6):  # Inequalities for columns
            for k in range(6):
                for j in range(6):
                    matrix[6 * i + k + 36][k + 6 * j + 36 * i] = 1
        for j in range(6):  # Inequalities for 3d rows (z-axis)
            for k in range(6):
                for i in range(6):
                    matrix[6 * j + k + 72][k + 6 * j + 36 * i] = 1
        for n in range(6):
            for k in range(6):
                for x in [0, 6, 12, 36, 42, 48]:
                    matrix[6 * n + k + 108][x + k + 18 * (n % 3) + 108 * (n // 3)] = 1
        b = np.full(144, 1).transpose()
        bound_list = [(0, 1) for _ in range(216)]
        for x in range(6):
            for y in range(6):
                if problem.initial[x][y] != 0:
                    bound_list[6 * (6 * x + y) + problem.initial[x][y] - 1] = (1, 1)
        result = sp.optimize.linprog(c=np.ones(216), A_eq=matrix, b_eq=b, bounds=bound_list, integrality=1, method='highs')
        result.x = np.round(result.x)
        output = np.reshape([np.where(row == 1)[0] + 1 for row in np.reshape(result.x, (36, 6))], (6, 6))
    elif len(problem.initial) == 12:  # board is 12x12
        matrix = np.zeros((576, 1728))
        for i in range(12):  # Inequalities for rows
            for j in range(12):
                for k in range(12):
                    matrix[12 * i + j][k + 12 * j + 144 * i] = 1
        for i in range(12):  # Inequalities for columns
            for k in range(12):
                for j in range(12):
                    matrix[12 * i + k + 144][k + 12 * j + 144 * i] = 1
        for j in range(12):  # Inequalities for 3d rows (z-axis)
            for k in range(12):
                for i in range(12):
                    matrix[12 * j + k + 288][k + 12 * j + 144 * i] = 1
        for n in range(12):
            for k in range(12):
                for x in [0, 12, 24, 36, 144, 156, 168, 180, 288, 300, 312, 324]:
                    matrix[12 * n + k + 432][x + k + 48 * (n % 3) + 432 * (n // 4)] = 1
        b = np.full(576, 1).transpose()
        bound_list = [(0, 1) for _ in range(1728)]
        for x in range(12):
            for y in range(12):
                if problem.initial[x][y] != 0:
                    bound_list[12 * (12 * x + y) + problem.initial[x][y] - 1] = (1, 1)
        result = sp.optimize.linprog(c=np.ones(1728), A_eq=matrix, b_eq=b, bounds=bound_list, integrality=1, method='highs')
        result.x = np.round(result.x)
        output = np.reshape([np.where(row == 1)[0] + 1 for row in np.reshape(result.x, (144, 12))], (12, 12))
    # create list of nodes
    start_board = copy.deepcopy(problem.initial)
    parent = Node(problem.initial)
    start_board_ones = np.where(start_board > 0, 0, 1)
    board_with_filled_in_values = np.multiply(start_board_ones, output)
    cur_board = Node(output)
    for x_value in range(len(start_board_ones)):
        for y_value in range(len(start_board_ones)):
            if board_with_filled_in_values[x_value][y_value] > 0:
                start_board[x_value][y_value] = board_with_filled_in_values[x_value][y_value]
                for row in range(len(start_board)):
                    start_board[row] = list(start_board[row])
                cur_board = Node(list(start_board), parent)
                parent = copy.deepcopy(cur_board)
    return cur_board
