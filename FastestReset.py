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

# The order of Unlocks.md with the programming unlocks (already owned in
# a leaderboard run) removed and levels above these caps skipped, since
# their cost outgrows what the rest of the route can earn back:
#   Grass 6, Trees 6, Carrots 6, Pumpkins 5, Cactus 3, Watering 7,
#   Fertilizer 3, Mazes 4, Dinosaurs 4, Expand 7 (16x16), Polyculture 1.
# Bones at Dinosaurs 4 take four full 16x16 snakes (520k each).
# Megafarm 1 to 3 moved up to right after Mazes 1 (gold is cheap there and
# the drones speed up every later phase), Megafarm 4 to right after
# Mazes 2.
ROUTE = [
	(Unlocks.Speed, 1),
	(Unlocks.Expand, 1),
	(Unlocks.Plant, 1),
	(Unlocks.Expand, 2),
	(Unlocks.Speed, 2),
	(Unlocks.Grass, 2),
	(Unlocks.Carrots, 1),
	(Unlocks.Trees, 1),
	(Unlocks.Expand, 3),
	(Unlocks.Speed, 3),
	(Unlocks.Carrots, 2),
	(Unlocks.Trees, 2),
	(Unlocks.Grass, 3),
	(Unlocks.Expand, 4),
	(Unlocks.Watering, 1),
	(Unlocks.Watering, 2),
	(Unlocks.Fertilizer, 1),
	(Unlocks.Carrots, 3),
	(Unlocks.Speed, 4),
	(Unlocks.Grass, 4),
	(Unlocks.Watering, 3),
	(Unlocks.Trees, 3),
	(Unlocks.Hats, 1),
	(Unlocks.Fertilizer, 2),
	(Unlocks.Speed, 5),
	(Unlocks.Carrots, 4),
	(Unlocks.Sunflowers, 1),
	(Unlocks.Trees, 4),
	(Unlocks.Grass, 5),
	(Unlocks.Watering, 4),
	(Unlocks.Fertilizer, 3),
	(Unlocks.Mazes, 1),
	(Unlocks.Megafarm, 1),
	(Unlocks.Megafarm, 2),
	(Unlocks.Megafarm, 3),
	(Unlocks.Trees, 5),
	(Unlocks.Grass, 6),
	(Unlocks.Watering, 5),
	(Unlocks.Carrots, 5),
	(Unlocks.Pumpkins, 1),
	(Unlocks.Pumpkins, 2),
	(Unlocks.Pumpkins, 3),
	(Unlocks.Expand, 5),
	(Unlocks.Watering, 6),
	(Unlocks.Pumpkins, 4),
	(Unlocks.Polyculture, 1),
	(Unlocks.Cactus, 1),
	(Unlocks.Carrots, 6),
	(Unlocks.Trees, 6),
	(Unlocks.Cactus, 2),
	(Unlocks.Dinosaurs, 1),
	(Unlocks.Mazes, 2),
	(Unlocks.Megafarm, 4),
	(Unlocks.Dinosaurs, 2),
	(Unlocks.Watering, 7),
	(Unlocks.Pumpkins, 5),
	(Unlocks.Expand, 6),
	(Unlocks.Expand, 7),
	(Unlocks.Cactus, 3),
	(Unlocks.Mazes, 3),
	(Unlocks.Mazes, 4),
	(Unlocks.Dinosaurs, 3),
	(Unlocks.Dinosaurs, 4),
	(Unlocks.Megafarm, 5),
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

# Partner for the wood crop. Only trees suffer the identical-neighbour
# growth penalty (measured: 17x with four tree neighbours, none for grass,
# bush or carrots), so trees get a grass checkerboard and bushes go solid.
def woodPartner():
	if have(Unlocks.Trees):
		return Entities.Grass
	return woodCrop()

# Farm whatever the crop costs to plant, enough for `tiles` plantings.
# Recursive through farm(): pumpkins need carrots, carrots need hay and
# wood, and each level of the chain farms its own planting cost first.
def ensurePlantable(crop, tiles):
	cost = get_cost(crop)
	for item in cost:
		need = cost[item] * tiles
		if num_items(item) < need:
			farm(item, need)

# Units one planting of the crop that yields `item` gives: 1 at level 1,
# doubling per level. A full board of pumpkins merges into a giant one
# worth n per tile up to 5x5 and 6 per tile from 6x6 on, and a fifth of
# the plantings die and get replanted, hence the 4/5.
def yieldOf(item):
	if have(Unlocks.Carrots) and item == Items.Carrot:
		return 2 ** (num_unlocked(Unlocks.Carrots) - 1)
	if have(Unlocks.Pumpkins) and item == Items.Pumpkin:
		n = get_world_size()
		if n > 6:
			n = 6
		return max(1, n * 2 ** (num_unlocked(Unlocks.Pumpkins) - 1) * 4 // 5)
	if have(Unlocks.Cactus) and item == Items.Cactus:
		return 2 ** (num_unlocked(Unlocks.Cactus) - 1)
	if have(Unlocks.Sunflowers) and item == Items.Power:
		# 1 power, or 8 for the flower with the most petals on the farm;
		# growing flowers count, so about one harvest in nine pays 8.
		return 2
	return 1

# Plantings still needed to bring `item` up to `amount`.
def plantingsFor(item, amount):
	missing = amount - num_items(item)
	if missing <= 0:
		return 0
	y = yieldOf(item)
	return (missing + y - 1) // y

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

# Power doubles every drone's speed and drains about one unit per 6,000
# ticks per drone (with the doubling, 800 ticks per second per Speed
# level). Before a farm phase, when the stock is under a minute of use,
# fill it to ten minutes. POWERING guards the recursion through the
# sunflowers' own carrot cost.
POWERING = [False]

def powerRate():
	return max_drones() * 800 * 1.5 ** num_unlocked(Unlocks.Speed) / 6000

def topUpPower():
	if POWERING[0] or not have(Unlocks.Sunflowers):
		return
	rate = powerRate()
	if num_items(Items.Power) < 60 * rate:
		POWERING[0] = True
		farm(Items.Power, num_items(Items.Power) + 600 * rate)
		POWERING[0] = False

# Farm `item` until `amount` is in stock. Returns False when nothing owned
# can produce it, which means the route is ordered wrong.
def farm(item, amount):
	until = (item, amount)
	n = get_world_size()
	quick_print("farm", item, "to", amount, "have", num_items(item), "world", n, "drones", max_drones())
	if not (have(Unlocks.Sunflowers) and item == Items.Power):
		topUpPower()
	if item == Items.Hay:
		farmCrops(Entities.Grass, Entities.Grass, False, until)
	elif have(Unlocks.Plant) and item == Items.Wood:
		farmCrops(woodCrop(), woodPartner(), False, until)
	elif have(Unlocks.Carrots) and item == Items.Carrot:
		# Carrots cost wood to plant, so the partner is the wood crop. A
		# solid carrot board stalls: the wood fallback puts trees next to
		# each other, where they take 17x longer to grow.
		farmCrops(Entities.Carrot, woodCrop(), False, until)
	elif have(Unlocks.Fertilizer) and item == Items.Weird_Substance:
		farmCrops(woodCrop(), woodPartner(), True, until)
	elif have(Unlocks.Pumpkins) and item == Items.Pumpkin:
		# Pumpkins cost carrots per planting: stock the predicted total up
		# front, grow until it runs out or the target is met, restock.
		while not Reached(until):
			ensurePlantable(Entities.Pumpkin, plantingsFor(item, amount))
			if dronesOn():
				CultivatePumpkinsWithDrones(have(Unlocks.Watering), False, until)
			else:
				CultivatePumpkins(have(Unlocks.Watering), False, until)
	elif have(Unlocks.Cactus) and item == Items.Cactus:
		# Cacti cost pumpkins per planting; same stock-then-grow loop, plus
		# one board, since the cactus code stops when a full board can no
		# longer be planted.
		while not Reached(until):
			ensurePlantable(Entities.Cactus, plantingsFor(item, amount) + n * n + 1)
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
	elif have(Unlocks.Sunflowers) and item == Items.Power:
		# A solid sunflower board through the plain sweep. Measured: no
		# neighbour penalty shows for sunflowers, and production is bound
		# by growth, so twice the flowers of a checkerboard is twice the
		# power. The one-carrot planting cost is stocked up front.
		ensurePlantable(Entities.Sunflower, plantingsFor(item, amount))
		farmCrops(Entities.Sunflower, Entities.Sunflower, False, until)
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
			quick_print("t", get_time() // 1, "route", target, "level", num_unlocked(target), "->", level, "cost", cost)
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
