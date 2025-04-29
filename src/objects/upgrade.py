# import random
import pygame
from src.static_items import global_vars

class Upgrade:
    """Yksittäisen päivityksen logiikka

    Attributes:
        self.rarity = harvinaisuus
        self.name = nimi
        self.scale = kokokerroin
        self.width = leveys
        self.height = korkeus
        self.image = kuva
        self.clicked = tsekkaa jos klikattu
    """
    def __init__(self, rarity, name, img, scale):
        self.rarity = rarity
        self.name = name
        self.scale = scale
        self.width = img.get_width()
        self.height = img.get_height()
        self.image = pygame.transform.scale(img, (int(self.width * scale[0]),
                                                  int(self.height * scale[1])))
        self.clicked = False

    def return_rect(self, pos):
        return self.image.get_rect(center=(global_vars.DISPLAY_WIDTH/2 + pos[0],
                                         global_vars.DISPLAY_HEIGHT/2 - pos[1]))

    def draw(self, display, pos):
        display.blit(self.image, self.return_rect(pos))
        rect = self.return_rect(pos)
        action = False
        mouse_pos = pygame.mouse.get_pos()
        if rect.collidepoint(mouse_pos) and pygame.mouse.get_pressed()[0] == 1: # pylint: disable=duplicate-code
            if self.clicked is False:
                action = True
                self.clicked = True
        if rect.collidepoint(mouse_pos) and pygame.mouse.get_pressed()[0] == 0:
            self.clicked = False
        return action
