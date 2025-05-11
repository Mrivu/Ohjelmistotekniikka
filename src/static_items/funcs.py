import pygame
from src.static_items import global_vars

def write_text(text: str, pos, fontize: int, display, color=(255,255,255)):
    # Pos is offset from centre
    font = pygame.font.SysFont("Arial", fontize)
    text = font.render(text, True, color)
    text_rect = text.get_rect(
        center=(global_vars.DISPLAY_WIDTH/2 + pos[0], global_vars.DISPLAY_HEIGHT/2 - pos[1]))
    display.blit(text, text_rect)
    return text_rect

def draw_image(image, size, pos, display):
    img = image
    width = img.get_width()
    height = img.get_height()
    img = pygame.transform.scale(img, (int(width * size[0]), int(height * size[1])))
    rect = img.get_rect(center=(global_vars.DISPLAY_WIDTH/2 + pos[0],
                                global_vars.DISPLAY_HEIGHT/2 - pos[1]))
    display.blit(img, rect)
