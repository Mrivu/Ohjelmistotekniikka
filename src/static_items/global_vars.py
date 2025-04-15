import pygame

# Static global values
DISPLAY_HEIGHT = 800
DISPLAY_WIDTH = 1200

def write_text(text: str, pos, fontize: int, display, color=(255,255,255)):
    # Pos is offset from centre
    font = pygame.font.SysFont("Arial", fontize)
    text = font.render(text, True, color)
    text_rect = text.get_rect(
        center=(DISPLAY_WIDTH/2 + pos[0], DISPLAY_HEIGHT/2 - pos[1]))
    display.blit(text, text_rect)
    return text_rect
