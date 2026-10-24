# Probe start file for SimRules.py. Not run directly. All unlocks.
# 1. Which crops have a companion preference: plant each, ask get_companion().
# 2. The identical-neighbour growth penalty per crop: seconds to ripen for a
#    plant alone versus the same plant surrounded by four of its kind.
from Utilities import *

set_world_size(8)
clear()
RefreshSoilCrops()
n = get_world_size()

def put(x, y, crop):
	MoveTo(n, get_pos_x(), get_pos_y(), x, y)
	if can_harvest():
		harvest()
	if get_entity_type() != None:
		till()
		till()
	TillIfNeeded(crop)
	plant(crop)

def ripeAfter(x, y):
	MoveTo(n, get_pos_x(), get_pos_y(), x, y)
	t0 = get_time()
	while not can_harvest():
		pass
	return get_time() - t0

crops = [Entities.Grass, Entities.Bush, Entities.Tree, Entities.Carrot, Entities.Sunflower, Entities.Pumpkin, Entities.Cactus]
for crop in crops:
	put(2, 2, crop)
	quick_print("companion of", crop, "->", get_companion())

# Pumpkins and cacti are grown as solid boards anyway, and a dead pumpkin
# never ripens, so only the sweep crops are timed.
for crop in [Entities.Grass, Entities.Bush, Entities.Tree, Entities.Carrot, Entities.Sunflower]:
	clear()
	put(1, 1, crop)
	alone = ripeAfter(1, 1)
	clear()
	put(5, 4, crop)
	put(3, 4, crop)
	put(4, 5, crop)
	put(4, 3, crop)
	put(4, 4, crop)
	together = ripeAfter(4, 4)
	quick_print("growth", crop, "alone", alone, "with four identical neighbours", together)
