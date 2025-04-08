import math
import random
import lists
import global_vars

class Level:
    def __init__(self, level: int, boss=False):
        self.level = level
        self.boss = boss

    def clear_score(self):
        # Return score needed to advance level
        difficulty = lists.level_difficulty[self.level-1][self.level]
        return math.ceil(((difficulty+3)**2) + difficulty*3)

    def current_score(self, dice):
        score = 0
        for num in range(20):
            amount = [die.get_result() for die in dice].count(num+1)
            mul = 1
            if amount == 3:
                mul = 1.5
            if amount == 4:
                mul = 2
            if amount == 5:
                mul = 3
            score += math.ceil(mul*(num+1)*amount)
        return score

    def complete(self, dice):
        # Check win
        win = self.current_score(dice) >= self.clear_score()
        # Coin increases
        if win:
            increase = 0
            # Reroll value
            increase += global_vars.MAX_REROLLS - global_vars.REROLLS
            # Excess
            extra = math.floor((self.current_score(dice) - self.clear_score())/
                               (self.clear_score()*0.5))
            increase += extra
            # Level comletion
            increase += 3
            global_vars.COINS += increase
        return win

    def boss_effect(self):
        if not self.boss:
            return None
        num = random.randint(0,len(lists.boss_effects)-1)
        return lists.boss_effects[num][num+1]

    def reroll(self, dice):
        no_select = True
        for die in dice:
            if die.selected or die.result is None:
                die.result = random.randint(1, die.sides)
                no_select = False
            die.selected = False
        if no_select:
            for die in dice:
                die.result = random.randint(1, die.sides)
        return sorted(dice, key=lambda die: die.get_result(), reverse=True)
