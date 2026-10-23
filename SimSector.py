# Sector test: a 16x16 farm split into square sectors, one drone and one
# maze per sector. Sector 16 is the single-drone baseline. Each worker
# prints its origin and explored bounds, which shows where a maze anchors
# and whether several mazes coexist. Run this file directly in the game.
from SimGlobals import SIM_GLOBALS

items = {Items.Weird_Substance: 1000000000, Items.Power: 1000000000}
seeds = [1, 2, 3]
world = 16
sizes = [16, 8, 4]
speedup = 256

SIM_GLOBALS["WORLD"] = world
for size in sizes:
	SIM_GLOBALS["SIZE"] = size
	total = 0
	for seed in seeds:
		t = simulate("SimSectorStart", Unlocks, items, SIM_GLOBALS, seed, speedup)
		quick_print("world", world, "size", size, "seed", seed, "time", t)
		total += t
	quick_print("world", world, "size", size, "average", total / len(seeds))
