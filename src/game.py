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
    
class Dice:
    def __init__(self, sides=6):
        self.sides = sides
    
    def roll_dice(self):
        return random.randint(1, self.sides)

def main():
    display_height = 300
    display_width = 300

    display = pygame.display.set_mode((display_width, display_height))

    pygame.display.set_caption("Game")

    pygame.init()

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
        pygame.display.update()
    pygame.quit()

if __name__ == "__main__":
    main()