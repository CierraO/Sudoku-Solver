import random

import pygame
import numpy

from sudoku_puzzle import SudokuPuzzle
from ui_elements import Button, OptionBox, TextComment


pygame.font.init()

# starting parameters
starting_grid = []

WIDTH = 1000
background_color = (251, 247, 245)
grid_original_color = (52, 31, 151)
font = pygame.font.SysFont('Comic Sans MS', 35)

clock = pygame.time.Clock()
win = pygame.display.set_mode((WIDTH, WIDTH))
win.fill(background_color)

# load all button images
gen_button_img = pygame.image.load('resources/button_generate_updated.png').convert_alpha()
sol_Button_img = pygame.image.load('resources/button_solve_updated.png').convert_alpha()
stp_Button_img = pygame.image.load('resources/button_step.png').convert_alpha()

# create button instances

gen_button = Button(100, 770, gen_button_img, 1)
sol_button = Button(100, 825, sol_Button_img, 1)
stp_button = Button(355, 825, stp_Button_img, 1)

# create option box instances
list1 = OptionBox(700, 400, 160, 40, (150, 150, 150), (100, 200, 255), pygame.font.SysFont('Comic Sans MS', 30),
                  ["9x9", "6x6", "12x12"])
list2 = OptionBox(700, 450, 160, 40, (150, 150, 150), (100, 200, 255), pygame.font.SysFont('Comic Sans MS', 25),
                  ["DFS", "Last Box", "A Star"])
# create comment instances
title = TextComment(50, 40, "Comic Sans MS", (0, 0, 0), 40)
names1 = TextComment(55, 90, "Comic Sans MS", (0, 0, 0), 20)
names2 = TextComment(55, 115, "Comic Sans MS", (0, 0, 0), 20)


def main():
    global starting_grid

    #   current_grid = 9
    pygame.init()
    pygame.display.set_caption("Sudoku")

    #    field1 = TextField(51, 150, 50, pygame.font.SysFont("Comic Sans MS", 30))
    #    field1group = pygame.sprite.Group(field1)

    #    base_font = pygame.font.Font(None, 32)
    #    user_text = ''

    # initialize starting grid
    grid_9x9 = numpy.zeros((9, 9), numpy.int8)
    # populate starting grid
    grid_9x9 = populate_grid(grid_9x9)
    starting_grid = grid_9x9
    # Ideally, creating a puzzle object will be handled by a puzzle generator class in the future
    puzzle = SudokuPuzzle(starting_grid)

    # sets up the starting board
    board(win, starting_grid)
    populate_board(starting_grid)

    # game loop
    run = True
    while run:
        clock.tick(60)
        event_list = pygame.event.get()
        for event in event_list:
            if event.type == pygame.QUIT:
                run = False
        #            if event.type == pygame.KEYDOWN:
        #                user_text += event.unicode

        # checks if boxes are highlighted
        selected_option_grid = list1.update(event_list)
        selected_option_algo = list2.update(event_list)
        if selected_option_grid >= 0:
            print("Grid Option: ", selected_option_grid)

            # board chosen to be 6x6
            if selected_option_grid == 1:
                # initialize + populate grid
                # current_grid = 6
                grid_6x6 = numpy.zeros((6, 6), numpy.int8)
                grid_6x6 = populate_grid(grid_6x6)
                starting_grid = grid_6x6
                puzzle = SudokuPuzzle(starting_grid)
                win.fill((251, 247, 245))
                board(win, starting_grid)

                populate_board(starting_grid)

            # board chosen to be 9x9
            elif selected_option_grid == 0:
                # initialize + populate grid
                # current_grid = 9
                grid_9x9 = numpy.zeros((9, 9), numpy.int8)
                grid_9x9 = populate_grid(grid_9x9)
                starting_grid = grid_9x9
                puzzle = SudokuPuzzle(starting_grid)
                win.fill((251, 247, 245))
                board(win, starting_grid)

                populate_board(starting_grid)

            # board chosen to be 12x12
            elif selected_option_grid == 2:
                # initialize + populate grid
                grid_12x12 = numpy.zeros((12, 12), numpy.int8)
                grid_12x12 = populate_grid(grid_12x12)
                starting_grid = grid_12x12
                puzzle = SudokuPuzzle(starting_grid)
                win.fill((251, 247, 245))
                board(win, starting_grid)
                populate_board(starting_grid)

        if selected_option_algo >= 0:
            print("Algo Option: ", selected_option_algo)
        # draw buttons and functionality
        if gen_button.draw(win):
            print("Generating Puzzle...")
        if sol_button.draw(win):
            print('Solving Puzzle...')
            if puzzle.get_solution():
                populate_board(puzzle.get_solution()[0])
            print("Solved! (If possible)")

        if stp_button.draw(win):
            print("Next Step is...")
            if puzzle.step == 1:
                print("CLEARING")
                clear_board()

            g, new_num = puzzle.step_through()
            if g:
                if new_num:
                    populate_board(g, new_num)
                else:
                    populate_board(g)

        # draws comments
        title.draw(win, "The Sudoku Solver")
        names1.draw(win, "Joseph Baliestiero, Cierra O'Grady,")
        names2.draw(win, "Gibson Phillips, and Andrew Simonini")

        # draws rectangles to hide the option box options
        pygame.draw.rect(win, (251, 247, 245), pygame.Rect(700, 440, 160, 120))
        pygame.draw.rect(win, (251, 247, 245), pygame.Rect(700, 490, 160, 120))
        # draws options boxes
        list2.draw(win)
        list1.draw(win)

        #        text_surface = base_font.render(user_text, True, (0, 0, 0))
        #        win.blit(text_surface, (0,0))

        pygame.display.flip()

    #        if current_grid == 6:
    #            field1group.update(event_list)
    #            field1group.draw(win)

    pygame.quit()
    exit()


