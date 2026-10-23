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

# Water the tile when its water level is under `threshold`. Growth speed
# is 1x at water 0 and 5x at water 1, and each watering adds 0.25, so a
# threshold of 0.75 keeps the level in the 0.75 to 1.0 band without
# overshooting the cap.
def WaterIfWanted(wanted = False, threshold = 0.75):
	if wanted and get_water() < threshold:
		use_item(Items.Water)

# Water the tile all the way up to `threshold` in one visit, for a prep
# pass so growth starts at full speed instead of climbing over passes.
def SoakIfWanted(wanted = False, threshold = 0.75):
	if wanted:
		while get_water() < threshold:
			use_item(Items.Water)

# True when every item in the crop's planting cost is in stock.
def CanAfford(crop):
	cost = get_cost(crop)
	for item in cost:
		if num_items(item) < cost[item]:
			return False
	return True

def FertilizeIfWanted(wanted = False):
	if not wanted:
		return

	if num_items(Items.Fertilizer) > 0:
		use_item(Items.Fertilizer)

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
