#!/usr/bin/python

import random
import Gnuplot   # Python 2 only
from planegeometry.structures.points import Point
from planegeometry.structures.segments import Segment
from planegeometry.triangulations.flipping import DelaunayFlipping
from planegeometry.triangulations.bowyerwatson import BowyerWatson
from planegeometry.triangulations.naive import DelaunayNaive

gnu = Gnuplot.Gnuplot (persist = 1)

point_list = [Point(-2, -2), Point(2, -2), Point(-2, 2), Point(2, 2),
    Point(-2, 0), Point(0, 1), Point(0, -2), Point(-1, 0), Point(1,0)]

big = 2 * max(max(abs(point.x), abs(point.y)) for point in point_list)

#algorithm = DelaunayNaive(point_list)
#algorithm = DelaunayFlipping(point_list) # ValueError("collinear points")
algorithm = BowyerWatson(point_list)
algorithm.run()
G = algorithm.tc.to_graph()
print ( "triangulation graph ..." )
G.show()

for edge in G.iteredges():
    segment = Segment(edge.source, edge.target)
    gnu(segment.gnu())

for point in G.iternodes():
    gnu(point.gnu())

# Wyswietlenie grafu.
gnu('set terminal pdf enhanced')
gnu('set output "triangulation1.pdf"')
#gnu('set grid')
gnu('unset key')
gnu('set size square') 
#gnu('unset border')
#gnu('unset tics')
gnu('set xlabel "x"')
gnu('set ylabel "y"')
gnu('set title "Delaunay triangulation"')
gnu('set xrange [{}:{}]'.format(-big, big))
gnu('set yrange [{}:{}]'.format(-big, big))
gnu.plot('NaN title ""')
gnu('unset output')

# EOF
