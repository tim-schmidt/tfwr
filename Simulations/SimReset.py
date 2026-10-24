# Leaderboard route A/B in one simulation call: no unlocks, no items, seed 1.
# The game drifts between sessions but repeats exactly within one, so both
# variants run back to back here and only their difference counts. Edit
# VARIANTS (see Route.py buildRoute). Run this file directly in the game.
VARIANTS = [0, 1]
times = []
for v in VARIANTS:
	t = simulate("SimResetStart", [], {}, {"VARIANT": v}, 1, 256)
	times.append(t)
	quick_print("variant", v, "sim time", t)
quick_print("variants", VARIANTS, "times", times)
