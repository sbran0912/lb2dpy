import numpy
import numba
import math

@numba.njit(numba.float61[:](numba.float64, numba.float64))
def createVector(x, y):
    return numpy.array[x, y]

@numba.njit(numba.float64(numba.float64[:], numba.float64[:]))
def dot(v1, v2):
  return v1[0] * v2[0] + v1[1] * v2[1]

@numba.njit(numba.float64(numba.float64[:]))
def magsq(v):
    return v[0] * v[0] + v[1] * v[1]

@numba.njit(numba.float64(numba.float64[:]))
def mag(v):
    return math.sqrt(magsq(v))

@numba.njit(numba.float64[:](numba.float64[:]))
def norm(v):
    size = mag(v)
    if size != 0:
        return (v / size)
    else:
        return v

@numba.njit(numba.float64[:](numba.float64[:], numba.float64))
def limit(v, max):
    msq = magsq(v)
    if msq > max * max:
        return norm(v) * max
    else:
        return v

@numba.njit(numba.float64(numba.float64[:], numba.float64[:]))
def cross2d(v1, v2):
  return v1[0] * v2[1] - v1[1] * v2[0];

@numba.njit(numba.float64[:](numba.float64[:]))
def perp(v):
    return numpy.array([-v[1], v[0]])

# Point of intersection between line a and line b
# @numba.njit(numba.optional(numba.float64[:])(numba.float64[:], numba.float64[:], numba.float64[:], numba.float64[:]))
@numba.njit
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
# @numba.njit(numba.optional(numba.float64)(numba.float64[:], numba.float64[:], numba.float64[:]))
@numba.njit
def minDist(p, start_a, end_a):
    line_a = end_a - start_a
    start_a_to_p = p - start_a
    mag_line_a = mag(line_a)

    #Scalarprojection from line(start_a_to_p) to line_a
    line_a_norm = norm(line_a)
    #sp = numpy.dot(line_a_norm, start_a_to_p)
    sp = dot(line_a_norm, start_a_to_p)
    #Scalarprojection in magnitude of line_a?
    if sp > 0 and sp <= mag_line_a:
        return mag(start_a_to_p - line_a_norm * sp)
    else:
        return None
    
@numba.experimental.jitclass([('vertices', numba.float64[:,:])])
class Box:
    def __init__(self, posx, posy, w, h):
        # 4 Koordinaten der Box. Je Spalte ein Eckpunkt
        # Zeile 1 = x
        # Zeile 2 = y
        # Zeile 3 = Konstante für Matrizenkalkulation

        self.vertices = numpy.array(
            [[posx, posx + w, posx + w, posx],
            [posy, posy, posy + h, posy + h],
            [1, 1, 1, 1]],
            dtype=numpy.float64
        )
        pass