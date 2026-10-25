# Master achievements: 1B Wood, 200M Carrots, 20M Pumpkins in one
# simulated minute. Measures the yield per harvest (mode 0) and the rate
# of the route's farming code (modes 1 to 3), see SimMasterStart.py.
# Run this file directly in the game.
from SimGlobals import SIM_GLOBALS

items = {Items.Power: 1000000000, Items.Water: 1000000000, Items.Hay: 1000000000, Items.Wood: 1000000000, Items.Carrot: 1000000000, Items.Pumpkin: 1000000000}
targets = {1: 1000000000, 2: 200000000, 3: 20000000, 4: 1000000000, 5: 200000000, 6: 20000000}
# (mode, side, pitch); side and pitch only matter to mode 6.
CASES = [(6, 4, 5), (6, 5, 6), (6, 6, 7)]
SEEDS = [1, 2, 3]
speedup = 256

for case in CASES:
	mode = case[0]
	SIM_GLOBALS["MODE"] = mode
	SIM_GLOBALS["SIDE"] = case[1]
	SIM_GLOBALS["PITCH"] = case[2]
	if mode in targets:
		SIM_GLOBALS["TARGET"] = targets[mode]
	for seed in SEEDS:
		t = simulate("SimMasterStart", Unlocks, items, SIM_GLOBALS, seed, speedup)
		quick_print("mode", mode, "side", case[1], "pitch", case[2], "seed", seed, "sim time", t)
