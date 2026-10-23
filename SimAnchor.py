# Maze anchor probe: one drone, one maze smaller than the farm, no
# relocations. Prints the explored bounds and cell count for each case.
# A size-s maze should report s*s cells; more means the walls leak.
from SimGlobals import SIM_GLOBALS

items = {Items.Weird_Substance: 1000000000, Items.Power: 1000000000}
cases = [(16, 8, 0, 0), (16, 8, 8, 0), (16, 8, 8, 8), (16, 4, 5, 7), (16, 4, 14, 14), (8, 3, 2, 2)]
speedup = 256

for case in cases:
	SIM_GLOBALS["WORLD"] = case[0]
	SIM_GLOBALS["SIZE"] = case[1]
	SIM_GLOBALS["OX"] = case[2]
	SIM_GLOBALS["OY"] = case[3]
	t = simulate("SimAnchorStart", Unlocks, items, SIM_GLOBALS, 1, speedup)
