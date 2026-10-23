from Utilities import *

def here():
	return (get_pos_x(), get_pos_y())

# Neighbour of pos in direction d, wrapping at the farm edge like move().
def step(n, delta, pos, d):
	return ((pos[0] + delta[d][0]) % n, (pos[1] + delta[d][1]) % n)

def scan(dirs, graph):
	exits = []
	for d in dirs:
		if can_move(d):
			exits.append(d)
	graph[here()] = exits

# Depth-first walk of the whole maze. Fills graph (open exits per cell),
# parent, depth and pdir (a spanning tree rooted where the walk began;
# pdir[cell] is the direction from cell to its parent).
def explore(dirs, delta, back, graph, parent, depth, pdir, order):
	n = get_world_size()
	stack = []
	depth[here()] = 0
	order.append(here())
	while True:
		pos = here()
		if pos not in graph:
			scan(dirs, graph)
		went = False
		for d in graph[pos]:
			c = step(n, delta, pos, d)
			if c not in graph:
				move(d)
				parent[c] = pos
				depth[c] = depth[pos] + 1
				pdir[c] = back[d]
				order.append(c)
				stack.append(back[d])
				went = True
				break
		if not went:
			if len(stack) == 0:
				return
			move(stack.pop())

# Directions to walk from start to goal along the spanning tree. Climbs
# from both ends toward the root until the climbs meet.
def tree_route(parent, depth, pdir, back, start, goal):
	a = start
	b = goal
	route = []       # moves from start upward
	tail = []        # moves from goal upward, reversed and flipped later
	while a != b:
		if depth[a] >= depth[b]:
			route.append(pdir[a])
			a = parent[a]
		else:
			tail.append(back[pdir[b]])
			b = parent[b]
	j = len(tail) - 1
	while j >= 0:
		route.append(tail[j])
		j -= 1
	return route

# Walk the tree route from here to goal. Shortcut checks through removed
# hedges were measured in simulation and cost more than they save.
def go_to(parent, depth, pdir, back, goal):
	route = tree_route(parent, depth, pdir, back, here(), goal)
	for d in route:
		move(d)

def createMaze(substanceAmount):
	plant(Entities.Bush)
	use_item(Items.Weird_Substance, substanceAmount)

def substanceFor(size):
	return size * 2**(num_unlocked(Unlocks.Mazes) - 1)

# Explore the maze under the drone. Returns a dict of maps:
#   graph  cell -> open directions      parent cell -> tree parent
#   depth  cell -> tree depth           pdir   cell -> direction to parent
#   order  cells in visit order         back   direction -> opposite
#   delta  direction -> (dx, dy)
def mapMaze():
	m = {}
	m["delta"] = {North: (0, 1), East: (1, 0), South: (0, -1), West: (-1, 0)}
	m["back"] = {North: South, East: West, South: North, West: East}
	m["graph"] = {}
	m["parent"] = {}
	m["depth"] = {}
	m["pdir"] = {}
	m["order"] = []
	explore([North, East, South, West], m["delta"], m["back"], m["graph"], m["parent"], m["depth"], m["pdir"], m["order"])
	return m

# One maze under the drone: build it, explore it, relocate the treasure
# `reuses` times, harvest. Returns the explored graph.
def goldMaze(size, reuses):
	substanceAmount = substanceFor(size)
	createMaze(substanceAmount)
	m = mapMaze()
	graph = m["graph"]
	parent = m["parent"]
	depth = m["depth"]
	pdir = m["pdir"]
	back = m["back"]

	for i in range(reuses):
		goal = measure()
		if goal == None:
			quick_print("goldMaze: maze gone after", i, "relocations at", here())
			return graph
		go_to(parent, depth, pdir, back, goal)
		use_item(Items.Weird_Substance, substanceAmount)
	harvest()
	return graph

# Single drone. `size` is the maze size; 0 means the whole farm.
def CultivateGold(size = 0, reuses = 300):
	if size == 0:
		size = get_world_size()
	goldMaze(size, reuses)

# Bounding box of the explored cells: (minX, minY, maxX, maxY).
def mazeBounds(graph):
	minX = get_world_size()
	minY = minX
	maxX = 0
	maxY = 0
	for cell in graph:
		minX = min(minX, cell[0])
		minY = min(minY, cell[1])
		maxX = max(maxX, cell[0])
		maxY = max(maxY, cell[1])
	return (minX, minY, maxX, maxY)

