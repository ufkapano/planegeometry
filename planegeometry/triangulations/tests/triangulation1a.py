#!/usr/bin/python

import random
import matplotlib.pyplot as plt
from planegeometry.structures.points import Point
from planegeometry.structures.segments import Segment
from planegeometry.triangulations.flipping import DelaunayFlipping
from planegeometry.triangulations.bowyerwatson import BowyerWatson
from planegeometry.triangulations.naive import DelaunayNaive

point_list = [Point(-2, -2), Point(2, -2), Point(-2, 2), Point(2, 2),
    Point(-2, 0), Point(0, 1), Point(0, -2), Point(-1, 0), Point(1,0)]

#algorithm = DelaunayNaive(point_list)
#algorithm = DelaunayFlipping(point_list) # ValueError("collinear points")
algorithm = BowyerWatson(point_list)
algorithm.run()
G = algorithm.tc.to_graph()
#print ( "triangulation graph ..." )
#G.show()

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
plt.show()

# EOF
