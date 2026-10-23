# Start file for SimGold.py. Reads SIZE and GREEDY from SIM_GLOBALS.
from SimGlobals import SIM_GLOBALS
from Gold import CultivateGold

SIZE = SIM_GLOBALS["SIZE"]
GREEDY = SIM_GLOBALS["GREEDY"]
quick_print("run: size", SIZE, "greedy", GREEDY)

set_world_size(SIZE)
CultivateGold(GREEDY)
