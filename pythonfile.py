import random

import pygame
import numpy

from ui_elements import Button, OptionBox

pygame.font.init()

# import requests

# starting parameters
WIDTH = 1000
background_color = (251, 247, 245)
grid_original_color = (52, 31, 151)

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
gen_button = Button(100, 770, gen_button_img, 1)
sol_button = Button(100, 825, sol_Button_img, 1)
stp_button = Button(225, 825, stp_Button_img, 1)
# create option box instances
list1 = OptionBox(700, 400, 160, 40, (150, 150, 150), (100, 200, 255), pygame.font.SysFont('Comic Sans MS', 30),
                  ["6x6", "9x9", "12x12"])
list2 = OptionBox(700, 450, 160, 40, (150, 150, 150), (100, 200, 255), pygame.font.SysFont('Comic Sans MS', 25),
                  ["Dijkstra", "Last Box", "A Star"])


def main():

    pygame.init()
    pygame.display.set_caption("Sudoku")
    Font = pygame.font.SysFont('Comic Sans MS', 35)

    # initialize starting grid
    grid_9x9 = numpy.zeros((9, 9), numpy.int8)
    # populate starting grid
    grid_9x9 = populate_grid(grid_9x9)
    # sets up the starting board
    board(win, grid_9x9)
    # populate starting board with starting numbers
    for i in range(0, len(grid_9x9[0])):
        for j in range(0, len(grid_9x9[0])):
            if 0 < grid_9x9[i][j] < 10:
                value = Font.render(str(grid_9x9[i][j]), True, grid_original_color)
                # add to screen with blit
                win.blit(value, ((j + 1) * 50 + 15, (i + 0.75) * 50 + 15 + 100))
                pygame.display.flip()

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
            # board chosen to be 6x6
            if selected_option_grid == 0:
                # initialize + populate grid
                grid_6x6 = numpy.zeros((6, 6), numpy.int8)
                grid_6x6 = populate_grid(grid_6x6)
                win.fill((251, 247, 245))
                board(win, grid_6x6)
                # populate board with starting numbers
                for i in range(0, len(grid_6x6[0])):
                    for j in range(0, len(grid_6x6[0])):
                        if 0 < grid_6x6[i][j] < 10:
                            value = Font.render(str(grid_6x6[i][j]), True, grid_original_color)
                            # add to screen with blit
                            win.blit(value, ((j + 1) * 50 + 15, (i + 0.75) * 50 + 15 + 100))
                            pygame.display.flip()
            # board chosen to be 9x9
            elif selected_option_grid == 1:
                # initialize + populate grid
                grid_9x9 = numpy.zeros((9, 9), numpy.int8)
                grid_9x9 = populate_grid(grid_9x9)
                win.fill((251, 247, 245))
                board(win, grid_9x9)
                # populate board with starting numbers
                for i in range(0, len(grid_9x9[0])):
                    for j in range(0, len(grid_9x9[0])):
                        if 0 < grid_9x9[i][j] < 10:
                            value = Font.render(str(grid_9x9[i][j]), True, grid_original_color)
                            # add to screen with blit
                            win.blit(value, ((j + 1) * 50 + 15, (i + 0.75) * 50 + 15 + 100))
                            pygame.display.flip()
            # board chosen to be 12x12
            elif selected_option_grid == 2:
                # initialize + populate grid
                grid_12x12 = numpy.zeros((12, 12), numpy.int8)
                grid_12x12 = populate_grid(grid_12x12)
                win.fill((251, 247, 245))
                board(win, grid_12x12)
                # populate board with starting numbers
                for i in range(0, len(grid_12x12[0])):
                    for j in range(0, len(grid_12x12[0])):
                        if 0 < grid_12x12[i][j] < 10:
                            value = Font.render(str(grid_12x12[i][j]), True, grid_original_color)
                            # add to screen with blit
                            win.blit(value, ((j + 1) * 50 + 15, (i + 0.75) * 50 + 15 + 100))
                            pygame.display.flip()

        if selected_option_algo >= 0:
            print("Algo Option: ", selected_option_algo)

        # draw buttons and functionality
        if gen_button.draw(win):
            print("Generating Puzzle...")
        if sol_button.draw(win):
            print('Solving Puzzle...')
        if stp_button.draw(win):
            print("Next Step is...")

        # draws rectangles to hide the option box options
        pygame.draw.rect(win, (251, 247, 245), pygame.Rect(700, 440, 160, 120))
        pygame.draw.rect(win, (251, 247, 245), pygame.Rect(700, 490, 160, 120))
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
    for i in range(0, len(grid[0])):
        for j in range(0, len(grid[0])):
            new_grid[i][j] = random.randint(0, len(grid))
    return new_grid


# game entry point
if __name__ == "__main__":
    main()
