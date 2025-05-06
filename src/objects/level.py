import math
import random
from src.static_items import lists

class Level:
    """Tason logiikka
    Attributes:
        self.level = tasonumero
        self.boss = onko boss-kenttä
    """
    def __init__(self, level: int, boss=False):
        self.level = level
        self.boss = boss

    def clear_score(self):
        # Return score needed to advance level
        difficulty = lists.level_difficulty[self.level]
        return math.ceil(((difficulty+3)**2) + difficulty*3)

    def current_score(self, dice, upgrades):
        score = 0
        if "Curtain call" in [name.name for name in upgrades]:
            for i in dice:
                if i.result == 1:
                    i.selected = True
            dice = self.reroll(dice)
        for num in range(6):
            amount = [die.get_result() for die in dice].count(num+1)
            mul = 1
            if amount == 3:
                mul = 1.5
            if amount == 4:
                mul = 2
            if amount == 5:
                mul = 3
            score += math.ceil(mul*(num+1)*amount)
        if "Five fives" in [name.name for name in upgrades] and len(set(dice)) == 1 and set(dice).pop() == 5:
            score += 55
        return score
    
    def complete(self, dice, max_rerolls, rerolls, upgrades):
        print(upgrades)
        # Check win
        score = self.current_score(dice, upgrades)
        win = score >= self.clear_score()
        increase = 0
        # Coin increases
        if win:
            # Reroll value
            increase += (max_rerolls - rerolls)*2
            # Excess
            extra = max(math.floor((score - self.clear_score()*2)), 0)
            increase += extra
            # Level completion
            increase += 3
            if "Fear of fours" in [name.name for name in upgrades]:
                increase += 4
            if "Five fives" in [name.name for name in upgrades]:
                increase += 5
        return win, increase

    def boss_effect(self):
        if not self.boss:
            return None
        num = random.randint(1,len(lists.boss_effects))
        return lists.boss_effects[num]

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

    def un_select_dice(self, dice):
        for die in dice:
            die.selected = False
