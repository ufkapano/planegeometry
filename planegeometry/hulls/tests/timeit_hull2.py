#!/usr/bin/python

import math
import timeit
import random
from fractions import Fraction
from planegeometry.structures.points import Point
from planegeometry.hulls.graham import GrahamScan1
from planegeometry.hulls.graham import GrahamScan2
from planegeometry.hulls.jarvis import JarvisMarch
from planegeometry.hulls.quickhull import QuickHull

N = 100
point_list = []
for i in range(N):
    point_list.append(Point(N * math.cos(i*2.0*math.pi/N),
                            N * math.sin(i*2.0*math.pi/N)))

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
