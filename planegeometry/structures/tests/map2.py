#!/usr/bin/env python3

from fractions import Fraction
from planegeometry.structures.points import Point
from planegeometry.structures.segments import Segment
from planegeometry.structures.triangles import Triangle
from planegeometry.structures.rectangles import Rectangle
from planegeometry.structures.polygons import Polygon
from planegeometry.structures.edges import Edge
from planegeometry.structures.planarmaps import PlanarMap
import matplotlib.pyplot as plt

# o---o---o---o   s = 4
# |   |   |   |
# o---o---o---o
# |   |   |   |
# o---o---o---o
# |   |   |   |
# o---o---o---o

s = 5
assert s > 2

M1 = PlanarMap(Rectangle(Point(0,0), Point(s-1,s-1)))
for i in range(1, s-1):
    M2 = PlanarMap(Segment(Point(i,0), Point(i,s-1)))
    M1 = M1.map_overlay(M2)
    M2 = PlanarMap(Segment(Point(0,i), Point(s-1,i)))
    M1 = M1.map_overlay(M2)
assert M1.v() == s*s
assert M1.e() == 2*s*(s-1)
assert M1.f() == (s-1)*(s-1)+1
assert len(M1.edge_next) == 2 * M1.e()
assert len(M1.edge_prev) == 2 * M1.e()

print("Tests passed!")
M1.show()

print("points ...")
print(list(M1.iterpoints()))

print("\nfaces ...")
print(list(M1.face2edge))
for face in M1.iterfaces():
    print(face)

# Plotting planar maps.
for segment in M1.itersegments():
    x = [segment.pt1.x, segment.pt2.x]
    y = [segment.pt1.y, segment.pt2.y]
    plt.plot(x, y, 'k.-')

plt.title("Mesh")
plt.xlabel("x")
plt.ylabel("y")
plt.gca().set_aspect('equal')
plt.show()

# EOF
