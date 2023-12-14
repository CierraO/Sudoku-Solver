import random
import time

import pygame
import numpy

from sudoku_puzzle import SudokuPuzzle
from ui_elements import Button, OptionBox, TextComment, TextField

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
sug_Button_img = pygame.image.load('resources/suggestion_button.png').convert_alpha()
ac_Button_img = pygame.image.load('resources/button_clear-all.png').convert_alpha()
x_Button_img = pygame.image.load('resources/button_x.png').convert_alpha()

# create button instances
gen_button = Button(100, 770, gen_button_img, 1)
sol_button = Button(100, 825, sol_Button_img, 1)
stp_button = Button(355, 825, stp_Button_img, 1)
sug_button = Button(660, 370, sug_Button_img, 1)
all_clear_button1 = Button(655, 800, ac_Button_img, 1)
all_clear_button2 = Button(655, 710, ac_Button_img, 1)
all_clear_button3 = Button(655, 890, ac_Button_img, 1)
single_clears = []
for i in range (0, 13):
    single_clears.append(Button(913, 523 + (30 * i), x_Button_img, 1))

# single_clear1 = Button(913, 523, x_Button_img, 1)
# single_clear2 = Button(913, 553, x_Button_img, 1)
# single_clear3 = Button(913, 583, x_Button_img, 1)
# single_clear4 = Button(913, 613, x_Button_img, 1)
# single_clear5 = Button(913, 643, x_Button_img, 1)
# single_clear6 = Button(913, 673, x_Button_img, 1)
# single_clear7 = Button(913, 703, x_Button_img, 1)
# single_clear8 = Button(913, 733, x_Button_img, 1)
# single_clear9 = Button(913, 763, x_Button_img, 1)
# single_clear10 = Button(913, 793, x_Button_img, 1)
# single_clear11 = Button(913, 823, x_Button_img, 1)
# single_clear12 = Button(913, 853, x_Button_img, 1)

# create option box instances
list1 = OptionBox(700, 150, 160, 40, (150, 150, 150), (100, 200, 255), pygame.font.SysFont('Comic Sans MS', 30),
                  ["9x9", "6x6", "12x12"])
list2 = OptionBox(700, 200, 160, 40, (150, 150, 150), (100, 200, 255), pygame.font.SysFont('Comic Sans MS', 25),
                  ["DFS", "LP", "Singles"])

# saves previously chosen grid and algorithm options
previous_grid = 0
previous_algo = 0

# create comment instances
title = TextComment(50, 40, "Comic Sans MS", (0, 0, 0), 40)
names1 = TextComment(55, 90, "Comic Sans MS", (0, 0, 0), 20)
names2 = TextComment(55, 115, "Comic Sans MS", (0, 0, 0), 20)
error_text = TextComment(100, 900, "Comic Sans MS", (255, 0, 0), 20)
suggested_algorithm_text = TextComment(660, 430, "Comic Sans MS", (0, 0, 255), 20)
dataInputTag = TextComment(655, 500, "Comic Sans MS", (0, 0, 0), 15)
warning_message1_1 = TextComment(655, 860, "Comic Sans MS", (205, 0, 0), 15)
warning_message1_2 = TextComment(655, 877, "Comic Sans MS", (205, 0, 0), 15)
warning_message2_1 = TextComment(655, 760, "Comic Sans MS", (205, 0, 0), 15)
warning_message2_2 = TextComment(655, 777, "Comic Sans MS", (205, 0, 0), 15)
warning_message3_1 = TextComment(655, 940, "Comic Sans MS", (205, 0, 0), 15)
warning_message3_2 = TextComment(655, 955, "Comic Sans MS", (205, 0, 0), 15)

# create text field instances
data_input_cols = []
data_input_groups = []
for i in range (0, 13):
    data_input_cols.append(TextField(655, 520 + (30 * i), 256, pygame.font.SysFont("Comic Sans MS", 15), False))
    data_input_groups.append(pygame.sprite.Group(data_input_cols[i]))
