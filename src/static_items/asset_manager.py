import pygame
from src.objects import upgrade
# from src.static_items import global_vars

green_sprites = {
    "Fear of fours": pygame.image.load("src/assets/upgrades/DiceGameUpgradesGreenFearOfFours.png"),
    "Five fives": pygame.image.load("src/assets/upgrades/DiceGameUpgradesGreenFiveFives.png"),
    "Curtain call": pygame.image.load("src/assets/upgrades/DiceGameUpgradesGreenCurtainCall.png"),
    "Bold fortune": pygame.image.load("src/assets/upgrades/DiceGameUpgradesBlueBoldFortune.png"),
    "Calculated gamble": pygame.image.load("src/assets/upgrades/DiceGameUpgradesBlueRandom.png"),
    "Rerolls+": pygame.image.load("src/assets/upgrades/DiceGameUpgradesBlueRerolls+.png"),
    "Snake eyes": pygame.image.load("src/assets/upgrades/DiceGameUpgradesRedSnakeEyes.png"),
    "Six shooter": pygame.image.load("src/assets/upgrades/DiceGameUpgradesRedSixShooter.png"),
    "Raise the stakes": pygame.image.load("src/assets/upgrades/DiceGameUpgradesRedRaiseTheStakes.png"),
}

upgrades = {
    "Green": [
        upgrade.Upgrade("Green", "Fear of fours", green_sprites["Fear of fours"], (1,1)),
        upgrade.Upgrade("Green", "Five fives", green_sprites["Five fives"], (1,1)),
        upgrade.Upgrade("Green", "Curtain call", green_sprites["Curtain call"], (1,1))
    ],
    "Blue": [
        upgrade.Upgrade("Blue", "Bold fortune", green_sprites["Bold fortune"], (1,1)),
        upgrade.Upgrade("Blue", "Calculated gamble", green_sprites["Calculated gamble"], (1,1)),
        upgrade.Upgrade("Blue", "Rerolls+", green_sprites["Rerolls+"], (1,1))
    ],
    "Red": [
        upgrade.Upgrade("Red", "Snake eyes", green_sprites["Snake eyes"], (1,1)),
        upgrade.Upgrade("Red", "Six shooter", green_sprites["Six shooter"], (1,1)),
        upgrade.Upgrade("Red", "Raise the stakes", green_sprites["Raise the stakes"], (1,1))
    ]
}

upgrade_descriptions = {
    "Fear of fours": "+4 coins if there are no 4’s in your final hand at the end of the level.",
    "Five fives": "If your hand has five fives, gain 5 coins and 55 points.",
    "Curtain call": "When you submit your hand, reroll any one’s.",
    "Bold fortune": "+1 Points for each die rerolled.",
    "Calculated gamble": "Whenever you reroll a six, this gains x1.1 points. Starts at 1.",
    "Rerolls+": "+1 Rerolls.",
    "Snake eyes": "When you submit your hand, all 1’s give an additional +5 points.",
    "Six shooter": "When you have 5 of a kind, automatically add the 6th one.",
    "Raise the stakes": "Point requirement is increased 1.5x. Your coins at the end of the. levels are increased 2x."
}