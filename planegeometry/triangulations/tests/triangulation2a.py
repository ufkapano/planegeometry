#!/usr/bin/env python3

import random
import matplotlib.pyplot as plt
from fractions import Fraction
from planegeometry.structures.points import Point
from planegeometry.structures.segments import Segment
from planegeometry.triangulations.flipping import DelaunayFlipping
from planegeometry.triangulations.bowyerwatson import BowyerWatson
from planegeometry.triangulations.naive import DelaunayNaive

size = 10   # points in square [0,size]x[0,size]

def make_point_list(n):
    """Prepare a point list."""
    point_list = []
    for _ in range(n):
        point_list.append(Point(
            Fraction(size * random.random()).limit_denominator(),
            Fraction(size * random.random()).limit_denominator()))
    return point_list

point_list = make_point_list(10)

#algorithm = DelaunayNaive(point_list)
#algorithm = DelaunayFlipping(point_list)
algorithm = BowyerWatson(point_list)
algorithm.run()
G = algorithm.tc.to_graph()
#G.show()
#print ( list(G.iternodes()) )

for segment in G.iteredges():
    x = [segment.pt1.x, segment.pt2.x]
    y = [segment.pt1.y, segment.pt2.y]
    #plt.plot(x, y, 'k.-')
    plt.plot(x, y, 'k-')

x = [p.x for p in G.iternodes()]
y = [p.y for p in G.iternodes()]
plt.plot(x, y, 'bo')

plt.title("Delaunay triangulation")
plt.xlabel("x")
plt.ylabel("y")
plt.gca().set_aspect('equal')
plt.show()

# EOF
