# Start file that simulate() loads for SimAnchor.py. Not run directly.
# WORLD, SIZE, OX, OY arrive through sim_globals. One drone walks to
# (OX, OY), spawns a maze of SIZE, explores it, and reports where the
# maze ended up and whether its walls hold at the farm edge.
from Utilities import *
from Gold import goldMaze, mazeBounds

set_world_size(WORLD)
MoveTo(WORLD, get_pos_x(), get_pos_y(), OX, OY)
graph = goldMaze(SIZE, 0)
quick_print("anchor world", WORLD, "size", SIZE, "origin", (OX, OY), "bounds", mazeBounds(graph), "cells", len(graph))
