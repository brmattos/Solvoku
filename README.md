# Solvoku
---

## Overview
This project provides a graphical user interface for playing and solving Sudoku puzzles using the Pygame library. Puzzles are solved using a backtracking algorithm, with images of puzzles also being solvable through the implementation of the OpenCV library for image processing. Predicts digits within the sudoku board cells using a Convolutional Neural Network (CNN) model using the keras library. From the GUI's menu, the user has the option to start a game with different difficulty levels, solve puzzles from uploaded images, and observe the solution and solution processes. The project's game logic is contained in the 'game' module, while the puzzle image processing is managed by the 'img_solver' module.

## Getting Started
To run the code on your local machine, follow these steps:

**1. Clone the repository:**
   ```bash
   git clone https://github.com/brmattos/Solvoku.git
   ```
**2. Install required dependencies and modules:**
   ```bash
   pip install -r requirements.txt
   ```
**3. Using your board images:**
- place any board images that you'd like to solve into the `Boards` folder

## Usage
- `PLAYING GAME`: click on empty cells to enter values, then press enter to finalize guess
- `SOLVING IMAGES`: type file name (ex. puzzle_5.jpg) and click upload to solve the image

## Project Structure
- `player.py`: main file of the project, implementing a GUI and menu for playing and solving Sudoku puzzles.
- `game.py`: implements a graphical user interface for playing randomized Sudoku puzzles, including user input, error tracking, timer display, and completion checking.
- `button.py`: class for creating functional buttons in Pygame.
- `algorithm.py`: uses a recursive backtracking algorithm to solve any solvable 9x9 Sudoku board
- `randomize.py`: generates random board for playing a game of Sudoku in the game module
- `process.py`: functions used for OpenCV image processing of Sudoku boards implemented in the img_solver module
- `img_solver.py`: processes images of Sudoku boards using the OpenCV library, with detecting the board, solving the board, and saving the solution and solution process as local files to be worked with in the player module

---

# Image Processing

- Implements an image processing pipeline to analyze Sudoku boards using functions from the `process.py` module
- Utilizes image preprocessing techniques, contour detection, and perspective transformation to isolate the Sudoku board in `img_solver.py`
- Employs a trained neural network model to predict digits within individual board spaces in the file `Resources/num_model.h5`, placed into a 2d array of int values
- Implements solver from `algorithm.py` to solve the Sudoku board using the predicted digit values
- Generates visualizations at various stages of the process, demonstrating the original board, digit predictions, and final solution
- Flexible mechanism for displaying images, facilitating testing and analysis of the Sudoku solving process

<p align="center">
   <img src="https://github.com/brmattos/Solvoku/assets/140926908/0ae34d37-242b-45c8-9951-c9398be38c41" alt="Image Processing" width="650" height="350">
</p>

---

# Application (GUI)

https://github.com/brmattos/Solvoku/assets/140926908/76ccb9be-0407-45a5-a691-12e863e8e43f

---

<h2 align="center">Gameplay</h2>
<p align="center">
   <img src="https://github.com/brmattos/Solvoku/assets/140926908/8c2af929-83ce-4d24-9365-25a4be5663fc" alt="Gameplay" width="650" height="500">
</p>

- Board generated with `random.py` with difficulty depending on its being chosen within `player.py`
- User navigates around board by clicking on cells and entering numeric guesses from (1-9)
- Placement is indicated by a red rectangle, with only empty cells being navigable
- Backspace resets selected cell's displayed value to zero, newly entered value immediately replaces previous
- Guess not finalized until enter pressed, then validated next to solved version of the board using `algorithm.py`
- Timer implemented using the time module, along with a mistake counter updated upon non-valid value entry
- New game button generates a new board, resetting timer and mistake counter with same difficulty as initial game start
- Capability to return back to menu at any time

---

<h2 align="center">Board Complete</h2>
<p align="center">
   <img src="https://github.com/brmattos/Solvoku/assets/140926908/f1f7138f-a12d-427b-8674-e5ef20628f14" alt="Game Ending" width="650" height="500">
</p>

- Appears on screen upon a couple second delay after completion of the sudoku board game
- Showcases game stats from completed game, including the time it took the user to solve as well as the amount of mistakes that were made

---

<h2 align="center">Image Uploader</h2>
<p align="center">
   <img src="https://github.com/brmattos/Solvoku/assets/140926908/1bb90d85-ac07-4292-84e8-cd8fc0a762bf" alt="Upload Image" width="650" height="500">
</p>

- Type in file name after adding it to `Boards` folder and click upload to start processing the image for solution
- 3 files saved to `Solutions` folder throughout the process: `board_image.jpg`, `process_image.jpg`, `solution_image.jpg`, which are cv2 image files created within the process of reading the image in `img_solver.py`
- Upon exiting the program, these files are deleted for user privacy
