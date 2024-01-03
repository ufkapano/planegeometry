#!/usr/bin/env python3

import random
import matplotlib.pyplot as plt
from planegeometry.structures.points import Point
from planegeometry.structures.polygons import Polygon
from planegeometry.triangulations.fanpm import FanTriangulationPM as Triangulation
#from triangulation2 import YMonotoneTriangulationPlanarMap as Triangulation

# 6|. . . o
# 5|. . / | . . .  trojkat z dodatkami
# 4|. o . | . . .  y-monotoniczny, jezeli dam wszystkie punkty
# 3|o . . o . . .
# 2|. o . | . . .
# 1|. . o | . . .
# 0|. . . o
#  --------------
#   0 1 2 3 4 5 6
#point_list = [Point(3, 0), Point(3, 6), Point(0, 3)] # jeden trojkat, OK

# Trojkat, ale 4 punkty.
#point_list = [Point(3, 0), Point(3, 3), Point(3, 6), Point(0, 3)] # OK
#point_list = [Point(3, 0), Point(3, 6), Point(1, 4), Point(0, 3)] # OK

# Patologia
#point_list = [Point(3, 0), Point(3, 6), Point(0, 3), Point(1, 2)]

# Patologia
#point_list = [Point(3, 0), Point(3, 6), Point(0, 3), Point(1, 2), Point(2, 1)]

# Trojkat, ale punkty na dwoch bokach. OK
#point_list = [Point(3, 0), Point(3, 6), Point(1, 4), Point(0, 3), Point(1, 2)]
#point_list = [Point(3, 0), Point(3, 3), Point(3, 6), Point(0, 3), Point(1, 2)]
#point_list = [Point(3, 0), Point(3, 3), Point(3, 6), Point(1, 4), Point(0, 3)]

# Trojkat, ale punkty na kazdym boku.
point_list = [Point(3, 0), Point(3, 3), Point(3, 6), Point(1, 4), Point(0, 3), Point(1, 2)]
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
plt.gca().set_aspect('equal')
plt.show()

# EOF
