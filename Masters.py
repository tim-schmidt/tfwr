from Utilities import *

# Throughput farming for the Master achievements (1B Wood, 200M Carrots,
# 20M Pumpkins in one minute), tuned in simulation (SimMaster) and run live
# from MasterWood.py, MasterCarrots.py and MasterPumpkins.py, since the
# achievements only count in the real game. All three unlocked 2026-10-25
# at 1.23B wood, 240M carrots and about 21.7M pumpkins per minute (sim
# rates; the live runs matched). Fertilizer is never used: half of a
# fertilized plant's yield turns into Weird Substance.
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

# Pumpkins: a ripe square of side n pays n^3 for n up to 5 and 6 per tile
# from 6 up. harvest() takes the ripe square that holds the drone's tile,
# so independent blocks only work with a gap between them, and the lost
# tiles cost more than the synchronisation they save (measured: 4x4
# blocks a tile apart on 32 drones 16.5M per minute, the route's synced
# board 19.4M). Hence a synced board, but without the route code's
# per-board respawn: spawn_drone costs 200 ticks and the main drone walks
# a column per worker before it farms, about 2 s of the 9.7 s per board.
#
# Layout on an n x n farm: workers own columns 0 .. n-2, rows 0 .. n-2,
# an (n-1) x (n-1) square. Row n-1 holds one flag tile per column. A
# worker that has its column ripe toggles its flag with till() (one move
# south from its origin, wrapping) and waits for its origin tile to be
# emptied by the harvest. The main drone patrols the flag row; every
# board flips which ground type means "ripe", so a stale flag never reads
# as ready. When all flags show the board's value it harvests the giant
# from the corner next to the flag row.

def flagMeans(board):
	if board % 2 == 0:
		return Grounds.Soil
	return Grounds.Grassland

# Move along the wrapped column from row y to row j the short way.
def toRow(n, y, j):
	d = (j - y) % n
	if d <= n - d:
		for i in range(d):
			move(North)
	else:
		for i in range(n - d):
			move(South)

# Plant the tile under the drone and water it to 0.75 (growth x4; water
# barely decays, so this is rare after the first board).
def plantPumpkin():
	plant(Entities.Pumpkin)
	while get_water() < 0.75:
		use_item(Items.Water)

# Grow rows 0 .. h-1 of the column under the drone, starting and ending at
# row 0: one lap planting, then laps over the tiles not yet ripe,
# replanting dead ones. With two or fewer tiles left the drone waits at
# each until it is ripe, replanting on death, since another lap costs
# about as much as the longest growth. The ground is tilled once, on the
# first board.
def pumpkinColumn(n, h, firstBoard):
	pending = []
	for j in range(h):
		pending.append(j)
	y = 0
	while len(pending) > 0:
		left = []
		stay = len(pending) <= 2
		for j in pending:
			toRow(n, y, j)
			y = j
			if firstBoard and get_ground_type() != Grounds.Soil:
				till()
			if stay:
				while not can_harvest():
					entity = get_entity_type()
					if entity == None or entity == Entities.Dead_Pumpkin:
						plantPumpkin()
			else:
				entity = get_entity_type()
				if entity == None or entity == Entities.Dead_Pumpkin:
					plantPumpkin()
					left.append(j)
				elif not can_harvest():
					left.append(j)
		pending = left
		firstBoard = False
	toRow(n, y, 0)

# Worker on column x: grow rows 0 .. h-1, raise the flag, wait for the
# harvest, repeat.
def flagColumn(n, x, h, until):
	MoveTo(n, get_pos_x(), get_pos_y(), x, 0)
	board = 0
	while not Reached(until):
		pumpkinColumn(n, h, board == 0)
		move(South)
		if get_ground_type() != flagMeans(board):
			till()
		move(North)
		while get_entity_type() == Entities.Pumpkin:
			pass
		board += 1

def SyncedPumpkins(until = None):
	clear()
	n = get_world_size()
	h = n - 1
	workers = []
	for x in range(h):
		drone = spawn_drone(flagColumn, n, x, h, until)
		if drone == None:
			break
		workers.append(drone)
	cols = len(workers)
	board = 0
	MoveTo(n, 0, 0, 0, h)
	x = 0
	while not Reached(until):
		# One lap over the flags noting the ones not ready, then only those,
		# until none is left; the harvest then follows the last flag by a
		# few moves instead of the rest of a lap.
		ready = flagMeans(board)
		waiting = []
		for i in range(cols):
			waiting.append(i)
		while len(waiting) > 0:
			left = []
			for i in waiting:
				MoveTo(n, x, h, i, h)
				x = i
				if get_ground_type() != ready:
					left.append(i)
			waiting = left
		MoveTo(n, x, h, cols - 1, h - 1)
		x = cols - 1
		harvest()
		MoveTo(n, x, h - 1, x, h)
		board += 1
	for drone in workers:
		wait_for(drone)
