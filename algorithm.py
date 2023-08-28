"""
File: algorithm.py
Description:
    Provides functions to solve a Sudoku board 
    using the recursive backtracking algorithm.
"""


def solve(b):
    """
    Solves a sudoku board with backtracking algorithm
    :param b: 2d array of ints (board)
    :return: updates board variable w/ solution (2d array)
    """

    # Base case
    empty = find_empty_space(b)
    if not empty:
        # Board solved
        return True
    else:
        row, col = empty

    # Try solutions
    for guess in range(1, 10):
        if is_valid(b, guess, (row, col)):
            # Add solution into board if valid
            b[row][col] = guess

            # Recursive guess call
            if solve(b):
                return True
            
            # Backtrack (reset value and restart loop)
            b[row][col] = 0

    # Looped through all nums &/or all possibled guesses invalid
    return False


def find_empty_space(b):
    """
    Finds zeros (empty spaces) in the board
    :param b: 2d lists of ints (board)
    :returns: empty position
    """

    for i in range(len(b)):
        for j in range(len(b[0])):
            if b[i][j] == 0:
                # row, col (y, x)
                return (i, j)
    # No blank spaces
    return None


def is_valid(b, num, pos):
    """
    Check if entered num is not in same row, col, or grid as position inserted
    :param b: 2d lists of ints (board)
    :param num: entered integer guess
    :param pos: position of guess (tuple of y, x)
    :returns: bool valid
    """

    # Check rows
    for i in range(len(b[0])):
        if b[pos[0]][i] == num and pos[1] != i:
            return False
    
    # Check columns
    for i in range(len(b)):
        if b[i][pos[1]] == num and pos[0] != i:
            return False
    
    # Check grid
    grid_x = pos[1] // 3
    grid_y = pos[0] // 3

    # Find current grid position
    for i in range(grid_y * 3, (grid_y * 3) + 3):
        for j in range (grid_x * 3, (grid_x * 3) + 3):
            if b[i][j] == num and pos != (i, j):
                return False

    return True  # Valid position


def show(b):
    """
    Prints board in a readable format (testing)
    :param b: 2d list of ints (board)
    :returns: formatted board as a str
    """

    for i in range(len(b)):
        if i % 3 == 0 and i != 0:
            # Seperate grids
            print('- - - - - - - - - - - -')

        for j in range(len(b[0])):
            if j % 3 == 0 and j != 0:
                # Seperate columns
                print(' | ', end='')
            if j == 8:
                # End of line
                print(b[i][j])
            else:
                print(str(b[i][j]) + ' ', end='')


# Test
if __name__ == '__main__':
    board = [
    [7,8,0,4,0,0,1,2,0],
    [6,0,0,0,7,5,0,0,9],
    [0,0,0,6,0,1,0,7,8],
    [0,0,7,0,4,0,2,6,0],
    [0,0,1,0,5,0,9,3,0],
    [9,0,4,0,6,0,0,0,5],
    [0,7,0,3,0,0,0,1,2],
    [1,2,0,0,0,7,4,0,0],
    [0,4,9,2,0,6,0,0,7]]
    
    show(board)
    solve(board)
    print('\n')
    show(board)