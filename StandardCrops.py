from Utilities import *
from Drones import *

# Single drone: the whole farm is one strip. Checkerboard of primaryCrop
# (even x + y) and secondaryCrop. `companions` turns on polyculture
# planting (needs the Polyculture unlock). `until` is None or
# (item, amount) to stop at.
def CultivateCrops(primaryCrop, secondaryCrop, water = False, fertilize = False, companions = False, until = None):
	n = get_world_size()
	MoveTo(n, get_pos_x(), get_pos_y(), 0, 0)
	farmStrip(n, primaryCrop, secondaryCrop, water, fertilize, companions, until)

def CultivateCropsWithDrones(primaryCrop, secondaryCrop, water = False, fertilize = False, companions = False, until = None):
	clear()
	n, w, d = layout()

	while get_pos_x() != 0:
		move(West)

	workers = []
	for k in range(d - 1):
		drone = spawn_drone(worker, primaryCrop, secondaryCrop, water, fertilize, companions, until)
		if drone == None:
			break
		workers.append(drone)
		for _ in range(w):
			move(East)
	worker(primaryCrop, secondaryCrop, water, fertilize, companions, until)
	for drone in workers:
		wait_for(drone)
