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

# The one or two directions that bring pos closer to goal by Manhattan distance.
def toward(pos, goal):
	dirs = []
	if goal[0] > pos[0]:
		dirs.append(East)
	elif goal[0] < pos[0]:
		dirs.append(West)
	if goal[1] > pos[1]:
		dirs.append(North)
	elif goal[1] < pos[1]:
		dirs.append(South)
	return dirs

# Greedy sidestep: leave the planned path through a hedge that was closed
# when the maze was explored and is open now, when that gets closer to the
# goal and the cell is new this walk. Tree edges off the path are never
# taken: they lead into dead ends. Returns the new cell, or None.
def sidestep(delta, graph, index, visited, pos, goal):
	for d in toward(pos, goal):
		if d not in graph[pos]:
			n = step(delta, pos, d)
			if n not in index:
				if n not in visited:
					if can_move(d):
						move(d)
						return n
	return None

# Walk to goal. Follows the tree path, jumping ahead along it wherever a
# hedge has been removed. With greedy on, it also steps off the path toward
# the goal through removed hedges and re-plans from there. `visited` keeps
# a sidestep from revisiting a cell, which bounds the walk.
def go_to(dirs, delta, dir_of, graph, parent, depth, goal, greedy):
	pos = here()
	visited = {}
	while pos != goal:
		path = tree_path(parent, depth, pos, goal)
		index = {}
		for k in range(len(path)):
			index[path[k]] = k

		k = 0
		n = None
		while k < len(path) - 1:
			pos = path[k]
			visited[pos] = True
			n = None
			if greedy:
				n = sidestep(delta, graph, index, visited, pos, goal)
			if n != None:
				break
			best = k + 1
			for d in dirs:
				c = step(delta, pos, d)
				if c in index and index[c] > best and can_move(d):
					best = index[c]      # removed hedge: jump ahead
			move(dir_to(dir_of, pos, path[best]))
			k = best
		if n == None:
			pos = goal
		else:
			pos = n

def createMaze(substanceAmount):
	plant(Entities.Bush)
	use_item(Items.Weird_Substance, substanceAmount)

# One maze: build it, explore it, relocate the treasure `reuses` times,
# harvest. `greedy` enables off-path shortcuts through removed hedges.
def CultivateGold(greedy = False, reuses = 300):
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
		go_to(dirs, delta, dir_of, graph, parent, depth, measure(), greedy)
		use_item(Items.Weird_Substance, substanceAmount)
	harvest()
