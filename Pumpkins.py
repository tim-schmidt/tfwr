from Utilities import *
from Drones import *

# Plant an empty or dead tile. Returns True when the tile is ripe.
def pumpkinTile(firstPass, water, fertilize):
	if firstPass:
		TillIfNeeded(Entities.Pumpkin)
	entity = get_entity_type()
	if entity == None or entity == Entities.Dead_Pumpkin:
		plant(Entities.Pumpkin)
		WaterIfWanted(water)
		FertilizeIfWanted(fertilize)
		return False
	return can_harvest()

# Grow a strip of w columns starting under the drone. Plants every tile,
# then revisits only the tiles not yet ripe, replanting dead ones, until
# none are left. Ripe pumpkins never die, so a tile is checked once after
# it ripens. Ends where it started.
def growPumpkinStrip(n, w, water, fertilize):
	x0 = get_pos_x()
	y0 = get_pos_y()
	pending = []
	for i in range(w):
		for j in range(n):
			pending.append((x0 + i, (y0 + j) % n))

	x = x0
	y = y0
	firstPass = True
	while len(pending) > 0:
		left = []
		for tile in pending:
			MoveTo(n, x, y, tile[0], tile[1])
			x = tile[0]
			y = tile[1]
			if not pumpkinTile(firstPass, water, fertilize):
				left.append(tile)
		pending = left
		firstPass = False
	MoveTo(n, x, y, x0, y0)

# Single drone: the whole field is one strip. A fully ripe field has merged
# into one giant pumpkin, so a single harvest takes all of it.
def CultivatePumpkins(water = False, fertilize = False):
	clear()
	n = get_world_size()
	while True:
		growPumpkinStrip(n, n, water, fertilize)
		harvest()

# Drone worker: strip width from layout(), clipped at the east edge.
def pumpkinStrip(water = False, fertilize = False):
	n, w, d = layout()
	growPumpkinStrip(n, min(w, n - get_pos_x()), water, fertilize)

def CultivatePumpkinsWithDrones(water = False, fertilize = False):
	clear()
	n, w, d = layout()
	while get_pos_x() != 0:
		move(West)

	while True:
		workers = []
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
			pumpkinStrip(water, fertilize)
			stripWidth = min(w, n - x)
			for _ in range(stripWidth):
				move(East)
			x += stripWidth

		for drone in workers:
			wait_for(drone)

		harvest()
