# Cost table and in-sim unlocking probe. Run this file directly in the game.
# No starting unlocks; the start file buys everything it can with a huge
# stock and prints each cost. Output is the cost table for the route.
from SimGlobals import SIM_GLOBALS

items = {Items.Hay: 1000000000, Items.Wood: 1000000000, Items.Carrot: 1000000000, Items.Pumpkin: 1000000000, Items.Cactus: 1000000000, Items.Gold: 1000000000, Items.Bone: 1000000000, Items.Power: 1000000000, Items.Weird_Substance: 1000000000, Items.Fertilizer: 1000000000, Items.Water: 1000000000}
t = simulate("SimLevelsStart", [], items, SIM_GLOBALS, 1, 256)
quick_print("levels probe time", t)
