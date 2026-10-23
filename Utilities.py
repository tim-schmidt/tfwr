# Starts empty. Append each crop when its first unlock level lands:
#   Unlocks.Carrots    -> Entities.Carrot
#   Unlocks.Sunflowers -> Entities.Sunflower
#   Unlocks.Pumpkins   -> Entities.Pumpkin
#   Unlocks.Cactus     -> Entities.Cactus
CROPS_NEEDING_SOIL = []

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

# Water the tile when its water level is under `threshold`.
def WaterIfWanted(wanted = False, threshold = 0.1):
	if wanted and get_water() < threshold:
		use_item(Items.Water)

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
