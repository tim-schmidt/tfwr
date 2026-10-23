# Start file that simulate() loads for SimCrops.py. Not run directly.
# WORLD, COMPANIONS, DRONES, TARGET arrive through sim_globals.
# Farms trees and grass until TARGET wood, so the returned time gives
# wood per second. Prints the other crops gained on the side.
from StandardCrops import CultivateCrops, CultivateCropsWithDrones

set_world_size(WORLD)
hay = num_items(Items.Hay)
carrots = num_items(Items.Carrot)
goal = (Items.Wood, num_items(Items.Wood) + TARGET)
if DRONES:
	CultivateCropsWithDrones(Entities.Tree, Entities.Grass, False, False, COMPANIONS, goal)
else:
	CultivateCrops(Entities.Tree, Entities.Grass, False, False, COMPANIONS, goal)
quick_print("result world", WORLD, "drones", DRONES, "companions", COMPANIONS, "hay", num_items(Items.Hay) - hay, "carrots", num_items(Items.Carrot) - carrots)
