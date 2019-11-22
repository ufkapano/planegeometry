#!/usr/bin/python

import random
import Gnuplot
from planegeometry.structures.points import Point

gnu = Gnuplot.Gnuplot (persist = 1)

for i in range(100):
    point = Point(random.random(), random.random())
    gnu(point.gnu())

# Wyswietlenie grafu.
gnu('set terminal pdf enhanced')
gnu('set output "random_points.pdf"')
gnu('set grid')
gnu('unset key')
gnu('set size square') 
#gnu('unset border')
#gnu('unset tics')
gnu('set xlabel "x"')
gnu('set ylabel "y"')
gnu('set title "Random points"')
gnu('set xrange [{}:{}]'.format(0, 1))
gnu('set yrange [{}:{}]'.format(0, 1))
gnu.plot('NaN title ""')
gnu('unset output')

# EOF