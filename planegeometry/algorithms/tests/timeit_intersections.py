#!/usr/bin/env python3

import timeit
from planegeometry.structures.points import Point
from planegeometry.structures.segments import Segment
from planegeometry.algorithms.bentleyottmann1 import BentleyOttmann
from planegeometry.algorithms.shamoshoey1 import ShamosHoey
from planegeometry.algorithms.geomtools import find_intersection_points


def make_segment_list(n):
    """Prepare a segment list (ladder)."""
    # Intersection list (n-1 points):
    # [Point(3*1+2, 3*i+2) for i in range(n-1)]
    segment_list = []
    for i in range(n-1):
        segment_list.append(Segment(1+3*i, 3+3*i, 3+3*i, 1+3*i))
    segment_list.append(Segment(0, 0, 3*n+1, 3*n+1))
    return segment_list


N = 100
segment_list = make_segment_list(N)

#print ( "segment_list {}".format(segment_list) )
#algorithm = BentleyOttmann(segment_list)
#algorithm.run()
#intersection_list = [Point(3*i+2, 3*i+2) for i in range(N-1)]
#assert algorithm.il == intersection_list
#algorithm = ShamosHoey(segment_list)
#assert algorithm.run()

print ( "Testing BentleyOttmann ..." )
t1 = timeit.Timer(lambda: BentleyOttmann(segment_list).run())
print ( "{} {}".format(N, t1.timeit(1)) )   # single run

print ( "Testing ShamosHoey ..." )
t1 = timeit.Timer(lambda: ShamosHoey(segment_list).run())
print ( "{} {}".format(N, t1.timeit(1)) )   # single run

print ( "Testing find_intersection_points ..." )
t1 = timeit.Timer(lambda: find_intersection_points(segment_list))
print ( "{} {}".format(N, t1.timeit(1)) )   # single run

# EOF
