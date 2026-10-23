# Probe start file for SimProbe.py. Not run directly.
# Plants two rows of sunflowers, waits for all of them, harvests the one
# with the most petals (8x rule) and then one with fewer petals (normal).
# Prints the power from each.
from Utilities import *

set_world_size(WORLD)
clear()
RefreshSoilCrops()
n = get_world_size()
x = 0
y = 0
tiles = []
for tx in range(n):
	for ty in range(2):
		MoveTo(n, x, y, tx, ty)
		x = tx
		y = ty
		if can_harvest():
			harvest()
		TillIfNeeded(Entities.Sunflower)
		plant(Entities.Sunflower)
		tiles.append((tx, ty))
petals = {}
for t in tiles:
	MoveTo(n, x, y, t[0], t[1])
	x = t[0]
	y = t[1]
	while not can_harvest():
		pass
	petals[t] = measure()
best = None
low = None
for t in tiles:
	if best == None or petals[t] > petals[best]:
		best = t
for t in tiles:
	if petals[t] < petals[best]:
		if low == None or petals[t] > petals[low]:
			low = t
MoveTo(n, x, y, best[0], best[1])
x = best[0]
y = best[1]
power = num_items(Items.Power)
harvest()
top = num_items(Items.Power) - power
normal = -1
if low != None:
	MoveTo(n, x, y, low[0], low[1])
	power = num_items(Items.Power)
	harvest()
	normal = num_items(Items.Power) - power
quick_print("power probe sunflowers", len(tiles), "best petals", petals[best], "power", top, "normal power", normal)
