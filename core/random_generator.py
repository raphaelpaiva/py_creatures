"""
A default random number generator. Use this if you want randoms consistent with the simulation.

Usage: `from core.random_generator import generator`

Used by the simulation to set a single random seed in order to provide
consistent generation across simulation instances.
"""
import random

generator = random.Random()

