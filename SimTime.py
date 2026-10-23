# Time test: seconds to each target of wood for each contender (see
# SimTimeStart for the MODE list), watered or not, same seeds.
# wood/s = target / time. Edit `worlds`, `modes`, `waters` and `targets`
# to pick the cases. Run this file directly in the game.
from SimGlobals import SIM_GLOBALS

items = {Items.Power: 1000000000, Items.Hay: 1000000000, Items.Wood: 1000000000, Items.Carrot: 1000000000, Items.Water: 1000000000}
seeds = [1, 2, 3]
worlds = [8, 16, 32]
modes = [4]
waters = [True]
targets = [5000000, 20000000, 80000000]
speedup = 256

for target in targets:
	SIM_GLOBALS["TARGET"] = target
	for world in worlds:
		SIM_GLOBALS["WORLD"] = world
		for mode in modes:
			SIM_GLOBALS["MODE"] = mode
			for water in waters:
				SIM_GLOBALS["WATER"] = water
				total = 0
				for seed in seeds:
					t = simulate("SimTimeStart", Unlocks, items, SIM_GLOBALS, seed, speedup)
					quick_print("target", target, "world", world, "mode", mode, "water", water, "seed", seed, "time", t, "wood/s", target / t)
					total += t
				quick_print("target", target, "world", world, "mode", mode, "water", water, "average time", total / len(seeds), "wood/s", target * len(seeds) / total)
