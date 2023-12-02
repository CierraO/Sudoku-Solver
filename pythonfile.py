import pygame
import numpy

from sudoku_puzzle import SudokuPuzzle
from ui_elements import Button, OptionBox

pygame.font.init()

# import requests

# starting parameters
WIDTH = 800
background_color = (251, 247, 245)
grid_original_colour = (52, 31, 151)
Font = pygame.font.SysFont('Comic Sans MS', 35)

grid = numpy.array([
    [2, 0, 0, 0, 0, 0, 0, 0, 0],
    [1, 0, 0, 2, 0, 6, 7, 0, 0],
    [0, 0, 0, 3, 0, 8, 0, 0, 4],
    [0, 0, 2, 4, 0, 5, 8, 0, 7],
    [0, 5, 0, 7, 0, 9, 0, 1, 3],
    [0, 0, 0, 1, 0, 0, 0, 5, 6],
    [0, 2, 1, 6, 0, 4, 9, 0, 0],
    [0, 0, 0, 5, 9, 0, 3, 0, 1],
    [0, 0, 0, 8, 1, 0, 5, 4, 0]])

grid_original = [[grid[x][y] for y in range(len(grid[0]))] for x in range(len(grid))]
clue_positions = [(x, y) for x in range(len(grid[0])) for y in range(len(grid[0])) if grid[x][y] != 0]
print(grid)
print(grid_original)
# Ideally, creating a puzzle object will be handled by a puzzle generator class in the future
puzzle = SudokuPuzzle(grid)

# ^^has to be made this way as direct assigning variables
# are just references to original, ie, completely connected to changes
clock = pygame.time.Clock()
win = pygame.display.set_mode((WIDTH, WIDTH))
win.fill(background_color)

# load all button images
gen_button_img = pygame.image.load('resources/button_generate.png').convert_alpha()
sol_Button_img = pygame.image.load('resources/button_solve-3.png').convert_alpha()
stp_Button_img = pygame.image.load('resources/button_step-3.png').convert_alpha()

# create button instances
gen_button = Button(100, 550, gen_button_img, 1)
sol_button = Button(100, 605, sol_Button_img, 1)
stp_button = Button(225, 605, stp_Button_img, 1)
# create option box instances
list1 = OptionBox(550, 300, 160, 40, (150, 150, 150), (100, 200, 255), pygame.font.SysFont('Comic Sans MS', 30),
                  ["5x5", "9x9", "12x12"])
list2 = OptionBox(550, 350, 160, 40, (150, 150, 150), (100, 200, 255), pygame.font.SysFont('Comic Sans MS', 25),
                  ["Dijkstra", "Last Box", "A Star"])


def main():

    pygame.init()
    pygame.display.set_caption("Sudoku")

    # sets up the board
    board(win)

    # populate board with starting numbers
    populate_board(grid)

    run = True
    while run:
        clock.tick(60)
        event_list = pygame.event.get()

        for event in event_list:
            if event.type == pygame.QUIT:
                run = False

        # checks if boxes are highlighted
        selected_option_grid = list1.update(event_list)
        selected_option_algo = list2.update(event_list)

        if selected_option_grid >= 0:
            print("Grid Option: ", selected_option_grid)

        if selected_option_algo >= 0:
            print("Algo Option: ", selected_option_algo)

        # win.fill((255, 255, 255))

        # draw buttons and functionality
        if gen_button.draw(win):
            print("Generating Puzzle...")
        if sol_button.draw(win):
            print('Solving Puzzle...')
            if puzzle.get_solution()[1]:
                populate_board(puzzle.get_solution()[0])

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

        # draws rectangles to hide the option box options
        pygame.draw.rect(win, (251, 247, 245), pygame.Rect(550, 340, 160, 120))
        pygame.draw.rect(win, (251, 247, 245), pygame.Rect(550, 390, 160, 120))
        # draws options boxes
        list2.draw(win)
        list1.draw(win)

        pygame.display.flip()

    pygame.quit()
    exit()


# helper function
# fill board with starting game
def starter():
    return


# helper function
# draws the basic game board
def board(window):
    # bolded sectors
    for i in range(4):
        # vertical bold lines
        pygame.draw.line(window,
                         (0, 0, 0),
                         (50 + 50 * i * 3, 50),
                         (50 + 50 * i * 3, 500),
                         4)

        # bold horizontal lines
        pygame.draw.line(window,
                         (0, 0, 0),
                         (50, 50 + 50 * i * 3),
                         (500, 50 + 50 * i * 3),
                         4)

    for i in range(10):
        print(i)

        # vertical lines
        pygame.draw.line(window,
                         (0, 0, 0),
                         (50 + 50 * i, 50),
                         (50 + 50 * i, 500),
                         1)

        # horizontal lines
        pygame.draw.line(window,
                         (0, 0, 0),
                         (50, 50 + 50 * i),
                         (500, 50 + 50 * i),
                         1)

    return pygame.display.update()


def populate_board(g, new_num=None):
    """Populate the sudoku board with numbers from the given grid."""
    for i in range(0, len(g[0])):
        for j in range(0, len(g[0])):
            if 0 < g[i][j] < 10:
                if (i, j) in clue_positions:
                    value = Font.render(str(g[i][j]), True, (0, 0, 0))
                elif (i, j) == new_num:
                    value = Font.render(str(g[i][j]), True, (255, 0, 0))
                else:
                    value = Font.render(str(g[i][j]), True, grid_original_colour)

                # add to screen with blit
                win.blit(value, ((j + 1) * 50 + 15, (i + 0.75) * 50 + 15))
                pygame.display.update()


def clear_board():
    win.fill(background_color)
    board(win)


# game entry point
if __name__ == "__main__":
    main()
