import math
import random
import time
import pygame
from objects import button
from objects import level
from objects import dice

from static_items import lists
from static_items import global_vars
from static_items import asset_manager

class Game():
    def __init__(self):
        self.load_images()

        self.level = level.Level(1)
        self.state = "game"

        self.dice = [dice.Dice(), dice.Dice(), dice.Dice(), dice.Dice(), dice.Dice()]

        # Create Buttons
        self.buttons = {
            "reroll": button.Button(self.sprites["restart"], (1,1)),
            "submit": button.Button(self.sprites["submit"], (1,1)),
            "continue": button.Button(self.sprites["continue"], (1,1)),
            "buy-reroll": button.Button(self.sprites["buy"], (1,1)),
            "buy-upgrade-count": button.Button(self.sprites["buy"], (1,1)),
            "buy-shop-size": button.Button(self.sprites["buy"], (1,1)),
            "buy-shop-rarity": button.Button(self.sprites["buy"], (1,1))
        }

        self.upgrades = []

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
        self.shop_buffer = False
        self.display_timer = [0,5, None]
        self.reset_gamevars()

        pygame.init() # pylint: disable=no-member
        self.game_loop()

    def reset_gamevars(self):
        # Gamevars
        self.coins = 11
        self.max_rerolls = 2
        self.rerolls = self.max_rerolls
        self.shop_items = 6
        self.shop_level = 1
        self.upgrade_amount = 2
        self.shop_buffer = False
        self.display_timer = [0,5, None]
        self.upgrades = []

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
                                             -global_vars.DISPLAY_HEIGHT/6.25), self.display)

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
                    global_vars.DISPLAY_HEIGHT/2 + global_vars.DISPLAY_HEIGHT/3.35))
        self.display.blit(self.sprites["remaining"], remaining_spire_rect)
        global_vars.write_text(str(self.rerolls),
                   (40,-global_vars.DISPLAY_HEIGHT/3.35), 20, self.display)

    def game_buttons(self):
        # Buttons
        if self.rerolls > 0:
            if self.buttons["reroll"].draw(self.display, (0, -global_vars.DISPLAY_HEIGHT/4)):
                self.rerolls -= 1
                self.dice = self.level.reroll(self.dice)
        else:
            self.buttons["reroll"].draw(self.display,
                                        (0, -global_vars.DISPLAY_HEIGHT/4), disabled=True)
        if self.buttons["submit"].draw(self.display, (0, global_vars.DISPLAY_HEIGHT/6.75),):
            self.level.un_select_dice(self.dice)
            self.state = "init_shop"

    def continue_button(self, complete_status, upgrades):
        if self.buttons["continue"].draw(self.display, (0, -global_vars.DISPLAY_HEIGHT/4)):
            self.rerolls = self.max_rerolls
            self.dice = self.level.reroll(self.dice)
            self.state = "game"
            if complete_status:
                self.level = level.Level(self.level.level+1)
                for upgrade in upgrades:
                    self.buttons[upgrade.name] = None
                    upgrades = []
            else:
                self.level = level.Level(1)
                self.reset_gamevars()
                upgrades = []

    def shop_background(self, complete_status, upgrades):
        if complete_status:
            self.display.fill("#038731")
            global_vars.write_text("LEVEL " + str(self.level.level) + " COMPLETE!",
                       (0,global_vars.DISPLAY_HEIGHT/2.5), 50, self.display)
            # Images
            global_vars.draw_image(self.sprites["shop"], (2,2),
                                    (0,global_vars.DISPLAY_HEIGHT/4.25), self.display)

            self.shop_text()
            self.shop_base_upgrades()
            self.shop_upgrades(upgrades)
            self.display_upgrades()
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
            if self.buttons["buy-reroll"].draw(self.display, (-30,0)) and self.coins >= lists.max_reroll_upgrade_prices[self.max_rerolls]: # pylint: disable=line-too-long
                self.coins -= lists.max_reroll_upgrade_prices[self.max_rerolls]
                self.max_rerolls += 1
            global_vars.write_text(str(lists.max_reroll_upgrade_prices[self.max_rerolls]),
                                   (-30,0), 20, self.display)
        if lists.upgrade_amount_upgrade_prices[self.upgrade_amount]:
            if self.buttons["buy-upgrade-count"].draw(self.display, (-30,30)) and self.coins >= lists.upgrade_amount_upgrade_prices[self.upgrade_amount]: # pylint: disable=line-too-long
                self.coins -= lists.upgrade_amount_upgrade_prices[self.upgrade_amount]
                self.upgrade_amount += 1
            global_vars.write_text(str(lists.upgrade_amount_upgrade_prices[self.upgrade_amount]),
                                   (-30,30), 20, self.display)
        if lists.shop_size_upgrade_prices[self.shop_items]:
            if self.buttons["buy-shop-size"].draw(self.display, (-30,60)) and self.coins >= lists.shop_size_upgrade_prices[self.shop_items]: # pylint: disable=line-too-long
                self.coins -= lists.shop_size_upgrade_prices[self.shop_items]
                self.shop_items += 1
            global_vars.write_text(str(lists.shop_size_upgrade_prices[self.shop_items]),
                                   (-30,60), 20, self.display)
        if lists.shop_rarity_upgrade_prices[self.shop_level]:
            if self.buttons["buy-shop-rarity"].draw(self.display, (-30,90)) and self.coins >= lists.shop_rarity_upgrade_prices[self.shop_level]: # pylint: disable=line-too-long
                self.coins -= lists.shop_rarity_upgrade_prices[self.shop_level]
                self.shop_level += 1
            global_vars.write_text(str(lists.shop_rarity_upgrade_prices[self.shop_level]),
                                   (-30,90), 20, self.display)

    def get_upgrades(self):
        rarity_array = lists.shop_level_rarities[self.shop_level]
        upgrades = []
        # Generoitu tekoälyllä - alku
        available_upgrades = {
            rarity: [
                upg for upg in asset_manager.upgrades[rarity]
                if upg not in self.upgrades
            ]
            for rarity in asset_manager.upgrades
        }
        # Generoitu tekoälyllä - loppu
        for i in range(self.shop_items):
            if random.randint(1,100) <= rarity_array[0]:
                rarity = "Green"
            elif random.randint(1,100) <= rarity_array[1]:
                rarity = "Blue"
            else:
                rarity = "Red"
            if len(available_upgrades[rarity]) > 0:
                upgrade = available_upgrades[rarity][
                    random.randint(0, len(available_upgrades[rarity])-1)]
                available_upgrades[rarity].remove(upgrade)
                upgrades.append(upgrade)
                self.buttons[upgrade.name] = button.Button(self.sprites["buy"], (1,1))
        return upgrades

    def init_shop(self, coin_increase):
        self.coins += coin_increase
        self.state = "results"
        return self.get_upgrades()

    def shop_upgrades(self, upgrades):
        for i, upgrade in enumerate(upgrades):
            if upgrade.draw(self.display, ((upgrade.width+10)*(i%3)+40, 90 if i < 3 else 30)):
                self.display_timer[0] = self.display_timer[1]
                self.display_timer[2] = upgrade.name
            if self.buttons[upgrade.name].draw(self.display,
                                               ((upgrade.width+10)*(i%3)+40,
                                                50 if i < 3 else -10)) and self.coins >= 5:
                if not self.shop_buffer and len(self.upgrades) < self.upgrade_amount:
                    self.coins -= 5
                    self.upgrades.append(upgrade)
                    self.buttons[upgrade.name] = None
                    self.buttons[upgrade.name+"_sell"] = button.Button(self.sprites["buy"], (1,1))
                    upgrades.remove(upgrade)
                    self.shop_buffer = True
            global_vars.write_text("5",
                                   ((upgrade.width+10)*(i%3)+40,
                                        50 if i < 3 else -10), 20, self.display)
        if pygame.mouse.get_pressed()[0] == 0:
            self.shop_buffer = False

    def display_upgrades(self, can_sell=True):
        global_vars.write_text("Upgrades owned: " + str(len(self.upgrades)) +
                               "/" + str(self.upgrade_amount),
                               (-global_vars.DISPLAY_WIDTH/3,300), 26, self.display)
        for i, upgrade in enumerate(self.upgrades):
            if upgrade.draw(self.display, (-global_vars.DISPLAY_WIDTH/2.5, 250 - i*50)):
                self.display_timer[0] = self.display_timer[1]
                self.display_timer[2] = upgrade.name
        if can_sell:
            for i, upgrade in enumerate(self.upgrades):
                global_vars.write_text("Sell: ",
                               (-global_vars.DISPLAY_WIDTH/3, 250 - i*50),
                               25, self.display)
                if self.buttons[upgrade.name+"_sell"].draw(self.display,
                                                           (-global_vars.DISPLAY_WIDTH/3.5, 250 - i*50)):
                    self.buttons[upgrade.name+"_sell"] = None
                    self.coins += lists.rarity_values[upgrade.rarity][1]
                    self.upgrades.remove(upgrade)
                global_vars.write_text(str(lists.rarity_values[upgrade.rarity][1]),
                                        (-global_vars.DISPLAY_WIDTH/3.5, 250 - i*50),
                                        20, self.display)

    def upgrade_description(self, upgrade_name):
        x = global_vars.DISPLAY_WIDTH*0.8
        y = 80
        desc_area = pygame.Surface((x, y))
        desc_area.fill((112, 112, 112))
        self.display.blit(desc_area,
                          ((global_vars.DISPLAY_WIDTH/2-(x/2)),
                                      (global_vars.DISPLAY_HEIGHT/2 +
                                       global_vars.DISPLAY_HEIGHT/2.5 - y*0.65)))
        global_vars.write_text(upgrade_name + ":",
                               (0, -global_vars.DISPLAY_HEIGHT/2.5 + 30),
                               25, self.display)
        global_vars.write_text(asset_manager.upgrade_descriptions[upgrade_name],
                               (0, -global_vars.DISPLAY_HEIGHT/2.5),
                               20, self.display)

    def desc_countdown(self, upgrade_name):
        start = time.time()
        self.upgrade_description(upgrade_name)
        self.display_timer[0] -= (time.time() - start)*10

    def game_loop(self):
        # Interface
        pygame.display.update()
        running = True
        self.dice = self.level.reroll(self.dice)
        complete_status = None
        coin_increase = 0
        upgrades = []
        while running:
            if self.state == "game":
                self.game_background()
                self.game_buttons()
                self.game_text()
                self.display_upgrades()

                # desc countdown
                if self.display_timer[0] > 0:
                    self.desc_countdown(self.display_timer[2])
            if self.state == "init_shop":
                complete_status, coin_increase = self.level.complete(
                    self.dice, self.max_rerolls, self.rerolls)
                upgrades = self.init_shop(coin_increase)
            if self.state == "results":
                self.shop_background(complete_status, upgrades)
                self.continue_button(complete_status, upgrades)

                # desc countdown
                if self.display_timer[0] > 0:
                    self.desc_countdown(self.display_timer[2])
            for event in pygame.event.get():
                if event.type == pygame.QUIT: # pylint: disable=no-member
                    running = False
            pygame.display.update()
        pygame.quit() # pylint: disable=no-member

if __name__ == "__main__":
    Game()
