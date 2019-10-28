import numpy as np

def normalize(v):
    return v / magnitude(v)

def magnitude(v):
    return(np.linalg.norm(v))
