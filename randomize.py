"""
File: randomize.py
Description: 
    Generates random sudoku board for 
    playing Sudoku in the game module.
"""

from dokusan import generators
from algorithm import solve, show


# Difficulties
EASY_MODE = 150
MEDIUM_MODE = 350
HARD_MODE = 600


def random_sudoku_board(difficulty=150):
    """
    Generate a random sudoku board
    :param difficulty: avg_rank level of difficulty (auto set to easy)
    :returns: (2d list) generated board
    """

    # Generate board and turn string into array
    random_board = (list(str(generators.random_sudoku(avg_rank=difficulty))))

    # Convert to 2d list of ints (9x9)
    random_board = [int(x) for x in random_board]
    random_board = [random_board[i:i+9] for i in range(0, len(random_board), 9)]

    return random_board


# Test Code
if __name__ == '__main__':
    board = random_sudoku_board(HARD_MODE)
    show(board)
    print('\n')
    solve(board)
    show(board)