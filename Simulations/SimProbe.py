# Four probes, all unlocks unless stated. Run this file directly in the game.
#   1 substance: Weird Substance from one fertilized tree, request met or not
#   2 unlocks: how simulate() reads a partial unlock sequence
#   3 power: sunflower power with the 8x rule and without
#   4 bones: one full snake on 16x16 with Bones.py as it stands
from SimGlobals import SIM_GLOBALS

items = {Items.Power: 1000000000, Items.Hay: 1000000000, Items.Wood: 1000000000, Items.Carrot: 1000000000, Items.Water: 1000000000, Items.Fertilizer: 100, Items.Cactus: 1000000000}
seeds = [1, 2, 3]
speedup = 256

SIM_GLOBALS["WORLD"] = 8
for satisfy in [True, False]:
	SIM_GLOBALS["SATISFY"] = satisfy
	for seed in seeds:
		simulate("SimSubstanceStart", Unlocks, items, SIM_GLOBALS, seed, speedup)

cases = [[Unlocks.Trees], [Unlocks.Trees, Unlocks.Trees], [Unlocks.Trees, Unlocks.Trees, Unlocks.Trees, Unlocks.Expand, Unlocks.Expand]]
for case in cases:
	quick_print("unlocks probe sequence length", len(case))
	simulate("SimUnlocksStart", case, {}, SIM_GLOBALS, 1, speedup)

for seed in seeds:
	simulate("SimPowerStart", Unlocks, items, SIM_GLOBALS, seed, speedup)

SIM_GLOBALS["WORLD"] = 16
for seed in seeds:
	t = simulate("SimBonesStart", Unlocks, items, SIM_GLOBALS, seed, speedup)
	quick_print("bones probe seed", seed, "time", t)
