import numpy as np

def compress_color(c): # takes a colour value (r,g,b,a) and returns them rescaled to the range [0,1]
    f = np.vectorize(lambda x: x/255)
    g = np.vectorize(lambda x: 255 if x > 255 else x) # clamp colour
    h = np.vectorize(lambda x: 0 if x < 0 else x) # clamp colour
    return f(g(h(c)))

def expand_color(c): # takes a colour value (r,g,b,a) and returns them rescaled to the range [0,255]
    f = np.vectorize(lambda x: int(x*255))
    g = np.vectorize(lambda x: 255 if x > 255 else x) # clamp colour
    h = np.vectorize(lambda x: 0 if x < 0 else x) # clamp colour
    return g(h(f(c)))

def alpha_composite_over(c1,c2): # takes two colour values and applies c1 over c2
    r_1,g_1,b_1,a_1 = c1
    r_2,g_2,b_2,a_2 = c2
    a_o = a_1 + (a_2 * (1 - a_1)) # alpha_o = alpha_c1 + alpha_c2 (1 - alpha_c1)
    if (a_o == 0):
        return np.array((0,0,0,0))
    c = a_1/a_o
    d = 1 - c
    r_o = c*r_1 + d*r_2
    g_o = c*g_1 + d*g_2
    b_o = c*b_1 + d*b_2
    return np.array((r_o,g_o,b_o,a_o))

def set_colour(pixels,colour):
    return [np.concatenate((p,colour)) for p in pixels]

def hex_to_rgb(c):
    return compress_color(np.array(int(c[1:3], 16),int(c[3:5], 16),int(c[5:7], 16)))

def hex_to_rgba(c):
    return compress_color(np.array(int(c[1:3], 16),int(c[3:5], 16),int(c[5:7], 16),int(c[7:9], 16)))