# dataInputCol1 = TextField(655, 520, 256, pygame.font.SysFont("Comic Sans MS", 15), False)
# dataInputCol2 = TextField(655, 550, 256, pygame.font.SysFont("Comic Sans MS", 15), False)
# dataInputCol3 = TextField(655, 580, 256, pygame.font.SysFont("Comic Sans MS", 15), False)
# dataInputCol4 = TextField(655, 610, 256, pygame.font.SysFont("Comic Sans MS", 15), False)
# dataInputCol5 = TextField(655, 640, 256, pygame.font.SysFont("Comic Sans MS", 15), False)
# dataInputCol6 = TextField(655, 670, 256, pygame.font.SysFont("Comic Sans MS", 15), False)
# dataInputCol7 = TextField(655, 700, 256, pygame.font.SysFont("Comic Sans MS", 15), False)
# dataInputCol8 = TextField(655, 730, 256, pygame.font.SysFont("Comic Sans MS", 15), False)
# dataInputCol9 = TextField(655, 760, 256, pygame.font.SysFont("Comic Sans MS", 15), False)
# dataInputCol10 = TextField(655, 790, 256, pygame.font.SysFont("Comic Sans MS", 15), False)
# dataInputCol11 = TextField(655, 820, 256, pygame.font.SysFont("Comic Sans MS", 15), False)
# dataInputCol12 = TextField(655, 850, 256, pygame.font.SysFont("Comic Sans MS", 15), False)
# dataInputGroup1 = pygame.sprite.Group(dataInputCol1)
# dataInputGroup2 = pygame.sprite.Group(dataInputCol2)
# dataInputGroup3 = pygame.sprite.Group(dataInputCol3)
# dataInputGroup4 = pygame.sprite.Group(dataInputCol4)
# dataInputGroup5 = pygame.sprite.Group(dataInputCol5)
# dataInputGroup6 = pygame.sprite.Group(dataInputCol6)
# dataInputGroup7 = pygame.sprite.Group(dataInputCol7)
# dataInputGroup8 = pygame.sprite.Group(dataInputCol8)
# dataInputGroup9 = pygame.sprite.Group(dataInputCol9)
# dataInputGroup10 = pygame.sprite.Group(dataInputCol10)
# dataInputGroup11 = pygame.sprite.Group(dataInputCol11)
# dataInputGroup12 = pygame.sprite.Group(dataInputCol12)

clickable_row9 = []
clickable_row12 = []
clickable_row6 = []


