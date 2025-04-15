import unittest
from src import game
import src.static_items.lists as lists

class TestGame(unittest.TestCase):
    def setUp(self):
        self.level = game.level.Level(1)
        self.dice = [game.dice.Dice(), game.dice.Dice(), game.dice.Dice(), game.dice.Dice(), game.dice.Dice()]
        self.max_rerolls = 2
        self.rerolls = self.max_rerolls

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