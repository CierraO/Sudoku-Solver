import pygame
import numpy
#import requests

# set window pane properties
WIDTH = 550
background_color = (251, 247, 245)

grid_original_colour = (52, 31, 151)

'''
get fucked, trying to get an api to write out starting stuff. couldn't get one working :(
# sudoku game api variables
response = requests.get("https://sugoku.herokuapp.com/board?difficulty=easy")
grid = response.json()['board']
'''

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


def main():
    pygame.init()
    win = pygame.display.set_mode((WIDTH, WIDTH))
    pygame.display.set_caption("Sudoku")
    win.fill(background_color)
    Font = pygame.font.SysFont('Comic Sans MS', 35)

    # sets up the board
    board(win)

    # populate board with starting numbers
    for i in range(0, len(grid[0])):
        for j in range(0, len(grid[0])):
            if 0 < grid[i][j] < 10:
                value = Font.render(str(grid[i][j]), True, grid_original_colour)

                # add to screen with blit
                win.blit(value, ((j + 1) * 50 + 15, (i + 1) * 50 + 15))
                pygame.display.update()

    # kill program condition
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return


# helper function
# fill board with starting game
def starter():
    return


# helper function
# draws the basic game board
def board(win):
    # bolded sectors
    for i in range(4):
        # vertical bold lines
        pygame.draw.line(win,
                         (0, 0, 0),
                         (50 + 50 * i * 3, 50),
                         (50 + 50 * i * 3, 500),
                         4)

        # bold horizontal lines
        pygame.draw.line(win,
                         (0, 0, 0),
                         (50, 50 + 50 * i * 3),
                         (500, 50 + 50 * i * 3),
                         4)

    for i in range(10):
        print(i)

        # vertical lines
        pygame.draw.line(win,
                         (0, 0, 0),
                         (50 + 50 * i, 50),
                         (50 + 50 * i, 500),
                         1)

        # horizontal lines
        pygame.draw.line(win,
                         (0, 0, 0),
                         (50, 50 + 50 * i),
                         (500, 50 + 50 * i),
                         1)

    return pygame.display.update()


# game entry point
if __name__ == "__main__":
    main()
