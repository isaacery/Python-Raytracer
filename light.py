import numpy as np
from vectors import *

class Sun:
    def __init__(self,direction,colour):
        self.direction = normalize(direction)
        self.colour = colour

class Bulb:
    def __init__(self,position,colour):
        self.position = position
        self.colour = colour
