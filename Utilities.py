# Crops that only grow on soil. Rebuilt from the unlock tree by
# RefreshSoilCrops(); an entity is only named once its unlock is owned.
CROPS_NEEDING_SOIL = []

def RefreshSoilCrops():
	while len(CROPS_NEEDING_SOIL) > 0:
		CROPS_NEEDING_SOIL.pop()
	if num_unlocked(Unlocks.Carrots) > 0:
		CROPS_NEEDING_SOIL.append(Entities.Carrot)
	if num_unlocked(Unlocks.Sunflowers) > 0:
		CROPS_NEEDING_SOIL.append(Entities.Sunflower)
	if num_unlocked(Unlocks.Pumpkins) > 0:
		CROPS_NEEDING_SOIL.append(Entities.Pumpkin)
	if num_unlocked(Unlocks.Cactus) > 0:
		CROPS_NEEDING_SOIL.append(Entities.Cactus)

def IsEven(number):
	return number % 2 == 0

def IsOdd(number):
	return number % 2 == 1

def HarvestIfAble():
	if can_harvest():
		harvest()

def NeedsSoil(crop):
	return crop in CROPS_NEEDING_SOIL

def TillIfNeeded(crop):
	if NeedsSoil(crop) and get_ground_type() != Grounds.Soil:
		till()

# Water the tile when its water level is under `threshold` and the stock
# holds a tank for every drone, since all drones may reach for one at the
# same moment. Growth speed is 1x at water 0 and 5x at water 1, and each
# watering adds 0.25, so a threshold of 0.75 keeps the level in the 0.75
# to 1.0 band without overshooting the cap.
def WaterIfWanted(wanted = False, threshold = 0.75):
	if wanted and get_water() < threshold and num_items(Items.Water) >= max_drones():
		use_item(Items.Water)

# True when every item in the crop's planting cost is in stock.
def CanAfford(crop):
	return ShortItem(crop) == None

# True when the stock covers one planting of the crop for every drone, so
# drones racing for the last unit do not fail a plant() call.
def CanAffordForAll(crop):
	cost = get_cost(crop)
	for item in cost:
		if num_items(item) < cost[item] * max_drones():
			return False
	return True

# The first item of the crop's planting cost that is out of stock, or None.
def ShortItem(crop):
	cost = get_cost(crop)
	for item in cost:
		if num_items(item) < cost[item]:
			return item
	return None

# The crop that yields `item`: grass for hay, tree or bush for wood,
# carrots for carrots, grass for anything else. Items are only named
# behind their unlock.
def CropFor(item):
	if item == Items.Hay:
		return Entities.Grass
	if num_unlocked(Unlocks.Plant) > 0 and item == Items.Wood:
		if num_unlocked(Unlocks.Trees) > 0:
			return Entities.Tree
		return Entities.Bush
	if num_unlocked(Unlocks.Carrots) > 0 and item == Items.Carrot:
		return Entities.Carrot
	return Entities.Grass

# An affordable crop that produces `item`, or failing that one that
# produces what its producer lacks: a sunflower tile short of carrots gets
# a carrot, a carrot tile short of wood gets a tree. Grass ends the chain.
def ProducerOf(item):
	crop = CropFor(item)
	short = ShortItem(crop)
	if short == None or short == item:
		return crop
	return ProducerOf(short)

# Fertilize when wanted and the stock holds a unit per drone, since drones
# race for the last one.
def FertilizeIfWanted(wanted = False):
	if wanted and num_items(Items.Fertilizer) >= max_drones():
		use_item(Items.Fertilizer)

# True when an (item, amount) stop condition is met. None never stops.
def Reached(until):
	if until == None:
		return False
	return num_items(until[0]) >= until[1]

# Walk from (x, y) to (toX, toY) on an n-wide farm, using edge wrap-around
# when that is shorter. Positions are tracked by the caller, so no sensing.
def MoveTo(n, x, y, toX, toY):
	dx = (toX - x) % n
	if dx <= n - dx:
		for _ in range(dx):
			move(East)
	else:
		for _ in range(n - dx):
			move(West)
	dy = (toY - y) % n
	if dy <= n - dy:
		for _ in range(dy):
			move(North)
	else:
		for _ in range(n - dy):
			move(South)
