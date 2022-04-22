#!/usr/bin/env python2

import random
import Gnuplot   # Python 2 only
from planegeometry.structures.points import Point
from planegeometry.structures.polygons import Polygon

gnu = Gnuplot.Gnuplot (persist = 1)

visible = True
point_list = [Point(random.random(), random.random()) for _ in range(5)]
polygon = Polygon(*point_list)
for segment in polygon.itersegments():
    gnu(segment.gnu(visible))

# Wyswietlenie grafu.
gnu('set terminal pdf enhanced')
gnu('set output "random_polygons.pdf"')
gnu('set grid')
gnu('unset key')
gnu('set size square') 
#gnu('unset border')
#gnu('unset tics')
gnu('set xlabel "x"')
gnu('set ylabel "y"')
gnu('set title "Random polygons"')
gnu('set xrange [{}:{}]'.format(0, 1))
gnu('set yrange [{}:{}]'.format(0, 1))
gnu.plot('NaN title ""')
gnu('unset output')

# EOF
