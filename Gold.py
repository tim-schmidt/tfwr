def here():
	return (get_pos_x(), get_pos_y())

def step(delta, pos, d):
	return (pos[0] + delta[d][0], pos[1] + delta[d][1])

def dir_to(dir_of, a, b):
	return dir_of[(b[0] - a[0], b[1] - a[1])]

def scan(dirs, graph):
	exits = []
	for d in dirs:
		if can_move(d):
			exits.append(d)
	graph[here()] = exits

# Depth-first walk of the whole maze. Fills graph (open exits per cell),
# parent and depth (a spanning tree rooted where the walk began).
def explore(dirs, delta, back, graph, parent, depth):
	stack = []
	depth[here()] = 0
	while True:
		pos = here()
		if pos not in graph:
			scan(dirs, graph)
		went = False
		for d in graph[pos]:
			n = step(delta, pos, d)
			if n not in graph:
				move(d)
				parent[n] = pos
				depth[n] = depth[pos] + 1
				stack.append(back[d])
				went = True
				break
		if not went:
			if len(stack) == 0:
				return
			move(stack.pop())

# Cells from start to goal along the spanning tree, both ends included.
def tree_path(parent, depth, start, goal):
	a = start
	b = goal
	path = []        # cells from start upward
	tail = []        # cells from goal upward, walked in reverse later
	while a != b:
		if depth[a] >= depth[b]:
			path.append(a)
			a = parent[a]
		else:
			tail.append(b)
			b = parent[b]
	path.append(a)   # meeting point
	j = len(tail) - 1
	while j >= 0:
		path.append(tail[j])
		j -= 1
	return path

# Index of every cell on the path, for shortcut checks.
def path_index(path):
	index = {}
	for k in range(len(path)):
		index[path[k]] = k
	return index

# Variant 0: tree path; at each step look at all four neighbours and jump
# ahead along the path wherever a removed hedge allows. Neighbour tuples and
# index lookups happen before can_move.
def go_to_scan(dirs, delta, dir_of, parent, depth, goal):
	path = tree_path(parent, depth, here(), goal)
	index = path_index(path)
	k = 0
	while k < len(path) - 1:
		pos = path[k]
		best = k + 1
		for d in dirs:
			c = step(delta, pos, d)
			if c in index and index[c] > best and can_move(d):
				best = index[c]
		move(dir_to(dir_of, pos, path[best]))
		k = best

# Variant 1: tree path only, no shortcut checks.
def go_to_lean(dir_of, parent, depth, goal):
	path = tree_path(parent, depth, here(), goal)
	for k in range(len(path) - 1):
		move(dir_to(dir_of, path[k], path[k + 1]))

# Variant 2: same shortcuts as variant 0, but can_move first so blocked
# directions cost one tick, and if-chains instead of `and`.
def go_to_fast(dirs, delta, dir_of, parent, depth, goal):
	path = tree_path(parent, depth, here(), goal)
	index = path_index(path)
	k = 0
	while k < len(path) - 1:
		pos = path[k]
		best = k + 1
		for d in dirs:
			if can_move(d):
				c = step(delta, pos, d)
				if c in index:
					if index[c] > best:
						best = index[c]
		move(dir_to(dir_of, pos, path[best]))
		k = best

def createMaze(substanceAmount):
	plant(Entities.Bush)
	use_item(Items.Weird_Substance, substanceAmount)

# One maze: build it, explore it, relocate the treasure `reuses` times,
# harvest. `variant` picks the walking strategy (see go_to_* above).
def CultivateGold(variant = 0, reuses = 300):
	substanceAmount = get_world_size() * 2**(num_unlocked(Unlocks.Mazes) - 1)
	createMaze(substanceAmount)

	dirs = [North, East, South, West]
	delta = {North: (0, 1), East: (1, 0), South: (0, -1), West: (-1, 0)}
	dir_of = {(0, 1): North, (1, 0): East, (0, -1): South, (-1, 0): West}
	back = {North: South, East: West, South: North, West: East}
	graph = {}    # cell -> list of open directions (used by explore)
	parent = {}   # cell -> the cell it was first reached from
	depth = {}    # cell -> distance from the start cell along the tree

	explore(dirs, delta, back, graph, parent, depth)

	for i in range(reuses):
		goal = measure()
		if variant == 1:
			go_to_lean(dir_of, parent, depth, goal)
		elif variant == 2:
			go_to_fast(dirs, delta, dir_of, parent, depth, goal)
		else:
			go_to_scan(dirs, delta, dir_of, parent, depth, goal)
		use_item(Items.Weird_Substance, substanceAmount)
	harvest()
