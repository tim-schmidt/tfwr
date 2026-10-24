# Rule probes: companion preferences per crop and the identical-neighbour
# growth penalty per crop. All unlocks, items stocked. Run directly in the game.
items = {Items.Hay: 1000000, Items.Wood: 1000000, Items.Carrot: 1000000, Items.Pumpkin: 1000000, Items.Power: 1000000}
simulate("SimRulesStart", Unlocks, items, {}, 1, 256)
