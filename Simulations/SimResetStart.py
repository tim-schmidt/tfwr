# Start file that simulate() loads for SimReset.py. Not run directly.
# VARIANT arrives through sim_globals and picks a route variant (Route.py).
from Route import *

run(buildRoute(VARIANT))
