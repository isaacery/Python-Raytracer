import numpy as np

class Scene():
    def __init__(self,objects,lights):
        self.objects = objects
        self.lights = lights
        # self.eye, self.forward, self.right, self.up = eye, forward, right, up
        # self.bounces = bounces

""" eye=np.array([0,0,0]),
    forward = np.array([0,0,-1]),
    right = np.array([1,0,0]),
    up = np.array([0,1,0]), bounces = 4 """
