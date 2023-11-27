import numpy as np
import numba
import math
import pyray as pr

#@numba.njit(numba.float64[:](numba.float64, numba.float64))
def createVector(x, y):
    return np.array([x, y])

#@numba.njit(numba.float64(numba.float64[:], numba.float64[:]))
def dot(v1, v2):
  return v1[0] * v2[0] + v1[1] * v2[1]

#@numba.njit(numba.float64(numba.float64[:]))
def magsq(v):
    return v[0] * v[0] + v[1] * v[1]

#@numba.njit(numba.float64(numba.float64[:]))
def mag(v):
    return math.sqrt(magsq(v))

#@numba.njit(numba.float64[:](numba.float64[:]))
def norm(v):
    size = mag(v)
    if size != 0:
        return (v / size)
    else:
        return v

#@numba.njit(numba.float64[:](numba.float64[:], numba.float64))
def limit(v, max):
    msq = magsq(v)
    if msq > max * max:
        return norm(v) * max
    else:
        return v

#@numba.njit(numba.float64(numba.float64[:], numba.float64[:]))
def cross2d(v1, v2):
  return v1[0] * v2[1] - v1[1] * v2[0];

#@numba.njit(numba.float64[:](numba.float64[:]))
def perp(v):
    return np.array([-v[1], v[0]])

# Point of intersection between line a and line b
#@numba.njit
def intersect(start_a, end_a, start_b, end_b):
    line_a = end_a - start_a
    line_b = end_b - start_b
    cross1 = cross2d(line_a, line_b)
    cross2 = cross2d(line_b, line_a)
    if cross1 != 0:
        s = cross2d(start_b - start_a, line_b) / cross1
        u = cross2d(start_a - start_b, line_a) / cross2
        if s > 0 and s < 1 and u > 0 and u < 1:
            return start_a + line_a * s
        else:
            return None

# Minimum distance between point p and line a
#@numba.njit
def minDist(p, start_a, end_a):
    line_a = end_a - start_a
    start_a_to_p = p - start_a
    mag_line_a = mag(line_a)

    #Scalarprojection from line(start_a_to_p) to line_a
    line_a_norm = norm(line_a)
    #sp = np.dot(line_a_norm, start_a_to_p)
    sp = dot(line_a_norm, start_a_to_p)
    #Scalarprojection in magnitude of line_a?
    if sp > 0 and sp <= mag_line_a:
        return mag(start_a_to_p - line_a_norm * sp)
    else:
        return None
    
#@numba.experimental.jitclass([('vertices', numba.float64[:,:])])
class Box:
    def __init__(self, posx, posy, w, h):
        # 4 Koordinaten der Box. Je Spalte ein Eckpunkt
        # Zeile 1 = x
        # Zeile 2 = y
        # Zeile 3 = Konstante für Matrizenkalkulation

        self.vertices = np.array(
            [[posx, posx + w, posx + w, posx],
            [posy, posy, posy + h, posy + h],
            [1, 1, 1, 1]],
            dtype=np.float64
        )
        self.location = np.array(
            [[posx + w/2], 
             [posy + h/2],
             [1]]
        )
        pass

    def rotate(self, angel):
        m_rotate = np.array(
            [[math.cos(angel), -math.sin(angel), 0],
            [math.sin(angel), math.cos(angel), 0],
            [0, 0, 1]]
        )
        m_transform_center = np.array(
            [[1, 0, -self.location[0,0]],
            [0, 1, -self.location[1,0]],
            [0, 0, 1]]
        )

        m_transform_center_back = np.array(
            [[1, 0, self.location[0,0]],
            [0, 1, self.location[1,0]],
            [0, 0, 1]]
        )
        pos_center = np.matmul(m_transform_center, self.vertices)
        pos_center_rotated = np.matmul(m_rotate, pos_center)
        self.vertices = np.matmul(m_transform_center_back, pos_center_rotated)
        pass


def draw_box(box: Box, color ):
    vertices = box.vertices
    for i in range(3):
        pr.draw_line_ex(pr.Vector2(vertices[0,i], vertices[1,i]), pr.Vector2(vertices[0, i+1], vertices[1, i+1]), 5, color)
        pass
    pr.draw_line_ex(pr.Vector2(vertices[0,3], vertices[1,3]), pr.Vector2(vertices[0, 0], vertices[1, 0]), 5, color)
    pass
