# Early hay: stay on one tile versus harvest and move, by Speed level, with
# and without the Plant unlock, on 1x1 and 3x3. Each case gathers 200 hay;
# the time is the cost. Run this file directly in the game.
items = {Items.Hay: 1000000, Items.Wood: 1000000}
globs = {"SPEED": 0, "EXPAND": 0, "PLANT": 0, "MODE": 0}
for plant in [0, 1]:
	for expand in [0, 2]:
		for speed in [0, 1, 2, 3]:
			for mode in [0, 1]:
				globs["SPEED"] = speed
				globs["EXPAND"] = expand
				globs["PLANT"] = plant
				globs["MODE"] = mode
				t = simulate("SimHayStart", [], items, globs, 1, 256)
				quick_print("plant", plant, "expand", expand, "speed", speed, "mode", mode, "time", t, "s per hay", t / 200)
