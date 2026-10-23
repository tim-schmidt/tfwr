# Times one maze of Gold.py per seed for each walking variant, same seeds.
# Lower is better. Run this file directly in the game.
#   0 = scan (current), 1 = lean (tree path only), 2 = fast (can_move first)
from SimGlobals import SIM_GLOBALS

items = {Items.Weird_Substance: 1000000000, Items.Power: 1000000000}
seeds = [1, 2, 3, 4, 5]
sizes = [8]
variants = [0, 1, 2]
speedup = 256

for size in sizes:
	for variant in variants:
		SIM_GLOBALS["SIZE"] = size
		SIM_GLOBALS["VARIANT"] = variant
		total = 0
		for seed in seeds:
			t = simulate("SimGoldRun", Unlocks, items, SIM_GLOBALS, seed, speedup)
			quick_print("size", size, "variant", variant, "seed", seed, "time", t)
			total += t
		quick_print("size", size, "variant", variant, "average", total / len(seeds))
