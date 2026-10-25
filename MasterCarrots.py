# Live run for Carrot Master (200M Carrots in one minute): about 2.5
# minutes at 32 drones, roughly 5,000 Power. Execute directly in the game.
from Masters import ChaseCrops
start = num_items(Items.Carrot)
t0 = get_time()
ChaseCrops(Entities.Carrot, (Items.Carrot, start + 600000000))
t = get_time() - t0
gained = num_items(Items.Carrot) - start
quick_print("MasterCarrots.py", gained, "in", t, "s, per minute", gained * 60 / t)
