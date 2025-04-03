import math
import random
import lists
import pygame

class Game:
    def __init__(self):
        pass

class Level:
    def __init__(self, level, boss=False):
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
    
    def reroll(self, list):
        pass

    
class Dice:
    def __init__(self, sides=6):
        self.sides = sides
        self.result = None
    
    def roll_dice(self):
        self.result = random.randint(1, self.sides)
    
    def get_result(self):
        return self.result

class Button:
    def  __init__(self, pos, img, scale):
        self.pos = pos
        self.scale = scale

class main():
    def __init__(self):
        self.display_height = 800
        self.display_width = 1200

        self.dice = [Dice(), Dice(), Dice(), Dice(), Dice()]

        self.display = pygame.display.set_mode((self.display_width, self.display_height))

        pygame.display.set_caption("Game")

        pygame.init()   
        self.display.fill("#470278")
        self.game_loop()

    def game_loop(self):
        pygame.display.update()
        running = True
        self.update_dice()
        while running:
            for i, die in enumerate(self.dice):
                self.write_text(str(die.get_result()), ((i-math.floor(len(self.dice)/2))*50, -self.display_height/5), 30)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
            pygame.display.update()
        pygame.quit()

    def write_text(self, text, pos, fontize, color=(255,255,255)):
        # Pos is offset from centre
        font = pygame.font.SysFont("Arial", fontize)
        text = font.render(text, True, color)

        text_rect = text.get_rect(center=(self.display_width/2 - pos[0], self.display_height/2 - pos[1]))
        self.display.blit(text, text_rect)
    
    def update_dice(self):
        for die in self.dice:
            die.result = random.randint(1, die.sides)

if __name__ == "__main__":
    main()