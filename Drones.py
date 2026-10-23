from Utilities import *

# Checkerboard: crop_a on even (x + y), crop_b on odd.
def crop_here(x, y, crop_a, crop_b):
	if IsEven(x + y):
		return crop_a, crop_b
	return crop_b, crop_a

# Strip width and drone count, derived the same way by every drone.
def layout():
	n = get_world_size()
	d = max_drones()
	w = (n + d - 1) // d          # columns per drone, rounded up
	d = (n + w - 1) // w          # drones actually needed for that width
	return n, w, d

# One pass up the column fixing the ground. Done once per column, so the
# hot loop never has to look at the ground again.
def prep_column(n, a, b):
	for _ in range(n):
		TillIfNeeded(a)
		move(North)
		a, b = b, a

# The hot loop: one check per tile when nothing is ready.
def farm_column(n, a, b, water, fertilize):
	for _ in range(n):
		if can_harvest():
			harvest()
			plant(a)
			FertilizeIfWanted(fertilize)
		elif get_entity_type() == None:
			plant(a)
			FertilizeIfWanted(fertilize)
		WaterIfWanted(water)
		move(North)
		a, b = b, a

# Entry point for every drone. Extra spawn_drone() arguments arrive here.
def worker(primaryCrop, secondaryCrop, water = False, fertilize = False):
	n, w, d = layout()
	x0 = get_pos_x()
	y0 = get_pos_y()
	w = min(w, n - x0)

	for i in range(w):
		a, b = crop_here(x0 + i, y0, primaryCrop, secondaryCrop)
		prep_column(n, a, b)
		if i < w - 1:
			move(East)
	for _ in range(w - 1):
		move(West)

	if w == 1:
		a, b = crop_here(x0, y0, primaryCrop, secondaryCrop)
		while True:
			farm_column(n, a, b, water, fertilize)
	else:
		while True:
			for i in range(w):
				a, b = crop_here(x0 + i, y0, primaryCrop, secondaryCrop)
				farm_column(n, a, b, water, fertilize)
				if i < w - 1:
					move(East)
			for _ in range(w - 1):
				move(West)
