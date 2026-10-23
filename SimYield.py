# Yield-per-board test, re-roll to full satisfaction, dispatch off.
# Cases are (world, share, slots): slots 0 mixed, 1 grass, 2 bush, 3 carrot.
#   slot crop at 50% on 8x8       -> does the companion type change tree yield?
#   share 93 on 8x8               -> the sparsest layout that still covers every tile
#   16x16 at 50% and 87%          -> does board size change per-tree yield?
# Same seeds throughout. Run this file directly in the game.
from SimGlobals import SIM_GLOBALS

items = {Items.Power: 1000000000, Items.Hay: 1000000000, Items.Wood: 1000000000, Items.Carrot: 1000000000}
seeds = [1, 2, 3]
cases = [(8, 50, 1), (8, 50, 2), (8, 50, 3), (8, 50, 0), (8, 93, 0), (16, 50, 0), (16, 87, 0)]
speedup = 256

SIM_GLOBALS["DISPATCH"] = False
SIM_GLOBALS["REROLL"] = True
for case in cases:
	SIM_GLOBALS["WORLD"] = case[0]
	SIM_GLOBALS["SHARE"] = case[1]
	SIM_GLOBALS["SLOTS"] = case[2]
	total = 0
	for seed in seeds:
		t = simulate("SimYieldStart", Unlocks, items, SIM_GLOBALS, seed, speedup)
		quick_print("world", case[0], "share", case[1], "slots", case[2], "seed", seed, "time", t)
		total += t
	quick_print("world", case[0], "share", case[1], "slots", case[2], "average time", total / len(seeds))
