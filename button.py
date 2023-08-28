"""
File: button.py
Description:
    Button class used in pygame GUIs
    for creating functional buttons.
"""

import pygame


class Button():
    def __init__(self, x, y, image, scale):
        self.image = pygame.transform.scale(image, scale)
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)
        self.clicked = False

    def draw(self, surface):
        """
        Draw button on screen
        :param self: button object
        :param surface: surface to blit onto (screen)
        """

        # Check mouse conditions for click
        mouse_pos = pygame.mouse.get_pos()
        if self.rect.collidepoint(mouse_pos):
            if pygame.mouse.get_pressed()[0] == 1 and self.clicked == False:
                self.clicked = True

        # Reset
        if pygame.mouse.get_pressed()[0] == 0:
            self.clicked = False

        # Draw button on screen
        surface.blit(self.image, (self.rect.x, self.rect.y))

    def get_clicked(self):
        """Assess clicks"""
        return self.clicked