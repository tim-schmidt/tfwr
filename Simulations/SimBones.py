# Bones pathing A/B: one full snake on 16x16 by Hamiltonian laps (mode 0)
# against the lap with shortcuts (mode 1) and shortcuts for the first 128
# segments only (mode 2), three seeds each, all unlocks, no power in stock.
# Run this file directly in the game.
from SimGlobals import SIM_GLOBALS

items = {Items.Cactus: 1000000000}
seeds = [1, 2, 3]
speedup = 256

SIM_GLOBALS["WORLD"] = 16
SIM_GLOBALS["LAPFROM"] = 128
for mode in [1, 2]:
	SIM_GLOBALS["MODE"] = mode
	for seed in seeds:
		t = simulate("SimBonesStart", Unlocks, items, SIM_GLOBALS, seed, speedup)
		quick_print("bones mode", mode, "seed", seed, "time", t)
