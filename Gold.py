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

def go_to(dirs, delta, dir_of, parent, depth, goal):
	# climb from both ends toward the root until the climbs meet
	a = here()
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

	# position of every cell on the path, for shortcut checks
	index = {}
	for k in range(len(path)):
		index[path[k]] = k

	k = 0
	while k < len(path) - 1:
		pos = path[k]
		best = k + 1
		for d in dirs:
			n = step(delta, pos, d)
			if n in index and index[n] > best and can_move(d):
				best = index[n]      # removed hedge: jump ahead
		move(dir_to(dir_of, pos, path[best]))
		k = best

def createMaze(substanceAmount):
	plant(Entities.Bush)
	use_item(Items.Weird_Substance, substanceAmount)

def CultivateGold():
#	set_world_size(6)
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

	for i in range(300):
		go_to(dirs, delta, dir_of, parent, depth, measure())
		use_item(Items.Weird_Substance, substanceAmount)
	harvest()
