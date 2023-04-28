#!/usr/bin/env python3

from fractions import Fraction
from planegeometry.structures.points import Point
from planegeometry.structures.segments import Segment
from planegeometry.structures.triangles import Triangle
from planegeometry.structures.rectangles import Rectangle
from planegeometry.structures.polygons import Polygon
from planegeometry.structures.edges import Edge
from planegeometry.structures.planarmaps import PlanarMap

# 6  A7------A6--------------A5
#    |     / /\            / |
# 5  |   /  /  \         /   |
#    | /   /    \      /     |
# 4  A8   /      \   /       |
#    | \ /        \/         |
# 3  |   B3------B2          |
#    | / |       | \-------\ |
# 2  A9  |window |           A4
#    | \ |       | /------// |
# 1  |   B0------B1      /   |
#    | /   \   /    \  /     |
# 0  A0------A1------A2------A3
#    0   1   2   3   4   5   6

A0, A1, A2, A3 = Point(0,0), Point(2,0), Point(4,0), Point(6,0)
A4, A5, A6, A7 = Point(6,2), Point(6,6), Point(2,6), Point(0,6)
A8, A9 = Point(0,4), Point(0,2)
B0, B1, B2, B3 = Point(1,1), Point(3,1), Point(3,3), Point(1,3)

M1 = PlanarMap(Rectangle(A0, A5))
M2 = PlanarMap(Rectangle(B0, B2))
M3 = PlanarMap(Triangle(A0, A1, B0))
M4 = PlanarMap(Triangle(A1, A2, B1))
M5 = PlanarMap(Triangle(A2, A3, A4))
M6 = PlanarMap(Triangle(A0, B0, A9))
M7 = PlanarMap(Triangle(A9, B3, A8))
M8 = PlanarMap(Triangle(A8, A6, A7))
M9 = PlanarMap(Triangle(B3, B2, A6))
M10 = PlanarMap(Triangle(B1, B2, A4))
M11 = PlanarMap(Triangle(B2, A4, A5))
M12 = PlanarMap(Triangle(B2, A5, A6))

for m in (M3,M4,M5,M6,M7,M8,M9,M10,M11,M12,M2):
    M1 = M1.map_overlay(m)
assert M1.v() == 14
assert M1.e() == 28
assert M1.f() == 16
assert len(M1.edge_next) == 2 * M1.e()
assert len(M1.edge_prev) == 2 * M1.e()

print("Tests passed!")
M1.show()

print("points ...")
print(list(M1.iterpoints()))

print("\nfaces ...")
for face in M1.iterfaces():
    print(face)

# EOF
