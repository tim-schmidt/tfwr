# Probe start file for SimProbe.py. Not run directly.
# One tree at (0, 0), fertilized once. SATISFY True plants the tree's
# requested companion on the requested tile; False plants a different crop
# there instead. Prints wood and Weird Substance from the single harvest.
from Utilities import *

set_world_size(WORLD)
clear()
RefreshSoilCrops()
n = get_world_size()
if can_harvest():
	harvest()
plant(Entities.Tree)
ask = get_companion()
if ask == None:
	quick_print("substance probe: tree has no request")
else:
	kind = ask[0]
	pos = ask[1]
	want = kind
	if not SATISFY:
		want = Entities.Bush
		if kind == Entities.Bush:
			want = Entities.Carrot
	MoveTo(n, 0, 0, pos[0], pos[1])
	if can_harvest():
		harvest()
	TillIfNeeded(want)
	plant(want)
	MoveTo(n, pos[0], pos[1], 0, 0)
	use_item(Items.Fertilizer)
	while not can_harvest():
		pass
	wood = num_items(Items.Wood)
	goo = num_items(Items.Weird_Substance)
	harvest()
	quick_print("substance probe satisfy", SATISFY, "asked", kind, "wood", num_items(Items.Wood) - wood, "substance", num_items(Items.Weird_Substance) - goo)
