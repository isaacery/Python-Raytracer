import numpy as np
from intersection import Intersection
from vectors import *

class Plane:
    def __init__(self,a,b,c,d,colour,shininess):
        self.normal = normalize(np.array((a,b,c)))
        self.d = d
        self.colour = colour
        self.shininess = shininess

    def intersect(self,ray):
        o = ray.origin
        dir = ray.direction
        n = self.normal
        d = self.d
        if np.dot(dir,n) == 0:
            return None
        t = -(np.dot(o,n) + d) / np.dot(dir,n)
        return Intersection(ray,self,t)
