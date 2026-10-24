# Probe start file for SimBones.py. Not run directly. All unlocks.
# One snake on a WORLD x WORLD farm, hat on, until the board is full:
#   MODE 0  Hamiltonian laps (BonesLap) until the tail blocks a move
#   MODE 1  the lap with shortcuts (ShortcutSnake)
#   MODE 2  shortcuts until LAPFROM segments are on, then plain lap following
# Prints what measure() says at the start, then bones and cactus spent.
# The returned time is the cost.
from Bones import BonesLap, ShortcutSnake, CashOutBones

set_world_size(WORLD)
clear()
bones = num_items(Items.Bone)
cactus = num_items(Items.Cactus)
change_hat(Hats.Dinosaur_Hat)
quick_print("measure with hat at", get_pos_x(), get_pos_y(), "->", measure(), "entity here", get_entity_type())
tail = 0
if MODE == 0:
	while BonesLap(get_world_size()):
		pass
elif MODE == 1:
	tail = ShortcutSnake(get_world_size(), 0, 0, True)
else:
	tail = ShortcutSnake(get_world_size(), 0, LAPFROM, True)
CashOutBones()
quick_print("bones probe mode", MODE, "world", WORLD, "tail", tail, "bones", num_items(Items.Bone) - bones, "cactus spent", cactus - num_items(Items.Cactus))
