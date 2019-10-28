import numpy as np
from ray import Ray
from sphere import Sphere
from plane import Plane
from vectors import *
from light import Sun, Bulb

EPSILON = 0.00000001

# store pixels
pixels = []

eye = np.array([0,0,0])
forward = np.array([0,0,-1])
right = np.array([1,0,0])
up = np.array([0,1,0])
bounces = 4

def drawScene(w,h,scene,init):
    # loop through raster
    eye,forward,right,up,bounces = init
    for x in range(w):
        for y in range(h):
            s_x = (2*x - w) / max(w,h) # scaling factor for x
            s_y = (h - 2*y) / max(w,h) # scaling factor for y
            # ray direction is forward, with x and y scaled based on
            # the pixel we are processing
            direction = forward + s_x * right + s_y * up
            # cast ray from eye through pixel (x,y) of raster
            ray = Ray(eye,direction,bounces)

            c = rayTrace(ray,scene)

            if c is not None:
                pixels.append(np.append(np.array((x,y)),c))
    return pixels

def rayTrace(ray,scene): # returns colour at intersection
    nearest = calculateIntersection(ray,scene.objects)
    if nearest is not None:
        lighting = calculateLighting(nearest,scene)
        if nearest.object.shininess > 0:
            if ray.bounces > 0:
                return bounce_ray(ray,nearest,scene,lighting)
        else:
            return lighting
    else:
        return None

def bounce_ray(ray,nearest,scene,lighting):
    s = nearest.object.shininess
    dir = ray.direction
    bounce_origin = nearest.t * dir
    n = getNormal(nearest.object,bounce_origin)
    bounce_dir = dir - 2 * np.dot(n,dir) * n
    bounce_ray = Ray(bounce_origin, bounce_dir, ray.bounces-1)
    bounced = rayTrace(bounce_ray,scene)
    if bounced is not None:
        return s * bounced  + (1-s) * lighting
    else:
        return (1-s) * lighting

def calculateLighting(i,scene):
    obj = i.object
    rgb = np.array((0.0,0.0,0.0))
    # calculate point of intersection
    p = i.ray.origin + i.ray.direction * i.t
    #print(scene.lights)
    for light in scene.lights:
        c = 0
        # elementwise multiplication of light and object colour
        colour = np.multiply(obj.colour,light.colour)
        # calculate normal vector
        # calculate vector from point to lightsource
        # TODO: this is bad
        d = 1
        if type(light) == Sun:
            l = light.direction
        elif type(light) == Bulb:
            v = light.position - p
            d = magnitude(v)
            l = normalize(v)
        # cast ray from slightly above object surface to avoid self intersection
        shadow_ray = Ray(p + EPSILON * l,l,0)
        if calculateIntersection(shadow_ray,scene.objects) is None: # if no shadow
            # calculate lambert intensitiy (i.e. cos(theta))
            # can ignore denomenator since vectors are normalized
            n = getNormal(obj,p)
            #if np.dot(i.ray.direction,n) > 0:
            #    n *= -1
            dot = np.dot(l,n)
            if dot >= 0:
                c = dot / d**2
            rgb += c * colour
    return rgb

def calculateIntersection(ray,objects):
            # find intersection with smallest t that is not behind us
            # TODO: what about objects between eye and raster?
            nearest = None
            # iterate through objects
            for obj in objects:
                intersection = obj.intersect(ray)
                # TODO: this is ugly
                if intersection is not None:
                    if nearest is not None:
                        if intersection.t < nearest.t and intersection.t > 0:
                            nearest = intersection
                    elif intersection.t > 0:
                        nearest = intersection
            return nearest

def getNormal(object,p):
    if type(object) == Sphere:
        return object.normal(p)
    elif type(object) == Plane:
        return object.normal
