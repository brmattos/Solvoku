# Solvoku
---

## Overview
This project provides a graphical user interface for playing and solving Sudoku puzzles using the Pygame library. Puzzles are solved using a backtracking algorithm, with images of puzzles also being solvable through the implementation of the OpenCV library for image processing. From the GUI's menu, the user can has the option to start a game with different difficulty levels, solve puzzles from uploaded images, and observe the solution and solution processes. The project's game logic is contained in the 'game' module, while the puzzle image processing is managed by the 'img_solver' module.

## Getting Started
To run the code on your local machine, follow these steps:

**1. Clone the repository:**
   ```bash
   git clone https://github.com/brmattos/CalCulator.git
   ```
**2. Install required dependencies and modules:**
   ```bash
   pip install -r requirements.txt
   ```

## Project Structure
- `player.py`: main file of the project, implementing a GUI and menu for playing and solving Sudoku puzzles.
- `game.py`: implements a graphical user interface for playing randomized Sudoku puzzles, including user input, error tracking, timer display, and completion checking.
- `button.py`: class for creating functional buttons in Pygame.
- `algorithm.py`: uses a recursive backtracking algorithm to solve any solvable 9x9 Sudoku board
- `randomize.py`: generates random board for playing a game of Sudoku in the game module
- `process.py`: functions used for OpenCV image processing of Sudoku boards implemented in the img_solver module
- `img_solver.py`: processes images of Sudoku boards using the OpenCV library, with detecting the board, solving the board, and saving the solution and solution process as local files to be worked with in the player module
