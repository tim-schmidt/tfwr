# Globals handed to simulate() as sim_globals. Each key becomes a global
# variable inside the simulated start file. The Sim*.py files set the
# values per run before calling simulate().
#   SIZE  - maze size (SimGold) or sector size (SimSector)
#   WORLD - farm size (SimSector, SimAnchor)
#   OX, OY - drone start tile (SimAnchor)
#   COMPANIONS, DRONES, TARGET - crop test switches (SimCrops)
SIM_GLOBALS = {"SIZE": 8, "WORLD": 16, "OX": 0, "OY": 0, "COMPANIONS": False, "DRONES": False, "TARGET": 20000}
