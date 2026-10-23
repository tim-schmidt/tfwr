from Utilities import *

# Yield mode: maximise the yield of ONE full board under polyculture,
# time second. Experimental, for simulation. Needs the Polyculture unlock.
#
# Phases per board:
#   fill      main sweeps and plants every empty tile; with `dispatch`, each
#             new plant's companion request is handed to a helper drone that
#             plants it at once and follows the chain of requests while the
#             requested tiles are empty
#   re-roll   with `reroll`, main sweeps until every plant's request is met,
#             harvesting and replanting (same crop) any ripe plant whose
#             request is not met, which rolls a new request
#   harvest   one sweep harvesting every tile, replanting the same crop at
#             once so companions stay standing for the tiles after them

def orthogonal(n, x, y):
	return [((x + 1) % n, y), ((x - 1) % n, y), (x, (y + 1) % n), (x, (y - 1) % n)]

# Fixed layout: `share` percent of tiles are `primary`, the rest are
# companion slots. 50 is a checkerboard; 62, 75 and 87 thin the slots to
# sparser lattices; 93 is four slots per 8x8 block, the fewest that keep
# every tile within three moves of one. `slots` picks the slot crop:
# None cycles secondary, bush, carrot; otherwise that one crop.
def layoutCrop(x, y, primary, secondary, share, slots):
	slot = IsOdd(x + y)
	if share >= 93:
		slot = x % 4 == 0 and y % 4 == (x // 4) % 2 * 2
	elif share >= 87:
		slot = x % 4 == 1 and y % 2 == 1
	elif share >= 75:
		slot = x % 2 == 1 and y % 2 == 1
	elif share >= 62:
		slot = IsOdd(x + y) and x % 4 != 0
	if not slot:
		return primary
	if slots != None:
		return slots
	kind = (x + 2 * y) % 3
	if kind == 0:
		return secondary
	if kind == 1:
		return Entities.Bush
	return Entities.Carrot

# Primary unless an orthogonal neighbour we know of already holds it.
def defaultCrop(n, x, y, primary, secondary, planted):
	for q in orthogonal(n, x, y):
		if q in planted:
			if planted[q] == primary:
				return secondary
	return primary

# Returns whether the plant went in (False when the crop is unaffordable).
def putPlant(crop, water, fertilize):
	if not CanAfford(crop):
		return False
	TillIfNeeded(crop)
	plant(crop)
	WaterIfWanted(water)
	FertilizeIfWanted(fertilize)
	return True

# Replant (x, y) with its recorded crop, falling back to the checkerboard
# crop when that cannot be afforded, and record what went in.
def replant(n, x, y, planted, primary, secondary, water, fertilize):
	crop = planted[(x, y)]
	if crop == None or not putPlant(crop, water, fertilize):
		crop = defaultCrop(n, x, y, primary, secondary, planted)
		if not putPlant(crop, water, fertilize):
			crop = secondary
			putPlant(crop, water, fertilize)
		planted[(x, y)] = crop

# Put `crop` on this tile. Bare grassland grows grass on its own, so grass
# is replaced; any other crop stays. Returns 1 when we planted, 0 when the
# crop already stood here, -1 when the tile is taken or the crop is
# unaffordable.
def takeTile(crop, water, fertilize):
	entity = get_entity_type()
	if entity == crop:
		return 0
	if not CanAfford(crop):
		return -1
	if entity == Entities.Grass:
		while not can_harvest():
			pass
		harvest()
	elif entity != None:
		return -1
	putPlant(crop, water, fertilize)
	return 1

# Helper drone. Walks from (fx, fy) to (x, y), plants `crop` there, then
# follows the new plant's own request, and so on. The chain ends at a tile
# that is taken, unaffordable, or already holds the crop (whoever planted
# it dispatched its request).
def plantCompanion(n, fx, fy, x, y, crop, water, fertilize):
	RefreshSoilCrops()
	while True:
		MoveTo(n, fx, fy, x, y)
		if takeTile(crop, water, fertilize) != 1:
			return
		ask = get_companion()
		if ask == None:
			return
		fx = x
		fy = y
		x = ask[1][0]
		y = ask[1][1]
		crop = ask[0]

# Fill sweep from (0, 0). Grass is replaced; anything else was put there
# by a helper and stays. Returns what main planted (helpers' plants are
# not in it; readBoard() fills the gaps).
def fillBoard(n, primary, secondary, water, fertilize, dispatch, share, slots):
	planted = {}
	wanted = {}
	helpers = []
	for x in range(n):
		for y in range(n):
			tile = (x, y)
			if dispatch:
				crop = defaultCrop(n, x, y, primary, secondary, planted)
			else:
				crop = layoutCrop(x, y, primary, secondary, share, slots)
			if tile in wanted:
				crop = wanted[tile]
			took = takeTile(crop, water, fertilize)
			if took == -1:
				crop = defaultCrop(n, x, y, primary, secondary, planted)
				took = takeTile(crop, water, fertilize)
			if took >= 0:
				planted[tile] = crop
			else:
				planted[tile] = get_entity_type()
			if took == 1:
				if dispatch:
					ask = get_companion()
					if ask != None:
						pos = ask[1]
						wanted[pos] = ask[0]
						drone = spawn_drone(plantCompanion, n, x, y, pos[0], pos[1], ask[0], water, fertilize)
						if drone != None:
							helpers.append(drone)
			move(North)
		move(East)
	for drone in helpers:
		wait_for(drone)
	return planted

# One sensing sweep: what stands on every tile. Empty tiles (a helper's
# plant was unaffordable) get the checkerboard crop.
def readBoard(n, primary, secondary, water, fertilize):
	planted = {}
	for x in range(n):
		for y in range(n):
			planted[(x, y)] = get_entity_type()
			if planted[(x, y)] == None:
				replant(n, x, y, planted, primary, secondary, water, fertilize)
			move(North)
		move(East)
	return planted

# Sweep until every plant's request is met. A ripe plant with an unmet
# request is harvested and replanted with the same crop for a new request.
# Returns the number of re-rolls.
def rerollBoard(n, planted, primary, secondary, water, fertilize):
	rolls = 0
	while True:
		unmet = 0
		for x in range(n):
			for y in range(n):
				ask = get_companion()
				if ask != None:
					if planted[ask[1]] != ask[0]:
						unmet += 1
						if can_harvest():
							harvest()
							replant(n, x, y, planted, primary, secondary, water, fertilize)
							rolls += 1
				move(North)
			move(East)
		if unmet == 0:
			return rolls

# Harvest every tile, waiting for each to ripen, replanting the same crop.
def harvestBoard(n, planted, primary, secondary, water, fertilize):
	for x in range(n):
		for y in range(n):
			while not can_harvest():
				pass
			harvest()
			replant(n, x, y, planted, primary, secondary, water, fertilize)
			move(North)
		move(East)

# `rounds` of 0 runs forever. `until` is None or (item, amount): stop
# once num_items(item) reaches amount, checked once per round.
# dispatch=False, reroll=False is a plain fixed-layout board, the
# baseline. `share` and `slots` shape the layout when dispatch is off (see
# layoutCrop). Returns the number of re-rolls over all rounds.
def CultivateYieldBoard(primary, secondary, water = False, fertilize = False, dispatch = True, reroll = True, rounds = 0, share = 50, slots = None, until = None):
	clear()
	RefreshSoilCrops()
	n = get_world_size()
	MoveTo(n, get_pos_x(), get_pos_y(), 0, 0)
	planted = fillBoard(n, primary, secondary, water, fertilize, dispatch, share, slots)
	if dispatch:
		planted = readBoard(n, primary, secondary, water, fertilize)
	rolls = 0
	done = 0
	while rounds == 0 or done < rounds:
		if reroll:
			rolls += rerollBoard(n, planted, primary, secondary, water, fertilize)
		harvestBoard(n, planted, primary, secondary, water, fertilize)
		done += 1
		if until != None:
			if num_items(until[0]) >= until[1]:
				break
	return rolls
