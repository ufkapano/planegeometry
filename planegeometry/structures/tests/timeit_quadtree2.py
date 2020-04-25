#!/usr/bin/python

import timeit
import random
from planegeometry.structures.points import Point
from planegeometry.structures.rectangles import Rectangle
from planegeometry.structures.quadtree import QuadTree

N = 100
quadtree = QuadTree(Rectangle(0, 0, 1, 1))
for i in range(N):
    pt = Point(random.random(), random.random())
    quadtree.insert(pt)
point1 = Point(random.random(), random.random())
print ( "height {}".format(quadtree.height()) )

print ( "Testing QuadTree.insert() ..." )
t1 = timeit.Timer(lambda: quadtree.insert(point1))
print ( "{} {}".format(N, t1.timeit(1)) )   # single run

# EOF
