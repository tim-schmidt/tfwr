# Start file that simulate() loads for SimTime.py. Not run directly.
# WORLD, TARGET, MODE, WATER arrive through sim_globals. Farms trees until
# TARGET wood with the contender MODE picks, watering when WATER is set,
# so the returned time gives wood per second. Prints the side crops gained.
#   1 sweep, single drone, no companions
#   2 sweep, single drone, companions
#   3 sweep, all drones, no companions
#   4 sweep, all drones, companions
#   5 yield board, 50 percent trees, bush slots, re-roll, single drone
from StandardCrops import CultivateCrops, CultivateCropsWithDrones
from YieldCrops import CultivateYieldBoard

set_world_size(WORLD)
hay = num_items(Items.Hay)
water = num_items(Items.Water)
carrots = num_items(Items.Carrot)
goal = (Items.Wood, num_items(Items.Wood) + TARGET)
rolls = 0
if MODE == 1:
	CultivateCrops(Entities.Tree, Entities.Grass, WATER, False, False, goal)
elif MODE == 2:
	CultivateCrops(Entities.Tree, Entities.Grass, WATER, False, True, goal)
elif MODE == 3:
	CultivateCropsWithDrones(Entities.Tree, Entities.Grass, WATER, False, False, goal)
elif MODE == 4:
	CultivateCropsWithDrones(Entities.Tree, Entities.Grass, WATER, False, True, goal)
elif MODE == 5:
	rolls = CultivateYieldBoard(Entities.Tree, Entities.Grass, WATER, False, False, True, 0, 50, Entities.Bush, goal)
quick_print("result world", WORLD, "mode", MODE, "water", WATER, "hay", num_items(Items.Hay) - hay, "carrots", num_items(Items.Carrot) - carrots, "water used", water - num_items(Items.Water), "rerolls", rolls)
