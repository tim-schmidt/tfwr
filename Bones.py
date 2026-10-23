from Utilities import *

# Taking the hat off turns the tail into bones.
def CashOutBones():
	change_hat(Hats.Straw_Hat)
	clear()

# One Hamiltonian lap from (0, 0): up column 0, serpentine over rows 1..n-1,
# then West along row 0 back to the start. Needs an even n.
# Returns False as soon as a move is blocked by the tail.
def BonesLap(n):
	if not move(North):
		return False
	for x in range(n):
		direction = North
		if IsOdd(x):
			direction = South
		for _ in range(n - 2):
			if not move(direction):
				return False
		if x < n - 1:
			if not move(East):
				return False
		elif not move(South):
			return False
	for _ in range(n - 1):
		if not move(West):
			return False
	return True

def CactiForFullGrid(n):
	return n * n * get_cost(Entities.Apple)[Items.Cactus]

# Each harvest: hat on, lap until the tail blocks a move, cash out.
# Repeats while there are enough cacti to fill the grid with apples.
def CultivateBones():
	n = get_world_size()
	clear()

	while num_items(Items.Cactus) > CactiForFullGrid(n):
		change_hat(Hats.Dinosaur_Hat)
		while BonesLap(n):
			pass
		CashOutBones()
