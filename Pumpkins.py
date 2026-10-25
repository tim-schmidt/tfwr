from Utilities import *
from Drones import *

# Plant an empty or dead tile. Returns True when the tile is ripe, False
# when it is growing, None when the planting cost is out of stock.
def pumpkinTile(firstPass, water, fertilize):
	if firstPass:
		TillIfNeeded(Entities.Pumpkin)
	entity = get_entity_type()
	if entity == None or entity == Entities.Dead_Pumpkin:
		if not CanAffordForAll(Entities.Pumpkin):
			return None
		plant(Entities.Pumpkin)
		WaterIfWanted(water)
		FertilizeIfWanted(fertilize)
		return False
	return can_harvest()

# Grow a strip of w columns starting under the drone, h tiles tall (the
# whole column when h is None). Plants every tile, then revisits only the
# tiles not yet ripe, replanting dead ones, until none are left. Ripe
# pumpkins never die, so a tile is checked once after it ripens. Ends
# where it started. Returns False when the planting cost ran out, leaving
# the strip part grown.
def growPumpkinStrip(n, w, water, fertilize, h = None):
	if h == None:
		h = n
	x0 = get_pos_x()
	y0 = get_pos_y()
	pending = []
	for i in range(w):
		for j in range(h):
			pending.append((x0 + i, (y0 + j) % n))

	x = x0
	y = y0
	firstPass = True
	ok = True
	while len(pending) > 0 and ok:
		left = []
		for tile in pending:
			MoveTo(n, x, y, tile[0], tile[1])
			x = tile[0]
			y = tile[1]
			state = pumpkinTile(firstPass, water, fertilize)
			if state == None:
				ok = False
				break
			elif not state:
				left.append(tile)
		pending = left
		firstPass = False
	MoveTo(n, x, y, x0, y0)
	return ok

# Single drone: the whole field is one strip. A fully ripe field has merged
# into one giant pumpkin, so a single harvest takes all of it.
# `until` is None or (item, amount) to stop at, checked after each harvest.
# Returns False when the planting cost ran out before `until` was reached.
def CultivatePumpkins(water = False, fertilize = False, until = None):
	RefreshSoilCrops()
	clear()
	n = get_world_size()
	while not Reached(until):
		ok = growPumpkinStrip(n, n, water, fertilize)
		harvest()
		if not ok:
			return False
	return True

# Drone worker: strip width from layout(), clipped at the east edge.
# Returns False when the planting cost ran out.
def pumpkinStrip(water = False, fertilize = False):
	RefreshSoilCrops()
	n, w, d = layout()
	return growPumpkinStrip(n, min(w, n - get_pos_x()), water, fertilize)

def CultivatePumpkinsWithDrones(water = False, fertilize = False, until = None):
	clear()
	n, w, d = layout()
	while get_pos_x() != 0:
		move(West)

	while not Reached(until):
		workers = []
		ok = True
		x = 0

		# Every strip but the last gets a worker; walk east to the next one.
		while x + w < n:
			drone = spawn_drone(pumpkinStrip, water, fertilize)
			if drone == None:
				break
			workers.append(drone)
			for _ in range(w):
				move(East)
			x += w

		# The main drone works what is left (normally just the last strip),
		# and its final eastward walk wraps it back to x == 0.
		while x < n:
			if not pumpkinStrip(water, fertilize):
				ok = False
			stripWidth = min(w, n - x)
			for _ in range(stripWidth):
				move(East)
			x += stripWidth

		for drone in workers:
			if not wait_for(drone):
				ok = False

		harvest()
		if not ok:
			return False
	return True
