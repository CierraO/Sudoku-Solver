"""The MIT License (MIT)

Copyright (c) 2016 aima-python contributors

Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE."""
from enum import Enum

from utils import *

import numpy as np

import scipy as sp


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
        algorithm = Algorithms(algorithm)
        match algorithm:
            case Algorithms.DEPTH_FIRST:
                goal_node = depth_first_tree_search(self.problem)
            case Algorithms.SIMPLEX:
                goal_node = simplex_search(self.problem)
            case Algorithms.LAST_BOX:
                raise NotImplementedError
            case Algorithms.A_STAR:
                raise NotImplementedError
            case _:
                goal_node = depth_first_tree_search(self.problem)

        return goal_node


# ______________________________________________________________________________
# Search Algorithms

class Algorithms(Enum):
    DEPTH_FIRST = 0
    SIMPLEX = 1
    LAST_BOX = 2
    A_STAR = 3


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
        output = Node(output.tolist())
    elif len(problem.initial) == 6:  # board is 6x6
        matrix = np.zeros((, 216))
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
                    matrix[6 * j + k + 162][k + 6 * j + 36 * i] = 1
        for n in range(6):
            for k in range(6):
                for x in [0, 6, 12, 36, 42, 48]:
                    matrix[9 * n + k + 243][x + k + 27 * (n % 3) + 243 * (n // 3)] = 1
        b = np.full(, 1).transpose()
        bound_list = [(0, 1) for _ in range(216)]
        for x in range(6):
            for y in range(6):
                if problem.initial[x][y] != 0:
                    bound_list[6 * (6 * x + y) + problem.initial[x][y] - 1] = (1, 1)
        result = sp.optimize.linprog(c=np.ones(216), A_eq=matrix, b_eq=b, bounds=bound_list, integrality=1, method='highs')
        result.x = np.round(result.x)
        output = np.reshape([np.where(row == 1)[0] + 1 for row in np.reshape(result.x, (36, 6))], (6, 6))
        output = Node(output.tolist())
    elif len(problem.initial) == 12:  # board is 12x12
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
                    bound_list[9 * (9 * x + y) + problem.initial[x][y] - 1] = (1, 1)
        result = sp.optimize.linprog(c=np.ones(729), A_eq=matrix, b_eq=b, bounds=bound_list, integrality=1,
                                     method='highs')
        result.x = np.round(result.x)
        output = np.reshape([np.where(row == 1)[0] + 1 for row in np.reshape(result.x, (81, 9))], (9, 9))
        output = Node(output.tolist())
    return output


def best_first_graph_search(problem, f, display=False):
    """Search the nodes with the lowest f scores first.
    You specify the function f(node) that you want to minimize; for example,
    if f is a heuristic estimate to the goal, then we have greedy best
    first search; if f is node.depth then we have breadth-first search.
    There is a subtlety: the line "f = memoize(f, 'f')" means that the f
    values will be cached on the nodes as they are computed. So after doing
    a best first search you can examine the f values of the path returned."""
    f = memoize(f, 'f')
    node = Node(problem.initial)
    frontier = PriorityQueue('min', f)
    frontier.append(node)
    explored = set()
    while frontier:
        node = frontier.pop()
        if problem.goal_test(node.state):
            if display:
                print(len(explored), "paths have been expanded and", len(frontier), "paths remain in the frontier")
            return node
        explored.add(node.state)
        for child in node.expand(problem):
            if child.state not in explored and child not in frontier:
                frontier.append(child)
            elif child in frontier:
                if f(child) < frontier[child]:
                    del frontier[child]
                    frontier.append(child)
    return None


def astar_search(problem, h=None, display=False):
    """A* search is best-first graph search with f(n) = g(n)+h(n).
    You need to specify the h function when you call astar_search, or
    else in your Problem subclass."""
    h = memoize(h or problem.h, 'h')
    return best_first_graph_search(problem, lambda n: n.path_cost + h(n), display)
