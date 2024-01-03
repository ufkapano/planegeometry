#!/usr/bin/env python3

import random
import matplotlib.pyplot as plt
from planegeometry.structures.points import Point
from planegeometry.structures.polygons import Polygon
from planegeometry.triangulations.fantc import FanTriangulationTC as Triangulation
#from triangulation1 import YMonotoneTriangulation as Triangulation

# 6|. . . o
# 5|. o . . . o     najprostszy wielokat wypukly bez degeneracji
# 4|. . . . . . .  x-monotoniczny i y-monotoniczny
# 3|o . . . . . o
# 2|. . . . . . .
# 1|. o . . . o
# 0|. . . o
#  --------------
#   0 1 2 3 4 5 6

#point_list = [Point(3, 0), Point(5, 1), Point(6, 3), Point(5, 5),
#    Point(3, 6), Point(1, 5), Point(0, 3), Point(1, 1)]
#polygon = Polygon(*point_list)

coordinates = [3, 0, 5, 1, 6, 3, 5, 5, 3, 6, 1, 5, 0, 3, 1, 1]
polygon = Polygon(*coordinates)

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
