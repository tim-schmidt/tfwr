# Bones pathing A/B on one full 16x16 snake, all unlocks, no power in stock,
# three seeds each. Run this file directly in the game.
#   mode 0  Hamiltonian laps (measured: 384 to 435 s)
#   mode 1  the lap with shortcuts the whole way
#   mode 2  shortcuts until LAPFROM segments are on, then plain lap following
from SimGlobals import SIM_GLOBALS

items = {Items.Cactus: 1000000000}
seeds = [1, 2, 3]
speedup = 256

SIM_GLOBALS["WORLD"] = 16
cases = [(1, 0), (2, 64), (2, 96), (2, 128)]
for case in cases:
	SIM_GLOBALS["MODE"] = case[0]
	SIM_GLOBALS["LAPFROM"] = case[1]
	for seed in seeds:
		t = simulate("SimBonesStart", Unlocks, items, SIM_GLOBALS, seed, speedup)
		quick_print("bones mode", case[0], "lapFrom", case[1], "seed", seed, "time", t)
