# Start file for the Fastest Reset leaderboard run:
#   leaderboard_run(Leaderboards.Fastest_Reset, "FastestReset", 256)
# Begins with no unlocks, items or globals. Walks ROUTE in order: for each
# (unlock, level) it reads get_cost(), farms whatever item is short with
# the crop modules, buys, and moves on. Ends once Leaderboard is unlocked.
# Entities and Items are only named behind a check of the unlock that
# introduces them.
from Utilities import *
from StandardCrops import CultivateCrops, CultivateCropsWithDrones
from Pumpkins import CultivatePumpkins, CultivatePumpkinsWithDrones
from Cacti import CultivateCacti, CultivateCactiWithDrones
from Bones import CultivateBones, CactiForFullGrid
from Gold import CultivateGold, CultivateGoldWithDrones, substanceFor

# First draft: the minimum set plus the cheap yield levels. Tune by
# measurement (see Costs.md for every price).
ROUTE = [
	(Unlocks.Expand, 1), (Unlocks.Speed, 1), (Unlocks.Plant, 1),
	(Unlocks.Expand, 2), (Unlocks.Speed, 2),
	(Unlocks.Carrots, 1), (Unlocks.Trees, 1),
	(Unlocks.Expand, 3), (Unlocks.Speed, 3), (Unlocks.Expand, 4),
	(Unlocks.Watering, 1), (Unlocks.Trees, 2), (Unlocks.Speed, 4),
	(Unlocks.Carrots, 2), (Unlocks.Trees, 3), (Unlocks.Watering, 2), (Unlocks.Speed, 5),
	(Unlocks.Pumpkins, 1), (Unlocks.Expand, 5), (Unlocks.Pumpkins, 2),
	(Unlocks.Polyculture, 1),
	(Unlocks.Trees, 4), (Unlocks.Carrots, 3), (Unlocks.Watering, 3), (Unlocks.Grass, 3),
	(Unlocks.Fertilizer, 1), (Unlocks.Mazes, 1),
	(Unlocks.Pumpkins, 3), (Unlocks.Cactus, 1),
	(Unlocks.Megafarm, 1), (Unlocks.Megafarm, 2),
	(Unlocks.Hats, 1), (Unlocks.Dinosaurs, 1),
	(Unlocks.Cactus, 2), (Unlocks.Dinosaurs, 2), (Unlocks.Mazes, 2),
	(Unlocks.Megafarm, 3),
	(Unlocks.Trees, 5), (Unlocks.Carrots, 4), (Unlocks.Watering, 4), (Unlocks.Pumpkins, 4),
	(Unlocks.Expand, 6), (Unlocks.Megafarm, 4), (Unlocks.Expand, 7),
	(Unlocks.Cactus, 3), (Unlocks.Dinosaurs, 3), (Unlocks.Mazes, 3),
	(Unlocks.Megafarm, 5),
	(Unlocks.Dinosaurs, 4), (Unlocks.Dinosaurs, 5),
	(Unlocks.Leaderboard, 1),
]

def have(unlock):
	return num_unlocked(unlock) > 0

def dronesOn():
	return max_drones() > 1

# Best wood crop owned: tree, else bush, else grass as a stand-in.
def woodCrop():
	if have(Unlocks.Trees):
		return Entities.Tree
	if have(Unlocks.Plant):
		return Entities.Bush
	return Entities.Grass

# Farm whatever the crop costs to plant, enough for `tiles` plantings.
def ensurePlantable(crop, tiles):
	cost = get_cost(crop)
	for item in cost:
		need = cost[item] * tiles
		if num_items(item) < need:
			farm(item, need)

def farmCrops(primary, secondary, fertilize, until):
	n = get_world_size()
	ensurePlantable(primary, (n * n + 1) // 2)
	ensurePlantable(secondary, n * n // 2)
	if dronesOn():
		CultivateCropsWithDrones(primary, secondary, have(Unlocks.Watering), fertilize, have(Unlocks.Polyculture), until)
	else:
		CultivateCrops(primary, secondary, have(Unlocks.Watering), fertilize, have(Unlocks.Polyculture), until)

# Gold: one maze over the whole farm, relocated as often as the missing
# gold needs (300 at most), with the substance for it farmed first.
def farmGold(amount):
	n = get_world_size()
	per = n * n * 2 ** (num_unlocked(Unlocks.Mazes) - 1)
	missing = amount - num_items(Items.Gold)
	harvests = (missing + per - 1) // per
	if harvests > 301:
		harvests = 301
	need = harvests * substanceFor(n)
	if num_items(Items.Weird_Substance) < need:
		farm(Items.Weird_Substance, need)
	until = (Items.Gold, amount)
	if dronesOn():
		CultivateGoldWithDrones(n, harvests - 1, 1, until)
	else:
		CultivateGold(n, harvests - 1, until)

# Farm `item` until `amount` is in stock. Returns False when nothing owned
# can produce it, which means the route is ordered wrong.
def farm(item, amount):
	until = (item, amount)
	n = get_world_size()
	if item == Items.Hay:
		farmCrops(Entities.Grass, woodCrop(), False, until)
	elif have(Unlocks.Plant) and item == Items.Wood:
		farmCrops(woodCrop(), Entities.Grass, False, until)
	elif have(Unlocks.Carrots) and item == Items.Carrot:
		farmCrops(Entities.Carrot, woodCrop(), False, until)
	elif have(Unlocks.Fertilizer) and item == Items.Weird_Substance:
		farmCrops(woodCrop(), Entities.Grass, True, until)
	elif have(Unlocks.Pumpkins) and item == Items.Pumpkin:
		ensurePlantable(Entities.Pumpkin, n * n)
		if dronesOn():
			CultivatePumpkinsWithDrones(have(Unlocks.Watering), False, until)
		else:
			CultivatePumpkins(have(Unlocks.Watering), False, until)
	elif have(Unlocks.Cactus) and item == Items.Cactus:
		ensurePlantable(Entities.Cactus, n * n + 1)
		if dronesOn():
			CultivateCactiWithDrones(have(Unlocks.Watering), False, until)
		else:
			CultivateCacti(have(Unlocks.Watering), False, until)
	elif have(Unlocks.Dinosaurs) and item == Items.Bone:
		need = CactiForFullGrid(n) + 1
		if num_items(Items.Cactus) < need:
			farm(Items.Cactus, need)
		CultivateBones(until)
	elif have(Unlocks.Mazes) and item == Items.Gold:
		farmGold(amount)
	else:
		quick_print("FastestReset: no producer for", item, "- route order is wrong")
		return False
	return True

def run():
	for step in ROUTE:
		target = step[0]
		level = step[1]
		while num_unlocked(target) < level:
			cost = get_cost(target)
			short = None
			for item in cost:
				if num_items(item) < cost[item]:
					short = item
			if short == None:
				unlock(target)
			elif not farm(short, cost[short]):
				return
	quick_print("FastestReset: done, Leaderboard level", num_unlocked(Unlocks.Leaderboard))

run()
