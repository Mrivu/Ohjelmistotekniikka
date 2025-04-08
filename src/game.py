import time
import math
import pygame
import button
import level
import dice

import global_vars

class Game():
    def __init__(self):
        self.load_images()

        self.level = level.Level(1)
        self.state = "game"

        self.dice = [dice.Dice(), dice.Dice(), dice.Dice(), dice.Dice(), dice.Dice()]

        # Create Buttons
        self.buttons = {
            "reroll": button.Button((0, -global_vars.DISPLAY_HEIGHT/3.5),
                                           self.sprites["restart"], 1),
            "submit": button.Button((0, global_vars.DISPLAY_HEIGHT/6.75),
                                           self.sprites["submit"], 1)
        }

        self.display = pygame.display.set_mode((global_vars.DISPLAY_WIDTH,
                                                global_vars.DISPLAY_HEIGHT))

        pygame.display.set_caption("Game")

        pygame.init()
        self.game_loop()

    def load_images(self):
        self.sprites = {
            "restart": pygame.image.load("src/assets/DiceGameRe-roll.png"),
            "remaining": pygame.image.load("src/assets/DiceGameRemaining.png"),
            "submit": pygame.image.load("src/assets/DiceGameSubmit.png")
        }

    def game_background(self):
        # Background
        self.display.fill("#470278")
        self.dice = sorted(self.dice, key=lambda die: die.get_result())
        for i, die in enumerate(self.dice):
            die.draw(str(die.get_result()), ((i-math.floor(len(self.dice)/2))*50,
                                             -global_vars.DISPLAY_HEIGHT/5), self.display)

    def game_text(self):
        # Text
        global_vars.write_text("LEVEL: " + str(self.level.level),
                   (0,global_vars.DISPLAY_HEIGHT/3), 55, self.display)
        global_vars.write_text("SCORE TO BEAT: " + str(self.level.clear_score()),
                   (0,global_vars.DISPLAY_HEIGHT/4), 40, self.display)
        global_vars.write_text("CURRENT: " + str(self.level.current_score(self.dice)),
                   (0,global_vars.DISPLAY_HEIGHT/5), 32, self.display)
        global_vars.write_text("COINS: " + str(global_vars.COINS),
                   (-global_vars.DISPLAY_WIDTH/2 + 80,
                    -global_vars.DISPLAY_HEIGHT/2 + 30), 32, self.display)
        # REROLLS text
        remaining_spire_rect = self.sprites["remaining"].get_rect(
            center=(global_vars.DISPLAY_WIDTH/2,
                    global_vars.DISPLAY_HEIGHT/2 + global_vars.DISPLAY_HEIGHT/3))
        self.display.blit(self.sprites["remaining"], remaining_spire_rect)
        global_vars.write_text(str(global_vars.REROLLS),
                   (40,-global_vars.DISPLAY_HEIGHT/3), 20, self.display)

    def game_buttons(self):
        # Buttons
        if global_vars.REROLLS > 0:
            if self.buttons["reroll"].draw(self.display):
                global_vars.REROLLS -= 1
                self.dice = self.level.reroll(self.dice)
        else:
            self.buttons["reroll"].draw(self.display, disabled=True)
        if self.buttons["submit"].draw(self.display):
            global_vars.REROLLS = 0
            self.state = "results"

    def results(self):
        if self.level.complete(self.dice):
            self.display.fill("#038731")
            global_vars.write_text("LEVEL " + str(self.level.level) + " COMPLETE!",
                       (0,global_vars.DISPLAY_HEIGHT/2.5), 50, self.display)
            pygame.display.update()
            time.sleep(3)
            self.level = level.Level(self.level.level+1)
        else:
            self.display.fill("#870319")
            global_vars.write_text("LEVEL " + str(self.level.level) + " FAILED!",
                       (0,global_vars.DISPLAY_HEIGHT/2.5), 50, self.display)
            pygame.display.update()
            time.sleep(3)
            self.level = level.Level(1)
            global_vars.COINS = 0
        global_vars.REROLLS = global_vars.MAX_REROLLS
        self.dice = self.level.reroll(self.dice)
        self.state = "game"

    def game_loop(self):
        pygame.display.update()
        running = True
        self.dice = self.level.reroll(self.dice)
        while running:
            if self.state == "game":
                self.game_background()
                self.game_buttons()
                self.game_text()
            if self.state == "results":
                self.results()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
            pygame.display.update()
        pygame.quit()

if __name__ == "__main__":
    Game()
