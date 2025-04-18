import pygame
from src.objects import upgrade
# from src.static_items import global_vars

green_sprites = {
    "Fear of fours": pygame.image.load("src/assets/upgrades/DiceGameUpgradesGreenFearOfFours.png"),
    "Five fives": pygame.image.load("src/assets/upgrades/DiceGameUpgradesGreenFiveFives.png"),
    "Curtain call": pygame.image.load("src/assets/upgrades/DiceGameUpgradesGreenCurtainCall.png"),
}

upgrades = {
    "green": [
        upgrade.Upgrade("Green", "Fear of fours", green_sprites["Fear of fours"], (1,1)),
        upgrade.Upgrade("Green", "Five fives", green_sprites["Five fives"], (1,1)),
        upgrade.Upgrade("Green", "Curtain call", green_sprites["Curtain call"], (1,1))
    ],
    "blue": [],
    "red": []
}

upgrade_descriptions = {
    "Fear of fours": "+4 coins if there are no 4’s in your final hand at the end of the level.",
    "Five fives": "If your hand has five fives, gain 5 coins and 55 points.",
    "Curtain call": "When you submit your hand, reroll any one’s."
}