def main():
    global starting_grid
    global previous_grid
    global previous_algo

    #   current_grid = 9
    pygame.init()
    pygame.display.set_caption("Sudoku")

    # initialize starting grid
    grid_9x9 = numpy.zeros((9, 9), numpy.int8)
    # populate starting grid
    grid_9x9 = populate_grid(grid_9x9)
    starting_grid = grid_9x9
    puzzle = SudokuPuzzle(starting_grid)

    # sets up the starting board

    populate_board(starting_grid)
    grid_check = 0

    # game loop
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
            previous_grid = selected_option_grid
        if selected_option_algo >= 0:
            print("Algo Option: ", selected_option_algo)
            previous_algo = selected_option_grid
        # draw buttons and functionality
        if gen_button.draw(win):
            print("Generating Puzzle...")

            # board chosen to be 6x6
            if previous_grid == 1:
                grid_check = 1
                # initialize + populate grid
                # current_grid = 6
                grid_6x6 = numpy.zeros((6, 6), numpy.int8)
                grid_6x6 = populate_grid(grid_6x6)
                starting_grid = grid_6x6
                puzzle = SudokuPuzzle(starting_grid)
                populate_board(starting_grid)
            # board chosen to be 9x9
            elif previous_grid == 0:
                grid_check = 0
                # initialize + populate grid
                # current_grid = 9
                grid_9x9 = numpy.zeros((9, 9), numpy.int8)
                grid_9x9 = populate_grid(grid_9x9)
                starting_grid = grid_9x9
                puzzle = SudokuPuzzle(starting_grid)
                populate_board(starting_grid)
            # board chosen to be 12x12
            elif previous_grid == 2:
                grid_check = 2
                # initialize + populate grid
                grid_12x12 = numpy.zeros((12, 12), numpy.int8)
                grid_12x12 = populate_grid(grid_12x12)
                starting_grid = grid_12x12
                puzzle = SudokuPuzzle(starting_grid)

                populate_board(starting_grid)

        if selected_option_algo >= 0:
            print("Algo Option: ", selected_option_algo)
        # draw buttons and functionality
        if gen_button.draw(win):
            print("Generating Puzzle...")

            def text_input(grid_len):
                for k in range(grid_len):
                    if len(data_input_cols[j].text) > 0:
                        return True
                return False

            if grid_check == 0:
                if text_input(9):
                    value_array = []
                    raw_lists = []
                    for j in range(9):
                        raw_lists.append(data_input_cols[j])

                    for raw_list in raw_lists:
                        if len(raw_list.text) < 25 or len(raw_list.text) > 25:
                            raw_list.color = (204, 0, 0)
                            raw_list.text = "0, 0, 0, 0, 0, 0, 0, 0, 0"
                            warning_message1_1.draw(win, "Warning: All Values Not Completely Filled")
                            warning_message1_2.draw(win, "Were Replaced By 0s and Highlighted Red")

                    for raw_list in raw_lists:
                        split_list = raw_list.text.split(", ")
                        split_list = [int(single_item) for single_item in split_list]
                        value_array.append(split_list)
                    print(value_array)
                    print(grid_check)
                    starting_grid = value_array
                    populate_board(starting_grid)

            elif grid_check == 1:
                if text_input(6):
                    value_array = []
                    raw_lists = []
                    for j in range(6):
                        raw_lists.append(data_input_cols[j])

                    for raw_list in raw_lists:
                        if len(raw_list.text) < 16 or len(raw_list.text) > 16:
                            raw_list.color = (204, 0, 0)
                            raw_list.text = "0, 0, 0, 0, 0, 0"
                            warning_message2_1.draw(win, "Warning: All Values Not Completely Filled")
                            warning_message2_2.draw(win, "Were Replaced By 0s and Highlighted Red")

                    for raw_list in raw_lists:
                        split_list = raw_list.text.split(", ")
                        split_list = [int(single_item) for single_item in split_list]
                        value_array.append(split_list)
                    print(value_array)
                    print(grid_check)
                    starting_grid = value_array
                    populate_board(starting_grid)

            elif grid_check == 2:
                if text_input(12):
                    value_array = []
                    raw_lists = []
                    for j in range(12):
                        raw_lists.append(data_input_cols[j])

                    for raw_list in raw_lists:
                        if len(raw_list.text) < 37 or len(raw_list.text) > 37:
                            raw_list.color = (204, 0, 0)
                            raw_list.text = "0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0"
                            warning_message3_1.draw(win, "Warning: All Values Not Completely Filled")
                            warning_message3_2.draw(win, "Were Replaced By 0s and Highlighted Red")

                    for raw_list in raw_lists:
                        split_list = raw_list.text.split(", ")
                        split_list = [int(single_item) for single_item in split_list]
                        value_array.append(split_list)
                    print(value_array)
                    print(grid_check)
                    starting_grid = value_array
                    populate_board(starting_grid)

        if sol_button.draw(win):
            print('Solving Puzzle...')
            print(list2.selected)
            try:
                if puzzle.get_solution(list2.selected):
                    populate_board(puzzle.get_solution(list2.selected)[0])
                    print("Solved!")
                else:
                    raise Exception
            except:
                print("No Possible Solution With This Algorithm")
                error_text.draw(win, "No Possible Solution With This Algorithm")
        if stp_button.draw(win):
            try:
                print("Next Step is...")
                if puzzle.step == 1:
                    print("CLEARING")
                    clear_board()
                g, new_num = puzzle.step_through(list2.selected)
                if g:
                    if new_num:
                        populate_board(g, new_num)
                    else:
                        populate_board(g)
            except:
                print("No Possible Solution With This Algorithm")
                error_text.draw(win, "No Possible Solution With This Algorithm")

        if grid_check == 0:
            if all_clear_button1.draw(win):
                revert_text_colors()
                pygame.draw.rect(win, (251, 247, 245), pygame.Rect(655, 860, 300, 250))
                for j in range(9):
                    data_input_cols[j].text = ""
        elif grid_check == 1:
            if all_clear_button2.draw(win):
                revert_text_colors()
                pygame.draw.rect(win, (251, 247, 245), pygame.Rect(655, 760, 300, 250))
                for j in range(6):
                    data_input_cols[j].text = ""
        elif grid_check == 2:
            if all_clear_button3.draw(win):
                revert_text_colors()
                pygame.draw.rect(win, (251, 247, 245), pygame.Rect(655, 940, 300, 250))
                for j in range(12):
                    data_input_cols[j].text = ""

        tmp = 0
        if grid_check == 0:
            tmp = 9
        elif grid_check == 1:
            tmp = 6
        elif grid_check == 2:
            tmp = 12
        for j in range(0, tmp):
            if single_clears[j].draw(win):
                data_input_cols[j].color = (0, 0, 0)
                data_input_cols[j].text = ""

        # if single_clear1.draw(win):
        #     dataInputCol1.color = (0, 0, 0)
        #     dataInputCol1.text = ""
        #
        # if (single_clear2.draw(win)):
        #     dataInputCol2.color = (0, 0, 0)
        #     dataInputCol2.text = ""
        #
        # if single_clear3.draw(win):
        #     dataInputCol3.color = (0, 0, 0)
        #     dataInputCol3.text = ""
        #
        # if single_clear4.draw(win):
        #     dataInputCol4.color = (0, 0, 0)
        #     dataInputCol4.text = ""
        #
        # if single_clear5.draw(win):
        #     dataInputCol5.color = (0, 0, 0)
        #     dataInputCol5.text = ""
        #
        # if single_clear6.draw(win):
        #     dataInputCol6.color = (0, 0, 0)
        #     dataInputCol6.text = ""
        #
        # if grid_check == 0:
        #     if single_clear7.draw(win):
        #         dataInputCol7.color = (0, 0, 0)
        #         dataInputCol7.text = ""
        #
        #     if single_clear8.draw(win):
        #         dataInputCol8.color = (0, 0, 0)
        #         dataInputCol8.text = ""
        #
        #     if single_clear9.draw(win):
        #         dataInputCol9.color = (0, 0, 0)
        #         dataInputCol9.text = ""
        #
        # elif grid_check == 2:
        #     if single_clear7.draw(win):
        #         dataInputCol7.color = (0, 0, 0)
        #         dataInputCol7.text = ""
        #
        #     if single_clear8.draw(win):
        #         dataInputCol8.color = (0, 0, 0)
        #         dataInputCol8.text = ""
        #
        #     if single_clear9.draw(win):
        #         dataInputCol9.color = (0, 0, 0)
        #         dataInputCol9.text = ""
        #
        #     if single_clear10.draw(win):
        #         dataInputCol10.color = (0, 0, 0)
        #         dataInputCol10.text = ""
        #
        #     if single_clear11.draw(win):
        #         dataInputCol11.color = (0, 0, 0)
        #         dataInputCol11.text = ""
        #
        #     if single_clear12.draw(win):
        #         dataInputCol12.color = (0, 0, 0)
        #         dataInputCol12.text = ""

        # draws comments
        title.draw(win, "The Sudoku Solver")
        names1.draw(win, "Joseph Baliestiero, Cierra O'Grady,")
        names2.draw(win, "Gibson Phillips, and Andrew Simonini")

        # draws rectangles to hide the option box options
        pygame.draw.rect(win, (251, 247, 245), pygame.Rect(700, 190, 160, 120))
        pygame.draw.rect(win, (251, 247, 245), pygame.Rect(700, 240, 160, 120))

        # draws rectangle to make font all cohesive for comment
        pygame.draw.rect(win, (251, 247, 245), pygame.Rect(655, 500, 400, 20))
        dataInputTag.draw(win, "Input String of Data w/ Commas in Between")

        if sug_button.draw(win):
            try:
                # algorithm DFS time
                start_time_algo0 = time.perf_counter()
                puzzle.get_solution(0)
                end_time_algo0 = time.perf_counter()
                time_algo0 = end_time_algo0 - start_time_algo0
                # algorithm LP time
                start_time_algo1 = time.perf_counter()
                puzzle.get_solution(1)
                end_time_algo1 = time.perf_counter()
                time_algo1 = end_time_algo1 - start_time_algo1
                # comparison
                if time_algo1 >= time_algo0:
                    print("LP Algorithm is the Fastest")
                    suggested_algorithm_text.draw(win, "LP Algorithm is the Fastest")
                else:
                    print("DFS Algorithm is the Fastest")
                    suggested_algorithm_text.draw(win, "DFS Algorithm is the Fastest")
            except:
                print("No Possible Solutions With Algorithms")
                suggested_algorithm_text.draw(win, "No Possible Solutions")

        # draws and updates data input text file
        if grid_check == 0:
            pygame.draw.rect(win, (251, 247, 245), pygame.Rect(655, 520, 256, 270))
        elif grid_check == 1:
            pygame.draw.rect(win, (251, 247, 245), pygame.Rect(655, 520, 256, 180))
        elif grid_check == 2:
            pygame.draw.rect(win, (251, 247, 245), pygame.Rect(655, 520, 256, 360))


        if grid_check == 0:
            for single in clickable_row9:
                single["group"].update(event_list)
                single["group"].draw(win)

                if len(single["field"].text) >= 1:
                    single["field"].limiter = True
                else:
                    single["field"].limiter = False


        elif grid_check == 1:
            for single in clickable_row6:
                single["group"].update(event_list)
                single["group"].draw(win)

                if len(single["field"].text) >= 1:
                    single["field"].limiter = True
                else:
                    single["field"].limiter = False

        elif grid_check == 2:
            for single in clickable_row12:
                single["group"].update(event_list)
                single["group"].draw(win)

                if len(single["field"].text) >= 2:
                    single["field"].limiter = True
                else:
                    single["field"].limiter = False

        # ---------------------------------------------------------------------------------------
        if grid_check == 0:
            # checks number limit for every single text input
            for j in range(9):
                data_input_cols[j].limiter = len(data_input_cols[j].text) >= 25

            # draws and updates every 9x9 text input
            for j in range(9):
                data_input_groups[j].update(event_list)
                data_input_groups[j].draw(win)

        if grid_check == 1:

            # checks number limit for every single text input
            for j in range(6):
                data_input_cols[j].limiter = len(data_input_cols[j].text) >= 16

            # draws and updates every 9x9 text input
            for j in range(6):
                data_input_groups[j].update(event_list)
                data_input_groups[j].draw(win)

        if grid_check == 2:

            # checks number limit for every single text input
            for j in range(12):
                data_input_cols[j].limiter = len(data_input_cols[j].text) >= 37

            # draws and updates every 9x9 text input
            for j in range(12):
                data_input_groups[j].update(event_list)
                data_input_groups[j].draw(win)

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
    # generate the limits of how many starting numbers for each board
    if len(grid) == 9:
        hint_limit = 17  # limits to 17 starting numbers for 9x9 grid
    elif len(grid) == 6:
        hint_limit = 6  # limits to 6 starting numbers for 6x6 grid
    elif len(grid) == 12:
        hint_limit = 24  # limits to 24 starting numbers for 12x12 grid
    # fill in board
    for i in range(0, len(grid[0])):
        for j in range(0, len(grid[0])):
            if random.randint(0, 100) <= 18 and numpy.count_nonzero(new_grid) < hint_limit - 1:  # if number is 0-18 -> fill the space with a number
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
    return [(x, y) for x in range(len(starting_grid[0])) for y in range(len(starting_grid[0])) if
            starting_grid[x][y] != 0]


