"""
File: game.py
Description:
    Implementation of the Sudoku game functionality using the Pygame library. 
    Provides a graphical user interface for playing Sudoku puzzles, 
    including user input, error tracking, timer display, and completion checking. 
    The game's logic is based on the 'randomize' module for generating Sudoku 
    puzzles and the 'algorithm' module for solving them.
"""

import pygame
import copy
import time
import sys

import button
from randomize import *
from algorithm import solve


def run_game(screen, difficulty):
    """
    Function called in player.py to run the game funcionality
    :param screen: screen to display to in player.py
    :param difficulty: difficulty of the generated game
    :returns: state if returning to menu within player.py
    """

    # Fonts
    err_font = pygame.font.SysFont('Veener Solid', 50)
    given_font = pygame.font.SysFont('Veener Solid', 40)
    final_font = pygame.font.SysFont('Veener Solid', 40)
    timer_font = pygame.font.SysFont('Veener Solid', 50)
    menu_color = (47, 54, 153)
    given_color = (0, 68, 129)
    final_color = (0, 0, 0)

    # Tracking variables
    incorrect_counter = 0

    def main():
        """Main display for the game (main function)"""

        screen.fill((154, 182, 217))

        # Images
        board_bg = pygame.image.load('Assets/Game/white_bg.jpg').convert_alpha()
        menu_bg = pygame.image.load('Assets/Game/cream_bg.jpeg').convert_alpha()
        border_img = pygame.image.load('Assets/Game/border_img.jpg').convert_alpha()
        mistakes_img = pygame.image.load('Assets/Game/mistakes_img.jpg').convert_alpha()
        border_line = pygame.image.load('Assets/Game/seper_line.jpg').convert_alpha()
        timer_img = pygame.image.load('Assets/Game/timer_img.jpg').convert_alpha()
        board_bg = pygame.transform.scale(board_bg, (450, 450))
        menu_bg = pygame.transform.scale(menu_bg, (900, 125))
        border_img = pygame.transform.scale(border_img, (5, 75))
        mistakes_img = pygame.transform.scale(mistakes_img, (180, 35))
        border_line = pygame.transform.scale(border_line, (900, 5))
        timer_img = pygame.transform.scale(timer_img, (120, 35))

        # Buttons
        menu_img = pygame.image.load('Assets/Other/menu_img.jpg').convert_alpha()
        new_game_img = pygame.image.load('Assets/Game/new_game.jpg').convert_alpha()
        menu_btn = button.Button(765, 25, menu_img, (110, 60))
        new_game_btn = button.Button(700, 600, new_game_img, (150, 75))

        # Construct and draw starting board
        screen.blit(board_bg, (220, 80))
        draw_grid()
        draw_original_values()

        # Bounds of the Sudoku board region
        board_region = pygame.Rect(220, 80, 450, 450)

        while True:

            # Images
            screen.blit(menu_bg, (0, 575))
            screen.blit(border_line, (0, 570))
            screen.blit(timer_img, (50, 618))
            screen.blit(border_img, (320, 600))
            screen.blit(border_img, (640, 600))
            screen.blit(mistakes_img, (370, 618))

            # Buttons
            menu_btn.draw(screen)
            new_game_btn.draw(screen)
            
            # Display incorrect count
            error_count = err_font.render(str(incorrect_counter), True, menu_color)
            screen.blit(error_count, (565, 620))

            # Timer
            current_time = time.time()
            elapsed_time = current_time - start_time
            draw_timer(elapsed_time)

            for event in pygame.event.get():
                if event.type == pygame.MOUSEBUTTONUP and event.button == 1:
                    pos = pygame.mouse.get_pos()

                    if board_region.collidepoint(pos):
                        # Cell selected and user guess prompted
                        cell = ((pos[0] - 174) // 50, (pos[1] - 34) // 50)
                        indicate(cell)
                        poss_nav = insert(cell)

                        if poss_nav == 'MENU':
                            return 'MENU'
                    
                    elif menu_btn.get_clicked():
                        return 'MENU'
                    elif new_game_btn.get_clicked():
                        # Restart screen with new board (new game)
                        run_game(screen, difficulty)

                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
        
            pygame.display.update()
            clock.tick(60)


    def draw_grid():
        """Draw 9x9 soduku board grid and border lines"""

        for i in range(0, 10):

            # Thicker borders
            line_width = 2
            if i % 3 == 0:
                line_width = 4

            # Draw horizontal & vertical grid lines
            pygame.draw.line(screen, (0, 0, 0), (220 + 50*i, 80), (220 + 50*i, 530), line_width)
            pygame.draw.line(screen, (0, 0, 0), (220, 80 + 50*i), (670, 80 + 50*i), line_width)


    def draw_original_values():
        """Draw given board values onto screen"""

        for i in range(0, len(board[0])):
            for j in range(0, len(board[0])):
                if (0 < board[i][j] < 10):
                    # Valid number (1 - 9)
                    given = given_font.render(str(board[i][j]), True, given_color)
                    screen.blit(given, ((j+1)*50 + 188, (i+1)*50 + 45))
    

    def insert(position):
        """
        Inserts user guess into board variable and displays if valid
        :param position: currently selected cell
        :returns: board for testing purposes
        """

        # Bounds of the Sudoku board region
        board_region = pygame.Rect(220, 80, 450, 450)

        # Images
        cover_img = pygame.image.load('Assets/Game/cream_bg.jpeg').convert_alpha()
        cover_img = pygame.transform.scale(cover_img, (50, 50))

        i,j = position[1], position[0]
        value = ''  # user guess in ASCII

        while True:

            # Update the timer display
            pygame.display.update()
            current_time = time.time()
            elapsed_time = current_time - start_time
            draw_timer(elapsed_time)

            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    if original_board[i-1][j-1] != 0:
                        # Not empty & not being changed
                        return

                    if event.key == pygame.K_BACKSPACE:
                        # Set to to zero
                        board[i-1][j-1] = 0
                        format_cells(position, 'White', 'inside')

                        pygame.display.update()
                        clock.tick(60)

                    if 0 < event.key - 48 < 10:
                        # Check for valid input & update
                        value = final_font.render(str(event.key - 48), True, final_color)
                        format_cells(position, 'White', 'inside')
                        screen.blit(value, (position[0]*50 + 188, position[1]*50 + 45))

                        if event.key - 48 == solved_board[i-1][j-1]:
                            # Update board with input value
                            board[i-1][j-1] = event.key - 48

                        pygame.display.update()
                        clock.tick(60)

                    if event.key == pygame.K_RETURN:
                        # Value is officially entered and checked for correctness
                        format_cells(position, 'White', 'cover')

                        if board[i-1][j-1] != 0:
                            # Finalize input onto display
                            screen.blit(value, (position[0]*50 + 188, position[1]*50 + 45))

                        if board[i-1][j-1] != solved_board[i-1][j-1]:
                            # Incorrect input
                            nonlocal incorrect_counter
                            incorrect_counter += 1
                            clear_incorrect_count()  # Cover previous count

                        if check_solved() == 'MENU':
                            return 'MENU'
                        
                        pygame.display.update()
                        clock.tick(60)
                        return board
                
                if event.type == pygame.MOUSEBUTTONUP and event.button == 1:
                        # Clicked elsewhere on the screen
                        pos = pygame.mouse.get_pos()

                        # Negate input if clicked elsewhere
                        if original_board[i-1][j-1] == 0:
                            format_cells(position, 'White', 'cover')
                            board[i-1][j-1] = 0

                            # Recursively insert for next click
                            if board_region.collidepoint(pos):
                                cell = ((pos[0] - 174) // 50, (pos[1] - 34) // 50)
                                indicate(cell)
                                insert(cell)
    
                            pygame.display.update()
                            clock.tick(60)
                            return board
                
                if event.type == pygame.QUIT:
                        pygame.quit()
                        sys.exit()


    def indicate(position):
        """Display an indicator for the currently selected cell"""

        i, j = position[1], position[0]
        input_font = pygame.font.SysFont('Veener Solid', 40)

        if original_board[i-1][j-1] == 0:
            # Draw squares
            format_cells(position, 'Red', 'cover')
            format_cells(position, 'White', 'inside')

            if board[i-1][j-1] != 0:
                # Place value on top of squares
                value = input_font.render(str(board[i-1][j-1]), True, final_color)
                screen.blit(value, (position[0]*50 + 188, position[1]*50 + 45))

            pygame.display.update()
            clock.tick(60)


    def format_cells(position, color, function):
            """
            Pre-formats and draws squares in cells on the board depending on if they touch any borders
            :param color: red = indicate, white = inside
            :param function: determines size of rectangle
            """

            i,j = position[1], position[0]
            top, bottom, left, right = 0, 0, 0, 0

            # Determine values based on cell's location
            if i % 3 == 1:
                top = 1
            if i % 3 == 0:
                bottom = 1
            if j % 3 == 1:
                left = 1
            if j % 3 == 0:
                right = 1
            if i % 3 == 2 and j % 3 == 2:
                pos = (position[0]*50 + 172, position[1]*50 + 32, 48, 48)

            # Add buffers depending on border position
            if function == 'cover':
                pos = (position[0]*50 + 172 + left, position[1]*50 + 32 + top, 48 - left - right, 48 - top - bottom)
            elif function == 'inside':
                pos = (position[0]*50 + 174 + left, position[1]*50 + 35, 43 - left - right, 43 - (2*bottom))

            pygame.draw.rect(screen, color, pos)


    def check_solved():
        """Displays solution page and stats after completion of the game"""

        if board == solved_board:
            
            # Stop and the timer
            end_time = time.time()
            elapsed_time = int(end_time - start_time)
            minutes = int(elapsed_time // 60)
            seconds = int(elapsed_time % 60)
            timer_text = timer_font.render(f"{minutes:02}:{seconds:02}", True, menu_color)

            # Get incorrect count
            error_count = err_font.render(str(incorrect_counter), True, menu_color)

            time.sleep(1)
            screen.fill((154, 182, 217))

            # Images
            solved_img = pygame.image.load('Assets/Game/solved_img.jpg').convert_alpha()
            stats_box = pygame.image.load('Assets/Game/cream_bg.jpeg').convert_alpha()
            horizontal_border = pygame.image.load('Assets/Game/seper_line.jpg').convert_alpha()
            vertical_border = pygame.image.load('Assets/Game/border_img_dark.jpg').convert_alpha()
            x_img = pygame.image.load('Assets/Game/x_img.jpg').convert_alpha()
            clock_img = pygame.image.load('Assets/Game/clock_img.jpg').convert_alpha()
            solved_img = pygame.transform.scale(solved_img, (400, 125))
            stats_box = pygame.transform.scale(stats_box, (500, 400))
            horizontal_border = pygame.transform.scale(horizontal_border, (500, 5))
            vertical_border = pygame.transform.scale(vertical_border, (5, 400))
            x_img = pygame.transform.scale(x_img, (75, 70))
            clock_img = pygame.transform.scale(clock_img, (75, 75))

            # Buttons
            menu_img = pygame.image.load('Assets/Other/menu_img.jpg').convert_alpha()
            menu_btn = button.Button(765, 25, menu_img, (110, 60))

            while True:
                
                menu_btn.draw(screen)
                screen.blit(solved_img, (250, 35))

                # Sats box
                screen.blit(stats_box, (200, 200))
                screen.blit(horizontal_border, (200, 200))
                screen.blit(horizontal_border, (200, 600))
                screen.blit(vertical_border, (200, 200))
                screen.blit(vertical_border, (700, 200))

                # Stats
                screen.blit(clock_img, (335, 300))
                screen.blit(timer_text, (450, 320))
                screen.blit(x_img, (335, 425))
                screen.blit(error_count, (485, 445))

                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        pygame.quit()
                        sys.exit()

                    if menu_btn.get_clicked():
                        return 'MENU'
                
                pygame.display.update()
                clock.tick(60)


    def clear_incorrect_count():
        """Covers and replaces mistake counter when updated"""

        cover_img = pygame.image.load('Assets/Game/cream_bg.jpeg').convert_alpha()
        cover_img = pygame.transform.scale(cover_img, (50, 50))
        screen.blit(cover_img, (565, 620))
        pygame.display.update()


    def draw_timer(elapsed_time):
        """Draws and updates the game timer"""

        cover_img = pygame.image.load('Assets/Game/cream_bg.jpeg').convert_alpha()
        cover_img = pygame.transform.scale(cover_img, (100, 40))
        minutes = int(elapsed_time // 60)
        seconds = int(elapsed_time % 60)
        timer_text = timer_font.render(f"{minutes:02}:{seconds:02}", True, menu_color)
        screen.blit(cover_img, (185, 620))
        screen.blit(timer_text, (185, 620))


    """RUN MAIN (MAIN VARIABLES)"""

    # Boards
    board = random_sudoku_board(difficulty)
    original_board = copy.deepcopy(board)
    solved_board = copy.deepcopy(board)
    solve(solved_board)

    clock = pygame.time.Clock()
    start_time = time.time()  # Start imer

    # Run code
    state = main()

    # Returning to player.py (menu)
    if state is not None:
        return state


# Test code
if __name__ == '__main__':
    pygame.init()
    pygame.font.init()
    pygame.display.set_caption('Solvoku')
    screen = pygame.display.set_mode((900, 700))
    run_game(screen, 20)