# Crop test: time to TARGET wood with trees and grass, checkerboard versus
# companion planting, single drone and all drones, same seeds.
# wood/s = TARGET / time. Run this file directly in the game.
from SimGlobals import SIM_GLOBALS

items = {Items.Power: 1000000000, Items.Hay: 1000000000, Items.Wood: 1000000000, Items.Carrot: 1000000000}
seeds = [1, 2, 3]
world = 8
target = 200000000
speedup = 256

SIM_GLOBALS["WORLD"] = world
SIM_GLOBALS["TARGET"] = target
for drones in [False, True]:
	for companions in [False, True]:
		SIM_GLOBALS["DRONES"] = drones
		SIM_GLOBALS["COMPANIONS"] = companions
		total = 0
		for seed in seeds:
			t = simulate("SimCropsStart", Unlocks, items, SIM_GLOBALS, seed, speedup)
			quick_print("drones", drones, "companions", companions, "seed", seed, "time", t, "wood/s", target / t)
			total += t
		quick_print("drones", drones, "companions", companions, "average time", total / len(seeds), "wood/s", target * len(seeds) / total)
