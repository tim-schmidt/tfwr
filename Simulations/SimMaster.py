# Master achievements: 1B Wood, 200M Carrots, 20M Pumpkins in one
# simulated minute. Measures the yield per harvest (mode 0) and the rate
# of the route's farming code (modes 1 to 3), see SimMasterStart.py.
# Run this file directly in the game.
from SimGlobals import SIM_GLOBALS

items = {Items.Power: 1000000000, Items.Water: 1000000000, Items.Hay: 1000000000, Items.Wood: 1000000000, Items.Carrot: 1000000000, Items.Pumpkin: 1000000000}
targets = {1: 1000000000, 2: 200000000, 3: 20000000, 4: 2500000000, 5: 500000000, 6: 60000000}
MODES = [6]
SEEDS = [1, 2, 3]
speedup = 256

for mode in MODES:
	SIM_GLOBALS["MODE"] = mode
	if mode in targets:
		SIM_GLOBALS["TARGET"] = targets[mode]
	for seed in SEEDS:
		t = simulate("SimMasterStart", Unlocks, items, SIM_GLOBALS, seed, speedup)
		quick_print("mode", mode, "seed", seed, "sim time", t)
