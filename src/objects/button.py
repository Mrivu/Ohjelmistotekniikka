import pygame
from src.static_items import global_vars

class Button:
    """Sisältää napin logiikan

    Attributes:
        self.scale = napin koko kerroin
        self.image = kuva
        self.clicked = varmistaa klikkaamisen tapahtuvan kerran
    """
    def  __init__(self, img, scale):
        self.scale = scale
        width = img.get_width()
        height = img.get_height()
        self.image = pygame.transform.scale(img, (int(width * scale[0]), int(height * scale[1])))
        self.clicked = False

    def return_rect(self, pos):
        return self.image.get_rect(center=(global_vars.DISPLAY_WIDTH/2 + pos[0],
                                         global_vars.DISPLAY_HEIGHT/2 - pos[1]))

    def draw(self, display, pos, disabled=False):
        action = False
        rect = self.return_rect(pos)
        if not disabled:
            display.blit(self.image, rect)
            mouse_pos = pygame.mouse.get_pos()
            if rect.collidepoint(mouse_pos) and pygame.mouse.get_pressed()[0] == 1: # pylint: disable=duplicate-code
                if self.clicked is False:
                    action = True
                    self.clicked = True
            if rect.collidepoint(mouse_pos) and pygame.mouse.get_pressed()[0] == 0:
                self.clicked = False
        else:
            display.blit(self.image, rect)
            gray_overlay = pygame.Surface(self.image.get_size())
            gray_overlay.fill((128, 128, 128))
            display.blit(gray_overlay, rect, special_flags=pygame.BLEND_RGB_MULT) # pylint: disable=no-member
        return action
