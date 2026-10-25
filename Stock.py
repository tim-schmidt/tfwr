# Live stock check before a Master run: what the save holds and what a
# planting costs at the current upgrade levels. Execute directly.
quick_print("world", get_world_size(), "drones", max_drones())
for item in [Items.Power, Items.Water, Items.Fertilizer, Items.Hay, Items.Wood, Items.Carrot, Items.Pumpkin]:
	quick_print(item, num_items(item))
for crop in [Entities.Tree, Entities.Carrot, Entities.Pumpkin]:
	quick_print("cost", crop, get_cost(crop))
