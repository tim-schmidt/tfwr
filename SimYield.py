# Yield-per-board test on an 8x8: re-roll to full satisfaction on boards
# with 50, 62, 75 and 87 percent trees, the rest companion slots. Same
# seeds. Compare the `result` lines for wood per board and re-roll count;
# the times are the cost. Run this file directly in the game.
from SimGlobals import SIM_GLOBALS

items = {Items.Power: 1000000000, Items.Hay: 1000000000, Items.Wood: 1000000000, Items.Carrot: 1000000000}
seeds = [1, 2, 3]
world = 8
shares = [50, 62, 75, 87]
speedup = 256

SIM_GLOBALS["WORLD"] = world
SIM_GLOBALS["DISPATCH"] = False
SIM_GLOBALS["REROLL"] = True
for share in shares:
	SIM_GLOBALS["SHARE"] = share
	total = 0
	for seed in seeds:
		t = simulate("SimYieldStart", Unlocks, items, SIM_GLOBALS, seed, speedup)
		quick_print("share", share, "seed", seed, "time", t)
		total += t
	quick_print("share", share, "average time", total / len(seeds))
