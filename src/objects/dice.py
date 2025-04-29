import random
import pygame
from src.static_items import funcs

class Dice:
    """Yksittäisen nopan logiikka
    Attributes:
        self.sides = noppien silmälukujen määrä
        self.result = nopanheiton tulos
        self.selected = nopan valittu tila
        self.clicked = onko noppaa painettu
    """
    def __init__(self, sides=6):
        self.sides = sides
        self.result = None
        self.selected = False
        self.clicked = False

    def roll_dice(self):
        self.result = random.randint(1, self.sides)

    def get_result(self):
        return self.result

    def draw(self, text, position, display):
        action = False
        if self.selected:
            dice_rect = funcs.write_text(text, position, 30, display, color=(0,0,0))
        else:
            dice_rect = funcs.write_text(text, position, 30, display)
        mouse_pos = pygame.mouse.get_pos()

        if dice_rect.collidepoint(mouse_pos) and pygame.mouse.get_pressed()[0] == 1:
            if self.clicked is False:
                self.selected = not self.selected
                self.clicked = True
        if dice_rect.collidepoint(mouse_pos) and pygame.mouse.get_pressed()[0] == 0:
            self.clicked = False
        return action
