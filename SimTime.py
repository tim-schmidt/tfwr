# Time test: seconds to TARGET wood for each contender (see SimTimeStart
# for the MODE list), same seeds. wood/s = TARGET / time. Edit `worlds`
# and `modes` to pick the cases.
# Run this file directly in the game.
from SimGlobals import SIM_GLOBALS

items = {Items.Power: 1000000000, Items.Hay: 1000000000, Items.Wood: 1000000000, Items.Carrot: 1000000000}
seeds = [1, 2, 3]
worlds = [32]
modes = [1, 2, 3, 4]
target = 200000000
speedup = 256

SIM_GLOBALS["TARGET"] = target
for world in worlds:
	SIM_GLOBALS["WORLD"] = world
	for mode in modes:
		SIM_GLOBALS["MODE"] = mode
		total = 0
		for seed in seeds:
			t = simulate("SimTimeStart", Unlocks, items, SIM_GLOBALS, seed, speedup)
			quick_print("world", world, "mode", mode, "seed", seed, "time", t, "wood/s", target / t)
			total += t
		quick_print("world", world, "mode", mode, "average time", total / len(seeds), "wood/s", target * len(seeds) / total)
