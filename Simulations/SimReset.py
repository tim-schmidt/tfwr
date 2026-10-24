# Full leaderboard route in a simulation: no unlocks, no items. Runs seed 1
# three times and prints each time and the mean, since identical code has
# shown about 100 s of run-to-run noise. Run this file directly in the game.
times = []
for seed in [1, 1, 1]:
	t = simulate("FastestReset", [], {}, {}, seed, 256)
	times.append(t)
	quick_print("FastestReset sim time", t)
total = 0
for t in times:
	total += t
quick_print("FastestReset mean of", len(times), "runs", total / len(times), "times", times)
