# Start file that simulate() loads for SimDrones.py. Not run directly.
# WORLD and SIZE arrive through sim_globals. One maze served by every
# available drone; prints gold gained and substance spent.
from Gold import CultivateGoldWithDrones

set_world_size(WORLD)
gold = num_items(Items.Gold)
substance = num_items(Items.Weird_Substance)
CultivateGoldWithDrones(SIZE, 300, 1)
quick_print("result world", WORLD, "size", SIZE, "drones", max_drones(), "gold", num_items(Items.Gold) - gold, "substance", substance - num_items(Items.Weird_Substance))
