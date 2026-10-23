# Shared-maze test: one maze the size of the farm, served by all drones.
# Compare against SimGold.py single-drone times for the same size.
# Run this file directly in the game.
from SimGlobals import SIM_GLOBALS

items = {Items.Weird_Substance: 1000000000, Items.Power: 1000000000}
seeds = [1, 2, 3]
worlds = [8, 16, 32]
speedup = 256

for world in worlds:
	SIM_GLOBALS["WORLD"] = world
	SIM_GLOBALS["SIZE"] = world
	total = 0
	for seed in seeds:
		t = simulate("SimDronesStart", Unlocks, items, SIM_GLOBALS, seed, speedup)
		quick_print("world", world, "seed", seed, "time", t)
		total += t
	quick_print("world", world, "average", total / len(seeds))
