"""
File: player.py
Author: Brooke Mattos
Date: June 17, 2023
Description:  
    Contains the implementation of a GUI for playing and solving Sudoku puzzles using the Pygame library. 
    Provides options to start the game, choose difficulty levels, solve puzzles from images, and view solution processes. 
    The GUI includes buttons, images, and entry boxes for user interaction. 
    The Sudoku game logic is implemented in the 'game' module, and puzzle image processing is handled by the 'img_solver' module.
"""

import pygame
import sys
import os

import button
from game import *
from img_solver import *


# Setup screen
pygame.init()
pygame.font.init()
screen = pygame.display.set_mode((900, 700))
new_icon = pygame.image.load('Assets/Other/sudoku_icon.png')
pygame.display.set_icon(new_icon)
clock = pygame.time.Clock()


def draw_text(text, font, color, x, y):
    """Renders text onto the screen"""
    img = font.render(text, True, color)
    screen.blit(img, (x, y))

def delete_solutions():
    """Deletes (resets) all files in Solutions folder"""

    # Specify folder path
    folder_path = 'Solutions'
    file_list = os.listdir(folder_path)

    # Loop through files and delete them
    for file_name in file_list:
        file_path = os.path.join(folder_path, file_name)
        if os.path.isfile(file_path):
            os.remove(file_path)


def menu():
    """Starting menu page for the GUI"""

    screen.fill((154, 182, 217))
    pygame.display.set_caption('Solvoku')

    # Images
    board_img = pygame.image.load('Assets/Menu/board_art_img.jpg').convert_alpha()
    board_img = pygame.transform.scale(board_img, (500, 500))
    esc_img = pygame.image.load('Assets/Menu/escape_img.jpg').convert_alpha()
    esc_img = pygame.transform.scale(esc_img, (110, 60))

    # Buttons
    play_img = pygame.image.load('Assets/Menu/play_img.jpg').convert_alpha()
    solve_img = pygame.image.load('Assets/Menu/solve_img.jpg').convert_alpha()
    settings_img = pygame.image.load('Assets/Menu/settings_img.jpg').convert_alpha()
    play_btn = button.Button(300, 600, play_img, (110, 60))
    solve_btn = button.Button(490, 600, solve_img, (110, 60))
    settings_btn = button.Button(20, 20, settings_img, (60, 60))

    while True:

        # Draw on screen
        screen.blit(board_img, (200, 60))
        play_btn.draw(screen)
        solve_btn.draw(screen)
        settings_btn.draw(screen)
        screen.blit(esc_img, (765, 25))

        if play_btn.get_clicked():
            play()

        if solve_btn.get_clicked():
            solve_image()

        if settings_btn.get_clicked():
            settings()

        # Exit and close all code
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                delete_solutions()
                pygame.quit()
                sys.exit()

        # Draw and update
        pygame.display.update()
        clock.tick(60)


def settings():
    """Settings page navigated to from menu"""

    screen.fill((154, 182, 217))

    # Images
    border_img = pygame.image.load('Assets/Settings/settings_box_img.jpg').convert_alpha()
    settings_title = pygame.image.load('Assets/Settings/settings_title_img.jpg').convert_alpha()
    about_title = pygame.image.load('Assets/Settings/about_title.jpg').convert_alpha()
    border_img = pygame.transform.scale(border_img, (600, 450))
    settings_title = pygame.transform.scale(settings_title, (350, 80))
    about_title = pygame.transform.scale(about_title, (150, 50))

    # Buttons
    back_img = pygame.image.load('Assets/Other/back_img.jpg').convert_alpha()
    back_btn = button.Button(765, 25, back_img, (110, 60))

    while True:
        
        screen.blit(border_img, (150, 150))
        screen.blit(settings_title, (20, 20))
        screen.blit(about_title, (375, 220))
        back_btn.draw(screen)

        draw_text('Sudoku solver and player using', 
                  pygame.font.SysFont('DroidSans', 35), 'White', 265, 310)
        draw_text('backtracking and image processing',
                  pygame.font.SysFont('DroidSans', 35), 'White', 240, 360)
        draw_text('to efficiently and quickly solve',
                  pygame.font.SysFont('DroidSans', 35), 'White', 265, 410)
        draw_text('any puzzle',
                  pygame.font.SysFont('DroidSans', 35), 'White', 380, 460)

        if back_btn.get_clicked():
            menu()

        # Exit and close all code
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                delete_solutions()
                pygame.quit()
                sys.exit()

        pygame.display.update()
        clock.tick(60)


