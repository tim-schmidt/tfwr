# Start file that simulate() loads for SimGold.py. Not run directly.
# SIZE (maze size) arrives through sim_globals.
# The farm cannot go below 3x3, so small mazes run on a 3x3 farm.
# Prints gold gained and substance spent by one maze, measured inside the
# simulation, so SimGold.py can report gold per second and per substance.
from Gold import CultivateGold

set_world_size(max(SIZE, 3))
gold = num_items(Items.Gold)
substance = num_items(Items.Weird_Substance)
CultivateGold(SIZE)
quick_print("result size", SIZE, "gold", num_items(Items.Gold) - gold, "substance", substance - num_items(Items.Weird_Substance))
