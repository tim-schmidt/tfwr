# Probe start file for SimHay.py. Not run directly. Starts with no
# unlocks and buys SPEED levels of Speed, EXPAND levels of Expand and
# Plant when PLANT is 1, then gathers 200 hay in one of two ways:
#   MODE 0  stay on one tile: harvest, replant if allowed, wait
#   MODE 1  harvest and move to the next tile, column by column
# The returned simulation time is the cost.
for i in range(SPEED):
	unlock(Unlocks.Speed)
for i in range(EXPAND):
	unlock(Unlocks.Expand)
if PLANT == 1:
	unlock(Unlocks.Plant)
n = get_world_size()
goal = num_items(Items.Hay) + 200
if MODE == 0:
	while num_items(Items.Hay) < goal:
		if can_harvest():
			harvest()
			if PLANT == 1:
				plant(Entities.Grass)
else:
	while num_items(Items.Hay) < goal:
		for i in range(n):
			for j in range(n):
				if can_harvest():
					harvest()
					if PLANT == 1:
						plant(Entities.Grass)
				move(North)
			move(East)
quick_print("hay probe speed", SPEED, "expand", EXPAND, "plant", PLANT, "mode", MODE, "world", n)
