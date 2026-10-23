# Start file that simulate() loads for SimYield.py. Not run directly.
# WORLD, DISPATCH, REROLL, SHARE, SLOTS arrive through sim_globals. SLOTS
# is 0 for mixed slots, 1 grass, 2 bush, 3 carrot. One board of trees with
# companion slots; prints the resources gained and the number of
# re-rolls, so yield per board is read straight off and the returned time
# is the cost.
from YieldCrops import CultivateYieldBoard

set_world_size(WORLD)
slots = None
if SLOTS == 1:
	slots = Entities.Grass
elif SLOTS == 2:
	slots = Entities.Bush
elif SLOTS == 3:
	slots = Entities.Carrot
wood = num_items(Items.Wood)
hay = num_items(Items.Hay)
carrots = num_items(Items.Carrot)
rolls = CultivateYieldBoard(Entities.Tree, Entities.Grass, False, False, DISPATCH, REROLL, 1, SHARE, slots)
quick_print("result world", WORLD, "share", SHARE, "slots", SLOTS, "wood", num_items(Items.Wood) - wood, "hay", num_items(Items.Hay) - hay, "carrots", num_items(Items.Carrot) - carrots, "rerolls", rolls)
