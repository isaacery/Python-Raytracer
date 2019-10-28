import math
from intersection import Intersection
import ray
import numpy as np
from vectors import *

class Sphere:
    def __init__(self,center,radius,colour,shininess):
        self.center = center
        self.radius = radius
        self.colour = colour
        self.shininess = shininess

    def intersect(self, ray):
        intersection = None
        p = self.center - ray.origin
        dirDotP = np.dot(ray.direction,p)
        '''r_2 = self.radius**2
        inside = np.dot(p,p) < r_2
        t_c = np.dot(ray.direction,p) / magnitude(ray.direction)
        if not inside and t_c < 0:
            return None
        a = ray.origin + t_c * ray.direction - self.center
        d_2 = np.dot(a,a)
        b = r_2 - d_2
        if not inside and b <= 0:
            return None
        t_o = math.sqrt(b) / magnitude(ray.direction)
        if inside:
            return Intersection(ray, self, t_c + t_o)
        else:
            return Intersection(ray, self, t_c - t_o)'''
        diff = np.dot(p,p) - self.radius**2
        n_2 = dirDotP**2 - diff
        if n_2 >= 0:
            n = math.sqrt(n_2)
            t0 = (dirDotP - n)
            t1 = (dirDotP + n)
            #if diff < 0: # if inside sphere
            #    intersection = Intersection(ray, self, t1)
            if t0 < t1:
                intersection = Intersection(ray, self, t0)
            else:
                intersection = Intersection(ray, self, t1)
        return intersection

    def normal(self,point):
        return normalize(point - self.center)
