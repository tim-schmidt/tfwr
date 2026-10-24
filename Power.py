from Utilities import *
from Drones import layout

# Sunflowers for power. Harvesting the sunflower with the most petals on
# the farm pays 8 power instead of 1 (needs ten or more standing), so each
# drone measures its strip and harvests in descending petal order,
# replanting at once so the board stays full. Petals run 7 to 15 and can
# be measured before the flower is grown.

# Walk to a tile, tracking position through the drone's own sensors.
def goTo(n, tile):
	MoveTo(n, get_pos_x(), get_pos_y(), tile[0], tile[1])

# Put a sunflower on the tile under the drone unless one stands there.
# Returns False when the planting cost is out of stock.
def sowTile():
	if get_entity_type() == Entities.Sunflower:
		return True
	if not CanAfford(Entities.Sunflower):
		return False
	if can_harvest():
		harvest()
	TillIfNeeded(Entities.Sunflower)
	return plant(Entities.Sunflower)

# One pass: measure every tile, then harvest from 15 petals down to 7,
# replanting each tile. Returns False when the planting cost ran out.
def powerCycle(n, tiles, until):
	petals = []
	for tile in tiles:
		goTo(n, tile)
		p = measure()
		if p == None:
			p = 0
		petals.append((p, tile))
	p = 15
	while p >= 7:
		for entry in petals:
			if entry[0] == p:
				goTo(n, entry[1])
				while not can_harvest():
					pass
				harvest()
				if not sowTile():
					return False
				if Reached(until):
					return True
		p -= 1
	return True

# Grow and harvest the w columns starting under the drone until `until`
# is reached. Returns False when the planting cost ran out.
def powerStrip(w, until):
	RefreshSoilCrops()
	n = get_world_size()
	x0 = get_pos_x()
	tiles = []
	for i in range(w):
		for y in range(n):
			tiles.append((x0 + i, y))
	for tile in tiles:
		goTo(n, tile)
		if not sowTile():
			return False
	while not Reached(until):
		if not powerCycle(n, tiles, until):
			return False
	return True

# Single drone, whole farm.
def CultivatePower(until):
	n = get_world_size()
	MoveTo(n, get_pos_x(), get_pos_y(), 0, 0)
	return powerStrip(n, until)

# Drone worker: strip width from layout(), clipped at the east edge.
def powerWorker(until):
	n, w, d = layout()
	return powerStrip(min(w, n - get_pos_x()), until)

def CultivatePowerWithDrones(until):
	n, w, d = layout()
	while get_pos_x() != 0:
		move(West)
	workers = []
	for k in range(d - 1):
		drone = spawn_drone(powerWorker, until)
		if drone == None:
			break
		workers.append(drone)
		for _ in range(w):
			move(East)
	ok = powerWorker(until)
	for drone in workers:
		if not wait_for(drone):
			ok = False
	return ok
