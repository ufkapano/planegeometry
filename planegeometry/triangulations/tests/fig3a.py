#!/usr/bin/env python3

import random
import matplotlib.pyplot as plt
from planegeometry.structures.points import Point
from planegeometry.structures.polygons import Polygon
from planegeometry.triangulations.fantc import FanTriangulationTC as Triangulation
#from triangulation1 import YMonotoneTriangulation as Triangulation

point_list = []
# wielokat wypukly z degeneracja
# x-monotoniczny i y-monotoniczny
#a, b = 6, 10   # duzy pochylony prostokat a x b
#a, b = 3, 5   # duzy pochylony prostokat a x b
a, b = 3, 3   # duzy pochylony prostokat a x b
#a, b = 2, 2   # duzy pochylony prostokat a x b
#a, b = 1, 2   # duzy pochylony prostokat a x b
#a, b = 2, 1   # duzy pochylony prostokat a x b
#a, b = 1, 1   # duzy pochylony prostokat a x b
x, y = 0, 0
for _ in range(a):   # / bok a
    x, y = x + 1, y + 1
    point_list.append(Point(x, y))
for _ in range(b):   # \ bok b
    x, y = x - 1, y + 1
    point_list.append(Point(x, y))
for _ in range(a):   # / bok a
    x, y = x - 1, y - 1
    point_list.append(Point(x, y))
for _ in range(b):   # \ bok b
    x, y = x + 1, y - 1
    point_list.append(Point(x, y))
assert len(point_list) == 2*(a+b)

polygon = Polygon(*point_list)

algorithm = Triangulation(polygon)
algorithm.run()
G = algorithm.tc.to_graph()
#G.show()

for segment in G.iteredges():
    x = [segment.pt1.x, segment.pt2.x]
    y = [segment.pt1.y, segment.pt2.y]
    #plt.plot(x, y, 'k.-')
    plt.plot(x, y, 'k-')

x = [p.x for p in G.iternodes()]
y = [p.y for p in G.iternodes()]
plt.plot(x, y, 'bo')

plt.title("Triangulation")
plt.xlabel("x")
plt.ylabel("y")
plt.gca().set_aspect('equal')
plt.show()

# EOF
