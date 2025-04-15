import math
import pygame
from objects import button
from objects import level
from objects import dice

from static_items import lists
from src.static_items import global_vars

class Game():
    def __init__(self):
        self.load_images()

        self.level = level.Level(1)
        self.state = "game"

        self.dice = [dice.Dice(), dice.Dice(), dice.Dice(), dice.Dice(), dice.Dice()]

        # Create Buttons
        self.buttons = {
            "reroll": button.Button((0, -global_vars.DISPLAY_HEIGHT/3.5),
                                           self.sprites["restart"], (1,1)),
            "submit": button.Button((0, global_vars.DISPLAY_HEIGHT/6.75),
                                           self.sprites["submit"], (1,1)),
            "continue": button.Button((0, -global_vars.DISPLAY_HEIGHT/2.5),
                                           self.sprites["continue"], (1,1)),
            "buy-reroll": button.Button((0, 0),
                                           self.sprites["buy"], (1,1)),
            "buy-upgrade-count": button.Button((0, 30),
                                           self.sprites["buy"], (1,1)),
            "buy-shop-size": button.Button((0, 60),
                                           self.sprites["buy"], (1,1)),
            "buy-shop-rarity": button.Button((0, 90),
                                           self.sprites["buy"], (1,1))
        }

        self.display = pygame.display.set_mode((global_vars.DISPLAY_WIDTH,
                                                global_vars.DISPLAY_HEIGHT))

        pygame.display.set_caption("Game")

        # Gamevars
        self.coins = 0
        self.max_rerolls = 2
        self.rerolls = self.max_rerolls
        self.shop_items = 3
        self.shop_level = 1
        self.upgrade_amount = 2
        self.reset_gamevars()

        pygame.init() # pylint: disable=no-member
        self.game_loop()

    def reset_gamevars(self):
        # Gamevars
        self.coins = 0
        self.max_rerolls = 2
        self.rerolls = self.max_rerolls
        self.shop_items = 3
        self.shop_level = 1
        self.upgrade_amount = 2

    def load_images(self):
        self.sprites = {
            "restart": pygame.image.load("src/assets/DiceGameRe-roll.png"),
            "remaining": pygame.image.load("src/assets/DiceGameRemaining.png"),
            "submit": pygame.image.load("src/assets/DiceGameSubmit.png"),
            "continue": pygame.image.load("src/assets/DiceGameContinue.png"),
            "buy": pygame.image.load("src/assets/DiceGameBuy.png"),
            "shop": pygame.image.load("src/assets/DiceGameShop.png")
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
        global_vars.write_text("COINS: " + str(self.coins),
                   (-global_vars.DISPLAY_WIDTH/2 + 80,
                    -global_vars.DISPLAY_HEIGHT/2 + 30), 32, self.display)
        # REROLLS text
        remaining_spire_rect = self.sprites["remaining"].get_rect(
            center=(global_vars.DISPLAY_WIDTH/2,
                    global_vars.DISPLAY_HEIGHT/2 + global_vars.DISPLAY_HEIGHT/3))
        self.display.blit(self.sprites["remaining"], remaining_spire_rect)
        global_vars.write_text(str(self.rerolls),
                   (40,-global_vars.DISPLAY_HEIGHT/3), 20, self.display)

    def game_buttons(self):
        # Buttons
        if self.rerolls > 0:
            if self.buttons["reroll"].draw(self.display):
                self.rerolls -= 1
                self.dice = self.level.reroll(self.dice)
        else:
            self.buttons["reroll"].draw(self.display, disabled=True)
        if self.buttons["submit"].draw(self.display):
            self.level.un_select_dice(self.dice)
            complete_status, coin_increase = self.level.complete(
                self.dice, self.max_rerolls, self.rerolls)
            self.coins += coin_increase
            self.state = "results"

    def continue_button(self, complete_status, coin_increase):
        if self.buttons["continue"].draw(self.display):
            self.rerolls = self.max_rerolls
            self.dice = self.level.reroll(self.dice)
            self.state = "game"
            if complete_status:
                self.level = level.Level(self.level.level+1)
            else:
                self.level = level.Level(1)
                self.reset_gamevars()

    def shop_background(self, complete_status):
        if complete_status:
            self.display.fill("#038731")
            global_vars.write_text("LEVEL " + str(self.level.level) + " COMPLETE!",
                       (0,global_vars.DISPLAY_HEIGHT/2.5), 50, self.display)
            # Images
            global_vars.draw_image(self.sprites["shop"], (2,2),
                                    (0,global_vars.DISPLAY_HEIGHT/4.5), self.display)

            self.shop_text()
            self.shop_base_upgrades()
        else:
            self.display.fill("#870319")
            global_vars.write_text("LEVEL " + str(self.level.level) + " FAILED!",
                       (0,global_vars.DISPLAY_HEIGHT/2.5), 50, self.display)

    def shop_text(self):
        # Text
        global_vars.write_text("MORE REROLLS",
                       (-global_vars.DISPLAY_WIDTH/6.5,0), 20, self.display)
        global_vars.write_text("MORE UPGRADE SLOTS",
                       (-global_vars.DISPLAY_WIDTH/6.5,30), 20, self.display)
        global_vars.write_text("MORE SHOP ITEMS",
                       (-global_vars.DISPLAY_WIDTH/6.5,60), 20, self.display)
        global_vars.write_text("MORE RARES IN SHOP",
                       (-global_vars.DISPLAY_WIDTH/6.5,90), 20, self.display)
        global_vars.write_text("COINS: " + str(self.coins),
                   (-global_vars.DISPLAY_WIDTH/2 + 80,
                    -global_vars.DISPLAY_HEIGHT/2 + 30), 32, self.display)

    def shop_base_upgrades(self):
        # Buttons
        if lists.max_reroll_upgrade_prices[self.max_rerolls]:
            if self.buttons["buy-reroll"].draw(self.display) and self.coins >= lists.max_reroll_upgrade_prices[self.max_rerolls]: # pylint: disable=line-too-long
                self.max_rerolls += 1
            global_vars.write_text(str(lists.max_reroll_upgrade_prices[self.max_rerolls]),
                                   (0,0), 20, self.display)
        if lists.upgrade_amount_upgrade_prices[self.upgrade_amount]:
            if self.buttons["buy-upgrade-count"].draw(self.display) and self.coins >= lists.upgrade_amount_upgrade_prices[self.upgrade_amount]: # pylint: disable=line-too-long
                self.upgrade_amount += 1
            global_vars.write_text(str(lists.upgrade_amount_upgrade_prices[self.upgrade_amount]),
                                   (0,30), 20, self.display)
        if lists.shop_size_upgrade_prices[self.shop_items]:
            if self.buttons["buy-shop-size"].draw(self.display) and self.coins >= lists.shop_size_upgrade_prices[self.shop_items]: # pylint: disable=line-too-long
                self.shop_items += 1
            global_vars.write_text(str(lists.shop_size_upgrade_prices[self.shop_items]),
                                   (0,60), 20, self.display)
        if lists.shop_rarity_upgrade_prices[self.shop_level]:
            if self.buttons["buy-shop-rarity"].draw(self.display) and self.coins >= lists.shop_rarity_upgrade_prices[self.shop_level]: # pylint: disable=line-too-long
                self.shop_level += 1
            global_vars.write_text(str(lists.shop_rarity_upgrade_prices[self.shop_level]),
                                   (0,90), 20, self.display)

    def game_loop(self):
        # Interface
        pygame.display.update()
        running = True
        self.dice = self.level.reroll(self.dice)
        while running:
            if self.state == "game":
                self.game_background()
                self.game_buttons()
                self.game_text()
            if self.state == "results":
                complete_status, coin_increase = self.level.complete(
                    self.dice, self.max_rerolls, self.rerolls)
                self.shop_background(complete_status)
                self.continue_button(complete_status, coin_increase)
            for event in pygame.event.get():
                if event.type == pygame.QUIT: # pylint: disable=no-member
                    running = False
            pygame.display.update()
        pygame.quit() # pylint: disable=no-member

if __name__ == "__main__":
    Game()
