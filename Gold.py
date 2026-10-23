def here():
	return (get_pos_x(), get_pos_y())

def step(delta, pos, d):
	return (pos[0] + delta[d][0], pos[1] + delta[d][1])

def scan(dirs, graph):
	exits = []
	for d in dirs:
		if can_move(d):
			exits.append(d)
	graph[here()] = exits

# Depth-first walk of the whole maze. Fills graph (open exits per cell),
# parent, depth and pdir (a spanning tree rooted where the walk began;
# pdir[cell] is the direction from cell to its parent).
def explore(dirs, delta, back, graph, parent, depth, pdir):
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
				pdir[n] = back[d]
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

# One maze: build it, explore it, relocate the treasure `reuses` times,
# harvest.
def CultivateGold(reuses = 300):
	substanceAmount = get_world_size() * 2**(num_unlocked(Unlocks.Mazes) - 1)
	createMaze(substanceAmount)

	dirs = [North, East, South, West]
	delta = {North: (0, 1), East: (1, 0), South: (0, -1), West: (-1, 0)}
	back = {North: South, East: West, South: North, West: East}
	graph = {}    # cell -> list of open directions (used by explore)
	parent = {}   # cell -> the cell it was first reached from
	depth = {}    # cell -> distance from the start cell along the tree
	pdir = {}     # cell -> direction from the cell to its parent

	explore(dirs, delta, back, graph, parent, depth, pdir)

	for i in range(reuses):
		go_to(parent, depth, pdir, back, measure())
		use_item(Items.Weird_Substance, substanceAmount)
	harvest()
