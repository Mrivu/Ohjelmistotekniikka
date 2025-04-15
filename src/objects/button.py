import pygame
from src.static_items import global_vars

class Button:
    def  __init__(self, pos, img, scale):
        self.pos = pos
        self.scale = scale
        width = img.get_width()
        height = img.get_height()
        self.image = pygame.transform.scale(img, (int(width * scale[0]), int(height * scale[1])))
        self.rect = img.get_rect(center=(global_vars.DISPLAY_WIDTH/2 + pos[0],
                                         global_vars.DISPLAY_HEIGHT/2 - pos[1]))
        self.clicked = False

    def draw(self, display, disabled=False):
        action = False
        if not disabled:
            display.blit(self.image, self.rect)
            mouse_pos = pygame.mouse.get_pos()
            if self.rect.collidepoint(mouse_pos) and pygame.mouse.get_pressed()[0] == 1:
                if self.clicked is False:
                    action = True
                    self.clicked = True
            if self.rect.collidepoint(mouse_pos) and pygame.mouse.get_pressed()[0] == 0:
                self.clicked = False
        else:
            display.blit(self.image, self.rect)
            gray_overlay = pygame.Surface(self.image.get_size())
            gray_overlay.fill((128, 128, 128))
            display.blit(gray_overlay, self.rect, special_flags=pygame.BLEND_RGB_MULT) # pylint: disable=no-member
        return action