def play():
    """Setup page for playing Sudoku"""

    screen.fill((154, 182, 217))

    # Buttons
    back_img = pygame.image.load('Assets/Other/back_img.jpg').convert_alpha()
    play_img = pygame.image.load('Assets/Setup/play_game_img.jpg').convert_alpha()
    easy_img = pygame.image.load('Assets/Setup/easy_img.jpg').convert_alpha()
    medium_img = pygame.image.load('Assets/Setup/medium_img.jpg').convert_alpha()
    hard_img = pygame.image.load('Assets/Setup/hard_img.jpg').convert_alpha()
    easy_on_img = pygame.image.load('Assets/Setup/easy_on_img.jpg').convert_alpha()
    medium_on_img = pygame.image.load('Assets/Setup/medium_on_img.jpg').convert_alpha()
    hard_on_img = pygame.image.load('Assets/Setup/hard_on_img.jpg').convert_alpha()
    back_btn = button.Button(765, 25, back_img, (110, 60))
    play_btn = button.Button(290, 500, play_img, (300, 100))
    easy_btn = button.Button(350, 100, easy_img, (180, 100))
    medium_btn = button.Button(300, 220, medium_img, (280, 100))
    hard_btn  = button.Button(350, 340, hard_img, (180, 100))
    easy_on_btn = button.Button(350, 100, easy_on_img, (180, 100))
    medium_on_btn = button.Button(300, 220, medium_on_img, (280, 100))
    hard_on_btn = button.Button(350, 340, hard_on_img, (180, 100))

    # Hashmap to store button states and images
    button_states = {
        'easy': False,
        'medium': False,
        'hard': False
    }

    while True:

        back_btn.draw(screen)
        play_btn.draw(screen)
        easy_btn.draw(screen)
        medium_btn.draw(screen)
        hard_btn.draw(screen)

        # Draw difficulty buttons based on their states
        if button_states['easy']:
            easy_on_btn.draw(screen)
        else:
            easy_btn.draw(screen)

        if button_states['medium']:
            medium_on_btn.draw(screen)
        else:
            medium_btn.draw(screen)

        if button_states['hard']:
            hard_on_btn.draw(screen)
        else:
            hard_btn.draw(screen)

        difficulty = 20
        # Check for button clicks and update button states
        if easy_btn.get_clicked():
            button_states = {'easy': True, 'medium': False, 'hard': False}
            difficulty = 20

        if medium_btn.get_clicked():
            button_states = {'easy': False, 'medium': True, 'hard': False}
            difficulty = 75

        if hard_btn.get_clicked():
            button_states = {'easy': False, 'medium': False, 'hard': True}
            difficulty = 100

        # Change screen
        if back_btn.get_clicked():
            menu()

        # Call game module
        if play_btn.get_clicked():
            state = run_game(screen, difficulty)
            if state == 'MENU':
                menu()

        # Exit and close all code
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                delete_solutions()
                pygame.quit()
                sys.exit()

        pygame.display.update()
        clock.tick(60)


