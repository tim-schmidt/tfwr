# Start file for SimGold.py. SIZE arrives through sim_globals.
# Prints gold gained and substance spent by one maze, measured inside the
# simulation, so SimGold.py can report gold per second and per substance.
from Gold import CultivateGold

set_world_size(SIZE)
gold = num_items(Items.Gold)
substance = num_items(Items.Weird_Substance)
CultivateGold()
quick_print("result size", SIZE, "gold", num_items(Items.Gold) - gold, "substance", substance - num_items(Items.Weird_Substance))