# helper function
# fill board with starting game
def starter():
    return


# helper function
# draws the basic game board, changes based on size of board requested
def board(window, grid_size):
    num_columns_rows = len(grid_size)
    # board is 9x9
    if num_columns_rows == 9:
        # bolded sectors
        for i in range(4):
            # vertical bold lines
            pygame.draw.line(window,
                             (0, 0, 0),
                             (50 + 50 * i * 3, 50 + 100),
                             (50 + 50 * i * 3, 50 * (num_columns_rows + 1) + 100),
                             4)
            # bold horizontal lines
            pygame.draw.line(window,
                             (0, 0, 0),
                             (50, 50 + 50 * i * 3 + 100),
                             (50 * (num_columns_rows + 1), 50 + 50 * i * 3 + 100),
                             4)
        # draw 1 more line than number of columns and rows
        for i in range(num_columns_rows + 1):
            # vertical lines
            pygame.draw.line(window,
                             (0, 0, 0),
                             (50 + 50 * i, 50 + 100),
                             (50 + 50 * i, 50 * (num_columns_rows + 1) + 100),
                             1)
            # horizontal lines
            pygame.draw.line(window,
                             (0, 0, 0),
                             (50, 50 + 50 * i + 100),
                             (50 * (num_columns_rows + 1), 50 + 50 * i + 100),
                             1)
    # board is 6x6
    elif num_columns_rows == 6:
        # bolded sectors
        for i in range(3):
            # vertical bold lines
            pygame.draw.line(window,
                             (0, 0, 0),
                             (50 + 50 * i * 3, 50 + 100),
                             (50 + 50 * i * 3, 50 * (num_columns_rows + 1) + 100),
                             4)
        for i in range(4):
            # bold horizontal lines
            pygame.draw.line(window,
                             (0, 0, 0),
                             (50, 50 + 50 * i * 2 + 100),
                             (50 * (num_columns_rows + 1), 50 + 50 * i * 2 + 100),
                             4)
        # draw 1 more line than number of columns and rows
        for i in range(num_columns_rows + 1):
            # vertical lines
            pygame.draw.line(window,
                             (0, 0, 0),
                             (50 + 50 * i, 50 + 100),
                             (50 + 50 * i, 50 * (num_columns_rows + 1) + 100),
                             1)
            # horizontal lines
            pygame.draw.line(window,
                             (0, 0, 0),
                             (50, 50 + 50 * i + 100),
                             (50 * (num_columns_rows + 1), 50 + 50 * i + 100),
                             1)
    # board is 12x12
    elif num_columns_rows == 12:
        # bolded sectors
        for i in range(4):
            # vertical bold lines
            pygame.draw.line(window,
                             (0, 0, 0),
                             (50 + 50 * i * 4, 50 + 100),
                             (50 + 50 * i * 4, 50 * (num_columns_rows + 1) + 100),
                             4)
        for i in range(5):
            # bold horizontal lines
            pygame.draw.line(window,
                             (0, 0, 0),
                             (50, 50 + 50 * i * 3 + 100),
                             (50 * (num_columns_rows + 1), 50 + 50 * i * 3 + 100),
                             4)
        # draw 1 more line than number of columns and rows
        for i in range(num_columns_rows + 1):
            # vertical lines
            pygame.draw.line(window,
                             (0, 0, 0),
                             (50 + 50 * i, 50 + 100),
                             (50 + 50 * i, 50 * (num_columns_rows + 1) + 100),
                             1)
            # horizontal lines
            pygame.draw.line(window,
                             (0, 0, 0),
                             (50, 50 + 50 * i + 100),
                             (50 * (num_columns_rows + 1), 50 + 50 * i + 100),
                             1)
    return pygame.display.flip()


