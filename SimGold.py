# Times one maze of Gold.py per seed and size. Lower is better.
# Run this file directly in the game. To A/B a change, run before and after.
from SimGlobals import SIM_GLOBALS

items = {Items.Weird_Substance: 1000000000, Items.Power: 1000000000}
seeds = [1, 2, 3, 4, 5]
sizes = [8]
speedup = 256

for size in sizes:
	SIM_GLOBALS["SIZE"] = size
	total = 0
	for seed in seeds:
		t = simulate("SimGoldRun", Unlocks, items, SIM_GLOBALS, seed, speedup)
		quick_print("size", size, "seed", seed, "time", t)
		total += t
	quick_print("size", size, "average", total / len(seeds))
