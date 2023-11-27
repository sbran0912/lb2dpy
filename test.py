import lib2d as l2d
import math
import numpy

b = l2d.Box(200, 200, 40, 60)
print(b.vertices)
b.rotate(math.pi/2)
print(b.vertices)
