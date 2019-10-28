import sys
import numpy as np
from scene import Scene
from raytrace import drawScene
import intersection
from sphere import Sphere
from light import Sun, Bulb
import vectors
from colour import *
from plane import Plane
# from dda import dda
# from tri import tri, fann, stripn
from vectors import *
from PIL import Image


# consulted https://docs.python.org/3/howto/sorting.html

def get_vertex(i):
    if i > 0:
        return vtxs[i-1]
    elif i < 0:
        return vtxs[i]

def draw(pixels):
    for pixel in pixels:
        x,y = [int(v) for v in pixel[0:2]]
        c = pixel[2:]
        r,g,b = expand_color(c)
        #print((x,y,r,g,b,a))
        putpixel((x,y),(r,g,b,255))

# read and validate argument
if len(sys.argv) < 2:
    print("Please provide a file name")
else:
    path = sys.argv[1]

# read from file
f = open(path, 'r')
f_type, width, height, file_name = f.readline().split()
width = int(width)
height = int(height)
commands = [c for c in f.readlines() if not c.isspace()]
f.close()

# create image
img = Image.new("RGBA", (width,height), (0,0,0,0))
putpixel = img.im.putpixel
getpixel = img.im.getpixel

# initialise list of vertexes referenced through commands
vtxs = []

# intiialise current_colour as pure white
current_colour = np.array((1.0,1.0,1.0))

# initialise shininess as 0
shininess = 0

# set defaults
eye = np.array([0,0,0])
forward = np.array([0,0,-1])
right = np.array([1,0,0])
up = np.array([0,1,0])
bounces = 4

# initialise scene
scene = Scene([],[])

# loop through and execute commands
for command in commands:
    cmd_id = command.split()[0]
    params = command.split()[1:]
    if cmd_id == "sphere":
        x,y,z,r = [float(p) for p in params]
        pos = np.array((x,y,z))
        s = Sphere(pos,r,current_colour,shininess)
        scene.objects.append(s)
    elif cmd_id == "sun":
        direction = np.array([float(p) for p in params])
        s = Sun(direction,current_colour)
        scene.lights.append(s)
    elif cmd_id == "bulb":
        position = np.array([float(p) for p in params])
        b = Bulb(position,current_colour)
        scene.lights.append(b)
    elif cmd_id == "color":
        current_colour = np.array([float(p) for p in params])
    elif cmd_id == "plane":
        a,b,c,d = [float(p) for p in params]
        p = Plane(a,b,c,d,current_colour,shininess)
        scene.objects.append(p)
    elif cmd_id == "shininess":
        shininess = float(params[0])
    elif cmd_id == "eye":
        eye = np.array([float(p) for p in params])
    elif cmd_id == "forward":
        forward = np.array([float(p) for p in params])
        p = np.cross(forward,right)
        up = np.cross(p,forward)
        right = np.cross(forward,up)
        print(np.dot(forward,right))
        print(np.dot(forward,up))
        print(np.dot(up,right))
        print(right)
        print(up)
    """if cmd_id == "xyz":
        x,y,z = [float(p) for p in params]
        vtxs.append(np.array((x,y,z,1)))
    elif cmd_id == "xyzw":
        x,y,z,w = [float(p) for p in params]
        vtxs.append(np.array((x,y,z,w)))
    elif cmd_id == "color":
        r,g,b = map(float, params)
        current_colour = np.array((r,g,b,1))
    elif cmd_id == "trif":
        i_1,i_2,i_3 = map(int, params)
        vertices = [get_vertex(i_1),get_vertex(i_2),get_vertex(i_3)]
        v1,v2,v3 = process_vertices(vertices)
        positions = tri(v1,v2,v3)
        pixels = set_colour(positions,current_colour)
        draw(pixels)
    elif cmd_id == "loadmv":
        params = to_float(params)
        model_view = load_matrix_4x4(params)
    elif cmd_id == "loadp":
        params = to_float(params)
        projection = load_matrix_4x4(params)
    elif cmd_id == "frustum":
        l,r,b,t,n,f = to_float(params)
        a = (r + l) / (r - l)
        b = (t + b) / (t - b)
        c = -1 * (f + n) / (f - n)
        d = -2 * (f * n) / (f - n)
        x = 2 * n / (r-l)
        y = 2 * n / (t-b)
        values = [x,0,a,0,0,y,b,0,0,0,c,d,0,0,-1,0]
        projection = load_matrix_4x4(values)"""

# draw image
init = (eye,forward,right,up,bounces)
draw(drawScene(width,height,scene,init))

# save Image
img.save(file_name)
