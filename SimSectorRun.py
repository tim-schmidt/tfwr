# Start file for SimSector.py. WORLD and SIZE arrive through sim_globals.
# One round of sector mazes; prints gold gained and substance spent.
from Gold import CultivateGoldInSectors

set_world_size(WORLD)
gold = num_items(Items.Gold)
substance = num_items(Items.Weird_Substance)
CultivateGoldInSectors(SIZE, 300, 1)
quick_print("result world", WORLD, "size", SIZE, "gold", num_items(Items.Gold) - gold, "substance", substance - num_items(Items.Weird_Substance))
