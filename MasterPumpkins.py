# Live run for Pumpkin Master (20M Pumpkins in one minute): about 2.5
# minutes at 32 drones, roughly 5,000 Power. Execute directly in the game.
from Masters import SyncedPumpkins
start = num_items(Items.Pumpkin)
t0 = get_time()
SyncedPumpkins((Items.Pumpkin, start + 60000000))
t = get_time() - t0
gained = num_items(Items.Pumpkin) - start
quick_print("MasterPumpkins.py", gained, "in", t, "s, per minute", gained * 60 / t)
