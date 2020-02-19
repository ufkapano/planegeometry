#!/usr/bin/python
#
# Testing Delaunay triangulation.
# General position of points is not tested.

import timeit
import random
from fractions import Fraction
from planegeometry.structures.points import Point
from planegeometry.triangulations.flipping import DelaunayFlipping
from planegeometry.triangulations.bowyerwatson import BowyerWatson
from planegeometry.triangulations.naive import DelaunayNaive

def make_point_list(n):
    """Prepare a point list."""
    point_list = []
    for _ in range(n):
        # AssertionError in legalize
        #point_list.append(Point(random.random(), random.random()))
        point_list.append(Point(
            Fraction(random.random()).limit_denominator(),
            Fraction(random.random()).limit_denominator()))
    return point_list

N = 10
point_list = make_point_list(N)

print ( "Testing DelaunayNaive ..." )
t1 = timeit.Timer(lambda: DelaunayNaive(point_list).run())
print ( "{} {}".format(N, t1.timeit(1)) )   # single run

print ( "Testing DelaunayFlipping ..." )
t1 = timeit.Timer(lambda: DelaunayFlipping(point_list).run())
print ( "{} {}".format(N, t1.timeit(1)) )   # single run

print ( "Testing BowyerWatson ..." )
t1 = timeit.Timer(lambda: BowyerWatson(point_list).run())
print ( "{} {}".format(N, t1.timeit(1)) )   # single run

# EOF
