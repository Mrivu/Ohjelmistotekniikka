# import random
import pygame
from src.static_items import global_vars

class Upgrade:
    def __init__(self, rarity, name, img, scale):
        self.rarity = rarity
        self.name = name
        self.scale = scale
        width = img.get_width()
        height = img.get_height()
        self.image = pygame.transform.scale(img, (int(width * scale[0]), int(height * scale[1])))
        self.clicked = False

    def return_rect(self, pos):
        return self.image.get_rect(center=(global_vars.DISPLAY_WIDTH/2 + pos[0],
                                         global_vars.DISPLAY_HEIGHT/2 - pos[1]))

    def draw(self, display, pos):
        display.blit(self.image, self.return_rect(pos))
