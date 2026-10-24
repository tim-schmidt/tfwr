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

EAST = (East, 1, 0)
WEST = (West, -1, 0)
NORTH = (North, 0, 1)
SOUTH = (South, 0, -1)

# The lap above as a cycle. Returns (index, ahead): index[x * n + y] is the
# position of tile (x, y) along the lap counted from (0, 0); ahead[i] is the
# step (direction, dx, dy) from lap position i to i + 1.
def lapIndex(n):
	N = n * n
	index = []
	ahead = []
	for _ in range(N):
		index.append(0)
		ahead.append(NORTH)
	x = 0
	y = 1
	i = 1
	for column in range(n):
		step = NORTH
		if IsOdd(column):
			step = SOUTH
		for _ in range(n - 2):
			index[x * n + y] = i
			ahead[i] = step
			i += 1
			y += step[2]
		index[x * n + y] = i
		if column < n - 1:
			ahead[i] = EAST
			x += 1
		else:
			ahead[i] = SOUTH
			y -= 1
		i += 1
	for _ in range(n - 1):
		index[x * n + y] = i
		ahead[i] = WEST
		i += 1
		x -= 1
	return (index, ahead)

# One snake that follows the lap but takes shortcuts: from the head it steps
# to the neighbour furthest ahead along the lap that does not pass the apple
# and does not reach the tail. The body then always occupies a contiguous
# stretch of the lap behind the head, so no move is ever blocked until the
# board is full. measure() gives the apple's position. Stops once `tail`
# segments are on (0 means a full board) or a move fails. From `lapFrom`
# segments on, the snake just follows the lap: choosing a shortcut costs
# ticks and a long body leaves little room for one. Returns the tail
# length reached.
def ShortcutSnake(n, tail = 0, lapFrom = 0):
	N = n * n
	index, ahead = lapIndex(n)
	steps = [EAST, WEST, NORTH, SOUTH]
	x = get_pos_x()
	y = get_pos_y()
	h = index[x * n + y]
	visited = [h]
	k = 0
	while tail == 0 or k < tail:
		apple = measure()
		if apple == None:
			return k
		a = index[apple[0] * n + apple[1]]
		if lapFrom > 0 and k >= lapFrom:
			step = ahead[h]
			if not move(step[0]):
				return k
			x += step[1]
			y += step[2]
			h = (h + 1) % N
			visited.append(h)
			if h == a:
				k += 1
			continue
		toApple = (a - h) % N
		tip = visited[len(visited) - 1 - k]
		limit = N - (h - tip) % N - 1
		if limit < 1:
			limit = 1
		if toApple < limit:
			limit = toApple
		bestD = 0
		best = None
		for step in steps:
			nx = x + step[1]
			ny = y + step[2]
			if nx >= 0 and nx < n and ny >= 0 and ny < n:
				d = (index[nx * n + ny] - h) % N
				if d > bestD and d <= limit:
					bestD = d
					best = step
		if best == None or not move(best[0]):
			return k
		x += best[1]
		y += best[2]
		h = index[x * n + y]
		visited.append(h)
		if h == a:
			k += 1
	return k

def CactiForFullGrid(n):
	return n * n * get_cost(Entities.Apple)[Items.Cactus]

# Bones from a tail of k segments: k * k times the Dinosaurs multiplier, which
# doubles per level from 1 at level 1.
def bonesFor(k):
	return k * k * 2 ** (num_unlocked(Unlocks.Dinosaurs) - 1)

# Tail length whose bones reach `amount` more, 0 for a full board when a
# full snake does not get there.
def tailFor(n, amount):
	k = 1
	while bonesFor(k) < amount and k < n * n - 1:
		k += 1
	if k >= n * n - 1:
		return 0
	return k

# Each snake: hat on, shortcut snake until the board is full or the bones
# still missing are on the tail, cash out. Repeats while there are enough
# cacti to fill the grid with apples and `until` (None or (item, amount))
# is not reached.
def CultivateBones(until = None):
	n = get_world_size()
	clear()

	while num_items(Items.Cactus) > CactiForFullGrid(n) and not Reached(until):
		tail = 0
		if until != None:
			tail = tailFor(n, until[1] - num_items(until[0]))
		change_hat(Hats.Dinosaur_Hat)
		k = ShortcutSnake(n, tail)
		CashOutBones()
		quick_print("snake tail", k, "bones", num_items(Items.Bone))
