#!/usr/bin/env python3

import timeit
import random
from planegeometry.structures.points import Point
from planegeometry.algorithms.geomtools import find_two_furthest_points1
from planegeometry.algorithms.geomtools import find_two_furthest_points2
from planegeometry.algorithms.geomtools import find_two_furthest_points3
from planegeometry.algorithms.geomtools import find_two_furthest_points4
# time: v3[O(n^2),lambda] > v1[O(n^2)] > v4[O(n),lambda] > v2[O(n)]

def make_point_list(n):
    """Prepare a point list."""
    point_list = []
    for _ in range(n):
        point_list.append(Point(random.random(), random.random()))
    return point_list


N = 3000
point_list = make_point_list(N)

print ( "Testing find_two_furthest_points1 ..." )
t1 = timeit.Timer(lambda: find_two_furthest_points1(point_list))
print ( "{} {}".format(N, t1.timeit(1)) )   # single run

print ( "Testing find_two_furthest_points2 ..." )
t1 = timeit.Timer(lambda: find_two_furthest_points2(point_list))
print ( "{} {}".format(N, t1.timeit(1)) )   # single run

print ( "Testing find_two_furthest_points3 ..." )
t1 = timeit.Timer(lambda: find_two_furthest_points3(point_list))
print ( "{} {}".format(N, t1.timeit(1)) )   # single run

print ( "Testing find_two_furthest_points4 ..." )
t1 = timeit.Timer(lambda: find_two_furthest_points4(point_list))
print ( "{} {}".format(N, t1.timeit(1)) )   # single run

# EOF
