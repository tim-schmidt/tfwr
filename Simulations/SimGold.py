# Single-drone gold sweep: one maze per size and seed. SimGoldStart prints
# gold gained and substance spent per maze from inside the simulation;
# this file prints the time. Together they give gold per second and gold
# per substance for each size. Run this file directly in the game.
from SimGlobals import SIM_GLOBALS

items = {Items.Weird_Substance: 1000000000, Items.Power: 1000000000}
seeds = [1, 2, 3]
sizes = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12]
speedup = 256

for size in sizes:
	SIM_GLOBALS["SIZE"] = size
	total = 0
	for seed in seeds:
		t = simulate("SimGoldStart", Unlocks, items, SIM_GLOBALS, seed, speedup)
		quick_print("size", size, "seed", seed, "time", t)
		total += t
	quick_print("size", size, "average", total / len(seeds))
