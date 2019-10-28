import numpy as np
from vectors import *

class Ray:
    def __init__(self,origin,direction,bounces):
        self.origin = origin
        self.direction = normalize(direction)
        self.bounces = bounces