def solve_image():
    """Image path entry page: uses img_solver module on user uploaded image of board"""

    screen.fill((154, 182, 217))
    upload_clicked = False  # Track if images uploaded

    # Images
    path_img = pygame.image.load('Assets/Solve/file_path_img.jpg').convert_alpha()
    path_img = pygame.transform.scale(path_img, (200, 80))
    loading_img = pygame.image.load('Assets/Solve/loading_img.jpg').convert_alpha()
    loading_img = pygame.transform.scale(loading_img, (180, 50))

    # Buttons
    back_img = pygame.image.load('Assets/Other/back_img.jpg').convert_alpha()
    upload_img = pygame.image.load('Assets/Solve/upload_img.jpg').convert_alpha()
    back_btn = button.Button(765, 25, back_img, (110, 60))
    upload_btn = button.Button(360, 500, upload_img, (180, 80))

    # Entrybox
    base_font = pygame.font.Font(None, 40)
    user_text = ''
    entry_rect = pygame.Rect(315, 312, 550, 50)
    entry_color = (60, 82, 145)

    while True:

        # Exit / check for Entrybox input
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                delete_solutions()
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_BACKSPACE:
                    # Remove the last character from user_text
                    user_text = user_text[:-1]
                elif event.unicode:
                    # Valid input
                    user_text += event.unicode

        screen.fill((154, 182, 217))

        # Create Entrybox
        text_surface = base_font.render(user_text, True, 'White')
        screen.blit(text_surface, (325, 325))

        # Draw on screen
        back_btn.draw(screen)
        upload_btn.draw(screen)
        screen.blit(path_img, (60, 300))
        pygame.draw.rect(screen, entry_color, entry_rect, 3)

        # Directions text
        draw_text('Write your file name in text below:', 
                  pygame.font.SysFont('DroidSans', 50), 'White', 150, 150)

        if back_btn.get_clicked():
            menu()

        if upload_btn.get_clicked():

            upload_clicked = True

            # Load user input file and store img_solver.py files
            user_text = f'Boards/{user_text}'
            error = display_image_solution(user_text, 'Board')
            display_image_solution(user_text, 'Solution')
            display_image_solution(user_text, 'Process')

            # Errors in img_solver.py or no input
            if error or user_text == '':
                cont = False
                user_text = 'ERROR'
            else:
                # Indicate succes & load
                screen.blit(loading_img, (680, 620))
                cont = True

            if upload_clicked and cont:
                show_solution()

        pygame.display.flip()
        clock.tick(60)


def show_solution():
    """Next page after uploading, shows the original image and solution"""

    screen.fill((154, 182, 217))

    # Images
    arrow_img = pygame.image.load('Assets/Solve/arrow_img.jpg')
    solution_title = pygame.image.load('Assets/Solve/solution_title.jpg')
    board_img = pygame.image.load('Solutions/board_image.jpg').convert_alpha()
    solution_img = pygame.image.load('Solutions/solution_image.jpg').convert_alpha()
    arrow_img = pygame.transform.scale(arrow_img, (60, 50))
    solution_title = pygame.transform.scale(solution_title, (400, 80))
    board_img = pygame.transform.scale(board_img, (350, 350))
    solution_img = pygame.transform.scale(solution_img, (350, 350))

    # Buttons
    menu_img = pygame.image.load('Assets/Other/menu_img.jpg').convert_alpha()
    show_process_img = pygame.image.load('Assets/Solve/show_process_img.jpg').convert_alpha()
    menu_btn = button.Button(765, 25, menu_img, (110, 60))
    show_process_btn = button.Button(525, 550, show_process_img, (300, 100))

    while True:

        menu_btn.draw(screen)
        show_process_btn.draw(screen)
        screen.blit(solution_title, (250, 35))
        screen.blit(arrow_img, (425, 300))
        screen.blit(board_img, (50, 150))
        screen.blit(solution_img, (500, 150))

        if menu_btn.get_clicked():
            menu()

        if show_process_btn.get_clicked():
            show_process()

        # Exit and close all code
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                delete_solutions()
                pygame.quit()
                sys.exit()

            # Draw and update
            pygame.display.update()
            clock.tick(60)


def show_process():
    """Page showing OpenCV image processing, navigated to optionally on solution page"""

    # Images
    process_image = pygame.image.load('Solutions/process_image.jpg').convert_alpha()
    process_title = pygame.image.load('Assets/Solve/process_title.jpg')
    process_image = pygame.transform.scale(process_image, (600, 300))
    process_title = pygame.transform.scale(process_title, (400, 80))

    # Buttons
    menu_img = pygame.image.load('Assets/Other/menu_img.jpg').convert_alpha()
    menu_btn = button.Button(765, 600, menu_img, (110, 60))

    while True:

        screen.fill((154, 182, 217))

        # Images
        menu_btn.draw(screen)
        screen.blit(process_title, (250, 50))
        screen.blit(process_image, (150, 200))

        if menu_btn.get_clicked():
            menu()

        # Exit and close all code
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                delete_solutions()
                pygame.quit()
                sys.exit()

            # Draw and update
            pygame.display.update()
            clock.tick(60)


# Start program from menu
menu()