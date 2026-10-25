# Start file that simulate() loads for SimMaster.py. Not run directly.
# MODE and TARGET arrive through sim_globals. All unlocks, huge stocks of
# Power, Water, Hay, Wood and Carrot, no Fertilizer (half of a fertilized
# plant's yield turns into Weird Substance).
#   MODE 0  yield probe: one tree and one carrot, request met and not met,
#           then a 6x6 and a 2x2 square of pumpkins
#   MODE 1  wood with the route's companion sweep, 32x32, all drones
#   MODE 2  carrots the same way
#   MODE 3  pumpkins with the route's strip code, 32x32, all drones
#   MODE 4  wood with Masters.ChaseCrops (companion chase, one column each)
#   MODE 5  carrots the same way
#   MODE 6  pumpkins with Masters.BlockPumpkins (one 6x6 block per drone)
# Modes 1 to 3 run until TARGET items are gained and print the rate per
# simulated minute, which is what the Master achievements count.
from Utilities import *
from StandardCrops import CultivateCropsWithDrones
from Pumpkins import CultivatePumpkinsWithDrones, growPumpkinStrip
from Masters import ChaseCrops, BlockPumpkins

# One plant at (0, 0) with its request met (satisfy True) or deliberately
# not met. Returns the items of `item` from the single harvest.
def oneHarvest(n, crop, item, satisfy):
	clear()
	if can_harvest():
		harvest()
	TillIfNeeded(crop)
	plant(crop)
	ask = get_companion()
	if ask == None:
		quick_print("probe: no request from", crop)
		return 0
	kind = ask[0]
	pos = ask[1]
	want = kind
	if not satisfy:
		want = Entities.Bush
		if kind == Entities.Bush:
			want = Entities.Tree
	MoveTo(n, 0, 0, pos[0], pos[1])
	if can_harvest():
		harvest()
	TillIfNeeded(want)
	plant(want)
	MoveTo(n, pos[0], pos[1], 0, 0)
	while not can_harvest():
		pass
	before = num_items(item)
	harvest()
	return num_items(item) - before

# A side x side square of pumpkins grown in the corner of the farm,
# harvested as one. Returns the pumpkins from that harvest.
def pumpkinSquare(n, side):
	clear()
	for x in range(side):
		for y in range(side):
			MoveTo(n, get_pos_x(), get_pos_y(), x, y)
			if can_harvest():
				harvest()
	MoveTo(n, get_pos_x(), get_pos_y(), 0, 0)
	pending = []
	for x in range(side):
		for y in range(side):
			pending.append((x, y))
	x = 0
	y = 0
	first = True
	while len(pending) > 0:
		left = []
		for tile in pending:
			MoveTo(n, x, y, tile[0], tile[1])
			x = tile[0]
			y = tile[1]
			if first:
				TillIfNeeded(Entities.Pumpkin)
			entity = get_entity_type()
			if entity == None or entity == Entities.Dead_Pumpkin:
				plant(Entities.Pumpkin)
				WaterIfWanted(True)
				left.append(tile)
			elif not can_harvest():
				left.append(tile)
		pending = left
		first = False
	before = num_items(Items.Pumpkin)
	harvest()
	return num_items(Items.Pumpkin) - before

RefreshSoilCrops()
if MODE == 0:
	set_world_size(8)
	n = get_world_size()
	quick_print("probe tree met", oneHarvest(n, Entities.Tree, Items.Wood, True), "unmet", oneHarvest(n, Entities.Tree, Items.Wood, False))
	quick_print("probe carrot met", oneHarvest(n, Entities.Carrot, Items.Carrot, True), "unmet", oneHarvest(n, Entities.Carrot, Items.Carrot, False))
	quick_print("probe pumpkins 6x6", pumpkinSquare(n, 6), "2x2", pumpkinSquare(n, 2))
else:
	set_world_size(32)
	item = Items.Wood
	if MODE == 2 or MODE == 5:
		item = Items.Carrot
	elif MODE == 3 or MODE == 6:
		item = Items.Pumpkin
	start = num_items(item)
	goal = (item, start + TARGET)
	t0 = get_time()
	if MODE == 1:
		CultivateCropsWithDrones(Entities.Tree, Entities.Grass, True, False, True, goal)
	elif MODE == 2:
		CultivateCropsWithDrones(Entities.Carrot, Entities.Grass, True, False, True, goal)
	elif MODE == 3:
		CultivatePumpkinsWithDrones(True, False, goal)
	elif MODE == 4:
		ChaseCrops(Entities.Tree, goal)
	elif MODE == 5:
		ChaseCrops(Entities.Carrot, goal)
	else:
		BlockPumpkins(6, goal)
	t = get_time() - t0
	gained = num_items(item) - start
	quick_print("master mode", MODE, item, "gained", gained, "in", t, "s, per minute", gained * 60 / t)
