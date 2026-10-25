# Live run for Wood Master (1B Wood in one minute): about 2.5
# minutes at 32 drones, roughly 5,000 Power. Execute directly in the game.
from Masters import ChaseCrops
start = num_items(Items.Wood)
t0 = get_time()
ChaseCrops(Entities.Tree, (Items.Wood, start + 3000000000))
t = get_time() - t0
gained = num_items(Items.Wood) - start
quick_print("MasterWood.py", gained, "in", t, "s, per minute", gained * 60 / t)
