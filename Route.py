# The leaderboard route as a library. FastestReset.py (the real run) and
# SimResetStart.py (simulations, with a VARIANT switch for A/B tests) both
# import this and call run(buildRoute(variant)).
# Walks the route in order: for each (unlock, level) it reads get_cost(),
# farms whatever item is short with the crop modules, buys, and moves on.
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
# Megafarm 1 and 2 moved up to right after Mazes 1 (cheap in gold, and the
# drones speed up every later phase); Megafarm 3 right after Mazes 2, where
# a maze harvest pays 128 gold instead of 36. Measured: Megafarm 3 at
# Mazes 1 on 6x6 cost 618 s of maze time, more than its drones saved.
# Megafarm 4 follows Megafarm 3 (A/B tested, 3.8 s better than after
# Mazes 4); Megafarm 5 stays after Mazes 4, where gold is cheapest.
# A third tuple element True marks an optional step: bought only when the
# cost is already in stock, never farmed for. (Watering 8 and 9 were tried
# this way; the byproduct wood only piles up during the final sweeps, so
# they never fired.)
BASE_ROUTE = [
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
	(Unlocks.Expand, 4),
	(Unlocks.Trees, 2),
	(Unlocks.Grass, 3),
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
	# Pumpkins and Polyculture before the first substance farm: a fertilized
	# tree with a companion yields ten times the substance, so Mazes 1 and
	# Megafarm 2 stop waiting on fertilizer income (variant 8 below).
	(Unlocks.Pumpkins, 1),
	(Unlocks.Pumpkins, 2),
	(Unlocks.Pumpkins, 3),
	(Unlocks.Polyculture, 1),
	(Unlocks.Mazes, 1),
	(Unlocks.Megafarm, 1),
	(Unlocks.Megafarm, 2),
	(Unlocks.Trees, 5),
	(Unlocks.Grass, 6),
	(Unlocks.Watering, 5),
	(Unlocks.Carrots, 5),
	(Unlocks.Expand, 5),
	(Unlocks.Watering, 6),
	(Unlocks.Pumpkins, 4),
	(Unlocks.Cactus, 1),
	(Unlocks.Carrots, 6),
	(Unlocks.Trees, 6),
	(Unlocks.Cactus, 2),
	(Unlocks.Dinosaurs, 1),
	(Unlocks.Mazes, 2),
	(Unlocks.Megafarm, 3),
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

# Route variants for in-session A/B tests (SimReset runs two back to back;
# the game drifts between sessions, so only same-call comparisons count).
#   0  the route above
#   1  bones by plain Hamiltonian laps, no fourth-snake trim (the old way)
#   2  power top-ups to 150 s (lost to 100 s by 73 s)
#   3  power floor 60 s, top-ups to 100 s; bones stock 650/750 s (the base)
#   4  power floor 40 s, top-ups to 70 s (lost to 100 s by 112 s)
#   5  power floor 25 s, top-ups to 45 s (lost to 100 s by 97 s)
#   The old 300 s target with bones stock 900/1000 s lost to 100 s by 151 s
#   (3,147.2 against 2,996.4).
#   6  Trees 5 before Mazes 1 (three-seed mean 3,035.5 against 3,052.2
#      for the old order; 7 won that call at 3,000.1)
#   7  as 6, plus Pumpkins 1-3 and Polyculture 1 before Mazes 1
#   8  Pumpkins 1-3 and Polyculture 1 before Mazes 1, Trees 5 left in
#      place (2,961.4 against 2,973.0 for 7: a draw, so the smaller move
#      is the base)
#   9  the same block before Megafarm 2 instead (3,060.0): Mazes 1's
#      substance then drains the fertilizer stock to zero, and the final
#      gold phase, which is bound by fertilizer, ran 90 to 135 s longer
#   Variants 6 to 9 are retired; the route above is 8.
# Decided in-session: Megafarm 4 after Megafarm 3 beat after Mazes 4 by
# 3.8 s (3,301.9 against 3,305.7); Expand 4 before Trees 2 beat its old
# place by 96 s (3,356.0 against 3,451.7); both are in the base route.
# Grass 2 and 3 after Expand 4 lost by 30 s (3,482.1 against 3,451.7).
# Sizing a gold phase's power up front from its harvest count lost by 150
# to 170 s: the estimate undershot real phase lengths and mazes ran dry.
def moveStep(route, step, before):
	out = []
	for s in route:
		if s == before:
			out.append(step)
		if s != step:
			out.append(s)
	return out

BONES_SHORTCUTS = [True]
# (floor, target) seconds of power for the phases that run every drone, and
# for the single-drone bones phase (see topUpPower).
POWER_STOCK = [60, 100]
BONES_POWER_STOCK = [650, 750]

def buildRoute(variant):
	BONES_SHORTCUTS[0] = variant != 1
	stocks = {2: (60, 150), 4: (40, 70), 5: (25, 45)}
	if variant in stocks:
		POWER_STOCK[0] = stocks[variant][0]
		POWER_STOCK[1] = stocks[variant][1]
	route = []
	for s in BASE_ROUTE:
		route.append(s)
	return route


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

# Only trees suffer the identical-neighbour growth penalty (measured: 17x
# with four tree neighbours, none for grass, bush or carrots). Solid grass
# and bush boards were tried anyway and lost 122 s in the early game: the
# hay phases' wood partner stocks the wood that carrots cost to plant.

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
		# Harvesting k cacti at once pays k squared, and the cactus code
		# sorts and harvests the whole n x n board in one call, so each
		# planting is worth n*n times the level multiplier.
		n = get_world_size()
		return n * n * 2 ** (num_unlocked(Unlocks.Cactus) - 1)
	if have(Unlocks.Sunflowers) and item == Items.Power:
		# 1 power, or 8 for the flower with the most petals on the farm;
		# growing flowers count, so harvests average about 1.8, and the
		# drones burn power while the phase runs. Low on purpose.
		return 1.5
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
	quick_print("sweep", primary, get_cost(primary), secondary, get_cost(secondary))
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
# ticks per running drone (with the doubling, 800 ticks per second per
# Speed level). Before a farm phase, when the stock is under `floor`
# seconds of use by the drones that phase will run, fill it to `target`
# seconds of them. Bones runs one drone (the hat) for about 560 s with no
# top-up inside, so it needs the whole phase in stock up front (the phase
# takes about 560 s; 650 s floor, 750 s target); everything else runs all
# drones and gets a minute's floor and 100 s target. Measured in one call:
# 300 s target 3,147 s, 150 s 3,069, 100 s 2,996; 70 s and 45 s targets
# lost to 100 s by 112 and 97 s.
# POWERING guards the recursion through the sunflowers' own carrot cost.
POWERING = [False]

def powerRate(drones):
	return drones * 800 * 1.5 ** num_unlocked(Unlocks.Speed) / 6000

def topUpPower(drones, floor, target):
	if POWERING[0] or not have(Unlocks.Sunflowers):
		return
	rate = powerRate(drones)
	if num_items(Items.Power) < floor * rate:
		POWERING[0] = True
		farm(Items.Power, target * rate)
		POWERING[0] = False

# Farm `item` until `amount` is in stock. Returns False when nothing owned
# can produce it, which means the route is ordered wrong.
def farm(item, amount):
	until = (item, amount)
	n = get_world_size()
	quick_print("t", get_time(), "farm", item, "to", amount, "have", num_items(item), "world", n, "drones", max_drones(), "fertilizer", num_items(Items.Fertilizer), "substance", num_items(Items.Weird_Substance))
	if have(Unlocks.Dinosaurs) and item == Items.Bone:
		topUpPower(1, BONES_POWER_STOCK[0], BONES_POWER_STOCK[1])
	elif not (have(Unlocks.Sunflowers) and item == Items.Power):
		topUpPower(max_drones(), POWER_STOCK[0], POWER_STOCK[1])
	if item == Items.Hay:
		if num_unlocked(Unlocks.Speed) < 3:
			# Bare grassland regrows ripe grass at once, and below Speed 3 a
			# move costs more than the regrowth, so one tile harvested in
			# place beats sweeping (measured on 3x3: 0.51 s per hay against
			# 0.55 at Speed 2, 0.37 at Speed 3).
			while not Reached(until):
				if can_harvest():
					harvest()
		else:
			farmCrops(Entities.Grass, woodCrop(), False, until)
	elif have(Unlocks.Plant) and item == Items.Wood:
		farmCrops(woodCrop(), Entities.Grass, False, until)
	elif have(Unlocks.Carrots) and item == Items.Carrot:
		# Carrots cost wood to plant, so the partner is the wood crop. A
		# solid carrot board stalls: the wood fallback puts trees next to
		# each other, where they take 17x longer to grow.
		farmCrops(Entities.Carrot, woodCrop(), False, until)
	elif have(Unlocks.Fertilizer) and item == Items.Weird_Substance:
		farmCrops(woodCrop(), Entities.Grass, True, until)
	elif have(Unlocks.Pumpkins) and item == Items.Pumpkin:
		# Pumpkins cost carrots per planting: stock the predicted total up
		# front, at least two boards' worth since a fifth die and get
		# replanted, grow until it runs out or the target is met, restock.
		while not Reached(until):
			plantings = max(plantingsFor(item, amount), 2 * n * n, max_drones())
			ensurePlantable(Entities.Pumpkin, plantings)
			if dronesOn():
				ok = CultivatePumpkinsWithDrones(have(Unlocks.Watering), False, until)
			else:
				ok = CultivatePumpkins(have(Unlocks.Watering), False, until)
			quick_print("pumpkin pass complete", ok, "pumpkins", num_items(Items.Pumpkin), "carrots", num_items(Items.Carrot))
	elif have(Unlocks.Cactus) and item == Items.Cactus:
		# Cacti cost pumpkins per planting; same stock-then-grow loop, plus
		# one board, since the cactus code stops when a full board can no
		# longer be planted.
		while not Reached(until):
			ensurePlantable(Entities.Cactus, plantingsFor(item, amount) + n * n + 1)
			pumpkins = num_items(Items.Pumpkin)
			cacti = num_items(Items.Cactus)
			if dronesOn():
				CultivateCactiWithDrones(have(Unlocks.Watering), False, until)
			else:
				CultivateCacti(have(Unlocks.Watering), False, until)
			quick_print("cactus pass: pumpkins spent", pumpkins - num_items(Items.Pumpkin), "cactus gained", num_items(Items.Cactus) - cacti, "level", num_unlocked(Unlocks.Cactus))
	elif have(Unlocks.Dinosaurs) and item == Items.Bone:
		need = CactiForFullGrid(n) + 1
		if num_items(Items.Cactus) < need:
			farm(Items.Cactus, need)
		CultivateBones(until, BONES_SHORTCUTS[0])
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

def run(route):
	for step in route:
		target = step[0]
		level = step[1]
		optional = len(step) > 2
		while num_unlocked(target) < level:
			cost = get_cost(target)
			quick_print("t", get_time() // 1, "route", target, "level", num_unlocked(target), "->", level, "cost", cost)
			short = None
			for item in cost:
				if num_items(item) < cost[item]:
					short = item
			if short == None:
				unlock(target)
			elif optional:
				quick_print("skipped optional", target, "short of", short)
				break
			elif not farm(short, cost[short]):
				return
	quick_print("FastestReset: done, Leaderboard level", num_unlocked(Unlocks.Leaderboard))
	# Leftover stock: anything large here was farmed past its need.
	for item in [Items.Hay, Items.Wood, Items.Carrot, Items.Pumpkin, Items.Cactus, Items.Gold, Items.Bone, Items.Power, Items.Weird_Substance, Items.Water, Items.Fertilizer]:
		quick_print("left", item, num_items(item))
