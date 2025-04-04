import math
import random
import lists
import pygame

import globals

class Game:
    def __init__(self):
        pass

class Level:
    def __init__(self, level: int, boss=False):
        self.level = level
        self.boss = boss
    
    def clear_score(self):
        # Return score needed to advance level
        difficulty = lists.level_difficulty[self.level-1][self.level]
        return math.ceil(((difficulty+3)**2) + difficulty*3)
    
    def boss_effect(self):
        if not self.boss:
            return None
        num = random.randint(0,len(lists.boss_effects)-1)
        return lists.boss_effects[num][num+1]

    def roll(self):
        results = []
        for d in self.dice:
            results.append(d.roll_dice())
        return
    
    def reroll(self, dice):
        for die in dice:
            if die.selected or die.result == None:
                die.result = random.randint(1, die.sides)
            die.selected = False
        return dice

    
class Dice:
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
            dice_rect = write_text(text, position, 30, display, color=(0,0,0))
        else:
            dice_rect = write_text(text, position, 30, display)
        mouse_pos = pygame.mouse.get_pos()

        if dice_rect.collidepoint(mouse_pos) and pygame.mouse.get_pressed()[0] == 1 and self.clicked == False:
            self.selected = not self.selected
            self.clicked = True
        if dice_rect.collidepoint(mouse_pos) and pygame.mouse.get_pressed()[0] == 0:
            self.clicked = False
        return action

class Button:
    def  __init__(self, pos, img, scale):
        self.pos = pos
        self.scale = scale
        self.image = img
        self.rect = img.get_rect(center=(globals.display_width/2 - pos[0], globals.display_height/2 - pos[1]))
        self.clicked = False
    
    def draw(self, display):
        action = False
        display.blit(self.image, self.rect)
        mouse_pos = pygame.mouse.get_pos()

        if self.rect.collidepoint(mouse_pos) and pygame.mouse.get_pressed()[0] == 1 and self.clicked == False:
            action = True
            self.clicked = True
        if self.rect.collidepoint(mouse_pos) and pygame.mouse.get_pressed()[0] == 0:
            self.clicked = False
        return action

class main():
    def __init__(self):
        self.display_width = globals.display_width
        self.display_height = globals.display_height

        self.load_images()

        self.level = Level(1)

        self.dice = [Dice(), Dice(), Dice(), Dice(), Dice()]

        # Create Buttons
        self.restart_button = Button((0,-globals.display_height/3.5), self.restart_sprite, 1)

        self.display = pygame.display.set_mode((self.display_width, self.display_height))

        pygame.display.set_caption("Game")

        pygame.init()   
        self.game_loop()
    
    def load_images(self):
        self.restart_sprite = pygame.image.load("src/assets/DiceGameRe-roll.png")

    def game_loop(self):
        pygame.display.update()
        running = True
        self.dice = self.level.reroll(self.dice)
        while running:
            # Background
            self.display.fill("#470278")

            self.dice = sorted(self.dice, key=lambda die: die.get_result())
            for i, die in enumerate(self.dice):
                die.draw(str(die.get_result()), ((i-math.floor(len(self.dice)/2))*50, -self.display_height/5), self.display)

            # Buttons
            if self.restart_button.draw(self.display):
                self.dice = self.level.reroll(self.dice)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
            pygame.display.update()
        pygame.quit()

def write_text(text: str, pos, fontize: int, display, color=(255,255,255)):
    # Pos is offset from centre
    font = pygame.font.SysFont("Arial", fontize)
    text = font.render(text, True, color)
    text_rect = text.get_rect(center=(globals.display_width/2 - pos[0], globals.display_height/2 - pos[1]))
    display.blit(text, text_rect)
    return text_rect

if __name__ == "__main__":
    main()