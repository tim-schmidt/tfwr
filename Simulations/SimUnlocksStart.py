# Probe start file for SimProbe.py. Not run directly.
# Prints the unlock levels the simulation started with, to learn how
# simulate() reads a partial unlock sequence.
quick_print("unlocks probe trees", num_unlocked(Unlocks.Trees), "grass", num_unlocked(Unlocks.Grass), "expand", num_unlocked(Unlocks.Expand), "speed", num_unlocked(Unlocks.Speed), "world", get_world_size(), "drones", max_drones())
