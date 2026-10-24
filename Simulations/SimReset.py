# Full leaderboard route in a simulation: no unlocks, no items, seed 1.
# Prints the run time in seconds. Run this file directly in the game.
t = simulate("FastestReset", [], {}, {}, 1, 256)
quick_print("FastestReset sim time", t)
