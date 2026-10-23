from Utilities import *
from Drones import *

# Single drone. Checkerboard of primaryCrop (even x + y) and secondaryCrop.
# Only touches a tile when it is ripe or empty.
def CultivateCrops(primaryCrop, secondaryCrop, water = False, fertilize = False):
	while True:
		for x in range(get_world_size()):
			for y in range(get_world_size()):
				crop = primaryCrop
				if IsOdd(x + y):
					crop = secondaryCrop

				if can_harvest():
					harvest()
					TillIfNeeded(crop)
					plant(crop)
					FertilizeIfWanted(fertilize)
				elif get_entity_type() == None:
					TillIfNeeded(crop)
					plant(crop)
					FertilizeIfWanted(fertilize)
				WaterIfWanted(water)

				move(North)
			move(East)

def CultivateCropsWithDrones(primaryCrop, secondaryCrop, water = False, fertilize = False):
	clear()
	n, w, d = layout()

	while get_pos_x() != 0:
		move(West)

	for k in range(d - 1):
		if spawn_drone(worker, primaryCrop, secondaryCrop, water, fertilize) == None:
			break
		for _ in range(w):
			move(East)
	worker(primaryCrop, secondaryCrop, water, fertilize)
