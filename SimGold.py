# Times one maze of Gold.py per seed, baseline against greedy, same seeds.
# Lower is better. Run this file directly in the game.
from SimGlobals import SIM_GLOBALS

items = {Items.Weird_Substance: 1000000000, Items.Power: 1000000000}
seeds = [1, 2, 3, 4, 5]
sizes = [8]
speedup = 256

for size in sizes:
	for greedy in [False, True]:
		SIM_GLOBALS["SIZE"] = size
		SIM_GLOBALS["GREEDY"] = greedy
		total = 0
		for seed in seeds:
			t = simulate("SimGoldRun", Unlocks, items, SIM_GLOBALS, seed, speedup)
			quick_print("size", size, "greedy", greedy, "seed", seed, "time", t)
			total += t
		quick_print("size", size, "greedy", greedy, "average", total / len(seeds))