# helper function
# fill board with random numbers
def populate_grid(grid):
    new_grid = numpy.zeros((len(grid), len(grid)), numpy.int8)
    # fill in board
    for i in range(0, len(grid[0])):
        for j in range(0, len(grid[0])):
            if random.randint(0, 10) <= 2:  # if number is 0,1,2 -> fill the space with a number
                new_grid[i][j] = random.randint(0, len(grid))
                # if the filled in non-zero number appears twice in the same row or column, remove most recent placement
                if (((numpy.sum(new_grid[i, :] == new_grid[i][j]) > 1) |
                        (numpy.sum(new_grid[:, j] == new_grid[i][j]) > 1)) &
                        (new_grid[i][j] != 0)):
                    new_grid[i][j] = 0
            # clear duplicates in the same subsection
            if len(grid) == 9:  # 9x9 grid, 3x3 subsections
                if (((numpy.sum(new_grid[:3, :3] == new_grid[i][j])) > 1) |  # top left subsection
                   ((numpy.sum(new_grid[3:6, :3] == new_grid[i][j])) > 1) |  # center left sub-section
                   ((numpy.sum(new_grid[6:9, :3] == new_grid[i][j])) > 1) |  # bottom left subsection
                   ((numpy.sum(new_grid[:3, 3:6] == new_grid[i][j])) > 1) |  # top center subsection
                   ((numpy.sum(new_grid[3:6, 3:6] == new_grid[i][j])) > 1) |  # center center subsection
                   ((numpy.sum(new_grid[6:9, 3:6] == new_grid[i][j])) > 1) |  # bottom center subsection
                   ((numpy.sum(new_grid[:3, 6:9] == new_grid[i][j])) > 1) |  # top right subsection
                   ((numpy.sum(new_grid[3:6, 6:9] == new_grid[i][j])) > 1) |  # center right subsection
                   ((numpy.sum(new_grid[6:9, 6:9] == new_grid[i][j])) > 1)):  # bottom right subsection
                    new_grid[i][j] = 0
            if len(grid) == 6:  # 6x6 grid, 3x2 subsections
                if (((numpy.sum(new_grid[:2, :2] == new_grid[i][j])) > 1) |  # top left subsection
                   ((numpy.sum(new_grid[2:4, :2] == new_grid[i][j])) > 1) |  # center left subsection
                   ((numpy.sum(new_grid[4:6, :2] == new_grid[i][j])) > 1) |  # bottom left subsection
                   ((numpy.sum(new_grid[:2, 2:4] == new_grid[i][j])) > 1) |  # top right subsection
                   ((numpy.sum(new_grid[2:4, 2:4] == new_grid[i][j])) > 1) |  # center right subsection
                   ((numpy.sum(new_grid[4:6, 2:4] == new_grid[i][j])) > 1)):  # bottom right subsection
                    new_grid[i][j] = 0
            if len(grid) == 12:  # 12x12 grid, 4x3 subsections
                if (((numpy.sum(new_grid[:3, :4] == new_grid[i][j])) > 1) |  # top left subsection
                   ((numpy.sum(new_grid[3:6, :4] == new_grid[i][j])) > 1) |  # top center left subsection
                   ((numpy.sum(new_grid[6:9, :4] == new_grid[i][j])) > 1) |  # bottom center left subsection
                   ((numpy.sum(new_grid[9:12, :4] == new_grid[i][j])) > 1) |  # bottom left subsection
                   ((numpy.sum(new_grid[:3, 4:8] == new_grid[i][j])) > 1) |  # top center subsection
                   ((numpy.sum(new_grid[3:6, 4:8] == new_grid[i][j])) > 1) |  # top center center subsection
                   ((numpy.sum(new_grid[6:9, 4:8] == new_grid[i][j])) > 1) |  # bottom center center subsection
                   ((numpy.sum(new_grid[9:12, 4:8] == new_grid[i][j])) > 1) |  # bottom center subsection
                   ((numpy.sum(new_grid[:3, 8:12] == new_grid[i][j])) > 1) |  # top right subsection
                   ((numpy.sum(new_grid[3:6, 8:12] == new_grid[i][j])) > 1) |  # top center right subsection
                   ((numpy.sum(new_grid[6:9, 8:12] == new_grid[i][j])) > 1) |  # bottom center right subsection
                   ((numpy.sum(new_grid[9:12, 8:12] == new_grid[i][j])) > 1)):  # bottom right subsection
                    new_grid[i][j] = 0
    return new_grid


def get_clue_positions():
    """Get a list of tuples containing the coords of every clue number."""
    return [(x, y) for x in range(len(starting_grid[0])) for y in range(len(starting_grid[0])) if starting_grid[x][y] != 0]


def populate_board(g, new_num=None):
    """Populate the sudoku board with numbers from the given grid."""
    for i in range(0, len(g[0])):
        for j in range(0, len(g[0])):
            if 0 < g[i][j] < 10:
                if (i, j) in get_clue_positions():
                    value = font.render(str(g[i][j]), True, (0, 0, 0))
                elif (i, j) == new_num:
                    value = font.render(str(g[i][j]), True, (255, 0, 0))
                else:
                    value = font.render(str(g[i][j]), True, grid_original_color)

                # add to screen with blit
                win.blit(value, ((j + 1) * 50 + 15, (i + 0.75) * 50 + 15 + 100))
                pygame.display.flip()


def clear_board():
    win.fill(background_color)
    board(win, starting_grid)


# game entry point
if __name__ == "__main__":
    main()
