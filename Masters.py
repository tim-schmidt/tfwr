from Utilities import *
from Pumpkins import growPumpkinStrip

# Throughput farming for the Master achievements (1B Wood, 200M Carrots,
# 20M Pumpkins in one minute), measured in simulation with every unlock
# and huge stocks of Power, Water and planting costs. Fertilizer is never
# used: half of a fertilized plant's yield turns into Weird Substance.
#
# Crops: a satisfied companion request multiplies the harvest 160-fold at
# full upgrades (409,600 against 2,560 wood per tree), so satisfaction is
# everything and ticks per harvest come second. Each drone owns one
# column. The crop stands on even tiles (x + y even), companions on odd
# ones. Only crop tiles are ever harvested. Right after planting, the
# drone walks to the plant's request position (within 3 moves), puts the
# requested companion there and walks back; requests that point at a crop
# tile are skipped. Companion tiles are never harvested, so a planted
# companion stays until another request overwrites it, which makes
# planting on a neighbour's column safe without any shared bookkeeping.

# Put `want` on the tile under the drone. Grass regrows on bare grassland
# by itself, so an existing match is left alone. A growing plant cannot be
# replaced; the request is lost.
def putCompanion(want):
	entity = get_entity_type()
	if entity == want:
		return
	if entity != None:
		if not can_harvest():
			return
		harvest()
	TillIfNeeded(want)
	plant(want)

# Plant `crop` at (x, y), then satisfy its request when the request falls
# on a companion tile. Ends back at (x, y).
def plantAndChase(n, x, y, crop):
	TillIfNeeded(crop)
	plant(crop)
	ask = get_companion()
	if ask == None:
		return
	pos = ask[1]
	if IsEven(pos[0] + pos[1]):
		return
	MoveTo(n, x, y, pos[0], pos[1])
	putCompanion(ask[0])
	MoveTo(n, pos[0], pos[1], x, y)

# Farm the crop tiles of column x until `until` (checked once per pass).
def chaseColumn(n, x, crop, until):
	y = x % 2
	MoveTo(n, get_pos_x(), get_pos_y(), x, y)
	while True:
		for i in range(n // 2):
			if can_harvest():
				harvest()
				plantAndChase(n, x, y, crop)
			elif get_entity_type() == None:
				plantAndChase(n, x, y, crop)
			WaterIfWanted(True)
			move(North)
			move(North)
			y = (y + 2) % n
		if Reached(until):
			return

# One drone per column, the main drone on column 0. `until` is None or
# (item, amount) to stop at.
def ChaseCrops(crop, until = None):
	clear()
	RefreshSoilCrops()
	n = get_world_size()
	workers = []
	for x in range(1, n):
		drone = spawn_drone(chaseColumn, n, x, crop, until)
		if drone == None:
			break
		workers.append(drone)
	chaseColumn(n, 0, crop, until)
	for drone in workers:
		wait_for(drone)

# Pumpkins: any ripe square of side 6 or more pays 6 per tile, the same as
# a full board, so every drone grows and harvests its own side x side
# block with no synchronisation and no respawning per board. Adjacent ripe
# blocks may merge into a bigger square and get taken by one harvest; the
# other owners find their tiles empty and replant.
def pumpkinBlock(n, ox, oy, side, until):
	RefreshSoilCrops()
	MoveTo(n, get_pos_x(), get_pos_y(), ox, oy)
	while not Reached(until):
		growPumpkinStrip(n, side, True, False, side)
		harvest()

# Blocks tile the farm from (0, 0); the remainder past the last full block
# stays unused. Drones beyond the block count stay unspawned.
def BlockPumpkins(side = 6, until = None):
	clear()
	RefreshSoilCrops()
	n = get_world_size()
	per = n // side
	blocks = []
	for bx in range(per):
		for by in range(per):
			blocks.append((bx * side, by * side))
	workers = []
	for i in range(1, len(blocks)):
		drone = spawn_drone(pumpkinBlock, n, blocks[i][0], blocks[i][1], side, until)
		if drone == None:
			break
		workers.append(drone)
	pumpkinBlock(n, 0, 0, side, until)
	for drone in workers:
		wait_for(drone)
