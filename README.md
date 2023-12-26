# The Sudoku Solver
An application for solving NxN Sudoku puzzles using various algorithms
<p align="center"><img align="center" src="https://imgur.com/EIJPCpx" alt="Program Demo" width="500"/></p>

## Features
* **Generate puzzles:** generate 9x9, 6x6, and 12x12 Sudoku puzzles
* **Input puzzles:** type clue numbers into the text fields to input your own puzzles
* **Play Sudoku:** click on any cell in the Sudoku board and type in a number
* **Solve puzzles:** compute and display a solution to the generated or inputted Sudoku puzzle using Depth-First Search, Linear Programming, or Naked Singles
* **Step through:** view a computed solution step by step
* **Suggested algorithm:** test each algorithm to determine which is the fastest at solving any given puzzle

## How to Use
### Generating Puzzles
In the top dropdown on the right side of the application, select the size of the board you wish to generate. If you would like to randomly generate a Sudoku puzzle, simply press the `Generate` button. Note that the text input fields must be cleared in order to <em>randomly</em> generate boards.

If you would like to input your own Sudoku board, first press the `Generate` button to spawn the appropriate amount of input text fields. Then, type your clue numbers into the text fields. Each field represents one row of the board. Cells without clue numbers should be represented by zeros. Numbers should be separated by commas and spaces. For example, for a 9x9 board, if the first row contains only one clue number (7) in the first cell, you would type `7, 0, 0, 0, 0, 0, 0, 0, 0` into the first text field. After every text field is filled in, press the `Generate` button.

You can clear all text fields using the `Clear All` button, or clear an individual text field using the red `X` button to its right.

If your input is invalid (e.g. you typed in letters or formatted it incorrectly), each invalid field will appear red and be populated with zeros.

### Playing Sudoku
To enter a number into a cell on the Sudoku board, click on the cell to select it and type a number using your keyboard. To erase a number you have entered, first ensure that the cell is selected, and then press `Backspace` on your keyboard. Note that there is no visual indication of a cell being selected.

### Solving and Stepping Through Puzzles
If you would like the program to solve a puzzle for you, first select which algorithm you would like to use in the second dropdown on the right side of the application. Then, press the `Solve` button. It may take some time for the algorithm to find a solution. If it appears that the program is not responding, this is because the algorithm is still searching for a solution. If no solution can be found, red text will be displayed.

To step through a solution, first ensure that the algorithm you would like to use is selected. Then, simply press the `Step` button. This will show you, step by step, how the solution was found. The most recent step will be displayed in red.

### Getting an Algorithm Suggestion
If you would like the program to suggest which algorithm is the fastest at solving the current puzzle, press the `Suggest an Algorithm` button. This will run through all three algorithms and test how long it takes each one to find a solution. Note that this may take some time. After all three algorithms have been tested, red text will be displayed telling you either which algorithm is the fastest, or, in some cases, that no solutions could be found with any algorithm. 