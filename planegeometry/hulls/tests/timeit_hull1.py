#!/usr/bin/env python3

import timeit
import random
from fractions import Fraction
from planegeometry.structures.points import Point
from planegeometry.hulls.graham import GrahamScan1
from planegeometry.hulls.graham import GrahamScan2
from planegeometry.hulls.jarvis import JarvisMarch
from planegeometry.hulls.quickhull import QuickHull

#   x o x      s = 5
# x o o o x
# o o o o o
# x o o o x
#   x o x

s = 10
# s =    7,  10,  20,  30,   70,   100,   200,   300,    700, 1e3
# s*s = 49, 100, 400, 900, 4900, 10000, 40000, 90000, 490000, 1e6
point_list = []
A = set([0, s-1])

for i in range(s):
    for j in range(s):
        if (i in A) and (j in A): # remove corners
            continue
        point_list.append(Point(i, j))
N = len(point_list)

random.shuffle(point_list)

print ( "Testing GrahamScan1 ..." )
t1 = timeit.Timer(lambda: GrahamScan1(point_list).run())
print ( "{} {}".format(N, t1.timeit(1)) )   # single run

random.shuffle(point_list)

print ( "Testing GrahamScan2 ..." )
t1 = timeit.Timer(lambda: GrahamScan2(point_list).run())
print ( "{} {}".format(N, t1.timeit(1)) )   # single run

random.shuffle(point_list)

print ( "Testing JarvisMarch ..." )
t1 = timeit.Timer(lambda: JarvisMarch(point_list).run())
print ( "{} {}".format(N, t1.timeit(1)) )   # single run

random.shuffle(point_list)

print ( "Testing QuickHull ..." )
t1 = timeit.Timer(lambda: QuickHull(point_list).run())
print ( "{} {}".format(N, t1.timeit(1)) )   # single run

# EOF
