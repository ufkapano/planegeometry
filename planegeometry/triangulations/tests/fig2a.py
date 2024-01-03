#!/usr/bin/env python3

import random
import matplotlib.pyplot as plt
from planegeometry.structures.points import Point
from planegeometry.structures.polygons import Polygon
from planegeometry.triangulations.ymonotonetc import YMonotoneTriangulationTC as Triangulation

# y-monotoniczny slabo
point_list = [Point(1, 0), Point(2, 1), Point(3, 1.1),
    Point(3, 2), Point(2, 2), Point(2, 3), Point(3, 3.1),
    Point(3, 4), Point(2, 4), Point(1, 5), Point(0, 2)]
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
