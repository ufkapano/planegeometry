#!/usr/bin/env python3

import random
import matplotlib.pyplot as plt
from planegeometry.structures.points import Point
from planegeometry.structures.polygons import Polygon
from planegeometry.triangulations.ymonotonepm import YMonotoneTriangulationPM as Triangulation

# y-monotoniczny
point_list = [Point(0, 0), Point(5, 1), Point(5, 2),
    Point(3, 3), Point(2, 4), Point(1, 6), Point(5, 7),
    Point(4, 12), Point(2, 13), Point(3, 11), Point(3, 10),
    Point(2, 9), Point(0, 8)]
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
#plt.axes().set_aspect('equal', 'datalim') # DeprecationWarning
#plt.axes().set_aspect('equal') # DeprecationWarning
plt.gca().set_aspect('equal')
plt.show()

# EOF
