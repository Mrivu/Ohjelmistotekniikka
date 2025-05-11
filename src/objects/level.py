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

    def clear_score(self, upgrades):
        # Return score needed to advance level
        difficulty = lists.level_difficulty[self.level]
        if "Raise the stakes" in [name.name for name in upgrades]:
            return math.ceil((((difficulty+3)**2) + difficulty*3))*1.5
        return math.ceil(((difficulty+3)**2) + difficulty*3)

    def current_score(self, dice, upgrades, rerolls_made):
        score = 0
        if "Calculated gamble" in [name.name for name in upgrades]:
            score += [name for name in upgrades if name.name == 'Calculated gamble'][0].multiplier
        if "Bold fortune" in [name.name for name in upgrades]:
            score += rerolls_made
        if "Curtain call" in [name.name for name in upgrades]:
            for i in dice:
                if i.result == 1:
                    i.selected = True
            dice = self.reroll(dice, upgrades)
        for num in range(6):
            amount = [die.get_result() for die in dice].count(num+1)
            mul = 1
            if amount == 3:
                mul = 1.5
            if amount == 4:
                mul = 2
            if amount == 5:
                mul = 3
                if "Six shooter" in [name.name for name in upgrades]:
                    amount += 1
            if amount == 6:
                mul = 4
            if num == 0 and "Snake eyes" in [name.name for name in upgrades]: # result == 1
                score += math.ceil(mul*(num+1)*amount)*6
            else:
                score += math.ceil(mul*(num+1)*amount)
        if "Five fives" in [name.name for name in upgrades
                            ] and len(set(dice)) == 1 and set(dice).pop() == 5:
            score += 55
        return math.ceil(score)

    def complete(self, dice, max_rerolls, rerolls, upgrades, rerolls_made):
        # Check win
        score = self.current_score(dice, upgrades, rerolls_made)
        win = score >= self.clear_score(upgrades)
        increase = 0
        # Coin increases
        if win:
            # Reroll value
            increase += (max_rerolls - rerolls)*2
            # Excess
            extra = max(math.floor((score - self.clear_score(upgrades)*2)), 0)
            increase += extra
            # Level completion
            increase += 3
            if "Fear of fours" in [name.name for name in upgrades]:
                increase += 4
            if "Five fives" in [name.name for name in upgrades]:
                increase += 5
            if "Raise the stakes" in [name.name for name in upgrades]:
                increase *= 2
        return win, increase

    def boss_effect(self):
        if not self.boss:
            return None
        num = random.randint(1,len(lists.boss_effects))
        return lists.boss_effects[num]

    def reroll(self, dice, upgrades, start_roll=False):
        no_select = True
        selected_dice = 0
        for die in dice:
            if die.selected or die.result is None:
                selected_dice += 1
                if die.result == 6 and "Calculated gamble" in [
                    name.name for name in upgrades] and not start_roll:
                    [name for name in upgrades if name.name == 'Calculated gamble'][
                        0].multiplier *= 1.1
                die.result = random.randint(1, die.sides)
                no_select = False
            die.selected = False
        if no_select:
            selected_dice += len(dice)
            for die in dice:
                if die.result == 6 and "Calculated gamble" in [
                    name.name for name in upgrades] and not start_roll:
                    [name for name in upgrades if name.name == 'Calculated gamble'][
                        0].multiplier *= 1.1
                die.result = random.randint(1, die.sides)
        return sorted(dice, key=lambda die: die.get_result(), reverse=True), selected_dice

    def un_select_dice(self, dice):
        for die in dice:
            die.selected = False
