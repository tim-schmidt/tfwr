# Probe start file for SimLevels.py. Not run directly.
# Starts with no unlocks and a huge stock, then buys every unlock level it
# can, in passes, until a pass buys nothing. Prints each purchase with the
# cost that get_cost() reported just before it, so the full cost table and
# the prerequisite order fall out. Also shows that unlock() inside a
# simulation sets levels, the way to measure a phase at its real state.
names = [Unlocks.Expand, Unlocks.Speed, Unlocks.Plant, Unlocks.Grass, Unlocks.Trees, Unlocks.Carrots, Unlocks.Watering, Unlocks.Fertilizer, Unlocks.Hats, Unlocks.Sunflowers, Unlocks.Mazes, Unlocks.Pumpkins, Unlocks.Polyculture, Unlocks.Cactus, Unlocks.Dinosaurs, Unlocks.Megafarm, Unlocks.Leaderboard]

quick_print("levels probe start world", get_world_size(), "expand", num_unlocked(Unlocks.Expand), "drones", max_drones())
progress = True
bought = 0
while progress:
	progress = False
	for u in names:
		cost = get_cost(u)
		if len(cost) > 0:
			if unlock(u):
				progress = True
				bought += 1
				quick_print("bought", u, "level", num_unlocked(u), "cost", cost, "world", get_world_size(), "drones", max_drones())
quick_print("levels probe done, bought", bought)
