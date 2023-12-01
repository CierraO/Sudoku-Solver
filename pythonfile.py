import pygame
import numpy
from ui_elements import Button, OptionBox

pygame.font.init()

# import requests

# starting parameters
WIDTH = 800
background_color = (251, 247, 245)
grid_original_colour = (52, 31, 151)

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
print(grid)
print(grid_original)

# ^^has to be made this way as direct assigning variables
# are just references to original, ie, completely connected to changes
clock = pygame.time.Clock()
win = pygame.display.set_mode((WIDTH, WIDTH))
win.fill(background_color)


# load all button images
gen_button_img = pygame.image.load('resources/button_generate_updated.png').convert_alpha()
sol_Button_img = pygame.image.load('resources/button_solve_updated.png').convert_alpha()
stp_Button_img = pygame.image.load('resources/button_step.png').convert_alpha()

# create button instances
gen_button = Button(75, 525, gen_button_img, 1)
sol_button = Button(75, 580, sol_Button_img, 1)
stp_button = Button(330, 580, stp_Button_img, 1)

# create option box instances
list1 = OptionBox(550, 300, 160, 40, (150, 150, 150), (100, 200, 255), pygame.font.SysFont('Comic Sans MS', 30),
                  ["5x5", "9x9", "12x12"])
list2 = OptionBox(550, 350, 160, 40, (150, 150, 150), (100, 200, 255), pygame.font.SysFont('Comic Sans MS', 25),
                  ["Dijkstra", "Last Box", "A Star"])


def main():
    pygame.init()
    pygame.display.set_caption("Sudoku")
    Font = pygame.font.SysFont('Comic Sans MS', 35)

    # sets up the board
    board(win)

    # populate board with starting numbers
    for i in range(0, len(grid[0])):
        for j in range(0, len(grid[0])):
            if 0 < grid[i][j] < 10:
                value = Font.render(str(grid[i][j]), True, grid_original_colour)

                # add to screen with blit
                win.blit(value, ((j + 1) * 50 + 15, (i + 0.75) * 50 + 15))
                pygame.display.update()

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
        if stp_button.draw(win):
            print("Next Step is...")

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


# game entry point
if __name__ == "__main__":
    main()
