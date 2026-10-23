# Yield-per-board test on an 8x8: checkerboard, dispatch only, re-roll
# only, dispatch then re-roll. Same seeds. Compare the `result` lines for
# yield and the times for cost. Run this file directly in the game.
from SimGlobals import SIM_GLOBALS

items = {Items.Power: 1000000000}
seeds = [1, 2, 3]
world = 8
speedup = 256

SIM_GLOBALS["WORLD"] = world
for mode in [(False, False), (True, False), (False, True), (True, True)]:
	SIM_GLOBALS["DISPATCH"] = mode[0]
	SIM_GLOBALS["REROLL"] = mode[1]
	total = 0
	for seed in seeds:
		t = simulate("SimYieldStart", Unlocks, items, SIM_GLOBALS, seed, speedup)
		quick_print("dispatch", mode[0], "reroll", mode[1], "seed", seed, "time", t)
		total += t
	quick_print("dispatch", mode[0], "reroll", mode[1], "average time", total / len(seeds))