# Sector worker. Walks from (0, 0) over the open field to its sector's
# center tile, waits for the shared deadline so every drone is in place
# before any hedges appear, then farms one maze there. A maze spawns
# centered on the drone (offset size // 2 down and left), so spawning from
# the center puts it exactly on the sector.
def sectorWorker(n, cx, cy, size, reuses, deadline):
	MoveTo(n, 0, 0, cx, cy)
	while get_time() < deadline:
		pass
	graph = goldMaze(size, reuses)
	quick_print("sector center", (cx, cy), "maze bounds", mazeBounds(graph))

# Many drones, one maze each, on a grid of square sectors of side `size`.
# `rounds` of 0 means run forever.
def CultivateGoldInSectors(size, reuses = 300, rounds = 0):
	n = get_world_size()
	k = n // size
	MoveTo(n, get_pos_x(), get_pos_y(), 0, 0)

	# Seconds per move at the current speed, for the arrival deadline.
	t0 = get_time()
	move(East)
	move(West)
	perMove = (get_time() - t0) / 2

	done = 0
	while rounds == 0 or done < rounds:
		deadline = get_time() + perMove * (2 * n + 4)
		workers = []
		half = size // 2
		for i in range(k):
			for j in range(k):
				if i == 0 and j == 0:
					continue
				drone = spawn_drone(sectorWorker, n, i * size + half, j * size + half, size, reuses, deadline)
				if drone == None:
					quick_print("no drone for sector", (i, j))
				else:
					workers.append(drone)
		sectorWorker(n, half, half, size, reuses, deadline)
		for drone in workers:
			wait_for(drone)
		done += 1

# ---------------- many drones, one maze ----------------
# Every cell is owned by the drone whose home is nearest along the maze.
# Multi-source breadth-first search over the open exits.
def ownerMap(n, m, homes):
	owner = {}
	queue = []
	for i in range(len(homes)):
		owner[homes[i]] = i
		queue.append(homes[i])
	k = 0
	while k < len(queue):
		cell = queue[k]
		k += 1
		for d in m["graph"][cell]:
			c = step(n, m["delta"], cell, d)
			if c not in owner:
				owner[c] = owner[cell]
				queue.append(c)
	return owner

# Serve one maze. `mine` holds the owner ids this drone answers for.
# Walk home from the root, then: whenever the treasure sits on a cell we
# own, walk there and relocate it, or harvest it on the last relocation.
# Everyone sees the maze vanish through measure() and returns. Relocations
# so far are read from the shared substance count, so no messages needed.
def serveMaze(mine, home, m, owner, amount, start, reuses):
	parent = m["parent"]
	depth = m["depth"]
	pdir = m["pdir"]
	back = m["back"]
	go_to(parent, depth, pdir, back, home)
	while True:
		target = measure()
		if target == None:
			return
		if owner[target] in mine:
			go_to(parent, depth, pdir, back, target)
			if (start - num_items(Items.Weird_Substance)) // amount >= reuses:
				harvest()
				return
			use_item(Items.Weird_Substance, amount)

# Worker entry point.
def mazeWorker(me, home, m, owner, amount, start, reuses):
	serveMaze({me: True}, home, m, owner, amount, start, reuses)

# Many drones share one maze. Main builds and maps the maze, picks a home
# per drone spread along the exploration order, hands every worker the
# map and owner table through spawn_drone, and serves as drone 0 itself.
# Ids whose spawn fails are served by main. `rounds` of 0 runs forever.
def CultivateGoldWithDrones(size = 0, reuses = 300, rounds = 0):
	n = get_world_size()
	if size == 0:
		size = n
	amount = substanceFor(size)

	done = 0
	while rounds == 0 or done < rounds:
		createMaze(amount)
		start = num_items(Items.Weird_Substance)
		m = mapMaze()
		order = m["order"]

		count = max_drones()
		if count > len(order):
			count = len(order)
		homes = []
		for i in range(count):
			homes.append(order[(i * len(order)) // count])
		owner = ownerMap(n, m, homes)

		workers = []
		mine = {0: True}
		for i in range(1, count):
			drone = spawn_drone(mazeWorker, i, homes[i], m, owner, amount, start, reuses)
			if drone == None:
				mine[i] = True
			else:
				workers.append(drone)
		serveMaze(mine, homes[0], m, owner, amount, start, reuses)
		for drone in workers:
			wait_for(drone)
		done += 1
