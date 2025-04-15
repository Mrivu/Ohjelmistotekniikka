import unittest
from src import game
import src.static_items.lists as lists

class TestGame(unittest.TestCase):
    def setUp(self):
        self.level = game.level.Level(1)
        self.dice = [game.dice.Dice(), game.dice.Dice(), game.dice.Dice(), game.dice.Dice(), game.dice.Dice()]
        self.max_rerolls = 2
        self.rerolls = self.max_rerolls
        self.shop_items = 3
        self.shop_level = 1
        self.upgrade_amount = 2
        self.coins = 0

    def test_level_stats(self):
        difficulty = lists.level_difficulty[self.level.level]
        clear_score = game.math.ceil(((difficulty+3)**2) + difficulty*3)
        self.assertEqual(self.level.clear_score(), clear_score)
        self.assertEqual(self.level.boss_effect(), None)
        self.level = game.level.Level(2,True)
        difficulty = lists.level_difficulty[self.level.level]
        clear_score = game.math.ceil(((difficulty+3)**2) + difficulty*3)
        self.assertEqual(self.level.clear_score(), clear_score)
        self.assertNotEqual(self.level.boss_effect(), None)
    
    def test_dice_roll(self):
        results = self.level.reroll(self.dice)
        self.assertEqual(len(results), 5)
    
    def test_victory(self):
        for die in self.dice:
            die.result = 1
        win_status, increase = self.level.complete(self.dice, self.max_rerolls, self.rerolls)
        self.assertEqual(win_status, False)
        for die in self.dice:
            die.result = 5
        win_status, increase = self.level.complete(self.dice, self.max_rerolls, self.rerolls)
        self.assertEqual(win_status, True)
    
    def test_purchase(self):
        # Not enough coins
        if lists.max_reroll_upgrade_prices[self.max_rerolls]:
            if self.coins >= lists.max_reroll_upgrade_prices[self.max_rerolls]:
                self.max_rerolls += 1
        self.assertEqual(self.max_rerolls, 2)
        # Enough coins
        self.coins += lists.max_reroll_upgrade_prices[self.max_rerolls]
        if lists.max_reroll_upgrade_prices[self.max_rerolls]:
            if self.coins >= lists.max_reroll_upgrade_prices[self.max_rerolls]:
                self.max_rerolls += 1
        self.assertEqual(self.max_rerolls, 3)
        # Max level
        self.max_rerolls = 5
        if lists.max_reroll_upgrade_prices[self.max_rerolls]:
            self.max_rerolls += 1
        self.assertEqual(self.max_rerolls, 5)

        # Tätä ei näy coverage reportissa, sillä functiot eivät palauta mitään
