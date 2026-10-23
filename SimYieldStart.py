# Start file that simulate() loads for SimYield.py. Not run directly.
# WORLD, DISPATCH, REROLL, SHARE arrive through sim_globals. One board of
# trees with companion slots; prints the resources gained and the number
# of re-rolls, so yield per board is read straight off and the returned
# time is the cost.
from YieldCrops import CultivateYieldBoard

set_world_size(WORLD)
wood = num_items(Items.Wood)
hay = num_items(Items.Hay)
carrots = num_items(Items.Carrot)
rolls = CultivateYieldBoard(Entities.Tree, Entities.Grass, False, False, DISPATCH, REROLL, 1, SHARE)
quick_print("result world", WORLD, "dispatch", DISPATCH, "reroll", REROLL, "share", SHARE, "wood", num_items(Items.Wood) - wood, "hay", num_items(Items.Hay) - hay, "carrots", num_items(Items.Carrot) - carrots, "rerolls", rolls)
