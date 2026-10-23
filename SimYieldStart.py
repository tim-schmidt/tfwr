# Start file that simulate() loads for SimYield.py. Not run directly.
# WORLD, DISPATCH, REROLL arrive through sim_globals. One board of trees
# and grass; prints the resources gained, so yield per board is read
# straight off and the returned time is the cost.
from YieldCrops import CultivateYieldBoard

set_world_size(WORLD)
wood = num_items(Items.Wood)
hay = num_items(Items.Hay)
carrots = num_items(Items.Carrot)
CultivateYieldBoard(Entities.Tree, Entities.Grass, False, False, DISPATCH, REROLL, 1)
quick_print("result world", WORLD, "dispatch", DISPATCH, "reroll", REROLL, "wood", num_items(Items.Wood) - wood, "hay", num_items(Items.Hay) - hay, "carrots", num_items(Items.Carrot) - carrots)