def populate_board(g, new_num=None):
    """Populate the sudoku board with numbers from the given grid."""
    clear_board()
    global clickable_row9, clickable_row12, clickable_row6
    if len(g[0]) == 9: clickable_row9 = make_click_cells(10, g)
    if len(g[0]) == 12: clickable_row12 = make_click_cells(13, g)
    if len(g[0]) == 6: clickable_row6 = make_click_cells(7, g)

    for i in range(0, len(g[0])):
        for j in range(0, len(g[0])):
            if 0 < g[i][j] < 13:
                if (i, j) in get_clue_positions():
                    value = font.render(str(g[i][j]), True, (0, 0, 0))
                elif (i, j) == new_num:
                    value = font.render(str(g[i][j]), True, (255, 0, 0))
                else:
                    value = font.render(str(g[i][j]), True, grid_original_color)

                # add to screen with blit
                if g[i][j] > 9:
                    win.blit(value, ((j + 0.9) * 50 + 15, (i + 0.75) * 50 + 15 + 100))  # for double digit numbers
                else:
                    win.blit(value, ((j + 1) * 50 + 15, (i + 0.75) * 50 + 15 + 100))
                pygame.display.flip()


def clear_board():
    win.fill(background_color)
    board(win, starting_grid)


def revert_text_colors():
    for data_input in data_input_cols:
        data_input.color = (0, 0, 0)


def make_click_cells(n, g=None):
    if g is None:
        g = starting_grid
    text_fields = []

    for i in range(1, n):
        for j in range (0, n-1):
            if g[j][i-1] == 0:
                new_field = TextField(50 * i, 150 + (j * 50), 50, pygame.font.SysFont("Comic Sans MS", 30), False)
                new_group = pygame.sprite.Group(new_field)

                text_fields.append({"group": new_group, "field": new_field})

    return text_fields


# game entry point
if __name__ == "__main__":
    main()
