def Reuses():
	return 300

# Go up a maze size only if it leaves at most this many cells uncovered.
def MaxUncovered():
	return 4

def Substance():
	return get_world_size() * 2**(num_unlocked(Unlocks.Mazes) - 1)

# Moves the main drone idles between mazes so every parked drone has read
# the substance count before the next maze consumes a dose.
def SettleMoves():
	return 4

# Largest n in 4..6 with n*n - MaxUncovered() <= drones.
def ChooseSize(drones):
	n = 4
	for size in [5, 6]:
		if size * size - MaxUncovered() <= drones:
			n = size
	return n

def Manhattan(a, b):
	dx = a[0] - b[0]
	dy = a[1] - b[1]
	if dx < 0:
		dx = -dx
	if dy < 0:
		dy = -dy
	return dx + dy

# How corner-like a cell is: 0 for a corner, 1 beside a corner, and so on.
def Cornerness(pos, n):
	x = min(pos[0], n - 1 - pos[0])
	y = min(pos[1], n - 1 - pos[1])
	return x + y

def Here():
	return (get_pos_x(), get_pos_y())

def Step(orders, pos, d):
	return (pos[0] + orders["delta"][d][0], pos[1] + orders["delta"][d][1])

def Walk(route):
	for d in route:
		move(d)

# Straight-line directions from a to b on an open field.
def OpenRoute(a, b):
	route = []
	for _ in range(b[0] - a[0]):
		route.append(East)
	for _ in range(a[0] - b[0]):
		route.append(West)
	for _ in range(b[1] - a[1]):
		route.append(North)
	for _ in range(a[1] - b[1]):
		route.append(South)
	return route

# Kill time without leaving the cell: step out and back.
def Idle(orders, moves):
	d = East
	if get_pos_x() == get_world_size() - 1:
		d = West
	for _ in range(moves // 2):
		move(d)
		move(orders["back"][d])

# ---------------- planning (main drone only) ----------------
# Which cells get a drone. With fewer drones than cells, the most
# corner-like cells go without.
def CoveredCells(n, drones):
	cells = []
	for y in range(n):
		for x in range(n):
			cells.append((x, y))
	spare = n * n - drones
	if spare <= 0:
		return cells
	covered = []
	for rank in range(n):
		for c in cells:
			if Cornerness(c, n) == rank:
				if spare > 0:
					spare -= 1
				else:
					covered.append(c)
	return covered

# For every uncovered cell, give each covered orthogonal neighbour a duty:
# (direction into the cell, directions from inside the cell toward the
# neighbours that outrank it). Priority follows orders["dirs"].
def AssignDuties(orders, n, covered):
	isCovered = {}
	duties = {}
	for c in covered:
		isCovered[c] = True
		duties[c] = {}
	for y in range(n):
		for x in range(n):
			cell = (x, y)
			if cell in isCovered:
				continue
			outranking = []
			for d in orders["dirs"]:
				neighbour = Step(orders, cell, d)
				if neighbour in isCovered:
					duties[neighbour][cell] = (orders["back"][d], outranking)
					higher = []
					for e in outranking:
						higher.append(e)
					higher.append(d)
					outranking = higher
			if len(outranking) == 0:
				print("maze: an uncovered cell has no covered neighbour")
	return duties

# ---------------- what every parked drone does ----------------
# Use the substance on the treasure under us, or harvest it after the cap.
# Returns True when the maze was harvested.
def ActOnTreasure(orders, start):
	amount = Substance()
	if (start - num_items(Items.Weird_Substance)) // amount >= Reuses():
		harvest()
		return True
	use_item(Items.Weird_Substance, amount)
	return False

# Serve one maze from our home cell until it is harvested. `start` is the
# substance count just after the maze was made.
def ServeMaze(orders, start):
	home = orders["home"]
	duties = orders["duties"]
	while True:
		target = measure()
		if target == None:
			return
		if target == home:
			if ActOnTreasure(orders, start):
				return
		elif target in duties:
			duty = duties[target]
			if can_move(duty[0]):
				move(duty[0])
				mine = True
				for d in duty[1]:
					if can_move(d):
						mine = False
				harvested = False
				if mine and measure() == target:
					harvested = ActOnTreasure(orders, start)
				move(orders["back"][duty[0]])
				if harvested:
					return

def Worker(orders):
#	orders = DM_ORDERS
	Walk(orders["route"])
	while True:
		before = num_items(Items.Weird_Substance)
		while measure() == None:
			pass
		ServeMaze(orders, before - Substance())

def CultivateGoldWithDrones(orders):
	orders["dirs"] = [East, North, West, South]
	orders["delta"] = {North: (0, 1), East: (1, 0), South: (0, -1), West: (-1, 0)}
	orders["back"] = {North: South, East: West, South: North, West: East}

	drones = max_drones()
	n = ChooseSize(drones)
	set_world_size(n)
	clear()

	covered = CoveredCells(n, drones)
	home = covered[0]
	for c in covered:
		if Manhattan(c, (0, 0)) < Manhattan(home, (0, 0)):
			home = c
	duties = AssignDuties(orders, n, covered)
	Walk(OpenRoute(Here(), home))

	# Deploy once, on the open field: each child gets a straight-line route.
	for c in covered:
		if c == home:
			continue
		orders["home"] = c
		orders["route"] = OpenRoute(home, c)
		orders["duties"] = duties[c]
		while spawn_drone(Worker, orders) == None:
			pass
	orders["home"] = home
	orders["route"] = []
	orders["duties"] = duties[home]

	# Let the farthest child arrive before the hedges go up.
	Idle(orders, 2 * (n - 1) + 2)

	while True:
		before = num_items(Items.Weird_Substance)
		plant(Entities.Bush)
		use_item(Items.Weird_Substance, Substance())
		ServeMaze(orders, before - Substance())
#		clear()
		Idle(orders, SettleMoves())
