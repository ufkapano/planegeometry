#!/usr/bin/env python3

import timeit
import random
from planegeometry.structures.points import Point
from planegeometry.algorithms.geomtools import find_two_closest_points
from planegeometry.algorithms.geomtools import find_two_closest_points2
from planegeometry.algorithms.geomtools import find_two_closest_points3
from planegeometry.algorithms.closestpair1 import ClosestPairSweepLine
from planegeometry.algorithms.closestpair3 import ClosestPairDivideConquer
from planegeometry.algorithms.closestpair4 import ClosestPairSortXY


def make_point_list(n):
    """Prepare a point list."""
    point_list = []
    for _ in range(n):
        point_list.append(Point(random.random(), random.random()))
    return point_list


N = 1000
point_list = make_point_list(N)

print ( "Testing find_two_closest_points ..." ) # v2 > v1 > v3
t1 = timeit.Timer(lambda: find_two_closest_points(point_list))
print ( "{} {}".format(N, t1.timeit(1)) )   # single run

print ( "Testing find_two_closest_points2 ..." )
t1 = timeit.Timer(lambda: find_two_closest_points2(point_list))
print ( "{} {}".format(N, t1.timeit(1)) )   # single run

print ( "Testing find_two_closest_points3 ..." )
t1 = timeit.Timer(lambda: find_two_closest_points3(point_list))
print ( "{} {}".format(N, t1.timeit(1)) )   # single run

print ( "Testing ClosestPairSweepLine ..." )
t1 = timeit.Timer(lambda: ClosestPairSweepLine(point_list).run())
print ( "{} {}".format(N, t1.timeit(1)) )   # single run

print ( "Testing ClosestPairDivideConquer ..." )
t1 = timeit.Timer(lambda: ClosestPairDivideConquer(point_list).run())
print ( "{} {}".format(N, t1.timeit(1)) )   # single run

print ( "Testing ClosestPairSortXY ..." )
t1 = timeit.Timer(lambda: ClosestPairSortXY(point_list).run())
print ( "{} {}".format(N, t1.timeit(1)) )   # single run

# EOF
