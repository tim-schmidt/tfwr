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
# First pass over a column: till, water once, and plant, so the first farm
# pass already finds the crop growing. One watering, not a soak: on long
# strips a pass outlasts growth anyway and extra uses up front are pure
# cost (measured at 20M wood on 32x32).
def prep_column(n, x, a, b, water, fertilize, poly):
	for y in range(n):
		TillIfNeeded(a)
		WaterIfWanted(water)
		if can_harvest():
			harvest()
			met = plantTile(n, x, y, a, poly)
			FertilizeIfWanted(fertilize and met)
		elif get_entity_type() == None:
			met = plantTile(n, x, y, a, poly)
			FertilizeIfWanted(fertilize and met)
		move(North)
		a, b = b, a

# ---------------- polyculture ----------------
# State for companion planting on one strip of columns x0 .. x0 + w - 1:
#   planted  tile -> crop we put there        wanted  tile -> crop a neighbour asked for
#   a, b     the checkerboard pair, assumed on tiles we have no record of
def polyState(x0, w, a, b):
	return {"planted": {}, "wanted": {}, "x0": x0, "x1": x0 + w, "a": a, "b": b}

# What we believe stands on tile q: our record, else its checkerboard crop.
def believed(poly, q):
	if q in poly["planted"]:
		return poly["planted"][q]
	if IsEven(q[0] + q[1]):
		return poly["a"]
	return poly["b"]

# True when an orthogonal neighbour of (x, y) holds `crop`. Planting the
# same crop there would halve its growth per such neighbour.
def sameNeighbour(n, x, y, crop, poly):
	for q in [((x + 1) % n, y), ((x - 1) % n, y), (x, (y + 1) % n), (x, (y - 1) % n)]:
		if believed(poly, q) == crop:
			return True
	return False

# Plant the tile under the drone. With poly, honour a companion request for
# this tile unless it would sit next to an identical crop or cannot be
# afforded, record what we planted, and record the new plant's own request
# if it falls on our strip. Returns True when the new plant's request is
# believed met already (or when there is no poly knowledge at all), which
# is when a fertilizer is worth spending: half of the multiplied yield
# becomes Weird Substance.
def plantTile(n, x, y, crop, poly):
	if poly == None:
		plant(crop)
		return True
	tile = (x, y)
	wanted = poly["wanted"]
	if tile in wanted:
		if CanAfford(wanted[tile]):
			if not sameNeighbour(n, x, y, wanted[tile], poly):
				crop = wanted[tile]
	TillIfNeeded(crop)
	plant(crop)
	poly["planted"][tile] = crop
	met = False
	ask = get_companion()
	if ask != None:
		pos = ask[1]
		if believed(poly, pos) == ask[0]:
			met = True
		if pos[0] >= poly["x0"]:
			if pos[0] < poly["x1"]:
				wanted[pos] = ask[0]
	return met

# The hot loop: one check per tile when nothing is ready.
def farm_column(n, x, a, b, water, fertilize, poly):
	for y in range(n):
		if can_harvest():
			harvest()
			met = plantTile(n, x, y, a, poly)
			FertilizeIfWanted(fertilize and met)
		elif get_entity_type() == None:
			met = plantTile(n, x, y, a, poly)
			FertilizeIfWanted(fertilize and met)
		WaterIfWanted(water)
		move(North)
		a, b = b, a

# Before the Plant unlock plant() is an error, so the strip is only
# grazed: harvest whatever regrows, pass after pass, until `until`.
def graze(n, w, until):
	while True:
		for i in range(w):
			for _ in range(n):
				if can_harvest():
					harvest()
				move(North)
			if i < w - 1:
				move(East)
		for _ in range(w - 1):
			move(West)
		if Reached(until):
			return

# Farm the strip of w columns starting under the drone, forever or until
# num_items(until[0]) reaches until[1], checked once per pass. Ends back at
# the strip's first column.
def farmStrip(w, primaryCrop, secondaryCrop, water, fertilize, companions, until):
	RefreshSoilCrops()
	n = get_world_size()
	if num_unlocked(Unlocks.Plant) == 0:
		graze(n, w, until)
		return
	x0 = get_pos_x()
	y0 = get_pos_y()
	poly = None
	if companions:
		poly = polyState(x0, w, primaryCrop, secondaryCrop)

	for i in range(w):
		a, b = crop_here(x0 + i, y0, primaryCrop, secondaryCrop)
		prep_column(n, x0 + i, a, b, water, fertilize, poly)
		if i < w - 1:
			move(East)
	for _ in range(w - 1):
		move(West)

	while True:
		for i in range(w):
			a, b = crop_here(x0 + i, y0, primaryCrop, secondaryCrop)
			farm_column(n, x0 + i, a, b, water, fertilize, poly)
			if i < w - 1:
				move(East)
		for _ in range(w - 1):
			move(West)
		if Reached(until):
			return

# Entry point for every drone. Extra spawn_drone() arguments arrive here.
def worker(primaryCrop, secondaryCrop, water = False, fertilize = False, companions = False, until = None):
	n, w, d = layout()
	w = min(w, n - get_pos_x())
	farmStrip(w, primaryCrop, secondaryCrop, water, fertilize, companions, until)
