# Leaderboard route A/B in one simulation call: no unlocks, no items. The
# game drifts between calls but repeats exactly within one, so every variant
# runs here back to back and only the differences count. The leaderboard
# posts the average of about three repeats with random seeds, and identical
# code spreads about 140 s across seeds, so each variant runs on SEEDS and
# the mean is the score. Edit VARIANTS (see Route.py buildRoute). Run this
# file directly in the game.
VARIANTS = [0]
SEEDS = [1, 2, 3]
means = []
for v in VARIANTS:
	total = 0
	for seed in SEEDS:
		t = simulate("SimResetStart", [], {}, {"VARIANT": v}, seed, 256)
		total += t
		quick_print("variant", v, "seed", seed, "sim time", t)
	means.append(total / len(SEEDS))
	quick_print("variant", v, "mean", means[len(means) - 1])
quick_print("variants", VARIANTS, "means", means)
