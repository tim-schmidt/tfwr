# Time test: seconds to each target of wood for each contender (see
# SimTimeStart for the MODE list), watered or not, same seeds.
# wood/s = target / time. Drones live on the Watering income inside the
# sim plus a starting reserve from `reserves`. Cases are (world, target).
# Edit `cases`, `modes`, `waters` and `reserves` to pick them. Run this
# file directly in the game.
from SimGlobals import SIM_GLOBALS

seeds = [1, 2, 3]
cases = [(16, 20000000)]
modes = [4]
waters = [True]
reserves = [0, 1000, 3000]
speedup = 256

for case in cases:
	world = case[0]
	target = case[1]
	SIM_GLOBALS["WORLD"] = world
	SIM_GLOBALS["TARGET"] = target
	for mode in modes:
		SIM_GLOBALS["MODE"] = mode
		for water in waters:
			SIM_GLOBALS["WATER"] = water
			for reserve in reserves:
				items = {Items.Power: 1000000000, Items.Hay: 1000000000, Items.Wood: 1000000000, Items.Carrot: 1000000000, Items.Water: reserve}
				total = 0
				for seed in seeds:
					t = simulate("SimTimeStart", Unlocks, items, SIM_GLOBALS, seed, speedup)
					quick_print("target", target, "world", world, "mode", mode, "water", water, "reserve", reserve, "seed", seed, "time", t, "wood/s", target / t)
					total += t
				quick_print("target", target, "world", world, "mode", mode, "water", water, "reserve", reserve, "average time", total / len(seeds), "wood/s", target * len(seeds) / total)
