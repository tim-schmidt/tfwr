from Utilities import *
from Drones import *

# Sort the n tiles starting under the drone. a[i] is the tile i steps in
# `toward`. s = 1 sorts ascending along `toward`, s = -1 descending.
# Ends at the far end of the line.
def sortLine(a, n, toward, back, s):
	pos = 0
	while pos < n - 1:
		if (a[pos + 1] - a[pos]) * s < 0:
			t = a[pos]
			a[pos] = a[pos + 1]
			a[pos + 1] = t
			swap(toward)
			if pos > 0:
				move(back)
				pos -= 1
		else:
			move(toward)
			pos += 1

# Plant n tiles walking in `step`. Ends on the last tile planted.
def plantLine(n, step, water, fertilize):
	for i in range(n):
		TillIfNeeded(Entities.Cactus)
		WaterIfWanted(water)
		plant(Entities.Cactus)
		FertilizeIfWanted(fertilize)
		if i < n - 1:
			move(step)

# Measure n tiles walking in `step`, waiting for each to finish growing.
# Returns the sizes in walking order. Ends on the last tile measured.
def waitAndMeasureLine(n, step):
	a = []
	for i in range(n):
		while not can_harvest():
			pass
		a.append(measure())
		if i < n - 1:
			move(step)
	return a

def measureLine(n, step):
	a = []
	for i in range(n):
		a.append(measure())
		if i < n - 1:
			move(step)
	return a

def reversed_(a, n):
	b = []
	for i in range(n - 1, -1, -1):
		b.append(a[i])
	return b

# Phase 1 over w columns starting under the drone. Each column: plant going
# `up`, wait and measure coming back `down`, sort going `up` again. That
# leaves the drone at the far end, so the directions flip for the next
# column instead of walking back. Sizes must ascend toward North: s is +1
# when `up` is North, -1 when South. Ends on the last column, top or bottom.
def cactusColumns(n, w, water, fertilize):
	up = North
	down = South
	s = 1
	for i in range(w):
		plantLine(n, up, water, fertilize)
		a = waitAndMeasureLine(n, down)
		sortLine(reversed_(a, n), n, up, down, s)
		if i < w - 1:
			move(East)
		up, down = down, up
		s = -s

# Phase 2 over h rows starting under the drone at x == 0. Every cactus is
# grown by now. Each row: measure going East, sort coming back West
# (descending toward West is ascending toward East). Ends at the west end
# of the last row. Sorting rows keeps the columns sorted.
def cactusRows(n, h):
	for i in range(h):
		a = measureLine(n, East)
		sortLine(reversed_(a, n), n, West, East, -1)
		if i < h - 1:
			move(North)

# Wrap-around walk to (0, 0). Cheapest when coming from the far edge.
def goHome():
	while get_pos_x() != 0:
		move(East)
	while get_pos_y() != 0:
		move(North)

# Single drone: columns, then rows, then one harvest for the whole field.
def CultivateCacti(water = False, fertilize = False):
	n = get_world_size()
	while num_items(Items.Pumpkin) > n * n * get_cost(Entities.Cactus)[Items.Pumpkin]:
		goHome()
		cactusColumns(n, n, water, fertilize)
		goHome()
		cactusRows(n, n)
		harvest()

# Drone strip workers. Both take the same arguments so runPhase can spawn
# either; the row phase has nothing to plant.
def cactusColumnStrip(water = False, fertilize = False):
	n, w, d = layout()
	cactusColumns(n, min(w, n - get_pos_x()), water, fertilize)

def cactusRowStrip(water = False, fertilize = False):
	n, w, d = layout()
	cactusRows(n, min(w, n - get_pos_y()))

# Spawn a worker per strip along `step`, work the leftover strips with the
# main drone, then wait for everyone. The main drone's last move wraps it
# back to the coordinate the phase began on.
def runPhase(worker, step, n, w, water, fertilize):
	workers = []
	pos = 0
	while pos + w < n:
		drone = spawn_drone(worker, water, fertilize)
		if drone == None:
			break
		workers.append(drone)
		for _ in range(w):
			move(step)
		pos += w
	while pos < n:
		worker(water, fertilize)
		move(step)
		pos += min(w, n - pos)
	for drone in workers:
		wait_for(drone)

def CultivateCactiWithDrones(water = False, fertilize = False):
	n, w, d = layout()
	while get_pos_x() != 0:
		move(West)
	while get_pos_y() != 0:
		move(South)

	while num_items(Items.Pumpkin) > n * n * get_cost(Entities.Cactus)[Items.Pumpkin]:
		runPhase(cactusColumnStrip, East, n, w, water, fertilize)
		# The column phase ends at the top or bottom of the field depending
		# on strip width; one wrap-around step puts the main drone on row 0.
		while get_pos_y() != 0:
			move(North)
		runPhase(cactusRowStrip, North, n, w, water, fertilize)
		# Every cactus is grown and the field is sorted on both axes:
		# a single harvest takes the whole field at full value.
		harvest()
