#!/usr/bin/env python3

import random
import matplotlib.pyplot as plt
from planegeometry.structures.points import Point
from planegeometry.structures.polygons import Polygon
from planegeometry.triangulations.fanpm import FanTriangulationPlanarMap as Triangulation
#from triangulation2 import YMonotoneTriangulationPlanarMap as Triangulation

point_list = []
# wielokat wypukly z degeneracja, y-monotoniczny
n = 11
n1 = n // 2
n2 = n - n1
# Dla n nieparzystego mamy n1 < n2.
# Ten wielokat mozna wykorzystac do testow wydajnosciowych.

for i in range(n2):
    point_list.append(Point(1, i))
for i in range(n1):
    point_list.append(Point(0, n2-i))

assert len(point_list) == n
polygon = Polygon(*point_list)

algorithm = Triangulation(polygon)
algorithm.run()
G = algorithm.planar_map
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
#plt.gca().set_aspect('equal')
plt.show()

# EOF
