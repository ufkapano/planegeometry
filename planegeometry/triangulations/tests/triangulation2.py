#!/usr/bin/python

import random
import Gnuplot   # Python 2 only
from fractions import Fraction
from planegeometry.structures.points import Point
from planegeometry.structures.segments import Segment
from planegeometry.triangulations.flipping import DelaunayFlipping
from planegeometry.triangulations.bowyerwatson import BowyerWatson
from planegeometry.triangulations.naive import DelaunayNaive

size = 10   # points in square [0,size]x[0,size]

def make_point_list(n):
    """Prepare a point list."""
    point_list = []
    for _ in range(n):
        point_list.append(Point(
            Fraction(size * random.random()).limit_denominator(),
            Fraction(size * random.random()).limit_denominator()))
    return point_list

gnu = Gnuplot.Gnuplot (persist = 1)

point_list = make_point_list(10)

#algorithm = DelaunayNaive(point_list)
#algorithm = DelaunayFlipping(point_list)
algorithm = BowyerWatson(point_list)
algorithm.run()
G = algorithm.tc.to_graph()
#G.show()
print ( list(G.iternodes()) )

for segment in G.iteredges():
    gnu(segment.gnu())

for point in G.iternodes():
    gnu(point.gnu())

# Wyswietlenie grafu.
gnu('set terminal pdf enhanced')
gnu('set output "triangulation2.pdf"')
#gnu('set grid')
gnu('unset key')
gnu('set size square') 
#gnu('unset border')
#gnu('unset tics')
gnu('set xlabel "x"')
gnu('set ylabel "y"')
gnu('set title "Delaunay triangulation"')
gnu('set xrange [{}:{}]'.format(0, size))
gnu('set yrange [{}:{}]'.format(0, size))
gnu.plot('NaN title ""')
gnu('unset output')

# EOF
