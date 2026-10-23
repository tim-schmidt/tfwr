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

# ---------------- polyculture ----------------
# State for companion planting on one strip of columns x0 .. x0 + w - 1:
#   planted  tile -> crop we put there        wanted  tile -> crop a neighbour asked for
def polyState(x0, w):
	return {"planted": {}, "wanted": {}, "x0": x0, "x1": x0 + w}

# True when an orthogonal neighbour of (x, y) holds `crop`. Planting the
# same crop there would halve its growth per such neighbour.
def sameNeighbour(n, x, y, crop, planted):
	for q in [((x + 1) % n, y), ((x - 1) % n, y), (x, (y + 1) % n), (x, (y - 1) % n)]:
		if q in planted:
			if planted[q] == crop:
				return True
	return False

# Plant the tile under the drone. With poly, honour a companion request for
# this tile unless it would sit next to an identical crop, record what we
# planted, and record the new plant's own request if it falls on our strip.
def plantTile(n, x, y, crop, poly):
	if poly == None:
		plant(crop)
		return
	tile = (x, y)
	wanted = poly["wanted"]
	if tile in wanted:
		if not sameNeighbour(n, x, y, wanted[tile], poly["planted"]):
			crop = wanted[tile]
	TillIfNeeded(crop)
	plant(crop)
	poly["planted"][tile] = crop
	ask = get_companion()
	if ask != None:
		pos = ask[1]
		if pos[0] >= poly["x0"]:
			if pos[0] < poly["x1"]:
				wanted[pos] = ask[0]

# The hot loop: one check per tile when nothing is ready.
def farm_column(n, x, a, b, water, fertilize, poly):
	for y in range(n):
		if can_harvest():
			harvest()
			plantTile(n, x, y, a, poly)
			FertilizeIfWanted(fertilize)
		elif get_entity_type() == None:
			plantTile(n, x, y, a, poly)
			FertilizeIfWanted(fertilize)
		WaterIfWanted(water)
		move(North)
		a, b = b, a

# Farm the strip of w columns starting under the drone, forever or until
# num_items(until[0]) reaches until[1], checked once per pass. Ends back at
# the strip's first column.
def farmStrip(w, primaryCrop, secondaryCrop, water, fertilize, companions, until):
	n = get_world_size()
	x0 = get_pos_x()
	y0 = get_pos_y()
	poly = None
	if companions:
		poly = polyState(x0, w)

	for i in range(w):
		a, b = crop_here(x0 + i, y0, primaryCrop, secondaryCrop)
		prep_column(n, a, b)
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
		if until != None:
			if num_items(until[0]) >= until[1]:
				return

# Entry point for every drone. Extra spawn_drone() arguments arrive here.
def worker(primaryCrop, secondaryCrop, water = False, fertilize = False, companions = False, until = None):
	n, w, d = layout()
	w = min(w, n - get_pos_x())
	farmStrip(w, primaryCrop, secondaryCrop, water, fertilize, companions, until)
