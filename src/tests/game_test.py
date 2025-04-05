import unittest
from src import game
from src import lists

class TestGame(unittest.TestCase):
    def setUp(self):
        self.level = game.Level(1)
        self.dice = [game.Dice(), game.Dice(), game.Dice(), game.Dice(), game.Dice()]

    def test_level_stats(self):
        difficulty = lists.level_difficulty[self.level.level-1][self.level.level]
        clear_score = game.math.ceil(((difficulty+3)**2) + difficulty*3)
        self.assertEqual(self.level.clear_score(), clear_score)
        self.assertEqual(self.level.boss_effect(), None)
        self.level = game.Level(2,True)
        difficulty = lists.level_difficulty[self.level.level-1][self.level.level]
        clear_score = game.math.ceil(((difficulty+3)**2) + difficulty*3)
        self.assertEqual(self.level.clear_score(), clear_score)
        self.assertNotEqual(self.level.boss_effect(), None)
    
    def test_dice_roll(self):
        results = self.level.reroll(self.dice)
        self.assertEqual(len(results), 5)
    
    def test_victory(self):
        for die in self.dice:
            die.result = 1
        win = self.level.complete(self.dice)
        self.assertEqual(win, False)
        for die in self.dice:
            die.result = 5
        win = self.level.complete(self.dice)
        self.assertEqual(win, True)