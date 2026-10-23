# Probe start file for SimProbe.py. Not run directly.
# One snake: hat on, Hamiltonian laps until the tail blocks a move, hat
# off. Prints bones and cactus spent; the returned time is the cost.
from Bones import BonesLap, CashOutBones

set_world_size(WORLD)
clear()
bones = num_items(Items.Bone)
cactus = num_items(Items.Cactus)
change_hat(Hats.Dinosaur_Hat)
laps = 0
while BonesLap(get_world_size()):
	laps += 1
CashOutBones()
quick_print("bones probe world", WORLD, "bones", num_items(Items.Bone) - bones, "laps", laps, "cactus spent", cactus - num_items(Items.Cactus))
